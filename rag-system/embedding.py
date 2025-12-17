"""
Embedding模型封装
支持BGE-M3、text2vec等模型
"""

from sentence_transformers import SentenceTransformer
from typing import List, Union
import torch
import logging

logger = logging.getLogger(__name__)

class EmbeddingModel:
    """Embedding模型封装类"""
    
    def __init__(self, model_name: str = "BAAI/bge-m3", device: str = "cpu"):
        """
        初始化Embedding模型
        
        Args:
            model_name: 模型名称或路径
            device: 设备类型 ("cpu" 或 "cuda")
        """
        self.model_name = model_name
        self.device = device if torch.cuda.is_available() and device == "cuda" else "cpu"
        
        logger.info(f"正在加载Embedding模型: {model_name} (设备: {self.device})")
        
        try:
            self.model = SentenceTransformer(
                model_name,
                device=self.device,
                trust_remote_code=True
            )
            logger.info(f"模型加载成功")
        except Exception as e:
            logger.error(f"模型加载失败: {e}")
            raise
    
    def encode(
        self,
        texts: Union[str, List[str]],
        normalize_embeddings: bool = True,
        show_progress_bar: bool = True,
        batch_size: int = 32
    ) -> Union[List[float], List[List[float]]]:
        """
        对文本列表进行向量化
        
        Args:
            texts: 文本或文本列表
            normalize_embeddings: 是否归一化向量
            show_progress_bar: 是否显示进度条
            batch_size: 批处理大小
            
        Returns:
            向量或向量列表
        """
        if isinstance(texts, str):
            texts = [texts]
        
        embeddings = self.model.encode(
            texts,
            normalize_embeddings=normalize_embeddings,
            show_progress_bar=show_progress_bar,
            batch_size=batch_size,
            convert_to_numpy=True
        )
        
        # 转换为列表格式
        if len(texts) == 1:
            return embeddings[0].tolist()
        return embeddings.tolist()
    
    def encode_query(self, query: str) -> List[float]:
        """
        对查询进行向量化
        BGE-M3支持query指令，可以提高检索效果
        
        Args:
            query: 查询文本
            
        Returns:
            查询向量
        """
        # BGE-M3支持query指令
        if "bge-m3" in self.model_name.lower():
            query_text = f"为这个句子生成表示以用于检索相关文章：{query}"
        else:
            query_text = query
        
        embedding = self.model.encode(
            [query_text],
            normalize_embeddings=True,
            show_progress_bar=False
        )
        
        return embedding[0].tolist()
    
    def encode_batch(
        self,
        texts: List[str],
        batch_size: int = 32,
        show_progress_bar: bool = True
    ) -> List[List[float]]:
        """
        批量向量化（用于大量文本）
        
        Args:
            texts: 文本列表
            batch_size: 批处理大小
            show_progress_bar: 是否显示进度条
            
        Returns:
            向量列表
        """
        return self.encode(
            texts,
            show_progress_bar=show_progress_bar,
            batch_size=batch_size
        )
    
    def get_embedding_dimension(self) -> int:
        """获取向量维度"""
        # 测试向量化一个短文本
        test_embedding = self.encode("test")
        return len(test_embedding)
