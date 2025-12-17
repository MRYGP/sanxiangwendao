# RAG知识库系统

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 构建索引

```bash
python scripts/build_index.py
```

### 3. 测试查询

```bash
python scripts/test_query.py "你的问题"
```

## 项目结构

```
rag-system/
├── config.py           # 配置文件
├── embedding.py        # Embedding模型封装
├── document_loader.py  # 文档加载器
├── vector_store.py     # 向量数据库封装
├── retriever.py        # 检索器实现
├── query_processor.py # 查询处理
└── rag_chain.py       # RAG链实现

scripts/
├── build_index.py     # 构建索引
├── test_query.py      # 测试查询
└── update_index.py   # 更新索引

api/
├── app.py             # FastAPI应用
└── routes.py          # API路由
```

## 配置说明

在 `config.py` 中配置：
- Embedding模型路径
- 向量数据库路径
- LLM API密钥
- 检索参数

## 使用示例

```python
from rag_system.retriever import HybridRetriever
from rag_system.embedding import EmbeddingModel
from rag_system.vector_store import VectorStore

# 初始化
embedding_model = EmbeddingModel("BAAI/bge-m3")
vector_store = VectorStore("vector_db", "wendao_kb")
retriever = HybridRetriever(vector_store, embedding_model, "rag-index/indexes")

# 检索
results = retriever.retrieve("AI用多了会变傻吗", top_k=5)
```
