# RAG知识库索引方案

## 一、方案目标

为38篇文档构建统一的索引系统，支持：
1. **精准检索**：通过元数据快速定位相关文档
2. **语义理解**：帮助RAG系统理解文档内容和关系
3. **上下文关联**：建立文档间的理论链条和应用场景链
4. **分层索引**：支持不同粒度的检索需求

---

## 二、索引结构设计

### 2.1 标准索引格式（YAML Front Matter）

每个文档开头添加YAML格式的元数据块：

```yaml
---
# 文档元数据
doc_id: "DOC-001"
doc_type: "theory"  # theory | methodology | framework | philosophy | technique
category: "AI与认知理论类"
subcategory: "核心理论框架"

# 核心信息
title: "认知内共生理论：AI时代人类能力进化的根本路径选择"
title_en: "Cognitive Endosymbiosis Theory"
summary: "AI作为认知教练内化训练人类认知结构，而非外置工具"
core_insight: "AI从外在的认知拐杖转变为内在的认知催化剂"

# 关键词体系
keywords:
  primary: ["认知内共生", "认知外骨骼", "正BUFF效应", "认知教练"]
  secondary: ["神经可塑性", "认知退化", "技能萎缩", "反脆弱性"]
  technical: ["认知增强", "人机协同", "AI训练", "能力内化"]

# 理论层级
theory_level: "foundational"  # foundational | intermediate | advanced | application
theory_chain_position: "基础理论"  # 在理论链中的位置

# 应用场景
applicable_scenarios:
  - "AI产品设计"
  - "教育技术开发"
  - "认知能力提升"
  - "人机交互设计"

target_audience:
  - "AI创业者"
  - "产品经理"
  - "认知提升者"
  - "教育工作者"

# 文档关系
related_docs:
  prerequisites: ["DOC-014"]  # 心智路径依赖理论
  builds_on: []
  extended_by: ["DOC-004", "DOC-005"]  # 双螺旋进化、递归认知进化
  similar_to: ["DOC-002"]  # 专家智慧AI化

# 理论链条
theory_chains:
  cognitive_evolution: 
    position: 2
    chain: ["DOC-014", "DOC-001", "DOC-004", "DOC-005", "DOC-006"]
  
# 应用链条
application_chains:
  product_design: ["DOC-020", "DOC-027", "DOC-037"]
  behavior_change: ["DOC-015", "DOC-017", "DOC-018"]

# 内容结构
content_structure:
  sections: ["理论基础", "核心机制", "实现路径", "应用案例"]
  has_code: false
  has_examples: true
  has_framework: true

# 检索增强信息
retrieval_boost:
  query_patterns:
    - "如何避免AI依赖导致认知退化"
    - "AI如何训练人类认知能力"
    - "认知内共生vs认知外骨骼"
  semantic_tags: ["认知增强", "人机协同", "能力内化", "反脆弱性"]

# 版本信息
version: "1.0"
last_updated: "2024-01-01"
author: "常松阳"
---
```

### 2.2 索引字段说明

#### 核心字段（必填）

| 字段 | 说明 | 示例 |
|------|------|------|
| `doc_id` | 唯一文档标识 | DOC-001 |
| `doc_type` | 文档类型 | theory/methodology/framework |
| `category` | 主分类 | AI与认知理论类 |
| `title` | 文档标题 | 认知内共生理论... |
| `summary` | 一句话摘要 | AI作为认知教练... |
| `keywords.primary` | 核心关键词 | ["认知内共生", "正BUFF"] |

#### 关系字段（重要）

| 字段 | 说明 | 用途 |
|------|------|------|
| `related_docs.prerequisites` | 前置文档 | 理解本文档需要先读的 |
| `related_docs.extended_by` | 扩展文档 | 基于本文档发展的理论 |
| `theory_chains` | 理论链条 | 建立理论演进路径 |
| `application_chains` | 应用链条 | 建立应用场景路径 |

#### 检索增强字段（优化）

| 字段 | 说明 | 用途 |
|------|------|------|
| `retrieval_boost.query_patterns` | 常见查询模式 | 匹配用户问题 |
| `semantic_tags` | 语义标签 | 语义检索增强 |
| `applicable_scenarios` | 应用场景 | 场景化检索 |

