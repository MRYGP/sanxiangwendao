# RAG知识库系统 - 安装指南

## 📋 前置要求

- Python 3.8+
- 8GB+ 内存（运行Embedding模型）
- 可选：NVIDIA GPU（加速向量化）

## 🚀 快速安装

### 1. 创建虚拟环境（推荐）

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置环境变量

```bash
# 复制环境变量模板
copy env.example.txt .env  # Windows
# 或
cp env.example.txt .env   # Linux/Mac

# 编辑 .env 文件，填入你的配置
# 特别是 OPENAI_API_KEY（如果使用OpenAI）
```

### 4. 验证安装

```bash
python -c "import langchain; import chromadb; import sentence_transformers; print('安装成功！')"
```

## 📁 项目结构

```
wendao/
├── rag-system/          # 核心RAG系统代码
│   ├── __init__.py
│   ├── config.py
│   ├── embedding.py
│   ├── document_loader.py
│   ├── vector_store.py
│   ├── retriever.py
│   └── ...
├── scripts/             # 工具脚本
│   ├── build_index.py
│   ├── test_query.py
│   └── ...
├── api/                 # API接口（可选）
│   └── ...
├── vector_db/           # 向量数据库存储目录
├── rag-index/           # 文档索引配置
│   └── indexes/         # 39个文档的YAML索引
├── requirements.txt      # Python依赖
└── .env                 # 环境变量配置
```

## 🔧 配置说明

### Embedding模型选择

**选项1：BGE-M3（推荐，免费）**
- 模型大小：约2.2GB
- 首次运行会自动下载
- 支持中英文混合检索

**选项2：OpenAI Embedding（付费，效果最好）**
- 需要在 .env 中配置 OPENAI_API_KEY
- 按使用量付费

### 向量数据库

默认使用 **Chroma**（轻量级，无需额外配置）

如需使用 Qdrant 或 Milvus，需要：
1. 安装对应依赖
2. 修改 `rag-system/config.py` 中的配置
3. 启动对应的服务

### LLM选择

**选项1：OpenAI（推荐用于开发）**
- 配置 OPENAI_API_KEY
- 模型：gpt-3.5-turbo 或 gpt-4

**选项2：Ollama（本地部署，免费）**
- 需要先安装 Ollama：https://ollama.ai
- 下载模型：`ollama pull qwen2.5`
- 配置 OLLAMA_BASE_URL

## 📝 下一步

安装完成后，继续：

1. **构建索引**：`python scripts/build_index.py`
2. **测试查询**：`python scripts/test_query.py "你的问题"`
3. **查看实施方案**：`RAG知识库实施方案.md`

## ❓ 常见问题

### Q: 安装 sentence-transformers 很慢？
A: 使用国内镜像：
```bash
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple sentence-transformers
```

### Q: 内存不足？
A: 
- 使用更小的Embedding模型
- 或使用OpenAI Embedding API

### Q: 需要GPU吗？
A: 不是必须的，CPU也可以运行，只是速度较慢。有GPU会自动使用。

## 📚 相关文档

- [RAG知识库实施方案.md](./RAG知识库实施方案.md) - 完整实施方案
- [RAG知识库索引方案_v2_精简版.md](./RAG知识库索引方案_v2_精简版.md) - 索引设计
- [rag-system/README.md](./rag-system/README.md) - 代码使用说明
