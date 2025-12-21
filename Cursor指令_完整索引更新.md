# Cursor指令：完整索引系统更新

> 一次性修复仓库索引系统的所有问题

---

## 任务概述

仓库的RAG索引系统存在严重滞后，需要：
1. 更新 config.py 的 DOC_MAPPING（缺少10篇文档）
2. 创建2个新的YAML索引文件（精益创业、从0到1）
3. 更新 learning-paths.md
4. 更新 README.md 文档列表

---

## 任务1：更新 rag-system/config.py

### 文件位置
`rag-system/config.py`

### 修改内容

找到 `DOC_MAPPING` 字典，在 `"DOC-S027"` 之后添加以下内容：

```python
    "DOC-S028": "芒格不会投你的AI创业公司.md",
    "DOC-S029": "跟着感觉走——可能是你听过的最坑人的建议.md",
    "DOC-S030": "为什么有些人明知道该离开，却怎么也走不了.md",
    "DOC-S031": "即兴演讲.md",
    "DOC-S032": "破坏式创新.md",
    "DOC-S033": "价值链创新.md",
    "DOC-S034": "供应链数字化.md",
    "DOC-S035": "高频业务的战略价值.md",
    "DOC-S036": "精益创业.md",
    "DOC-S037": "从0到1.md",
```

**注意**：确保最后一行有逗号，整个字典的闭合花括号 `}` 在新增内容之后。

---

## 任务2：创建YAML索引文件

### 文件1：rag-index/indexes/DOC-S036.yaml

```yaml
---
doc_id: "DOC-S036"
doc_type: "methodology"
title: "精益创业"
layer: "shu"
summary: "Build-Measure-Learn循环验证商业假设，用MVP快速测试，数据驱动决策，在不确定中找到可重复的增长模式"
keywords:
  - "精益创业"
  - "MVP"
  - "Build-Measure-Learn"
  - "验证性学习"
  - "Pivot转型"
  - "创新计量"
related_docs:
  - "DOC-S005"
  - "DOC-S037"
  - "DOC-S003"
  - "DOC-S004"
  - "DOC-S020"
query_patterns:
  - "怎么验证商业想法"
  - "什么是MVP"
  - "创业怎么快速试错"
  - "精益创业和从0到1有什么区别"
  - "Pivot是什么意思"
  - "怎么知道该不该转型"
doc_weight: "core"
training_order: 11
---
```

### 文件2：rag-index/indexes/DOC-S037.yaml

```yaml
---
doc_id: "DOC-S037"
doc_type: "methodology"
title: "从0到1"
layer: "shu"
summary: "垄断优于竞争，找到别人不知道的秘密，做从0到1的创新而非1到N的复制，七个问题检验创业机会"
keywords:
  - "从0到1"
  - "垄断"
  - "秘密理论"
  - "幂次法则"
  - "Peter Thiel"
  - "逆向思维"
  - "七个问题"
related_docs:
  - "DOC-S036"
  - "DOC-D011"
  - "DOC-S003"
  - "DOC-S001"
  - "DOC-S032"
query_patterns:
  - "怎么做从0到1的创新"
  - "竞争和垄断哪个好"
  - "创业要回答的七个问题"
  - "什么是秘密理论"
  - "从0到1和精益创业有什么区别"
  - "怎么找到别人不知道的秘密"
doc_weight: "core"
training_order: 12
---
```

---

## 任务3：更新 rag-index/learning-paths.md

### 修改位置
找到 `## 路径二：创业实战之路（术）` 部分

### 修改内容

将原有内容替换为：

```markdown
## 路径二：创业实战之路（术）

**目标**：掌握从0到1的创新方法论

**学习序列**：

1. DOC-S037 从0到1 → 战略选择：做什么，为什么（道）

2. DOC-S036 精益创业 → 执行验证：怎么验证，怎么迭代（术）

3. DOC-S005 最小可行启动点 → 找到切入点

4. DOC-S001 创新三元法 → 建立创新框架

5. DOC-S003 初创企业生存法则 → 理解生存逻辑

6. DOC-S004 动态决策框架 → 应对不确定性

7. DOC-S006 战略性杠杆 → 借力放大

8. DOC-S007 马斯克五步法 → 执行方法论

**预期时长**：3周（每篇精读+讨论）

**学习逻辑**：
- 先从《从0到1》理解"做什么"（战略选择）
- 再用《精益创业》掌握"怎么验证"（执行方法）
- 然后学习具体的启动、创新、生存、决策技巧
- 形成完整的"道→术"闭环
```

---

## 任务4：更新现有文档的交叉引用

### 4.1 更新 rag-index/indexes/DOC-S005.yaml

在 `related_docs` 中添加：
```yaml
related_docs:
  - "DOC-S036"  # 新增：精益创业
  # ... 保留原有的
```

### 4.2 更新 rag-index/indexes/DOC-S003.yaml

在 `related_docs` 中添加：
```yaml
related_docs:
  - "DOC-S036"  # 新增：精益创业
  - "DOC-S037"  # 新增：从0到1
  # ... 保留原有的
```

### 4.3 更新 rag-index/indexes/DOC-S032.yaml（破坏式创新）

在 `related_docs` 中添加：
```yaml
related_docs:
  - "DOC-S037"  # 新增：从0到1
  # ... 保留原有的
```

---

## 任务5：验证和重建向量索引

完成上述修改后，运行以下命令重建向量索引：

```bash
# 进入项目目录
cd /path/to/sanxiangwendao

# 重建完整索引（推荐）
python scripts/build_index.py --reset

# 或者只更新新增的两篇
python scripts/update_index.py DOC-S036 DOC-S037
```

---

## 执行检查清单

- [ ] config.py 的 DOC_MAPPING 已更新（共37篇术层文档）
- [ ] DOC-S036.yaml 已创建
- [ ] DOC-S037.yaml 已创建
- [ ] learning-paths.md 已更新
- [ ] DOC-S005.yaml 的 related_docs 已更新
- [ ] DOC-S003.yaml 的 related_docs 已更新
- [ ] DOC-S032.yaml 的 related_docs 已更新
- [ ] 向量索引已重建
- [ ] 测试查询验证（搜索"MVP"能找到精益创业）

---

## 同步到GitHub

```bash
git add rag-system/config.py
git add rag-index/indexes/DOC-S036.yaml
git add rag-index/indexes/DOC-S037.yaml
git add rag-index/learning-paths.md
git add rag-index/indexes/DOC-S005.yaml
git add rag-index/indexes/DOC-S003.yaml
git add rag-index/indexes/DOC-S032.yaml

git commit -m "feat: 完善索引系统，新增《精益创业》《从0到1》索引，更新学习路径"
git push
```

---

*指令完成，请按顺序执行*