---

## 三、不同文档类型的索引模板

### 3.1 理论类文档模板

```yaml
---
doc_id: "DOC-001"
doc_type: "theory"
category: "AI与认知理论类"
subcategory: "核心理论框架"

title: "[文档标题]"
title_en: "[English Title]"
summary: "[一句话核心摘要]"
core_insight: "[核心洞察，1-2句话]"

keywords:
  primary: ["关键词1", "关键词2", "关键词3"]
  secondary: ["相关概念1", "相关概念2"]
  technical: ["技术术语1", "技术术语2"]

theory_level: "foundational"  # foundational/intermediate/advanced
theory_chain_position: "基础理论"

related_docs:
  prerequisites: []
  builds_on: []
  extended_by: []
  similar_to: []

theory_chains:
  [chain_name]:
    position: 1
    chain: ["DOC-XXX", "DOC-YYY"]

applicable_scenarios:
  - "场景1"
  - "场景2"

target_audience:
  - "受众1"
  - "受众2"

retrieval_boost:
  query_patterns:
    - "用户可能问的问题1"
    - "用户可能问的问题2"
  semantic_tags: ["标签1", "标签2"]
---
```

### 3.2 方法论类文档模板

```yaml
---
doc_id: "DOC-007"
doc_type: "methodology"
category: "创新与创业方法论类"
subcategory: "创新方法论"

title: "[文档标题]"
summary: "[一句话摘要]"
core_framework: "[核心框架名称]"
framework_steps: ["步骤1", "步骤2", "步骤3"]

keywords:
  primary: ["框架名", "核心方法"]
  process: ["步骤关键词"]
  application: ["应用场景关键词"]

applicable_stages:
  - "想法验证期"
  - "产品开发期"
  - "市场拓展期"

use_cases:
  - "用例1：描述"
  - "用例2：描述"

related_docs:
  prerequisites: []
  complementary: []  # 互补方法
  alternatives: []  # 替代方法

application_chains:
  innovation_process: ["DOC-008", "DOC-010", "DOC-007"]

retrieval_boost:
  query_patterns:
    - "如何[应用场景]"
    - "[问题]的解决方法"
  semantic_tags: ["方法论", "框架", "流程"]
---
```

### 3.3 框架类文档模板

```yaml
---
doc_id: "DOC-025"
doc_type: "framework"
category: "战略思维与决策框架类"

title: "[文档标题]"
summary: "[摘要]"
framework_name: "[框架名称]"
framework_structure: ["阶段1", "阶段2", "阶段3", "阶段4"]

keywords:
  primary: ["框架名"]
  stages: ["阶段关键词"]
  principles: ["原则关键词"]

applicable_domains:
  - "战略规划"
  - "产品设计"
  - "个人成长"

framework_components:
  - name: "组件1"
    description: "描述"
  - name: "组件2"
    description: "描述"

related_docs:
  prerequisites: []
  implements: []  # 实现该框架的文档
  extends: []  # 扩展该框架的文档

retrieval_boost:
  query_patterns:
    - "如何使用[框架名]"
    - "[框架名]的步骤"
  semantic_tags: ["框架", "流程", "方法论"]
---
```

### 3.4 技巧类文档模板

```yaml
---
doc_id: "DOC-020"
doc_type: "technique"
category: "沟通与社交技巧类"

title: "[文档标题]"
summary: "[摘要]"
core_principle: "[核心原则]"
key_techniques: ["技巧1", "技巧2", "技巧3"]

keywords:
  primary: ["核心概念"]
  techniques: ["具体技巧"]
  scenarios: ["应用场景"]

applicable_contexts:
  - "客户沟通"
  - "团队协作"
  - "产品设计"

example_scenarios:
  - "场景1：描述"
  - "场景2：描述"

related_docs:
  prerequisites: []
  complementary: []
  similar_to: []

retrieval_boost:
  query_patterns:
    - "如何[场景]"
    - "[问题]的沟通技巧"
  semantic_tags: ["技巧", "沟通", "社交"]
---
```

---

## 四、索引实施策略

### 4.1 实施步骤

#### 阶段一：核心索引（必填字段）
1. 为所有文档添加基础元数据
   - doc_id, doc_type, category
   - title, summary
   - keywords.primary
   - related_docs（基础关系）

