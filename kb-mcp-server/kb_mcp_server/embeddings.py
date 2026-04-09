"""Embedding 抽象层 — 支持本地模型和 DashScope API 切换"""

from abc import ABC, abstractmethod
from typing import List


class BaseEmbedding(ABC):
    @abstractmethod
    def embed(self, texts: List[str]) -> List[List[float]]:
        """将文本列表转为向量列表"""
        ...

    @abstractmethod
    def dimension(self) -> int:
        """返回向量维度"""
        ...


class LocalEmbedding(BaseEmbedding):
    """基于 sentence-transformers 的本地 embedding（不消耗 API token）"""

    def __init__(self, model_name: str = "shibing624/text2vec-base-chinese"):
        from sentence_transformers import SentenceTransformer

        self._model = SentenceTransformer(model_name)
        self._dimension = self._model.get_sentence_embedding_dimension()

    def embed(self, texts: List[str]) -> List[List[float]]:
        embeddings = self._model.encode(texts, normalize_embeddings=True)
        return embeddings.tolist()

    def dimension(self) -> int:
        return self._dimension


class DashScopeEmbedding(BaseEmbedding):
    """基于阿里云 DashScope API 的 embedding"""

    def __init__(self, api_key: str, model: str = "text-embedding-v3"):
        import dashscope

        dashscope.api_key = api_key
        self._model = model
        self._dimension = 1024  # text-embedding-v3 默认维度

    def embed(self, texts: List[str]) -> List[List[float]]:
        from dashscope import TextEmbedding

        # DashScope 单次最多 25 条，分批处理
        all_embeddings = []
        batch_size = 25
        for i in range(0, len(texts), batch_size):
            batch = texts[i : i + batch_size]
            resp = TextEmbedding.call(
                model=self._model,
                input=batch,
            )
            if resp.status_code != 200:
                raise RuntimeError(f"DashScope API 错误: {resp.code} {resp.message}")
            for item in resp.output["embeddings"]:
                all_embeddings.append(item["embedding"])
        return all_embeddings

    def dimension(self) -> int:
        return self._dimension


def create_embedding(config: dict) -> BaseEmbedding:
    """根据配置创建 embedding 实例"""
    embedding_cfg = config.get("embedding", {})
    provider = embedding_cfg.get("provider", "local")

    if provider == "local":
        model_name = embedding_cfg.get("local", {}).get(
            "model_name", "shibing624/text2vec-base-chinese"
        )
        return LocalEmbedding(model_name)
    elif provider == "dashscope":
        ds_cfg = embedding_cfg.get("dashscope", {})
        api_key = ds_cfg.get("api_key", "")
        if not api_key:
            raise ValueError(
                "DashScope API Key 未配置。请在 config.yaml 中设置或设置环境变量 DASHSCOPE_API_KEY"
            )
        model = ds_cfg.get("model", "text-embedding-v3")
        return DashScopeEmbedding(api_key, model)
    else:
        raise ValueError(f"不支持的 embedding provider: {provider}")
