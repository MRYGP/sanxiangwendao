# RAG索引重建操作指南

> **目的**：在文档目录重组后，重建RAG向量索引以适配新的目录结构  
> **重要性**：⚠️ 如果不重建，Project Knowledge搜索功能将失效  
> **预计时间**：5-10分钟（取决于文档数量）

---

## 📋 前置检查清单

在开始之前，请确认以下事项：

- [ ] Python环境已安装（推荐Python 3.8+）
- [ ] Git仓库已同步最新代码
- [ ] 当前在项目根目录（wendao/）
- [ ] 有足够的磁盘空间（至少500MB）

---

## 🔧 步骤一：环境检查

### 1.1 确认当前位置

打开终端，确认你在项目根目录：

```bash
# Windows PowerShell
pwd
# 应该显示类似：
# E:\wendao

# macOS/Linux
pwd
# 应该显示类似：
# /Users/yourname/wendao
```

如果不在根目录，执行：

```bash
cd /path/to/wendao
```

### 1.2 检查Python版本

```bash
python --version
# 或
python3 --version

# 应该显示：
# Python 3.8.x 或更高版本
```

**如果Python版本过低**：
- macOS: `brew install python@3.11`
- Ubuntu: `sudo apt install python3.11`
- Windows: 从官网下载安装

### 1.3 检查文件结构

```bash
# Windows PowerShell
Get-ChildItem | Where-Object {$_.Name -match "01-dao|02-shu"}

# macOS/Linux
ls -la | grep -E "01-dao|02-shu"

# 应该看到：
# 01-dao/
# 02-shu/
```

### 1.4 确认脚本文件存在

```bash
# Windows PowerShell
Test-Path scripts\build_index.py
Test-Path rag-system\config.py
Test-Path requirements.txt

# macOS/Linux
ls scripts/build_index.py
ls rag-system/config.py
ls requirements.txt
```

**如果文件不存在**，请先执行 `git pull` 同步最新代码。

---

## 📦 步骤二：安装依赖

### 2.1 创建虚拟环境（推荐）

```bash
# 创建虚拟环境
python3 -m venv venv

# 激活虚拟环境
# Windows PowerShell:
venv\Scripts\Activate.ps1

# Windows CMD:
venv\Scripts\activate.bat

# macOS/Linux:
source venv/bin/activate

# 激活后，命令行前面会显示 (venv)
```

**如果PowerShell执行策略限制**，运行：
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**为什么推荐虚拟环境？**
- 隔离项目依赖，避免污染全局Python环境
- 便于管理不同项目的依赖版本
- 卸载项目时只需删除虚拟环境文件夹

### 2.2 升级pip

```bash
python -m pip install --upgrade pip
```

### 2.3 安装项目依赖

**如果遇到网络/代理问题**（如 `ValueError: check_hostname requires server_hostname`）：

**方案1：使用国内镜像源（推荐）**

```bash
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple --trusted-host pypi.tuna.tsinghua.edu.cn -r requirements.txt
```

**方案2：清除代理环境变量**

```powershell
# Windows PowerShell
$env:HTTP_PROXY = $null
$env:HTTPS_PROXY = $null
$env:http_proxy = $null
$env:https_proxy = $null
pip install -r requirements.txt
```

**方案3：修改pip配置**

创建或编辑 `%APPDATA%\pip\pip.ini`（Windows）或 `~/.pip/pip.conf`（macOS/Linux）：

```ini
[global]
index-url = https://pypi.tuna.tsinghua.edu.cn/simple
trusted-host = pypi.tuna.tsinghua.edu.cn
```

然后执行：
```bash
pip install -r requirements.txt
```

**预期输出**：

```
Collecting sentence-transformers
  Downloading sentence_transformers-x.x.x.tar.gz
Collecting chromadb
  Downloading chromadb-x.x.x-cp3x-cp3x-xxx.whl
...
Successfully installed sentence-transformers-x.x.x chromadb-x.x.x ...
```