#### 阶段二：关系索引（重要字段）
2. 建立文档关系网络
   - prerequisites（前置文档）
   - extended_by（扩展文档）
   - theory_chains（理论链条）
   - application_chains（应用链条）

#### 阶段三：检索优化（增强字段）
3. 添加检索增强信息
   - retrieval_boost.query_patterns
   - semantic_tags
   - applicable_scenarios

### 4.2 索引生成方式

#### 方案A：手动添加（推荐初期）
- 优点：精确控制，质量高
- 缺点：工作量大
- 适用：核心文档、重要文档

#### 方案B：AI辅助生成
- 使用AI读取文档内容，自动生成：
  - summary
  - keywords
  - related_docs（基于内容相似度）
  - query_patterns
- 人工审核和调整

#### 方案C：混合方式（推荐）
- AI生成基础索引
- 人工补充关系网络
- 人工优化检索字段

---

## 五、RAG检索优化建议

### 5.1 向量检索优化

#### 文档分块策略
```
每个文档建议分块：
1. 索引块（YAML front matter）- 元数据，用于过滤
2. 摘要块（前200字）- 核心内容，高权重
3. 正文块（按章节）- 详细内容
4. 案例块（如有）- 应用示例，单独索引
```

#### 向量化建议
- 使用中文embedding模型（如text2vec, m3e）
- 对索引块和摘要块提高权重
- 对关键词进行特殊标记

### 5.2 混合检索策略

```
检索流程：
1. 关键词匹配（YAML中的keywords）→ 快速过滤
2. 语义检索（向量相似度）→ 找到相关内容
3. 关系检索（related_docs）→ 扩展上下文
4. 链条检索（theory_chains）→ 提供完整理论路径
```

### 5.3 上下文增强

当检索到文档A时，自动包含：
- prerequisites（前置知识）
- extended_by（后续发展）
- theory_chains中的相邻文档
- application_chains中的相关应用

---

## 六、索引示例

### 示例1：理论类文档

```yaml
---
doc_id: "DOC-001"
doc_type: "theory"
category: "AI与认知理论类"
subcategory: "核心理论框架"

title: "认知内共生理论：AI时代人类能力进化的根本路径选择"
title_en: "Cognitive Endosymbiosis Theory"
summary: "AI作为认知教练内化训练人类认知结构，而非外置工具，实现去除AI后能力反而更强的正BUFF效应"
core_insight: "AI从外在的认知拐杖转变为内在的认知催化剂，让技术成为人类进化的加速器而非替代者"

keywords:
  primary: ["认知内共生", "认知外骨骼", "正BUFF效应", "认知教练", "反脆弱性"]
  secondary: ["神经可塑性", "认知退化", "技能萎缩", "决策外包", "自主性消解"]
  technical: ["认知增强", "人机协同", "AI训练", "能力内化", "认知健身房"]

theory_level: "foundational"
theory_chain_position: "基础理论"

related_docs:
  prerequisites: ["DOC-014"]  # 心智路径依赖理论
  builds_on: []
  extended_by: ["DOC-004", "DOC-005"]  # 双螺旋进化、递归认知进化
  similar_to: ["DOC-002"]  # 专家智慧AI化

theory_chains:
  cognitive_evolution:
    position: 2
    chain: ["DOC-014", "DOC-001", "DOC-004", "DOC-005", "DOC-006"]
    description: "认知进化理论链：从问题诊断到个体进化到集体涌现"

applicable_scenarios:
  - "AI产品设计（避免用户认知退化）"
  - "教育技术开发（认知增强系统）"
  - "个人认知能力提升"
  - "人机交互设计"

target_audience:
  - "AI创业者"
  - "产品经理"
  - "认知提升者"
  - "教育工作者"

content_structure:
  sections: ["理论基础", "核心机制", "实现路径", "应用案例", "理论局限"]
  has_code: false
  has_examples: true
  has_framework: true

retrieval_boost:
  query_patterns:
    - "如何避免AI依赖导致认知退化"
    - "AI如何训练人类认知能力"
    - "认知内共生vs认知外骨骼的区别"
    - "什么是正BUFF效应"
    - "如何设计认知增强的AI产品"
  semantic_tags: ["认知增强", "人机协同", "能力内化", "反脆弱性", "认知退化", "AI训练"]

version: "1.0"
last_updated: "2024-01-01"
author: "常松阳"
---
```

