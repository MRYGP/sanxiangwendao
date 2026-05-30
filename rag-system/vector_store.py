"""
向量数据库封装
Windows 上 ChromaDB 原生层 add() 会 segfault，默认使用 NumPy 持久化后端。
"""

from __future__ import annotations

import json
import logging
import shutil
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

import numpy as np

logger = logging.getLogger(__name__)

DEFAULT_VECTOR_DB_TYPE = "numpy" if sys.platform == "win32" else "chroma"


def _build_chunk_metadata(chunk: Dict) -> Dict[str, str]:
    metadata = {
        "doc_id": chunk["doc_id"],
        "chunk_type": chunk["chunk_type"],
        "weight": str(chunk.get("weight", 1.0)),
    }
    if "metadata" in chunk:
        for key, value in chunk["metadata"].items():
            metadata[key] = str(value) if value is not None else ""
    if "chunk_index" in chunk:
        metadata["chunk_index"] = str(chunk["chunk_index"])
    if "pattern_index" in chunk:
        metadata["pattern_index"] = str(chunk["pattern_index"])
    if "example_index" in chunk:
        metadata["example_index"] = str(chunk["example_index"])
    return metadata


class NumpyVectorStore:
    """纯 NumPy 持久化向量库，兼容 retriever 期望的 Chroma 返回格式。"""

    def __init__(self, db_path: Path, collection_name: str = "wendao_knowledge_base"):
        self.db_path = db_path
        self.collection_name = collection_name
        self.store_dir = db_path / "numpy_store" / collection_name
        self.store_dir.mkdir(parents=True, exist_ok=True)
        self.meta_path = self.store_dir / "meta.json"
        self.embeddings_path = self.store_dir / "embeddings.npy"
        self.records_path = self.store_dir / "records.json"
        self.ids: List[str] = []
        self.documents: List[str] = []
        self.metadatas: List[Dict[str, str]] = []
        self.embeddings = np.empty((0, 0), dtype=np.float32)
        self._load()
        logger.info(
            "NumPy 向量库已加载: %s (%d 块)",
            self.store_dir,
            len(self.ids),
        )

    def _load(self) -> None:
        if not self.records_path.exists():
            return
        with open(self.records_path, "r", encoding="utf-8") as f:
            records = json.load(f)
        self.ids = records["ids"]
        self.documents = records["documents"]
        self.metadatas = records["metadatas"]
        self.embeddings = np.load(self.embeddings_path)

    def _save(self) -> None:
        with open(self.records_path, "w", encoding="utf-8") as f:
            json.dump(
                {
                    "ids": self.ids,
                    "documents": self.documents,
                    "metadatas": self.metadatas,
                },
                f,
                ensure_ascii=False,
            )
        np.save(self.embeddings_path, self.embeddings)
        with open(self.meta_path, "w", encoding="utf-8") as f:
            json.dump(
                {
                    "collection_name": self.collection_name,
                    "backend": "numpy",
                    "count": len(self.ids),
                },
                f,
                ensure_ascii=False,
            )

    def add_documents(
        self,
        chunks: List[Dict],
        embeddings: List[List[float]],
        ids: Optional[List[str]] = None,
    ) -> None:
        if len(chunks) != len(embeddings):
            raise ValueError("chunks和embeddings数量不匹配")

        if ids is None:
            ids = [
                f"{chunk['doc_id']}_{chunk['chunk_type']}_"
                f"{chunk.get('chunk_index', chunk.get('pattern_index', chunk.get('example_index', 0)))}"
                for chunk in chunks
            ]

        new_embeddings = np.asarray(embeddings, dtype=np.float32)
        if self.embeddings.size == 0:
            self.embeddings = new_embeddings
        else:
            self.embeddings = np.vstack([self.embeddings, new_embeddings])

        for chunk, chunk_id in zip(chunks, ids):
            self.ids.append(chunk_id)
            self.documents.append(chunk["content"])
            self.metadatas.append(_build_chunk_metadata(chunk))

        self._save()
        logger.info("成功添加 %d 个文档块到 NumPy 向量库", len(chunks))

    def _matches_filter(self, metadata: Dict[str, str], where: Optional[Dict[str, Any]]) -> bool:
        if not where:
            return True
        for key, expected in where.items():
            if metadata.get(key) != str(expected):
                return False
        return True

    def search(
        self,
        query_embedding: List[float],
        n_results: int = 5,
        where: Optional[Dict[str, Any]] = None,
        where_document: Optional[Dict[str, Any]] = None,
    ) -> Dict:
        if not self.ids:
            return {"ids": [[]], "documents": [[]], "metadatas": [[]], "distances": [[]]}

        query = np.asarray(query_embedding, dtype=np.float32)
        candidate_indices = [
            i
            for i, metadata in enumerate(self.metadatas)
            if self._matches_filter(metadata, where)
        ]
        if not candidate_indices:
            return {"ids": [[]], "documents": [[]], "metadatas": [[]], "distances": [[]]}

        matrix = self.embeddings[candidate_indices]
        scores = matrix @ query
        local_top = np.argsort(scores)[::-1][:n_results]

        result_ids: List[str] = []
        result_documents: List[str] = []
        result_metadatas: List[Dict[str, str]] = []
        result_distances: List[float] = []

        for local_idx in local_top:
            global_idx = candidate_indices[int(local_idx)]
            if where_document:
                matched = False
                for op, value in where_document.items():
                    content = self.documents[global_idx]
                    if op == "$contains" and value in content:
                        matched = True
                    elif op == "$eq" and content == value:
                        matched = True
                if not matched:
                    continue

            similarity = float(scores[int(local_idx)])
            result_ids.append(self.ids[global_idx])
            result_documents.append(self.documents[global_idx])
            result_metadatas.append(self.metadatas[global_idx])
            result_distances.append(1.0 - similarity)

        return {
            "ids": [result_ids],
            "documents": [result_documents],
            "metadatas": [result_metadatas],
            "distances": [result_distances],
        }

    def get_collection_info(self) -> Dict:
        return {
            "collection_name": self.collection_name,
            "document_count": len(self.ids),
            "db_path": str(self.store_dir),
            "backend": "numpy",
        }

    def delete_collection(self) -> None:
        if self.store_dir.exists():
            shutil.rmtree(self.store_dir)
        logger.warning("已删除 NumPy 向量库: %s", self.store_dir)

    def reset_collection(self) -> None:
        self.delete_collection()
        self.store_dir.mkdir(parents=True, exist_ok=True)
        self.ids = []
        self.documents = []
        self.metadatas = []
        self.embeddings = np.empty((0, 0), dtype=np.float32)
        logger.info("NumPy 向量库已重置: %s", self.collection_name)