**如果遇到错误**：

| 错误信息 | 解决方案 |
|---------|----------|
| `No module named 'pip'` | `python3 -m ensurepip --upgrade` |
| `ERROR: Could not find a version` | 检查Python版本是否≥3.8 |
| `Permission denied` | 使用 `pip install --user -r requirements.txt` |
| `ValueError: check_hostname requires server_hostname` | 使用方案1-3解决代理问题 |

### 2.4 验证依赖安装

```bash
# 检查关键依赖
pip list | findstr /i "sentence-transformers chromadb yaml tiktoken"

# macOS/Linux
pip list | grep -E "sentence-transformers|chromadb|yaml|tiktoken"

# 应该看到：
# sentence-transformers  x.x.x
# chromadb               x.x.x
# PyYAML                 x.x.x
# tiktoken               x.x.x
```

---

## 💾 步骤三：备份现有索引（可选但推荐）

如果之前有索引数据，建议先备份：

```bash
# Windows PowerShell
New-Item -ItemType Directory -Force -Path backups
Copy-Item -Recurse vector_db backups\vector_db_backup_$(Get-Date -Format "yyyyMMdd_HHmmss")

# macOS/Linux
mkdir -p backups
cp -r vector_db backups/vector_db_backup_$(date +%Y%m%d_%H%M%S)

# 确认备份成功
ls backups/
```

**为什么备份？**
- 如果重建失败，可以快速恢复
- 便于对比新旧索引的差异

---

## 🚀 步骤四：重建RAG索引

### 4.1 执行重建命令

```bash
python scripts/build_index.py --reset
```

**参数说明**：
- `--reset`: 删除旧索引，从头重建（**必须使用**，因为路径已改变）
- 不加参数: 增量更新（不推荐，因为路径已改变）

### 4.2 预期输出

```
2024-12-26 10:30:15 - __main__ - INFO - ============================================================
2024-12-26 10:30:15 - __main__ - INFO - 开始构建RAG知识库向量索引
2024-12-26 10:30:15 - __main__ - INFO - ============================================================
2024-12-26 10:30:15 - __main__ - INFO - 初始化组件...
2024-12-26 10:30:16 - __main__ - WARNING - 重置现有索引...
2024-12-26 10:30:16 - __main__ - INFO - 共 51 篇文档需要处理
2024-12-26 10:30:16 - __main__ - INFO - 开始处理文档...
处理文档: 100%|████████████████████| 51/51 [02:30<00:00, 2.94s/it]
2024-12-26 10:30:18 - __main__ - INFO - ✅ DOC-D001 处理完成: 8 个块
2024-12-26 10:30:18 - __main__ - INFO - ✅ DOC-D002 处理完成: 7 个块
...
2024-12-26 10:32:45 - __main__ - INFO - ✅ DOC-S039 处理完成: 6 个块
2024-12-26 10:32:45 - __main__ - INFO - 
开始添加到向量数据库，共 350+ 个块...
添加到向量数据库: 100%|████████████| 4/4 [00:10<00:00, 2.5s/it]
2024-12-26 10:32:55 - __main__ - INFO - ✅ 所有文档块已添加到向量数据库
2024-12-26 10:32:55 - __main__ - INFO - 
============================================================
2024-12-26 10:32:55 - __main__ - INFO - 索引构建完成！
2024-12-26 10:32:55 - __main__ - INFO - ============================================================
2024-12-26 10:32:55 - __main__ - INFO - 集合名称: wendao_knowledge_base
2024-12-26 10:32:55 - __main__ - INFO - 文档块数量: 350+
2024-12-26 10:32:55 - __main__ - INFO - 数据库路径: E:\wendao\vector_db
2024-12-26 10:32:55 - __main__ - INFO - ============================================================
```

### 4.3 可能的警告信息

**警告1：部分文档未找到**

```
❌ 处理文档 DOC-S999 失败: FileNotFoundError: 找不到文档文件: xxx.md
```

