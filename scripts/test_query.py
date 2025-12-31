"""
测试查询脚本
使用测试用例验证RAG系统的检索效果
"""

import sys
import logging
from pathlib import Path
from typing import List, Dict

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# 处理 rag-system 目录的导入（目录名包含连字符，不能直接导入）
import importlib.util
rag_system_path = project_root / "rag-system"
rag_system_init = rag_system_path / "__init__.py"
if rag_system_init.exists():
    spec = importlib.util.spec_from_file_location("rag_system", rag_system_init)
    rag_system_module = importlib.util.module_from_spec(spec)
    sys.modules["rag_system"] = rag_system_module
    spec.loader.exec_module(rag_system_module)
    # 导入子模块
    for module_file in ["config", "embedding", "vector_store", "retriever", "rag_chain"]:
        module_path = rag_system_path / f"{module_file}.py"
        if module_path.exists():
            spec = importlib.util.spec_from_file_location(f"rag_system.{module_file}", module_path)
            module = importlib.util.module_from_spec(spec)
            sys.modules[f"rag_system.{module_file}"] = module
            spec.loader.exec_module(module)

from rag_system.config import (
    INDEX_DIR, VECTOR_DB_DIR, COLLECTION_NAME,
    EMBEDDING_MODEL, EMBEDDING_DEVICE, TOP_K
)
from rag_system.embedding import EmbeddingModel
from rag_system.vector_store import VectorStore
from rag_system.retriever import HybridRetriever
from rag_system.rag_chain import RAGChain

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 测试查询列表
TEST_QUERIES = [
    "AI用多了会变傻吗",
    "如何进行产品创新",
    "客户嫌贵怎么沟通",
    "如何建立长期思维",
    "什么是正BUFF效应",
    "如何避免AI依赖",
    "第一性原理怎么用",
    "怎么设计简单好用的产品",
    "如何让客户HI起来",
    "怎么做到用户思维",
    "如何理解客户真实需求",
    "沟通时怎么引导对方",
    "如何从0到1启动项目",
    "最小可行启动点是什么",
    "马斯克五步工作法是什么",
    "如何应对不确定性",
    "动态决策框架怎么用",
    "如何建立微习惯",
    "为什么知道却做不到",
    "如何保持初心",
]

def test_retrieval(query: str, top_k: int = TOP_K) -> Dict:
    """
    测试检索功能
    
    Args:
        query: 查询文本
        top_k: 返回结果数量
        
    Returns:
        检索结果
    """
    logger.info(f"\n{'='*60}")
    logger.info(f"查询: {query}")
    logger.info(f"{'='*60}")
    
    # 初始化组件
    embedding_model = EmbeddingModel(EMBEDDING_MODEL, EMBEDDING_DEVICE)
    vector_store = VectorStore(VECTOR_DB_DIR, COLLECTION_NAME)
    retriever = HybridRetriever(vector_store, embedding_model, INDEX_DIR)
    
    # 执行检索
    results = retriever.retrieve(query, top_k=top_k)
    
    # 显示结果
    logger.info(f"\n检索到 {len(results)} 个结果:\n")
    for i, result in enumerate(results, 1):
        doc_id = result['doc_id']
        score = result['score']
        content_preview = result['content'][:150] + "..." if len(result['content']) > 150 else result['content']
        
        logger.info(f"[{i}] {doc_id} (分数: {score:.3f})")
        logger.info(f"    内容: {content_preview}")
        logger.info("")
    
    return {
        'query': query,
        'results': results,
        'count': len(results)
    }

