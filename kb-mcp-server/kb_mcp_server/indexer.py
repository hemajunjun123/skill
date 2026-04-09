"""知识库索引器 — Markdown 解析 + ChromaDB 向量入库"""

import json
import os
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import chromadb
import yaml

from .embeddings import BaseEmbedding

# 跳过的系统文件
SKIP_FILES = {"_summary.md", "_tags.md"}

# 四个分类目录
CATEGORIES = ["业务知识", "策略沉淀", "数据口径", "会议纪要"]


def parse_frontmatter(content: str) -> Tuple[dict, str]:
    """解析 YAML frontmatter，返回 (metadata, body)"""
    if not content.startswith("---"):
        return {}, content

    parts = content.split("---", 2)
    if len(parts) < 3:
        return {}, content

    try:
        metadata = yaml.safe_load(parts[1]) or {}
    except yaml.YAMLError:
        metadata = {}

    body = parts[2].strip()
    return metadata, body


def chunk_body(title: str, category: str, body: str) -> List[dict]:
    """将正文按 ### 分段，每段作为一个 chunk"""
    sections = re.split(r"(?=^### )", body, flags=re.MULTILINE)
    chunks = []

    for i, section in enumerate(sections):
        section = section.strip()
        if not section:
            continue

        # 提取段落标题
        lines = section.split("\n", 1)
        section_title = lines[0].lstrip("#").strip() if lines[0].startswith("###") else ""
        section_content = lines[1].strip() if len(lines) > 1 else section

        # 拼接上下文以提升检索质量
        chunk_text = f"{title} | {category}"
        if section_title:
            chunk_text += f" | {section_title}"
        chunk_text += f"\n\n{section_content}"

        chunks.append(
            {
                "index": i,
                "section": section_title or f"段落{i}",
                "text": chunk_text,
                "raw": section,
            }
        )

    # 如果没有 ### 分段，整体作为一个 chunk
    if not chunks and body.strip():
        chunks.append(
            {
                "index": 0,
                "section": "全文",
                "text": f"{title} | {category}\n\n{body}",
                "raw": body,
            }
        )

    return chunks


def scan_knowledge_files(kb_path: str) -> List[dict]:
    """扫描知识库目录，返回所有知识条目信息"""
    entries = []
    kb = Path(kb_path)

    for category in CATEGORIES:
        cat_dir = kb / category
        if not cat_dir.exists():
            continue

        for md_file in sorted(cat_dir.glob("*.md")):
            if md_file.name in SKIP_FILES:
                continue

            content = md_file.read_text(encoding="utf-8")
            metadata, body = parse_frontmatter(content)
            mtime = md_file.stat().st_mtime

            chunks = chunk_body(
                metadata.get("标题", md_file.stem),
                metadata.get("分类", category),
                body,
            )

            # 处理子标签 — 可能是列表或字符串
            sub_tags = metadata.get("子标签", [])
            if isinstance(sub_tags, list):
                sub_tag = ", ".join(sub_tags)
            else:
                sub_tag = str(sub_tags)

            entries.append(
                {
                    "file_name": md_file.name,
                    "file_path": str(md_file),
                    "category": category,
                    "mtime": mtime,
                    "metadata": {
                        "title": metadata.get("标题", md_file.stem),
                        "category": metadata.get("分类", category),
                        "sub_tag": sub_tag,
                        "project": metadata.get("关联项目", ""),
                        "date": str(metadata.get("日期", "")),
                        "status": metadata.get("状态", "有效"),
                        "source_file": md_file.name,
                    },
                    "chunks": chunks,
                }
            )

    return entries