class ChromaVectorStore:
    """ChromaDB 后端（Linux/macOS 可用；Windows 上 add() 可能 segfault）。"""

    def __init__(self, db_path: Path, collection_name: str = "wendao_knowledge_base"):
        import chromadb
        from chromadb.config import Settings

        self.db_path = db_path
        self.collection_name = collection_name
        db_path.mkdir(parents=True, exist_ok=True)

        self.client = chromadb.PersistentClient(
            path=str(db_path),
            settings=Settings(anonymized_telemetry=False),
        )
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine", "hnsw:batch_size": 10000},
        )
        logger.info("Chroma 向量库初始化成功，集合: %s", collection_name)

    def add_documents(
        self,
        chunks: List[Dict],
        embeddings: List[List[float]],
        ids: Optional[List[str]] = None,
    ) -> None:
        if len(chunks) != len(embeddings):
            raise ValueError("chunks和embeddings数量不匹配")

        if ids is None:
            ids = [
                f"{chunk['doc_id']}_{chunk['chunk_type']}_"
                f"{chunk.get('chunk_index', chunk.get('pattern_index', chunk.get('example_index', 0)))}"
                for chunk in chunks
            ]

        documents = [chunk["content"] for chunk in chunks]
        metadatas = [_build_chunk_metadata(chunk) for chunk in chunks]
        self.collection.add(
            embeddings=embeddings,
            documents=documents,
            metadatas=metadatas,
            ids=ids,
        )
        logger.info("成功添加 %d 个文档块到 Chroma", len(chunks))

    def search(
        self,
        query_embedding: List[float],
        n_results: int = 5,
        where: Optional[Dict[str, Any]] = None,
        where_document: Optional[Dict[str, Any]] = None,
    ) -> Dict:
        return self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            where=where,
            where_document=where_document,
        )

    def get_collection_info(self) -> Dict:
        return {
            "collection_name": self.collection_name,
            "document_count": self.collection.count(),
            "db_path": str(self.db_path),
            "backend": "chroma",
        }

    def delete_collection(self) -> None:
        self.client.delete_collection(name=self.collection_name)
        logger.warning("已删除 Chroma 集合: %s", self.collection_name)

    def reset_collection(self) -> None:
        self.delete_collection()
        self.collection = self.client.get_or_create_collection(
            name=self.collection_name,
            metadata={"hnsw:space": "cosine", "hnsw:batch_size": 10000},
        )
        logger.info("Chroma 集合已重置: %s", self.collection_name)


class VectorStore:
    """向量库统一入口，按配置选择后端。"""

    def __init__(
        self,
        db_path: Path,
        collection_name: str = "wendao_knowledge_base",
        backend: Optional[str] = None,
    ):
        from .config import VECTOR_DB_TYPE

        selected = (backend or VECTOR_DB_TYPE or DEFAULT_VECTOR_DB_TYPE).lower()
        if selected == "numpy":
            self._store = NumpyVectorStore(db_path, collection_name)
        elif selected == "chroma":
            self._store = ChromaVectorStore(db_path, collection_name)
        else:
            raise ValueError(f"不支持的向量库类型: {selected}")

        self.backend = selected
        self.db_path = db_path
        self.collection_name = collection_name

    def add_documents(self, chunks, embeddings, ids=None):
        return self._store.add_documents(chunks, embeddings, ids)

    def search(self, query_embedding, n_results=5, where=None, where_document=None):
        return self._store.search(
            query_embedding,
            n_results=n_results,
            where=where,
            where_document=where_document,
        )

    def get_collection_info(self):
        return self._store.get_collection_info()

    def delete_collection(self):
        return self._store.delete_collection()

    def reset_collection(self):
        return self._store.reset_collection()
