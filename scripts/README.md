# 工具脚本说明

## 📝 脚本列表

### 1. build_index.py - 构建索引

批量加载39篇文档，进行分块、向量化，存储到向量数据库。

**使用方法：**

```bash
# 构建索引（首次运行）
python scripts/build_index.py

# 重置并重新构建索引
python scripts/build_index.py --reset
```

**功能：**
- 自动加载所有39篇文档
- 智能分块（元数据、摘要、正文、案例）
- 批量向量化
- 存储到Chroma向量数据库

**输出：**
- 向量数据库存储在 `vector_db/` 目录
- 显示处理进度和统计信息

---

### 2. test_query.py - 测试查询

测试RAG系统的检索和问答功能。

**使用方法：**

```bash
# 交互式测试（单个查询）
python scripts/test_query.py

# 测试单个查询
python scripts/test_query.py --query "AI用多了会变傻吗"

# 批量测试（使用默认测试查询列表）
python scripts/test_query.py --batch

# 使用RAG链模式（包含查询处理）
python scripts/test_query.py --query "如何进行产品创新" --mode rag

# 使用LLM生成回答（需要配置OPENAI_API_KEY）
python scripts/test_query.py --query "AI用多了会变傻吗" --mode rag --use-llm
```

**参数说明：**
- `--query`: 查询文本
- `--mode`: 测试模式
  - `retrieval`: 仅测试检索功能
  - `rag`: 测试完整RAG链（包含查询处理）
- `--batch`: 批量测试模式
- `--top-k`: 返回结果数量（默认5）
- `--use-llm`: 使用LLM生成回答（仅rag模式）

**默认测试查询列表：**
包含20个真实用户可能问的问题，如：
- "AI用多了会变傻吗"
- "如何进行产品创新"
- "客户嫌贵怎么沟通"
- ...

---

### 3. update_index.py - 更新索引

增量更新单个或部分文档的索引（用于文档修改后更新）。

**使用方法：**

```bash
# 更新单个文档
python scripts/update_index.py DOC-D001

# 更新多个文档
python scripts/update_index.py DOC-D001 DOC-S010 DOC-S015

# 不删除旧索引（可能导致重复）
python scripts/update_index.py DOC-D001 --no-delete
```

**参数说明：**
- `doc_ids`: 要更新的文档ID列表
- `--no-delete`: 不删除旧的文档块

**使用场景：**
- 文档内容修改后需要更新索引
- 索引文件（YAML）更新后需要重新向量化
- 部分文档需要重新处理

---

## 🚀 快速开始

### 1. 首次使用

```bash
# 1. 构建索引（必须）
python scripts/build_index.py

# 2. 测试查询
python scripts/test_query.py --query "AI用多了会变傻吗"
```

### 2. 日常使用

```bash
# 测试单个查询
python scripts/test_query.py --query "你的问题"

# 批量测试
python scripts/test_query.py --batch
```

### 3. 更新文档后

```bash
# 更新修改的文档
python scripts/update_index.py DOC-D001 DOC-S010
```

---

## 📊 测试结果示例

```
============================================================
查询: AI用多了会变傻吗
============================================================

检索到 5 个结果:

[1] DOC-D001 (分数: 0.892)
    内容: AI应作为认知教练内化训练人类认知结构，而非外置工具。核心检验标准：去除AI后能力是否比使用前更强（正BUFF效应）...

[2] DOC-D007 (分数: 0.756)
    内容: 心智路径依赖理论描述了人类认知困境的系统性分析框架...
```

---

## ⚠️ 注意事项

1. **首次运行需要时间**：
   - 构建索引需要下载Embedding模型（约2.2GB）
   - 39篇文档的向量化需要几分钟时间

2. **内存要求**：
   - 建议至少8GB内存
   - 如果内存不足，可以减小batch_size

3. **LLM功能**：
   - 使用 `--use-llm` 需要配置 `OPENAI_API_KEY`
   - 或使用Ollama本地模型

4. **索引更新**：
   - 更新索引不会自动删除旧数据
   - 建议使用 `--reset` 重新构建完整索引

---

## 🔧 故障排除

### 问题1：找不到模块
```bash
# 确保在项目根目录运行
cd /path/to/wendao
python scripts/build_index.py
```

### 问题2：向量数据库错误
```bash
# 删除旧数据库重新构建
rm -rf vector_db/
python scripts/build_index.py --reset
```

### 问题3：内存不足
修改 `build_index.py` 中的 `batch_size` 参数，减小批处理大小。

---

## 📚 相关文档

- [RAG知识库实施方案.md](../RAG知识库实施方案.md)
- [SETUP.md](../SETUP.md)
- [rag-system/README.md](../rag-system/README.md)
