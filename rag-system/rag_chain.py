"""
RAG链实现
整合检索和生成
"""

from typing import List, Dict, Optional
import logging

from .retriever import HybridRetriever
from .query_processor import QueryProcessor
from .config import LLM_PROVIDER, LLM_MODEL, OPENAI_API_KEY

logger = logging.getLogger(__name__)

class RAGChain:
    """RAG链"""
    
    def __init__(
        self,
        retriever: HybridRetriever,
        query_processor: Optional[QueryProcessor] = None,
        llm_provider: str = LLM_PROVIDER,
        llm_model: str = LLM_MODEL,
        use_llm: bool = True
    ):
        """
        初始化RAG链
        
        Args:
            retriever: 检索器实例
            query_processor: 查询处理器（可选）
            llm_provider: LLM提供商
            llm_model: LLM模型名称
            use_llm: 是否启用LLM（如果为False，只返回检索结果）
        """
        self.retriever = retriever
        self.query_processor = query_processor or QueryProcessor()
        self.llm_provider = llm_provider
        self.llm_model = llm_model
        self.use_llm = use_llm
        self.llm = None
        
        # 初始化LLM（如果需要）
        if use_llm:
            if llm_provider == "openai":
                self._init_openai()
            elif llm_provider == "ollama":
                self._init_ollama()
    
    def _init_openai(self):
        """初始化OpenAI"""
        try:
            from openai import OpenAI
            if not OPENAI_API_KEY:
                logger.warning("OPENAI_API_KEY未设置，将无法使用LLM生成回答")
            else:
                self.llm = OpenAI(api_key=OPENAI_API_KEY)
                logger.info("OpenAI LLM初始化成功")
        except ImportError:
            logger.warning("openai包未安装，将无法使用LLM生成回答")
    
    def _init_ollama(self):
        """初始化Ollama"""
        try:
            from langchain_community.llms import Ollama
            self.llm = Ollama(model=self.llm_model)
            logger.info(f"Ollama LLM初始化成功: {self.llm_model}")
        except ImportError:
            logger.warning("ollama未安装或未运行，将无法使用LLM生成回答")
    
    def query(
        self,
        query: str,
        top_k: int = 5,
        use_llm: bool = True
    ) -> Dict:
        """
        执行RAG查询
        
        Args:
            query: 查询文本
            top_k: 检索文档数量
            use_llm: 是否使用LLM生成回答
            
        Returns:
            结果字典，包含：
            - query: 查询文本
            - retrieved_docs: 检索到的文档
            - answer: LLM生成的回答（如果use_llm=True）
            - sources: 来源文档列表
        """
        # 1. 查询处理
        processed_query = self.query_processor.process_query(query)
        
        # 2. 检索
        retrieved_docs = self.retriever.retrieve(
            processed_query['enhanced_query'],
            top_k=top_k,
            layer=processed_query['layer'],
            doc_type=processed_query['doc_type']
        )
        
        # 3. 构建上下文
        context = self._build_context(retrieved_docs)
        
        # 4. 生成回答（如果启用）
        answer = None
        if use_llm and self.llm:
            answer = self._generate_answer(query, context)
        
        # 5. 构建来源列表
        sources = [
            {
                'doc_id': doc['doc_id'],
                'title': self._get_doc_title(doc['doc_id']),
                'content': doc['content'][:200] + '...' if len(doc['content']) > 200 else doc['content'],
                'score': doc['score']
            }
            for doc in retrieved_docs
        ]
        
        return {
            'query': query,
            'processed_query': processed_query,
            'retrieved_docs': retrieved_docs,
            'context': context,
            'answer': answer,
            'sources': sources
        }
    
    def _build_context(self, docs: List[Dict]) -> str:
        """构建上下文"""
        context_parts = []
        
        for i, doc in enumerate(docs, 1):
            doc_id = doc['doc_id']
            title = self._get_doc_title(doc_id)
            content = doc['content']
            
            context_parts.append(
                f"【文档{i}】{title} (ID: {doc_id})\n{content}\n"
            )
        
        return "\n---\n".join(context_parts)
    
    def _generate_answer(self, query: str, context: str) -> str:
        """使用LLM生成回答"""
        if not self.llm:
            return None
        
        prompt = f"""基于以下知识库内容回答用户问题。

知识库内容：
{context}

用户问题：{query}

请基于上述知识库内容，用中文回答用户问题。如果知识库中没有相关信息，请说明。

回答："""
        
        try:
            if self.llm_provider == "openai":
                response = self.llm.chat.completions.create(
                    model=self.llm_model,
                    messages=[
                        {"role": "system", "content": "你是一个知识库助手，基于提供的知识库内容回答问题。"},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7,
                    max_tokens=1000
                )
                return response.choices[0].message.content
            elif self.llm_provider == "ollama":
                return self.llm.invoke(prompt)
        except Exception as e:
            logger.error(f"LLM生成回答失败: {e}")
            return None
    
    def _get_doc_title(self, doc_id: str) -> str:
        """获取文档标题"""
        doc_info = self.retriever.get_doc_info(doc_id)
        if doc_info:
            return doc_info.get('title', doc_id)
        return doc_id
