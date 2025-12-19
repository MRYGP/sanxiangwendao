# RAG知识库实施方案

> 将44篇认知体系文档构建为可检索、可问答的RAG知识库系统

---

## 📋 一、现状分析

### 1.1 已有资源

✅ **已完成**：
- 44篇核心文档（道层12篇 + 术层27篇 + 新增5篇）
- 45个索引文件（YAML格式，包含元数据，含培训材料）
- 文档映射表（doc-mapping.md）
- 学习路径配置（learning-paths.md）
- 索引方案设计文档（RAG知识库索引方案_v2_精简版.md）

❌ **待实现**：
- 文档向量化（Embedding）
- 向量数据库构建
- 检索系统实现
- 问答系统集成
- API接口开发

---

## 🏗️ 二、技术架构设计

### 2.1 整体架构

```
┌─────────────────────────────────────────────────────────┐
│                    用户查询层                            │
│  (Web界面 / API / 命令行 / GPT集成)                      │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│                   查询处理层                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │ 意图识别     │  │ 查询改写     │  │ 查询路由     │  │
│  │ (LLM)        │  │ (Query       │  │ (Layer/Type) │  │
│  │              │  │ Enhancement) │  │              │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│                   混合检索层                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │ 关键词检索   │  │ 向量检索     │  │ 关系检索     │  │
│  │ (BM25)       │  │ (Embedding)  │  │ (Graph)      │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
│           │                │                │            │
│           └────────────────┴────────────────┘            │
│                          │                                │
│                          ▼                                │
│              ┌──────────────────────┐                    │
│              │   结果融合与重排序    │                    │
│              │   (Rerank + Weight)   │                    │
│              └──────────────────────┘                    │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│                   知识库存储层                            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │ 向量数据库   │  │ 元数据索引   │  │ 文档存储     │  │
│  │ (Chroma/    │  │ (YAML解析)   │  │ (Markdown)   │  │
│  │  Milvus/    │  │              │  │              │  │
│  │  Qdrant)     │  │              │  │              │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
└─────────────────────────────────────────────────────────┘
```

### 2.2 技术选型

#### 2.2.1 向量数据库

**推荐方案（按优先级）**：

1. **Chroma** ⭐⭐⭐⭐⭐（推荐）
   - 优点：轻量级、易部署、Python原生、支持元数据过滤
   - 缺点：不适合超大规模（但44篇文档完全够用）
   - 适用场景：中小型知识库、快速原型

2. **Qdrant** ⭐⭐⭐⭐
   - 优点：性能好、支持复杂过滤、有Docker镜像
   - 缺点：需要单独部署服务
   - 适用场景：生产环境、需要高性能

3. **Milvus** ⭐⭐⭐
   - 优点：企业级、支持大规模
   - 缺点：部署复杂、资源消耗大
   - 适用场景：超大规模知识库

**选择建议**：先用 **Chroma** 快速实现，后续可迁移到 Qdrant。

#### 2.2.2 Embedding模型

**推荐方案（中文场景）**：

1. **BGE-M3** ⭐⭐⭐⭐⭐（首选）
   - 模型：`BAAI/bge-m3`
   - 优点：多语言、检索效果好、支持中文
   - 缺点：模型较大（约2.2GB）
   - 使用：HuggingFace Transformers

2. **text2vec-large-chinese** ⭐⭐⭐⭐
   - 模型：`GanymedeNil/text2vec-large-chinese`
   - 优点：专门优化中文、轻量级
   - 缺点：仅支持中文

3. **OpenAI text-embedding-3-large** ⭐⭐⭐⭐
   - 优点：效果最好、API调用简单
   - 缺点：需要API Key、有成本

**选择建议**：本地部署用 **BGE-M3**，预算充足用 **OpenAI**。

#### 2.2.3 检索框架

**推荐方案**：

1. **LangChain** ⭐⭐⭐⭐⭐
   - 优点：生态完善、文档丰富、支持多种向量库
   - 缺点：学习曲线稍陡
   - 适用：快速开发、集成LLM

2. **LlamaIndex** ⭐⭐⭐⭐
   - 优点：专门为RAG设计、查询优化好
   - 缺点：相对较新
   - 适用：复杂查询场景