class KnowledgeIndexer:
    """知识库向量索引器"""

    MTIME_FILE = "_file_mtimes.json"

    def __init__(self, config: dict, embedding: BaseEmbedding):
        self.kb_path = config["knowledge_base_path"]
        self.chroma_path = config["chroma_db_path"]
        self.embedding = embedding

        self._client = chromadb.PersistentClient(path=self.chroma_path)
        self._collection = self._client.get_or_create_collection(
            name="knowledge_base",
            metadata={"hnsw:space": "cosine"},
        )

    def _load_mtimes(self) -> dict:
        mtime_path = os.path.join(self.chroma_path, self.MTIME_FILE)
        if os.path.exists(mtime_path):
            with open(mtime_path, "r") as f:
                return json.load(f)
        return {}

    def _save_mtimes(self, mtimes: dict):
        os.makedirs(self.chroma_path, exist_ok=True)
        mtime_path = os.path.join(self.chroma_path, self.MTIME_FILE)
        with open(mtime_path, "w") as f:
            json.dump(mtimes, f, ensure_ascii=False, indent=2)

    def index(self, full: bool = False) -> dict:
        """建立/更新向量索引

        Args:
            full: True=全量重建，False=增量更新

        Returns:
            统计信息 {"added": N, "updated": N, "skipped": N, "total_chunks": N}
        """
        entries = scan_knowledge_files(self.kb_path)
        old_mtimes = {} if full else self._load_mtimes()
        new_mtimes = {}

        stats = {"added": 0, "updated": 0, "skipped": 0, "total_chunks": 0}

        if full:
            # 全量重建：删除旧 collection 重新创建
            self._client.delete_collection("knowledge_base")
            self._collection = self._client.create_collection(
                name="knowledge_base",
                metadata={"hnsw:space": "cosine"},
            )

        for entry in entries:
            file_name = entry["file_name"]
            new_mtimes[file_name] = entry["mtime"]

            # 增量模式：跳过未修改的文件
            if not full and file_name in old_mtimes:
                if old_mtimes[file_name] == entry["mtime"]:
                    stats["skipped"] += 1
                    stats["total_chunks"] += len(entry["chunks"])
                    continue

            # 删除该文件的旧 chunks
            if not full:
                old_ids = [
                    f"{file_name}#{i}" for i in range(100)
                ]
                try:
                    self._collection.delete(ids=old_ids)
                except Exception:
                    pass

            # 添加新 chunks
            if not entry["chunks"]:
                continue

            ids = []
            documents = []
            metadatas = []

            for chunk in entry["chunks"]:
                chunk_id = f"{file_name}#{chunk['index']}"
                ids.append(chunk_id)
                documents.append(chunk["text"])
                meta = dict(entry["metadata"])
                meta["section"] = chunk["section"]
                metadatas.append(meta)

            # 生成 embeddings
            embeddings = self.embedding.embed(documents)

            self._collection.add(
                ids=ids,
                documents=documents,
                metadatas=metadatas,
                embeddings=embeddings,
            )

            if file_name in old_mtimes:
                stats["updated"] += 1
            else:
                stats["added"] += 1
            stats["total_chunks"] += len(entry["chunks"])

        self._save_mtimes(new_mtimes)
        return stats

    def search(
        self,
        query: str,
        top_k: int = 5,
        category: Optional[str] = None,
    ) -> List[dict]:
        """语义搜索知识库

        Returns:
            匹配结果列表，每项包含 title, category, section, content, score, source_file
        """
        query_embedding = self.embedding.embed([query])[0]

        where_filter = None
        if category:
            where_filter = {"category": category}

        results = self._collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            where=where_filter,
            include=["documents", "metadatas", "distances"],
        )

        matches = []
        if results["ids"] and results["ids"][0]:
            for i, doc_id in enumerate(results["ids"][0]):
                meta = results["metadatas"][0][i]
                distance = results["distances"][0][i]
                # ChromaDB cosine distance: 0=完全匹配, 2=完全不匹配
                similarity = 1 - distance / 2

                matches.append(
                    {
                        "title": meta.get("title", ""),
                        "category": meta.get("category", ""),
                        "sub_tag": meta.get("sub_tag", ""),
                        "project": meta.get("project", ""),
                        "section": meta.get("section", ""),
                        "content": results["documents"][0][i],
                        "similarity": round(similarity, 4),
                        "source_file": meta.get("source_file", ""),
                        "date": meta.get("date", ""),
                    }
                )

        return matches

    def list_entries(
        self,
        category: Optional[str] = None,
        project: Optional[str] = None,
        tag: Optional[str] = None,
    ) -> List[dict]:
        """列出知识库条目（不做语义搜索）"""
        entries = scan_knowledge_files(self.kb_path)
        results = []

        seen = set()
        for entry in entries:
            meta = entry["metadata"]

            if category and meta["category"] != category:
                continue
            if project and meta["project"] != project:
                continue
            if tag and tag not in meta["sub_tag"]:
                continue

            # 去重（一个文件只出现一次）
            if meta["source_file"] in seen:
                continue
            seen.add(meta["source_file"])

            results.append(
                {
                    "title": meta["title"],
                    "category": meta["category"],
                    "sub_tag": meta["sub_tag"],
                    "project": meta["project"],
                    "date": meta["date"],
                    "status": meta["status"],
                    "source_file": meta["source_file"],
                }
            )

        return results
