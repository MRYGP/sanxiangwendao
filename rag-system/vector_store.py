"""
向量数据库封装
支持Chroma、Qdrant等向量数据库
"""

import chromadb
from chromadb.config import Settings
from typing import List, Dict, Optional, Any
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class VectorStore:
    """向量数据库封装类"""
    
    def __init__(
        self,
        db_path: Path,
        collection_name: str = "wendao_knowledge_base"
    ):
        """
        初始化向量数据库
        
        Args:
            db_path: 数据库存储路径
            collection_name: 集合名称
        """
        self.db_path = db_path
        self.collection_name = collection_name
        
        # 确保目录存在
        db_path.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"初始化向量数据库: {db_path}")
        
        try:
            self.client = chromadb.PersistentClient(
                path=str(db_path),
                settings=Settings(anonymized_telemetry=False)
            )
            
            # 获取或创建集合
            self.collection = self.client.get_or_create_collection(
                name=collection_name,
                metadata={"hnsw:space": "cosine"}  # 使用余弦相似度
            )
            
            logger.info(f"向量数据库初始化成功，集合: {collection_name}")
        except Exception as e:
            logger.error(f"向量数据库初始化失败: {e}")
            raise
    
    def add_documents(
        self,
        chunks: List[Dict],
        embeddings: List[List[float]],
        ids: Optional[List[str]] = None
    ):
        """
        添加文档块到向量数据库
        
        Args:
            chunks: 文档块列表（包含content和metadata）
            embeddings: 向量列表
            ids: 文档块ID列表（可选，自动生成）
        """
        if len(chunks) != len(embeddings):
            raise ValueError("chunks和embeddings数量不匹配")
        
        # 生成ID（如果未提供）
        if ids is None:
            ids = [
                f"{chunk['doc_id']}_{chunk['chunk_type']}_{chunk.get('chunk_index', chunk.get('pattern_index', chunk.get('example_index', 0)))}"
                for chunk in chunks
            ]
        
        metadatas = []
        documents = []
        
        for chunk in chunks:
            # 构建metadata
            metadata = {
                'doc_id': chunk['doc_id'],
                'chunk_type': chunk['chunk_type'],
                'weight': str(chunk.get('weight', 1.0))  # Chroma需要字符串
            }
            
            # 添加chunk的metadata
            if 'metadata' in chunk:
                for k, v in chunk['metadata'].items():
                    metadata[k] = str(v) if v is not None else ""
            
            # 添加索引信息
            if 'chunk_index' in chunk:
                metadata['chunk_index'] = str(chunk['chunk_index'])
            if 'pattern_index' in chunk:
                metadata['pattern_index'] = str(chunk['pattern_index'])
            if 'example_index' in chunk:
                metadata['example_index'] = str(chunk['example_index'])
            
            metadatas.append(metadata)
            documents.append(chunk['content'])
        
        try:
            self.collection.add(
                embeddings=embeddings,
                documents=documents,
                metadatas=metadatas,
                ids=ids
            )
            logger.info(f"成功添加 {len(chunks)} 个文档块到向量数据库")
        except Exception as e:
            logger.error(f"添加文档块失败: {e}")
            raise
    
    def search(
        self,
        query_embedding: List[float],
        n_results: int = 5,
        where: Optional[Dict[str, Any]] = None,
        where_document: Optional[Dict[str, Any]] = None
    ) -> Dict:
        """
        向量检索
        
        Args:
            query_embedding: 查询向量
            n_results: 返回结果数量
            where: 元数据过滤条件（如 {"doc_type": "theory"}）
            where_document: 文档内容过滤条件
            
        Returns:
            检索结果字典，包含ids、documents、metadatas、distances
        """
        try:
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=n_results,
                where=where,
                where_document=where_document
            )
            return results
        except Exception as e:
            logger.error(f"向量检索失败: {e}")
            raise
    
    def get_collection_info(self) -> Dict:
        """获取集合信息"""
        count = self.collection.count()
        return {
            'collection_name': self.collection_name,
            'document_count': count,
            'db_path': str(self.db_path)
        }
    
    def delete_collection(self):
        """删除集合（谨慎使用）"""
        self.client.delete_collection(name=self.collection_name)
        logger.warning(f"已删除集合: {self.collection_name}")
    
    def reset_collection(self):
        """重置集合（删除所有数据）"""
        self.delete_collection()
        self.collection = self.client.get_or_create_collection(
            name=self.collection_name,
            metadata={"hnsw:space": "cosine"}
        )
        logger.info(f"集合已重置: {self.collection_name}")