**选择建议**：使用 **LangChain**（更成熟）。

#### 2.2.4 LLM集成

**推荐方案**：

1. **OpenAI GPT-4/GPT-3.5** ⭐⭐⭐⭐⭐
   - 优点：效果最好、API稳定
   - 缺点：需要API Key、有成本

2. **本地模型（Ollama）** ⭐⭐⭐⭐
   - 模型：`qwen2.5`、`deepseek-chat`
   - 优点：免费、数据安全
   - 缺点：需要本地GPU资源

**选择建议**：开发阶段用 **OpenAI**，生产环境根据需求选择。

---

## 🔧 三、实施步骤

### 阶段一：环境准备（1天）

#### 3.1 依赖安装

```bash
# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装核心依赖
pip install langchain
pip install langchain-community
pip install chromadb
pip install sentence-transformers
pip install pyyaml
pip install markdown
pip install tiktoken  # 用于token计数
```

#### 3.2 项目结构

```
wendao/
├── rag-system/              # RAG系统代码
│   ├── __init__.py
│   ├── config.py           # 配置文件
│   ├── embedding.py         # Embedding模型封装
│   ├── vector_store.py      # 向量数据库封装
│   ├── retriever.py         # 检索器实现
│   ├── query_processor.py  # 查询处理
│   └── rag_chain.py        # RAG链实现
├── scripts/                 # 工具脚本
│   ├── build_index.py      # 构建索引
│   ├── test_query.py       # 测试查询
│   └── update_index.py     # 更新索引
├── api/                    # API接口（可选）
│   ├── app.py
│   └── routes.py
├── requirements.txt
└── README.md
```

### 阶段二：核心功能实现（2-3天）

#### 3.3 文档加载与解析

**功能**：
- 读取Markdown文档
- 解析YAML Front Matter（元数据）
- 文档分块（Chunking）

**实现要点**：
```python
# 分块策略
- 元数据块：单独索引（doc_id, summary, keywords）
- 摘要块：前500字，权重1.5
- 正文块：800-1200 tokens，重叠200 tokens
- 案例块：独立提取，标注为"example"
```

#### 3.4 向量化处理

**功能**：
- 加载Embedding模型
- 对文档块进行向量化
- 存储到向量数据库

**实现要点**：
```python
# 向量化内容
1. query_patterns（单独向量化，建立问题-文档映射）
2. summary（高权重1.5）
3. keywords（BM25补充）
4. 正文块（标准权重1.0）
5. 案例块（权重1.2）
```

#### 3.5 混合检索实现

**功能**：
- 关键词检索（BM25）
- 向量检索（语义相似度）
- 关系检索（related_docs）
- 结果融合与重排序

**实现要点**：
```python
# 检索流程
1. 意图识别（理论/方法/场景）
2. 多路召回（BM25 + Vector + Graph）
3. 权重加权（doc_weight）
4. 理论链扩展（theory_chain）
5. 场景匹配（scenario_bundles）
6. 返回Top-K文档
```

### 阶段三：系统集成（1-2天）

#### 3.6 RAG链实现

**功能**：
- 查询处理
- 文档检索
- 上下文构建
- LLM生成回答

#### 3.7 API接口（可选）

**功能**：
- RESTful API
- 查询接口
- 文档管理接口

### 阶段四：测试与优化（1-2天）

#### 3.8 测试用例

- 使用 `测试查询列表_20个真实问题.md` 中的问题
- 评估检索准确率
- 优化query_patterns

#### 3.9 性能优化

- 检索速度优化
- 缓存机制
- 批量处理优化

---

## 💻 四、核心代码实现

### 4.1 配置文件（config.py）

```python
# rag-system/config.py

import os
from pathlib import Path

# 项目路径
PROJECT_ROOT = Path(__file__).parent.parent
DOCS_DIR = PROJECT_ROOT / "."
INDEX_DIR = PROJECT_ROOT / "rag-index" / "indexes"
VECTOR_DB_DIR = PROJECT_ROOT / "vector_db"

# Embedding配置
EMBEDDING_MODEL = "BAAI/bge-m3"
EMBEDDING_DEVICE = "cpu"  # 或 "cuda"

# 向量数据库配置
VECTOR_DB_TYPE = "chroma"  # chroma | qdrant | milvus
COLLECTION_NAME = "wendao_knowledge_base"

# 检索配置
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
TOP_K = 5  # 返回文档数量

# LLM配置
LLM_PROVIDER = "openai"  # openai | ollama | local
LLM_MODEL = "gpt-3.5-turbo"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# 权重配置
WEIGHT_METADATA = 1.0
WEIGHT_SUMMARY = 1.5
WEIGHT_CONTENT = 1.0
WEIGHT_EXAMPLE = 1.2
```

