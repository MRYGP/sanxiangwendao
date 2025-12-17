"""
更新索引脚本
用于增量更新单个或部分文档的索引
"""

import sys
import logging
from pathlib import Path
from typing import List

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from rag_system.config import (
    INDEX_DIR, VECTOR_DB_DIR, COLLECTION_NAME,
    EMBEDDING_MODEL, EMBEDDING_DEVICE, DOC_MAPPING
)
from rag_system.embedding import EmbeddingModel
from rag_system.document_loader import DocumentLoader
from rag_system.vector_store import VectorStore

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def update_document(doc_id: str, delete_old: bool = True):
    """
    更新单个文档的索引
    
    Args:
        doc_id: 文档ID
        delete_old: 是否删除旧的文档块
    """
    logger.info(f"更新文档索引: {doc_id}")
    
    # 初始化组件
    embedding_model = EmbeddingModel(EMBEDDING_MODEL, EMBEDDING_DEVICE)
    vector_store = VectorStore(VECTOR_DB_DIR, COLLECTION_NAME)
    document_loader = DocumentLoader()
    
    # 删除旧的文档块（如果需要）
    if delete_old:
        # 注意：Chroma不直接支持按metadata删除，需要先查询再删除
        # 这里简化处理，实际可能需要更复杂的逻辑
        logger.info(f"删除文档 {doc_id} 的旧索引...")
        # TODO: 实现删除逻辑
    
    # 加载文档
    try:
        doc = document_loader.load_document(doc_id)
    except Exception as e:
        logger.error(f"加载文档失败: {e}")
        return False
    
    # 分块
    chunks = document_loader.chunk_document(doc)
    logger.info(f"文档分块完成，共 {len(chunks)} 个块")
    
    # 向量化
    chunk_texts = [chunk['content'] for chunk in chunks]
    embeddings = embedding_model.encode_batch(
        chunk_texts,
        batch_size=32,
        show_progress_bar=True
    )
    
    # 生成ID
    chunk_ids = [
        f"{doc_id}_{chunk['chunk_type']}_{chunk.get('chunk_index', chunk.get('pattern_index', chunk.get('example_index', 0)))}"
        for chunk in chunks
    ]
    
    # 添加到向量数据库
    try:
        vector_store.add_documents(chunks, embeddings, chunk_ids)
        logger.info(f"✅ 文档 {doc_id} 索引更新成功")
        return True
    except Exception as e:
        logger.error(f"❌ 文档 {doc_id} 索引更新失败: {e}")
        return False

def update_documents(doc_ids: List[str], delete_old: bool = True):
    """
    批量更新文档索引
    
    Args:
        doc_ids: 文档ID列表
        delete_old: 是否删除旧的文档块
    """
    logger.info(f"批量更新 {len(doc_ids)} 个文档的索引")
    
    success_count = 0
    for doc_id in doc_ids:
        if update_document(doc_id, delete_old):
            success_count += 1
    
    logger.info(f"更新完成: {success_count}/{len(doc_ids)} 成功")
    return success_count

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="更新RAG知识库索引")
    parser.add_argument(
        "doc_ids",
        nargs="+",
        help="要更新的文档ID列表（如 DOC-D001 DOC-S010）"
    )
    parser.add_argument(
        "--no-delete",
        action="store_true",
        help="不删除旧的文档块（可能导致重复）"
    )
    
    args = parser.parse_args()
    
    # 验证文档ID
    invalid_ids = [doc_id for doc_id in args.doc_ids if doc_id not in DOC_MAPPING]
    if invalid_ids:
        logger.error(f"无效的文档ID: {invalid_ids}")
        logger.info(f"可用的文档ID: {list(DOC_MAPPING.keys())[:10]}...")
        sys.exit(1)
    
    try:
        update_documents(args.doc_ids, delete_old=not args.no_delete)
    except KeyboardInterrupt:
        logger.info("\n用户中断操作")
    except Exception as e:
        logger.error(f"更新索引失败: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()
