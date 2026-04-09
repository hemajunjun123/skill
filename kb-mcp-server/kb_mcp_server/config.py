"""配置加载模块"""

import os
from pathlib import Path

import yaml


def load_config(config_path: str = None) -> dict:
    """加载配置文件，支持环境变量替换"""
    if config_path is None:
        # 默认查找顺序：当前目录 → 包所在目录的上级
        candidates = [
            Path.cwd() / "config.yaml",
            Path(__file__).parent.parent / "config.yaml",
        ]
        for p in candidates:
            if p.exists():
                config_path = str(p)
                break
        else:
            raise FileNotFoundError(
                "找不到 config.yaml，请在项目目录下创建或通过 --config 指定路径"
            )

    with open(config_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    # 处理知识库路径
    kb_path = os.path.expanduser(config["knowledge_base_path"])
    config["knowledge_base_path"] = kb_path

    # 处理 ChromaDB 路径
    chroma_path = config.get("chroma_db_path", "")
    if not chroma_path:
        chroma_path = os.path.join(kb_path, ".vectordb")
    config["chroma_db_path"] = chroma_path

    # 处理 DashScope API Key（支持环境变量）
    embedding_cfg = config.get("embedding", {})
    dashscope_cfg = embedding_cfg.get("dashscope", {})
    api_key = dashscope_cfg.get("api_key", "")
    if not api_key:
        api_key = os.environ.get("DASHSCOPE_API_KEY", "")
    dashscope_cfg["api_key"] = api_key

    return config
