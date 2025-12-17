"""
混合检索器实现
支持向量检索、关键词匹配、关系扩展
"""

from typing import List, Dict, Optional, Set
from pathlib import Path
import yaml
import logging
from collections import defaultdict

from .vector_store import VectorStore
from .embedding import EmbeddingModel
from .config import INDEX_DIR, TOP_K

logger = logging.getLogger(__name__)

class HybridRetriever:
    """混合检索器"""
    
    def __init__(
        self,
        vector_store: VectorStore,
        embedding_model: EmbeddingModel,
        index_dir: Path = INDEX_DIR
    ):
        """
        初始化混合检索器
        
        Args:
            vector_store: 向量数据库实例
            embedding_model: Embedding模型实例
            index_dir: 索引文件目录
        """
        self.vector_store = vector_store
        self.embedding_model = embedding_model
        self.index_dir = index_dir
        self.index_cache = {}  # 缓存索引数据
    
    def retrieve(
        self,
        query: str,
        top_k: int = TOP_K,
        layer: Optional[str] = None,  # dao | shu
        doc_type: Optional[str] = None,  # theory | methodology | ...
        expand_related: bool = True  # 是否扩展关联文档
    ) -> List[Dict]:
        """
        混合检索
        
        Args:
            query: 查询文本
            top_k: 返回结果数量
            layer: 层级过滤（道/术）
            doc_type: 文档类型过滤
            expand_related: 是否扩展关联文档
            
        Returns:
            检索结果列表，每个结果包含：
            - doc_id: 文档ID
            - content: 文档内容
            - score: 相关性分数
            - metadata: 元数据
        """
        logger.info(f"开始检索: {query}")
        
        # 1. 向量检索
        query_embedding = self.embedding_model.encode_query(query)
        vector_results = self.vector_store.search(
            query_embedding,
            n_results=top_k * 3,  # 多召回一些，后续重排序
            where=self._build_filter(layer, doc_type)
        )
        
        # 2. 关键词匹配（query_patterns）
        pattern_matches = self._match_query_patterns(query, layer, doc_type)
        
        # 3. 结果融合与重排序
        final_results = self._rerank(
            vector_results,
            pattern_matches,
            query,
            top_k,
            expand_related
        )
        
        logger.info(f"检索完成，返回 {len(final_results)} 个结果")
        return final_results
    
    def _match_query_patterns(
        self,
        query: str,
        layer: Optional[str] = None,
        doc_type: Optional[str] = None
    ) -> List[str]:
        """
        匹配query_patterns
        
        Args:
            query: 查询文本
            layer: 层级过滤
            doc_type: 文档类型过滤
            
        Returns:
            匹配的文档ID列表
        """
        matches = []
        query_lower = query.lower()
        
        for index_file in self.index_dir.glob("*.yaml"):
            doc_id = index_file.stem
            
            # 加载索引
            if doc_id not in self.index_cache:
                try:
                    with open(index_file, 'r', encoding='utf-8') as f:
                        self.index_cache[doc_id] = yaml.safe_load(f)
                except Exception as e:
                    logger.warning(f"加载索引文件失败 {index_file}: {e}")
                    continue
            
            index_data = self.index_cache[doc_id]
            
            # 过滤检查
            if layer and index_data.get('layer') != layer:
                continue
            if doc_type and index_data.get('doc_type') != doc_type:
                continue
            
            # 匹配query_patterns
            patterns = index_data.get('query_patterns', [])
            for pattern in patterns:
                pattern_lower = pattern.lower()
                # 简单匹配：查询包含模式或模式包含查询
                if pattern_lower in query_lower or query_lower in pattern_lower:
                    matches.append(doc_id)
                    break
        
        return matches
    
    def _expand_related_docs(self, doc_ids: List[str]) -> Set[str]:
        """
        扩展关联文档
        
        Args:
            doc_ids: 文档ID列表
            
        Returns:
            扩展后的文档ID集合（包含原始文档和关联文档）
        """
        related_docs = set(doc_ids)
        
        for doc_id in doc_ids:
            if doc_id not in self.index_cache:
                index_file = self.index_dir / f"{doc_id}.yaml"
                if index_file.exists():
                    try:
                        with open(index_file, 'r', encoding='utf-8') as f:
                            self.index_cache[doc_id] = yaml.safe_load(f)
                    except Exception as e:
                        logger.warning(f"加载索引文件失败 {index_file}: {e}")
                        continue
            
            if doc_id in self.index_cache:
                related = self.index_cache[doc_id].get('related_docs', [])
                related_docs.update(related)
        
        return related_docs
    
    def _rerank(
        self,
        vector_results: Dict,
        pattern_matches: List[str],
        query: str,
        top_k: int,
        expand_related: bool
    ) -> List[Dict]:
        """
        重排序结果
        
        Args:
            vector_results: 向量检索结果
            pattern_matches: 关键词匹配的文档ID
            query: 查询文本
            top_k: 返回数量
            expand_related: 是否扩展关联文档
            
        Returns:
            重排序后的结果列表
        """
        # 收集所有候选结果
        candidates = {}
        
        # 处理向量检索结果
        if vector_results and 'ids' in vector_results and vector_results['ids']:
            ids = vector_results['ids'][0]
            documents = vector_results['documents'][0]
            metadatas = vector_results['metadatas'][0]
            distances = vector_results['distances'][0] if 'distances' in vector_results else [0.0] * len(ids)
            
            for i, doc_id_chunk in enumerate(ids):
                # 提取doc_id（格式：DOC-D001_metadata_0）
                doc_id = doc_id_chunk.split('_')[0]
                
                score = 1.0 - distances[i]  # 距离转相似度
                weight = float(metadatas[i].get('weight', 1.0))
                
                # 应用权重
                final_score = score * weight
                
                # 如果是query_pattern匹配，额外加分
                if doc_id in pattern_matches:
                    final_score *= 1.5
                
                # 如果是core文档，额外加分
                doc_weight = metadatas[i].get('doc_weight', 'important')
                if doc_weight == 'core':
                    final_score *= 1.3
                elif doc_weight == 'important':
                    final_score *= 1.1
                
                # 合并同一文档的不同块
                if doc_id not in candidates:
                    candidates[doc_id] = {
                        'doc_id': doc_id,
                        'content': documents[i],
                        'score': final_score,
                        'metadata': metadatas[i],
                        'chunks': [{
                            'content': documents[i],
                            'score': score,
                            'chunk_type': metadatas[i].get('chunk_type', 'content')
                        }]
                    }
                else:
                    # 如果这个块的分数更高，更新内容
                    if final_score > candidates[doc_id]['score']:
                        candidates[doc_id]['content'] = documents[i]
                        candidates[doc_id]['score'] = final_score
                        candidates[doc_id]['metadata'] = metadatas[i]
                    
                    # 添加块信息
                    candidates[doc_id]['chunks'].append({
                        'content': documents[i],
                        'score': score,
                        'chunk_type': metadatas[i].get('chunk_type', 'content')
                    })
        
        # 处理关键词匹配但未在向量结果中的文档
        for doc_id in pattern_matches:
            if doc_id not in candidates:
                # 加载文档摘要作为内容
                if doc_id in self.index_cache:
                    index_data = self.index_cache[doc_id]
                    candidates[doc_id] = {
                        'doc_id': doc_id,
                        'content': index_data.get('summary', ''),
                        'score': 0.8,  # 关键词匹配的基础分数
                        'metadata': {
                            'doc_type': index_data.get('doc_type', ''),
                            'layer': index_data.get('layer', ''),
                            'doc_weight': index_data.get('doc_weight', 'important')
                        },
                        'chunks': []
                    }
        
        # 扩展关联文档（可选）
        if expand_related:
            related_doc_ids = self._expand_related_docs(list(candidates.keys()))
            for doc_id in related_doc_ids:
                if doc_id not in candidates and doc_id in self.index_cache:
                    index_data = self.index_cache[doc_id]
                    # 关联文档分数较低
                    candidates[doc_id] = {
                        'doc_id': doc_id,
                        'content': index_data.get('summary', ''),
                        'score': 0.5,
                        'metadata': {
                            'doc_type': index_data.get('doc_type', ''),
                            'layer': index_data.get('layer', ''),
                            'doc_weight': index_data.get('doc_weight', 'important')
                        },
                        'chunks': [],
                        'is_related': True
                    }
        
        # 按分数排序
        sorted_results = sorted(
            candidates.values(),
            key=lambda x: x['score'],
            reverse=True
        )
        
        # 返回Top-K
        return sorted_results[:top_k]
    
    def _build_filter(
        self,
        layer: Optional[str] = None,
        doc_type: Optional[str] = None
    ) -> Optional[Dict]:
        """
        构建过滤条件
        
        Args:
            layer: 层级（dao/shu）
            doc_type: 文档类型
            
        Returns:
            过滤条件字典或None
        """
        where = {}
        
        if layer:
            where['layer'] = layer
        if doc_type:
            where['doc_type'] = doc_type
        
        return where if where else None
    
    def get_doc_info(self, doc_id: str) -> Optional[Dict]:
        """
        获取文档信息
        
        Args:
            doc_id: 文档ID
            
        Returns:
            文档索引信息
        """
        if doc_id not in self.index_cache:
            index_file = self.index_dir / f"{doc_id}.yaml"
            if index_file.exists():
                try:
                    with open(index_file, 'r', encoding='utf-8') as f:
                        self.index_cache[doc_id] = yaml.safe_load(f)
                except Exception as e:
                    logger.warning(f"加载索引文件失败 {index_file}: {e}")
                    return None
        
        return self.index_cache.get(doc_id)
