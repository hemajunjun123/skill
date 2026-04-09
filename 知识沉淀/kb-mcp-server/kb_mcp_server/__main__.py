"""CLI 入口 — 启动 MCP Server 或执行索引操作"""

import argparse
import sys

from .config import load_config
from .embeddings import create_embedding
from .indexer import KnowledgeIndexer


def _run_index(config: dict, full: bool = False):
    """执行索引操作"""
    embedding = create_embedding(config)
    indexer = KnowledgeIndexer(config, embedding)
    mode = "全量重建" if full else "增量更新"
    print(f"开始{mode}索引...")
    print(f"知识库路径: {config['knowledge_base_path']}")
    print(f"向量数据库: {config['chroma_db_path']}")
    print(f"Embedding: {config.get('embedding', {}).get('provider', 'local')}")
    print()

    stats = indexer.index(full=full)
    print(f"索引{mode}完成：")
    print(f"  新增: {stats['added']} 个文件")
    print(f"  更新: {stats['updated']} 个文件")
    print(f"  跳过: {stats['skipped']} 个文件")
    print(f"  总 chunks: {stats['total_chunks']}")


def _run_server(config_path: str = None):
    """启动 MCP Server（stdio 模式）"""
    from .server import mcp

    mcp.run(transport="stdio")


def main():
    parser = argparse.ArgumentParser(
        description="知识库向量搜索 MCP Server",
    )
    parser.add_argument(
        "--config",
        type=str,
        default=None,
        help="配置文件路径（默认自动查找 config.yaml）",
    )
    parser.add_argument(
        "--index",
        action="store_true",
        help="建立向量索引（增量更新）",
    )
    parser.add_argument(
        "--reindex",
        action="store_true",
        help="全量重建向量索引",
    )

    args = parser.parse_args()

    if args.index or args.reindex:
        config = load_config(args.config)
        _run_index(config, full=args.reindex)
    else:
        _run_server(args.config)


if __name__ == "__main__":
    main()