### 4.2 Embedding封装（embedding.py）

```python
# rag-system/embedding.py

from sentence_transformers import SentenceTransformer
from typing import List
import torch

class EmbeddingModel:
    def __init__(self, model_name: str, device: str = "cpu"):
        self.model = SentenceTransformer(model_name, device=device)
        self.device = device
    
    def encode(self, texts: List[str]) -> List[List[float]]:
        """对文本列表进行向量化"""
        embeddings = self.model.encode(
            texts,
            normalize_embeddings=True,  # 归一化，便于余弦相似度计算
            show_progress_bar=True
        )
        return embeddings.tolist()
    
    def encode_query(self, query: str) -> List[float]:
        """对查询进行向量化（可能需要不同的处理）"""
        # BGE-M3支持query指令
        query_text = f"为这个句子生成表示以用于检索相关文章：{query}"
        embedding = self.model.encode(
            [query_text],
            normalize_embeddings=True
        )
        return embedding[0].tolist()
```

### 4.3 文档加载器（document_loader.py）

```python
# rag-system/document_loader.py

import yaml
import re
from pathlib import Path
from typing import Dict, List, Tuple
import markdown
from markdown.extensions import codehilite, fenced_code

class DocumentLoader:
    def __init__(self, docs_dir: Path, index_dir: Path):
        self.docs_dir = docs_dir
        self.index_dir = index_dir
    
    def load_document(self, doc_id: str) -> Dict:
        """加载单个文档及其索引"""
        # 加载索引文件
        index_file = self.index_dir / f"{doc_id}.yaml"
        with open(index_file, 'r', encoding='utf-8') as f:
            index_data = yaml.safe_load(f)
        
        # 加载文档内容
        doc_file = self.docs_dir / index_data['title'].replace('.md', '') + '.md'
        if not doc_file.exists():
            # 尝试从doc-mapping查找文件名
            # ... 实现文件名映射逻辑
            pass
        
        with open(doc_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        return {
            'doc_id': doc_id,
            'index': index_data,
            'content': content
        }
    
    def chunk_document(self, doc: Dict) -> List[Dict]:
        """文档分块"""
        chunks = []
        
        # 1. 元数据块
        metadata_chunk = {
            'doc_id': doc['doc_id'],
            'chunk_type': 'metadata',
            'content': self._format_metadata(doc['index']),
            'weight': 1.0
        }
        chunks.append(metadata_chunk)
        
        # 2. 摘要块
        summary_chunk = {
            'doc_id': doc['doc_id'],
            'chunk_type': 'summary',
            'content': doc['index'].get('summary', ''),
            'weight': 1.5
        }
        chunks.append(summary_chunk)
        
        # 3. 正文块（按段落和token数切分）
        content_chunks = self._split_content(
            doc['content'],
            chunk_size=1000,
            overlap=200
        )
        
        for i, chunk_text in enumerate(content_chunks):
            chunks.append({
                'doc_id': doc['doc_id'],
                'chunk_type': 'content',
                'chunk_index': i,
                'content': chunk_text,
                'weight': 1.0
            })
        
        # 4. 案例块（从内容中提取）
        example_chunks = self._extract_examples(doc['content'])
        for example in example_chunks:
            chunks.append({
                'doc_id': doc['doc_id'],
                'chunk_type': 'example',
                'content': example,
                'weight': 1.2
            })
        
        return chunks
    
    def _format_metadata(self, index: Dict) -> str:
        """格式化元数据为文本"""
        parts = [
            f"文档ID: {index.get('doc_id', '')}",
            f"标题: {index.get('title', '')}",
            f"类型: {index.get('doc_type', '')}",
            f"摘要: {index.get('summary', '')}",
            f"关键词: {', '.join(index.get('keywords', []))}"
        ]
        return '\n'.join(parts)
    
    def _split_content(self, content: str, chunk_size: int, overlap: int) -> List[str]:
        """按token数切分内容"""
        # 简化实现：按段落和字符数切分
        # 实际应该用tiktoken计算token数
        paragraphs = content.split('\n\n')
        chunks = []
        current_chunk = []
        current_length = 0
        
        for para in paragraphs:
            para_length = len(para)
            if current_length + para_length > chunk_size and current_chunk:
                chunks.append('\n\n'.join(current_chunk))
                # 重叠处理
                overlap_text = '\n\n'.join(current_chunk[-2:]) if len(current_chunk) >= 2 else current_chunk[-1]
                current_chunk = [overlap_text, para]
                current_length = len(overlap_text) + para_length
            else:
                current_chunk.append(para)
                current_length += para_length
        
        if current_chunk:
            chunks.append('\n\n'.join(current_chunk))
        
        return chunks
    
    def _extract_examples(self, content: str) -> List[str]:
        """提取案例块"""
        # 查找"案例"、"例子"等标记的段落
        examples = []
        pattern = r'(?:案例|例子|示例)[：:]\s*\n(.*?)(?=\n\n|\n#|$)'
        matches = re.finditer(pattern, content, re.DOTALL)
        for match in matches:
            examples.append(match.group(1).strip())
        return examples
```