**解决方案**：
- 检查该文档ID是否存在于 `rag-index/indexes/` 中
- 确认文档是否已移动到正确位置（`01-dao/` 或 `02-shu/` 子目录）
- 如果文档已删除，从 `rag-index/indexes/DOC-XXX.yaml` 中移除，并更新 `rag-system/config.py` 中的 `DOC_MAPPING`

**警告2：内存不足**

```
MemoryError: Unable to allocate array
```

**解决方案**：
- 编辑 `scripts/build_index.py`，将第77行的 `batch_size=32` 改为 `batch_size=16`
- 关闭其他占内存的程序
- 如果是虚拟机，增加分配的内存

### 4.4 错误处理

| 错误信息 | 可能原因 | 解决方案 |
|---------|---------|----------|
| `ModuleNotFoundError: No module named 'rag_system'` | 模块导入路径错误 | 确认在项目根目录执行脚本 |
| `ModuleNotFoundError: No module named 'sentence_transformers'` | 依赖未安装 | 重新执行步骤二 |
| `FileNotFoundError: 找不到文档文件` | 文档路径错误 | 检查文档是否在新目录中，确认 `rag-system/config.py` 中的 `get_doc_file_path` 函数支持新路径 |
| `yaml.scanner.ScannerError` | YAML文件格式错误 | 检查 `rag-index/indexes/DOC-XXX.yaml` 文件语法 |
| `ValueError: 未知的文档ID` | DOC_MAPPING中缺少该ID | 在 `rag-system/config.py` 的 `DOC_MAPPING` 中添加该文档ID |

---

## ✅ 步骤五：验证索引

### 5.1 运行测试查询

```bash
python scripts/test_query.py --query "什么是价值链创新"
```

**预期输出**：

```
2024-12-26 10:35:00 - __main__ - INFO - ============================================================
2024-12-26 10:35:00 - __main__ - INFO - 查询: 什么是价值链创新
2024-12-26 10:35:00 - __main__ - INFO - ============================================================

2024-12-26 10:35:02 - __main__ - INFO - 
检索到 5 个结果:

2024-12-26 10:35:02 - __main__ - INFO - [1] DOC-S033 (分数: 0.923)
2024-12-26 10:35:02 - __main__ - INFO -     内容: 创新不只发生在用户端，价值链有四个环节可以创新：用户端（谁能买）、分发端（谁能被看见）、供给端（谁能卖）、基础设施端（怎么交付）。改写规则比做得更好更重要。...
```

### 5.2 多查询测试

```bash
# 测试道层文档
python scripts/test_query.py --query "什么是认知内共生"

# 测试术层文档
python scripts/test_query.py --query "如何做好沟通"

# 测试跨类别查询
python scripts/test_query.py --query "创业公司如何生存"

# 测试新文档
python scripts/test_query.py --query "什么是受益方共创模式"
```

### 5.3 批量测试（可选）

```bash
# 运行所有预设测试查询
python scripts/test_query.py --batch
```

### 5.4 验证文档路径

打开返回的文档路径，确认能正确访问：

```bash
# Windows PowerShell
Get-Content "02-shu\innovation\价值链创新.md" -Head 20

# macOS/Linux
head -20 "02-shu/innovation/价值链创新.md"
```

### 5.5 验证检查清单

- [ ] 查询能返回相关文档
- [ ] 返回的文档路径正确（新目录结构：`01-dao/` 或 `02-shu/`）
- [ ] 相似度分数合理（>0.7）
- [ ] 能访问返回的文档路径
- [ ] 多个查询都能正常工作
- [ ] 新文档（DOC-S039）能被搜索到

**如果所有检查都通过，说明RAG索引重建成功！**

---

## 🔄 步骤六：提交更改

### 6.1 检查向量数据库

```bash
# Windows PowerShell
Get-ChildItem -Recurse vector_db | Measure-Object -Property Length -Sum

# macOS/Linux
du -sh vector_db/

# 应该显示类似：
# 120M    vector_db/
```