### 示例2：方法论类文档

```yaml
---
doc_id: "DOC-008"
doc_type: "methodology"
category: "创新与创业方法论类"
subcategory: "创新方法论"

title: "创新三元法"
summary: "通过第一性原理洞察→边缘用户拓展→喂饭思维交付的三位一体创新闭环"
core_framework: "创新三元法"
framework_steps: ["第一性原理思维", "边缘用户考量", "喂饭思维交付"]

keywords:
  primary: ["创新三元法", "第一性原理", "边缘用户", "喂饭思维"]
  process: ["深度洞察", "广泛拓展", "极致交付"]
  application: ["产品创新", "用户体验", "市场突破"]

applicable_stages:
  - "产品设计期"
  - "市场验证期"
  - "用户体验优化期"

use_cases:
  - "AI产品从技术可行到用户成功的突破"
  - "颠覆性创新方案设计"
  - "用户体验极致简化"

related_docs:
  prerequisites: []
  complementary: ["DOC-007", "DOC-010"]  # 创新工程系统、动态决策框架
  alternatives: []

application_chains:
  innovation_process:
    chain: ["DOC-012", "DOC-008", "DOC-007", "DOC-010", "DOC-013"]
    description: "创新流程链：从启动点到三元法到工程系统到决策框架到战略杠杆"

retrieval_boost:
  query_patterns:
    - "如何进行产品创新"
    - "如何从技术可行到用户成功"
    - "第一性原理在创新中的应用"
    - "如何设计极致简单的用户体验"
    - "边缘用户如何启发创新"
  semantic_tags: ["创新方法", "产品设计", "用户体验", "第一性原理", "边缘创新"]

version: "1.0"
last_updated: "2024-01-01"
---
```

---

## 七、实施建议

### 7.1 优先级排序

**高优先级（必须）：**
1. doc_id, doc_type, category
2. title, summary
3. keywords.primary
4. related_docs（基础关系）

**中优先级（重要）：**
5. theory_chains / application_chains
6. applicable_scenarios
7. retrieval_boost.query_patterns

**低优先级（优化）：**
8. semantic_tags
9. content_structure
10. 详细的关系网络

### 7.2 质量保证

1. **一致性检查**
   - doc_id唯一性
   - related_docs的双向一致性（A指向B，B应指向A）
   - theory_chains的完整性

2. **完整性检查**
   - 必填字段是否齐全
   - 关键词是否充分
   - 关系网络是否完整

3. **准确性检查**
   - summary是否准确
   - related_docs关系是否正确
   - query_patterns是否覆盖常见问题

### 7.3 工具支持

建议开发：
1. **索引验证工具**：检查YAML格式、必填字段、关系一致性
2. **关系可视化工具**：生成文档关系图
3. **检索测试工具**：测试不同查询的检索效果

---

## 八、后续优化方向

### 8.1 动态索引
- 根据用户查询反馈调整query_patterns
- 根据使用频率调整文档权重

### 8.2 多语言支持
- 添加英文索引字段
- 支持中英文混合检索

### 8.3 版本管理
- 索引版本控制
- 文档更新时同步更新索引

---

## 九、讨论要点

### 9.1 需要确认的问题

1. **索引粒度**
   - 是否所有文档都需要完整索引？
   - 还是核心文档详细，其他文档简化？

2. **关系网络深度**
   - 是否建立完整的双向关系？
   - 理论链条的粒度如何？

3. **检索优化程度**
   - query_patterns的数量？
   - semantic_tags的粒度？

4. **实施方式**
   - 手动 vs AI辅助 vs 混合？
   - 分批实施还是一次性完成？

### 9.2 建议的实施方案

**推荐方案：分阶段实施**

**第一阶段（1周）：**
- 为所有38篇文档添加基础索引（必填字段）
- 建立核心文档的完整关系网络（约10-15篇）

**第二阶段（1周）：**
- 补充所有文档的关系网络
- 添加理论链条和应用链条

**第三阶段（1周）：**
- 添加检索优化字段
- 测试和优化

---

*方案设计完成，等待讨论和确认*

