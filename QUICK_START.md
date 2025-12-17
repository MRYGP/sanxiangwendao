# RAG知识库系统 - 快速开始指南

## 🚀 5分钟快速开始

### 步骤1：安装依赖

```bash
# 创建虚拟环境（推荐）
python -m venv venv
venv\Scripts\activate  # Windows
# 或
source venv/bin/activate  # Linux/Mac

# 安装依赖
pip install -r requirements.txt
```

### 步骤2：配置环境变量（可选）

```bash
# 复制环境变量模板
copy env.example.txt .env  # Windows
# 或
cp env.example.txt .env   # Linux/Mac

# 编辑 .env 文件，填入你的配置
# 特别是 OPENAI_API_KEY（如果使用OpenAI生成回答）
```

### 步骤3：构建索引

```bash
# 构建向量索引（首次运行需要几分钟）
python scripts/build_index.py
```

**首次运行会：**
- 自动下载BGE-M3模型（约2.2GB，只需下载一次）
- 加载39篇文档
- 进行分块和向量化
- 存储到向量数据库

### 步骤4：测试查询

```bash
# 交互式测试
python scripts/test_query.py

# 或测试单个查询
python scripts/test_query.py --query "AI用多了会变傻吗"

# 批量测试（20个测试查询）
python scripts/test_query.py --batch
```

## 📖 使用示例

### 示例1：简单检索

```python
from rag_system.config import *
from rag_system.embedding import EmbeddingModel
from rag_system.vector_store import VectorStore
from rag_system.retriever import HybridRetriever

# 初始化
embedding_model = EmbeddingModel(EMBEDDING_MODEL, EMBEDDING_DEVICE)
vector_store = VectorStore(VECTOR_DB_DIR, COLLECTION_NAME)
retriever = HybridRetriever(vector_store, embedding_model, INDEX_DIR)

# 检索
results = retriever.retrieve("AI用多了会变傻吗", top_k=5)

# 查看结果
for result in results:
    print(f"{result['doc_id']}: {result['score']:.3f}")
    print(f"  {result['content'][:200]}...")
```

### 示例2：完整RAG查询

```python
from rag_system.rag_chain import RAGChain

# 初始化RAG链
rag_chain = RAGChain(retriever, use_llm=True)

# 查询
result = rag_chain.query("如何进行产品创新", top_k=5)

# 查看结果
print("回答:", result['answer'])
print("\n来源文档:")
for source in result['sources']:
    print(f"  - {source['doc_id']}: {source['title']}")
```

## 🛠️ 常用命令

### 构建索引

```bash
# 首次构建
python scripts/build_index.py

# 重置并重新构建
python scripts/build_index.py --reset
```

### 测试查询

```bash
# 交互式测试
python scripts/test_query.py

# 单个查询
python scripts/test_query.py --query "你的问题"

# 批量测试
python scripts/test_query.py --batch

# 使用LLM生成回答
python scripts/test_query.py --query "你的问题" --mode rag --use-llm
```

### 更新索引

```bash
# 更新单个文档
python scripts/update_index.py DOC-D001

# 更新多个文档
python scripts/update_index.py DOC-D001 DOC-S010
```

## 📊 项目结构

```
wendao/
├── rag-system/          # 核心RAG系统
│   ├── config.py
│   ├── embedding.py
│   ├── document_loader.py
│   ├── vector_store.py
│   ├── retriever.py
│   ├── query_processor.py
│   └── rag_chain.py
├── scripts/             # 工具脚本
│   ├── build_index.py
│   ├── test_query.py
│   └── update_index.py
├── vector_db/           # 向量数据库（自动生成）
├── rag-index/           # 文档索引配置
│   └── indexes/         # 39个YAML索引文件
├── requirements.txt
└── .env                 # 环境变量配置
```

## ❓ 常见问题

### Q1: 首次运行很慢？
**A:** 首次运行需要下载BGE-M3模型（约2.2GB），这是正常的。后续运行会很快。

### Q2: 内存不足？
**A:** 
- 确保至少8GB内存
- 或使用OpenAI Embedding API（需要API Key）

### Q3: 找不到模块？
**A:** 
- 确保在项目根目录运行脚本
- 确保虚拟环境已激活
- 确保已安装所有依赖：`pip install -r requirements.txt`

### Q4: LLM生成回答失败？
**A:** 
- 检查是否配置了 `OPENAI_API_KEY`
- 或使用 `--mode retrieval` 仅测试检索功能

## 📚 更多文档

- [SETUP.md](./SETUP.md) - 详细安装指南
- [RAG知识库实施方案.md](./RAG知识库实施方案.md) - 完整实施方案
- [scripts/README.md](./scripts/README.md) - 脚本使用说明
- [rag-system/README.md](./rag-system/README.md) - 代码使用说明

## 🎯 下一步

1. ✅ 安装依赖
2. ✅ 构建索引
3. ✅ 测试查询
4. 🔄 集成到你的应用
5. 🔄 优化检索效果

---

**祝使用愉快！** 🚀