### 4.4 向量数据库封装（vector_store.py）

```python
# rag-system/vector_store.py

import chromadb
from chromadb.config import Settings
from typing import List, Dict, Optional
from pathlib import Path

class VectorStore:
    def __init__(self, db_path: Path, collection_name: str):
        self.client = chromadb.PersistentClient(
            path=str(db_path),
            settings=Settings(anonymized_telemetry=False)
        )
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"}  # 余弦相似度
        )
    
    def add_documents(
        self,
        chunks: List[Dict],
        embeddings: List[List[float]],
        ids: List[str]
    ):
        """添加文档块到向量数据库"""
        metadatas = []
        documents = []
        
        for chunk in chunks:
            metadata = {
                'doc_id': chunk['doc_id'],
                'chunk_type': chunk['chunk_type'],
                'weight': chunk.get('weight', 1.0)
            }
            if 'chunk_index' in chunk:
                metadata['chunk_index'] = chunk['chunk_index']
            
            metadatas.append(metadata)
            documents.append(chunk['content'])
        
        self.collection.add(
            embeddings=embeddings,
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
    
    def search(
        self,
        query_embedding: List[float],
        n_results: int = 5,
        where: Optional[Dict] = None,
        where_document: Optional[Dict] = None
    ) -> Dict:
        """向量检索"""
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            where=where,
            where_document=where_document
        )
        return results
```

### 4.5 检索器实现（retriever.py）