def test_rag_chain(query: str, top_k: int = TOP_K, use_llm: bool = False) -> Dict:
    """
    测试完整RAG链
    
    Args:
        query: 查询文本
        top_k: 返回结果数量
        use_llm: 是否使用LLM生成回答
        
    Returns:
        RAG结果
    """
    logger.info(f"\n{'='*60}")
    logger.info(f"RAG查询: {query}")
    logger.info(f"{'='*60}")
    
    # 初始化组件
    embedding_model = EmbeddingModel(EMBEDDING_MODEL, EMBEDDING_DEVICE)
    vector_store = VectorStore(VECTOR_DB_DIR, COLLECTION_NAME)
    retriever = HybridRetriever(vector_store, embedding_model, INDEX_DIR)
    rag_chain = RAGChain(retriever, llm_provider="openai", use_llm=use_llm)
    
    # 执行RAG查询
    result = rag_chain.query(query, top_k=top_k, use_llm=use_llm)
    
    # 显示结果
    logger.info(f"\n处理后的查询:")
    logger.info(f"  意图: {result['processed_query']['intent']}")
    logger.info(f"  层级: {result['processed_query']['layer'] or '无'}")
    logger.info(f"  类型: {result['processed_query']['doc_type'] or '无'}")
    
    logger.info(f"\n检索到 {len(result['retrieved_docs'])} 个文档:")
    for i, doc in enumerate(result['retrieved_docs'], 1):
        logger.info(f"  [{i}] {doc['doc_id']} (分数: {doc['score']:.3f})")
    
    if result['answer']:
        logger.info(f"\n生成的回答:")
        logger.info(f"  {result['answer']}")
    
    logger.info(f"\n来源文档:")
    for i, source in enumerate(result['sources'], 1):
        logger.info(f"  [{i}] {source['doc_id']} - {source['title']}")
    
    return result

def run_batch_tests(queries: List[str] = None, mode: str = "retrieval"):
    """
    批量运行测试
    
    Args:
        queries: 查询列表，如果为None则使用默认测试查询
        mode: 测试模式 ("retrieval" 或 "rag")
    """
    if queries is None:
        queries = TEST_QUERIES
    
    logger.info("=" * 60)
    logger.info(f"开始批量测试 ({mode} 模式)")
    logger.info(f"测试查询数量: {len(queries)}")
    logger.info("=" * 60)
    
    results = []
    for i, query in enumerate(queries, 1):
        logger.info(f"\n[{i}/{len(queries)}]")
        try:
            if mode == "retrieval":
                result = test_retrieval(query)
            else:
                result = test_rag_chain(query, use_llm=False)
            results.append(result)
        except Exception as e:
            logger.error(f"测试查询失败: {query} - {e}")
            results.append({'query': query, 'error': str(e)})
    
    # 统计信息
    logger.info("\n" + "=" * 60)
    logger.info("测试完成统计")
    logger.info("=" * 60)
    successful = sum(1 for r in results if 'error' not in r)
    logger.info(f"成功: {successful}/{len(results)}")
    logger.info(f"失败: {len(results) - successful}/{len(results)}")
    
    return results

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="测试RAG系统查询功能")
    parser.add_argument(
        "--query",
        type=str,
        help="单个查询文本"
    )
    parser.add_argument(
        "--mode",
        choices=["retrieval", "rag"],
        default="retrieval",
        help="测试模式: retrieval(仅检索) 或 rag(完整RAG链)"
    )
    parser.add_argument(
        "--batch",
        action="store_true",
        help="批量测试（使用默认测试查询列表）"
    )
    parser.add_argument(
        "--top-k",
        type=int,
        default=TOP_K,
        help="返回结果数量"
    )
    parser.add_argument(
        "--use-llm",
        action="store_true",
        help="使用LLM生成回答（仅rag模式）"
    )
    
    args = parser.parse_args()
    
    try:
        if args.batch:
            # 批量测试
            run_batch_tests(mode=args.mode)
        elif args.query:
            # 单个查询测试
            if args.mode == "retrieval":
                test_retrieval(args.query, top_k=args.top_k)
            else:
                test_rag_chain(args.query, top_k=args.top_k, use_llm=args.use_llm)
        else:
            # 交互式测试
            logger.info("RAG系统测试工具")
            logger.info("输入查询（输入 'quit' 退出）\n")
            
            while True:
                query = input("查询: ").strip()
                if query.lower() in ['quit', 'exit', 'q']:
                    break
                if not query:
                    continue
                
                try:
                    if args.mode == "retrieval":
                        test_retrieval(query, top_k=args.top_k)
                    else:
                        test_rag_chain(query, top_k=args.top_k, use_llm=args.use_llm)
                except Exception as e:
                    logger.error(f"查询失败: {e}")
    
    except KeyboardInterrupt:
        logger.info("\n用户中断操作")
    except Exception as e:
        logger.error(f"测试失败: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()
