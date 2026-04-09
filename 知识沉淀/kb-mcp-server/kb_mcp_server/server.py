"""FastMCP Server — 知识库向量搜索工具"""

import json
from typing import Optional

from fastmcp import FastMCP

from .config import load_config
from .embeddings import create_embedding
from .indexer import KnowledgeIndexer

mcp = FastMCP(
    name="kb-search",
    instructions="知识库语义搜索服务。使用 search_knowledge 进行语义搜索，使用 list_knowledge 浏览条目列表。",
)

# 延迟初始化：MCP server 启动时加载
_indexer: Optional[KnowledgeIndexer] = None


def _get_indexer() -> KnowledgeIndexer:
    global _indexer
    if _indexer is None:
        config = load_config()
        embedding = create_embedding(config)
        _indexer = KnowledgeIndexer(config, embedding)
    return _indexer


@mcp.tool(annotations={"readOnlyHint": True})
def search_knowledge(
    query: str,
    top_k: int = 5,
    category: Optional[str] = None,
) -> str:
    """语义搜索知识库。输入自然语言查询，返回最相关的知识条目。
    用于查找业务知识、策略经验、数据口径等。
    category 可选值：业务知识、策略沉淀、数据口径、会议纪要。不传则搜索全部分类。"""
    indexer = _get_indexer()
    results = indexer.search(query, top_k=top_k, category=category)

    if not results:
        return "未找到相关知识条目。"

    output = []
    for i, r in enumerate(results, 1):
        output.append(
            f"### [{i}] {r['title']}  (相似度: {r['similarity']})\n"
            f"分类: {r['category']} | 子标签: {r['sub_tag']} | 项目: {r['project']} | 日期: {r['date']}\n"
            f"段落: {r['section']}\n"
            f"文件: {r['source_file']}\n\n"
            f"{r['content']}\n"
        )
    return "\n---\n".join(output)


@mcp.tool(annotations={"readOnlyHint": True})
def list_knowledge(
    category: Optional[str] = None,
    project: Optional[str] = None,
    tag: Optional[str] = None,
) -> str:
    """列出知识库中的所有条目概览。可按分类、项目、标签过滤。
    不做语义搜索，直接返回条目列表。
    category 可选值：业务知识、策略沉淀、数据口径、会议纪要。"""
    indexer = _get_indexer()
    entries = indexer.list_entries(category=category, project=project, tag=tag)

    if not entries:
        return "未找到匹配的知识条目。"

    output = [f"共 {len(entries)} 条知识条目：\n"]
    for e in entries:
        output.append(
            f"- [{e['category']}] {e['title']} | {e['sub_tag']} | {e['project']} | {e['date']} | {e['status']}"
        )
    return "\n".join(output)


@mcp.tool()
def reindex_knowledge(full: bool = False) -> str:
    """重建知识库的向量索引。在手动添加或修改知识条目后调用。
    默认增量更新（只处理修改过的文件），传 full=true 全量重建。"""
    indexer = _get_indexer()
    stats = indexer.index(full=full)
    mode = "全量重建" if full else "增量更新"
    return (
        f"索引{mode}完成：\n"
        f"- 新增: {stats['added']} 个文件\n"
        f"- 更新: {stats['updated']} 个文件\n"
        f"- 跳过: {stats['skipped']} 个文件\n"
        f"- 总 chunks: {stats['total_chunks']}"
    )