```python
# rag-system/retriever.py

from typing import List, Dict
from .vector_store import VectorStore
from .embedding import EmbeddingModel
import yaml
from pathlib import Path

class HybridRetriever:
    def __init__(
        self,
        vector_store: VectorStore,
        embedding_model: EmbeddingModel,
        index_dir: Path
    ):
        self.vector_store = vector_store
        self.embedding_model = embedding_model
        self.index_dir = index_dir
        self.index_cache = {}  # 缓存索引数据
    
    def retrieve(
        self,
        query: str,
        top_k: int = 5,
        layer: str = None,  # dao | shu
        doc_type: str = None  # theory | methodology | ...
    ) -> List[Dict]:
        """混合检索"""
        # 1. 向量检索
        query_embedding = self.embedding_model.encode_query(query)
        vector_results = self.vector_store.search(
            query_embedding,
            n_results=top_k * 2,  # 多召回一些，后续重排序
            where=self._build_filter(layer, doc_type)
        )
        
        # 2. 关键词匹配（query_patterns）
        pattern_matches = self._match_query_patterns(query)
        
        # 3. 关系扩展（related_docs）
        related_docs = self._expand_related_docs(vector_results)
        
        # 4. 结果融合与重排序
        final_results = self._rerank(
            vector_results,
            pattern_matches,
            related_docs,
            top_k
        )
        
        return final_results
    
    def _match_query_patterns(self, query: str) -> List[str]:
        """匹配query_patterns"""
        matches = []
        for index_file in self.index_dir.glob("*.yaml"):
            doc_id = index_file.stem
            if doc_id not in self.index_cache:
                with open(index_file, 'r', encoding='utf-8') as f:
                    self.index_cache[doc_id] = yaml.safe_load(f)
            
            patterns = self.index_cache[doc_id].get('query_patterns', [])
            for pattern in patterns:
                if pattern.lower() in query.lower() or query.lower() in pattern.lower():
                    matches.append(doc_id)
                    break
        
        return matches
    
    def _expand_related_docs(self, results: Dict) -> List[str]:
        """扩展关联文档"""
        related_docs = set()
        for doc_id in results.get('ids', [[]])[0]:
            if doc_id not in self.index_cache:
                index_file = self.index_dir / f"{doc_id}.yaml"
                if index_file.exists():
                    with open(index_file, 'r', encoding='utf-8') as f:
                        self.index_cache[doc_id] = yaml.safe_load(f)
            
            if doc_id in self.index_cache:
                related = self.index_cache[doc_id].get('related_docs', [])
                related_docs.update(related)
        
        return list(related_docs)
    
    def _rerank(
        self,
        vector_results: Dict,
        pattern_matches: List[str],
        related_docs: List[str],
        top_k: int
    ) -> List[Dict]:
        """重排序"""
        # 实现权重加权、去重、排序逻辑
        # ... 详细实现
        pass
    
    def _build_filter(self, layer: str, doc_type: str) -> Dict:
        """构建过滤条件"""
        where = {}
        if layer:
            where['layer'] = layer
        if doc_type:
            where['doc_type'] = doc_type
        return where if where else None
```

---

## 📝 五、实施计划

### 5.1 时间安排

| 阶段 | 任务 | 时间 | 负责人 |
|------|------|------|--------|
| 阶段一 | 环境准备、项目结构 | 1天 | - |
| 阶段二 | 核心功能实现 | 2-3天 | - |
| 阶段三 | 系统集成 | 1-2天 | - |
| 阶段四 | 测试与优化 | 1-2天 | - |
| **总计** | | **5-8天** | |

### 5.2 优先级

**P0（必须）**：
- 文档加载与解析
- 向量化处理
- 基础向量检索
- 简单RAG问答

**P1（重要）**：
- 混合检索（BM25 + Vector）
- 结果重排序
- 元数据过滤

**P2（优化）**：
- 关系扩展
- 场景匹配
- API接口
- 性能优化

---

## 🧪 六、测试方案

### 6.1 测试用例

使用 `测试查询列表_20个真实问题.md` 中的问题：

1. "AI用多了会变傻吗"
2. "如何进行产品创新"
3. "客户嫌贵怎么沟通"
4. "如何建立长期思维"
5. ...（共20个问题）

### 6.2 评估指标

- **检索准确率**：Top-K中是否包含正确答案
- **响应时间**：查询到返回结果的时间
- **相关性评分**：人工评估结果相关性（1-5分）

### 6.3 优化迭代

根据测试结果：
1. 优化query_patterns
2. 调整权重配置
3. 改进分块策略
4. 优化Embedding模型

---

## 🚀 七、快速开始

### 7.1 安装依赖

```bash
pip install -r requirements.txt
```

### 7.2 构建索引

```bash
python scripts/build_index.py
```

### 7.3 测试查询

```bash
python scripts/test_query.py "AI用多了会变傻吗"
```

### 7.4 启动API（可选）

```bash
python api/app.py
```

---

## 📚 八、后续优化方向

1. **多模态支持**：支持图片、表格等
2. **增量更新**：支持文档增量更新
3. **用户反馈**：收集用户反馈优化检索
4. **A/B测试**：测试不同检索策略效果
5. **缓存机制**：缓存常见查询结果

---

## 📄 九、参考资源

- [LangChain文档](https://python.langchain.com/)
- [Chroma文档](https://docs.trychroma.com/)
- [BGE-M3模型](https://huggingface.co/BAAI/bge-m3)
- [RAG最佳实践](https://www.pinecone.io/learn/retrieval-augmented-generation/)

---

*方案完成，等待实施*