### 6.2 提交到Git

```bash
# 查看更改
git status

# 应该看到：
# modified: vector_db/
# new file: backups/  (如果创建了备份)

# 添加向量数据库
git add vector_db/

# 提交
git commit -m "Rebuild RAG vector index for new directory structure

- Rebuilt index for 51 documents
- Adapted to 01-dao and 02-shu directory structure
- Generated 350+ text chunk vectors
- Test queries working correctly"

# 推送到远程
git push origin master
```

**注意**：如果向量数据库文件很大（>100MB），考虑添加到 `.gitignore`，不提交到Git。

### 6.3 清理备份（可选）

如果确认新索引工作正常，可以删除备份：

```bash
# Windows PowerShell
Remove-Item -Recurse -Force backups\vector_db_backup_*

# macOS/Linux
rm -rf backups/vector_db_backup_*
```

---

## 🎯 步骤七：在Claude Projects中测试

### 7.1 打开Claude Projects

1. 访问 https://claude.ai/
2. 进入你的项目（sanxiangwendao）

### 7.2 测试Project Knowledge搜索

在对话中输入：

```
帮我搜索一下价值链创新相关的内容
```

**预期结果**：
- Claude会调用 `project_knowledge_search` 工具
- 返回《价值链创新.md》相关内容
- 能正确引用新路径下的文档（`02-shu/innovation/价值链创新.md`）

### 7.3 测试多个查询

```
# 测试道层文档
搜索认知内共生理论

# 测试术层文档  
搜索沟通技巧相关内容

# 测试跨类别
搜索创业公司生存相关内容

# 测试新文档
搜索受益方共创模式
```

### 7.4 验证检查清单

- [ ] Project Knowledge能搜索到文档
- [ ] 返回的内容准确
- [ ] Claude能正确引用文档（路径正确）
- [ ] 搜索速度正常（<2秒）
- [ ] 新文档能被搜索到

**如果所有测试通过，说明整个系统已经成功适配新目录结构！**

---

## 🐛 故障排查

### 问题1：找不到文档

**症状**：
```
❌ 处理文档 DOC-S033 失败: FileNotFoundError: 找不到文档文件: 价值链创新.md
```

**排查步骤**：

1. 确认文档是否存在：
   ```bash
   # Windows PowerShell
   Get-ChildItem -Recurse -Filter "价值链创新.md"
   
   # macOS/Linux
   find . -name "价值链创新.md"
   ```

2. 检查config.py是否支持新目录：
   ```bash
   # 查看 get_doc_file_path 函数
   cat rag-system/config.py | grep -A 20 "def get_doc_file_path"
   ```

3. 手动测试路径查找：
   ```python
   python -c "from rag_system.config import get_doc_file_path; print(get_doc_file_path('DOC-S033'))"
   ```

**解决方案**：
- 如果文档存在但找不到，检查 `rag-system/config.py` 中的 `possible_dirs` 列表是否包含文档所在目录
- 如果文档不存在，从 `rag-index/indexes/DOC-S033.yaml` 中移除，并更新 `rag-system/config.py` 中的 `DOC_MAPPING`

---

### 问题2：索引构建很慢

**症状**：
```
处理文档: 10%|█         | 5/51 [05:00<45:00, 60.00s/it]
```

**排查步骤**：

1. 检查网络连接（首次运行需要下载模型）
2. 检查CPU使用率（应该接近100%）
3. 检查内存使用（应该<8GB）

**解决方案**：
- 首次运行慢是正常的（需要下载Embedding模型，约500MB）
- 减小batch_size：编辑 `scripts/build_index.py`，将第77行的 `batch_size=32` 改为 `batch_size=16`
- 关闭其他程序释放资源

---

### 问题3：查询返回不准确

**症状**：
```
查询"价值链创新"返回了"微习惯"
```

**排查步骤**：

1. 检查查询相似度分数（应该>0.7）
2. 尝试更具体的查询
3. 检查文档内容是否相关

