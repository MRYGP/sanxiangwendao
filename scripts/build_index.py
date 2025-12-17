"""
构建向量索引脚本
批量加载39篇文档，进行分块、向量化，存储到向量数据库
"""

import sys
import logging
from pathlib import Path
from tqdm import tqdm

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from rag_system.config import (
    INDEX_DIR, VECTOR_DB_DIR, COLLECTION_NAME,
    EMBEDDING_MODEL, EMBEDDING_DEVICE,
    DOC_MAPPING
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

def build_index(reset: bool = False):
    """
    构建向量索引
    
    Args:
        reset: 是否重置现有索引
    """
    logger.info("=" * 60)
    logger.info("开始构建RAG知识库向量索引")
    logger.info("=" * 60)
    
    # 1. 初始化组件
    logger.info("初始化组件...")
    embedding_model = EmbeddingModel(EMBEDDING_MODEL, EMBEDDING_DEVICE)
    vector_store = VectorStore(VECTOR_DB_DIR, COLLECTION_NAME)
    document_loader = DocumentLoader()
    
    # 2. 重置索引（如果需要）
    if reset:
        logger.warning("重置现有索引...")
        vector_store.reset_collection()
    
    # 3. 获取所有文档ID
    doc_ids = list(DOC_MAPPING.keys())
    logger.info(f"共 {len(doc_ids)} 篇文档需要处理")
    
    # 4. 批量处理文档
    all_chunks = []
    all_embeddings = []
    all_ids = []
    
    logger.info("开始处理文档...")
    for doc_id in tqdm(doc_ids, desc="处理文档"):
        try:
            # 加载文档
            doc = document_loader.load_document(doc_id)
            logger.debug(f"加载文档: {doc_id} - {doc['index'].get('title', '')}")
            
            # 分块
            chunks = document_loader.chunk_document(doc)
            logger.debug(f"文档 {doc_id} 分块完成，共 {len(chunks)} 个块")
            
            # 向量化
            chunk_texts = [chunk['content'] for chunk in chunks]
            embeddings = embedding_model.encode_batch(
                chunk_texts,
                batch_size=32,
                show_progress_bar=False
            )
            
            # 生成ID
            chunk_ids = [
                f"{doc_id}_{chunk['chunk_type']}_{chunk.get('chunk_index', chunk.get('pattern_index', chunk.get('example_index', 0)))}"
                for chunk in chunks
            ]
            
            # 收集数据
            all_chunks.extend(chunks)
            all_embeddings.extend(embeddings)
            all_ids.extend(chunk_ids)
            
            logger.info(f"✅ {doc_id} 处理完成: {len(chunks)} 个块")
            
        except Exception as e:
            logger.error(f"❌ 处理文档 {doc_id} 失败: {e}")
            continue
    
    # 5. 批量添加到向量数据库
    if all_chunks:
        logger.info(f"\n开始添加到向量数据库，共 {len(all_chunks)} 个块...")
        
        # 分批添加（避免内存问题）
        batch_size = 100
        for i in tqdm(range(0, len(all_chunks), batch_size), desc="添加到向量数据库"):
            batch_chunks = all_chunks[i:i+batch_size]
            batch_embeddings = all_embeddings[i:i+batch_size]
            batch_ids = all_ids[i:i+batch_size]
            
            try:
                vector_store.add_documents(
                    batch_chunks,
                    batch_embeddings,
                    batch_ids
                )
            except Exception as e:
                logger.error(f"添加批次 {i//batch_size + 1} 失败: {e}")
        
        logger.info("✅ 所有文档块已添加到向量数据库")
    else:
        logger.warning("没有文档块需要添加")
    
    # 6. 显示统计信息
    info = vector_store.get_collection_info()
    logger.info("\n" + "=" * 60)
    logger.info("索引构建完成！")
    logger.info("=" * 60)
    logger.info(f"集合名称: {info['collection_name']}")
    logger.info(f"文档块数量: {info['document_count']}")
    logger.info(f"数据库路径: {info['db_path']}")
    logger.info("=" * 60)

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="构建RAG知识库向量索引")
    parser.add_argument(
        "--reset",
        action="store_true",
        help="重置现有索引（删除所有数据）"
    )
    
    args = parser.parse_args()
    
    try:
        build_index(reset=args.reset)
    except KeyboardInterrupt:
        logger.info("\n用户中断操作")
    except Exception as e:
        logger.error(f"构建索引失败: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()
