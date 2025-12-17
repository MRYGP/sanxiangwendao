"""
查询处理模块
负责查询意图识别、查询改写等
"""

import re
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)

class QueryProcessor:
    """查询处理器"""
    
    def __init__(self):
        """初始化查询处理器"""
        # 意图关键词映射
        self.intent_keywords = {
            'theory': ['理论', '原理', '机制', '模型', '框架', '为什么', '是什么', '如何理解'],
            'methodology': ['方法', '如何做', '怎么做', '步骤', '流程', '技巧', '策略'],
            'example': ['例子', '案例', '示例', '场景', '应用'],
            'comparison': ['区别', '对比', '比较', '差异', 'vs', '和', '与'],
        }
        
        # 层级关键词
        self.layer_keywords = {
            'dao': ['道', '理念', '价值观', '思维', '认知', '哲学'],
            'shu': ['术', '方法', '技巧', '执行', '实践', '操作']
        }
    
    def process_query(
        self,
        query: str
    ) -> Dict:
        """
        处理查询
        
        Args:
            query: 原始查询
            
        Returns:
            处理后的查询信息，包含：
            - original_query: 原始查询
            - intent: 意图（theory/methodology/example/comparison/general）
            - layer: 层级（dao/shu/None）
            - doc_type: 文档类型（theory/methodology/.../None）
            - enhanced_query: 增强后的查询
        """
        query_lower = query.lower()
        
        # 意图识别
        intent = self._detect_intent(query)
        
        # 层级识别
        layer = self._detect_layer(query)
        
        # 文档类型识别
        doc_type = self._detect_doc_type(query)
        
        # 查询增强
        enhanced_query = self._enhance_query(query, intent)
        
        result = {
            'original_query': query,
            'intent': intent,
            'layer': layer,
            'doc_type': doc_type,
            'enhanced_query': enhanced_query
        }
        
        logger.info(f"查询处理结果: {result}")
        return result
    
    def _detect_intent(self, query: str) -> str:
        """检测查询意图"""
        query_lower = query.lower()
        
        scores = {}
        for intent, keywords in self.intent_keywords.items():
            score = sum(1 for kw in keywords if kw in query_lower)
            if score > 0:
                scores[intent] = score
        
        if scores:
            return max(scores, key=scores.get)
        
        return 'general'
    
    def _detect_layer(self, query: str) -> Optional[str]:
        """检测层级"""
        query_lower = query.lower()
        
        for layer, keywords in self.layer_keywords.items():
            if any(kw in query_lower for kw in keywords):
                return layer
        
        return None
    
    def _detect_doc_type(self, query: str) -> Optional[str]:
        """检测文档类型"""
        query_lower = query.lower()
        
        # 理论类
        if any(kw in query_lower for kw in ['理论', '原理', '机制', '模型']):
            return 'theory'
        
        # 方法论类
        if any(kw in query_lower for kw in ['方法', '框架', '流程', '步骤']):
            return 'methodology'
        
        # 技巧类
        if any(kw in query_lower for kw in ['技巧', '如何', '怎么', '怎样']):
            return 'technique'
        
        # 哲学类
        if any(kw in query_lower for kw in ['意义', '价值', '人生', '哲学']):
            return 'philosophy'
        
        return None
    
    def _enhance_query(self, query: str, intent: str) -> str:
        """
        增强查询（添加相关关键词）
        
        Args:
            query: 原始查询
            intent: 意图
            
        Returns:
            增强后的查询
        """
        # 根据意图添加相关关键词
        enhancements = {
            'theory': ' 理论 原理 机制',
            'methodology': ' 方法 步骤 流程',
            'example': ' 例子 案例 示例',
        }
        
        if intent in enhancements:
            return query + enhancements[intent]
        
        return query