**解决方案**：
- 使用更具体的查询词
- 调整相似度阈值（在 `rag-system/config.py` 中）
- 检查文档摘要是否准确（在YAML索引文件中）

---

### 问题4：Project Knowledge搜索失败

**症状**：
Claude回复"我无法访问Project Knowledge"

**排查步骤**：

1. 确认在正确的项目中
2. 检查项目设置中是否启用了Knowledge
3. 尝试刷新页面
4. 检查文档是否已同步到Claude Projects

**解决方案**：
- 在项目设置中重新上传文档
- 等待几分钟让系统同步
- 联系Anthropic支持

---

## 📚 附录

### A. 常用命令速查

```bash
# 激活虚拟环境
# Windows PowerShell:
venv\Scripts\Activate.ps1
# macOS/Linux:
source venv/bin/activate

# 重建索引
python scripts/build_index.py --reset

# 测试查询
python scripts/test_query.py --query "查询内容"

# 批量测试
python scripts/test_query.py --batch

# 查看向量数据库大小
# Windows PowerShell:
Get-ChildItem -Recurse vector_db | Measure-Object -Property Length -Sum
# macOS/Linux:
du -sh vector_db/

# 查看索引文件
ls rag-index/indexes/
```

### B. 目录结构参考

```
wendao/
├── 01-dao/                    # 道层文档（12篇）
│   ├── theory/                # 理论（7篇）
│   ├── framework/             # 框架（1篇）
│   └── philosophy/            # 哲学（4篇）
├── 02-shu/                    # 术层文档（39篇）
│   ├── innovation/            # 创新（15篇）
│   ├── communication/         # 沟通（7篇）
│   ├── behavior-change/       # 行为（6篇）
│   ├── strategy/              # 战略（6篇）
│   ├── execution/             # 执行（3篇）
│   └── psychology/            # 心理（2篇）
├── scripts/                   # 脚本
│   ├── build_index.py         # 重建索引
│   └── test_query.py          # 测试查询
├── rag-system/                # RAG系统
│   ├── config.py              # 配置文件
│   ├── document_loader.py     # 文档加载
│   ├── embedding.py           # 嵌入模型
│   └── vector_store.py        # 向量存储
├── rag-index/                 # 索引元数据
│   ├── indexes/               # YAML索引文件（51个）
│   └── doc-mapping.md         # 文档ID映射
├── vector_db/                 # 向量数据库（生成）
└── requirements.txt           # 依赖列表
```

### C. 依赖版本参考

```txt
sentence-transformers>=2.2.2
chromadb>=0.4.22
PyYAML>=6.0
tiktoken>=0.5.0
torch>=2.0.0
tqdm>=4.66.0
```

### D. 相关文档链接

- [Sentence Transformers文档](https://www.sbert.net/)
- [ChromaDB文档](https://docs.trychroma.com/)
- [RAG技术介绍](https://arxiv.org/abs/2005.11401)

---

## ✅ 完成检查清单

完成以下所有项目后，RAG索引重建工作即告完成：

- [ ] 环境检查通过
- [ ] 依赖安装成功
- [ ] 备份现有索引（可选）
- [ ] 执行重建命令
- [ ] 重建过程无错误
- [ ] 测试查询通过
- [ ] 文档路径正确（新目录结构）
- [ ] 新文档（DOC-S039）能被搜索到
- [ ] 提交到Git（可选）
- [ ] Claude Projects测试通过
- [ ] 清理备份文件（可选）

---

## 🎉 恭喜！

如果你完成了所有步骤，说明：

✅ RAG向量索引已成功重建  
✅ 新目录结构已完全适配  
✅ Project Knowledge搜索功能正常  
✅ 知识库可以正常使用了  

现在你可以：
- 在Claude Projects中使用Project Knowledge搜索
- 通过脚本测试各种查询
- 继续添加新文档到知识库

---

**版本**：v1.0  
**更新时间**：2025-01-20  
**作者**：三湘问道团队

