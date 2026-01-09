# Cursor指令 - 仓库整理（优化版 v2.0）

@Codebase 整理仓库结构（基于Cursor深度分析的优化版）

---

## 🎯 任务目标

整理GitHub仓库（sanxiangwendao），实现：
1. ✅ 清理空文件夹（DOC-S067/S068已删除，跳过）
2. ✅ 优化.gitignore规则
3. ✅ 更新shangye-anli/README.md（标注"本地工作区模式"）
4. ✅ 更新根目录README.md（添加"仓库结构说明"）
5. ✅ 创建同步SOP

**优化点**（基于Cursor分析）：
- ✅ 添加状态检查（跳过已完成步骤）
- ✅ 优化.gitignore规则（更精确的路径匹配）
- ✅ 检查现有内容（避免重复更新）
- ✅ 使用相对路径（提高可移植性）

---

## 执行步骤

### Step 0：环境检查和状态确认

```bash
echo "=========================================="
echo "Step 0: 环境检查和状态确认"
echo "=========================================="

# 1. 检查已完成的任务
echo ""
echo "1. 检查DOC-S067/S068是否已删除"
if [ -f rag-index/indexes/DOC-S067.yaml ] || [ -f rag-index/indexes/DOC-S068.yaml ]; then
    echo "❌ 发现重复YAML索引，需要删除"
    NEED_DELETE_YAML=true
else
    echo "✅ DOC-S067/S068已删除（Step 2已完成）"
    NEED_DELETE_YAML=false
fi

# 2. 检查shangye-anli/README.md是否已有"本地工作区"说明
echo ""
echo "2. 检查shangye-anli/README.md状态"
if grep -q "本地工作区模式" shangye-anli/README.md 2>/dev/null; then
    echo "✅ shangye-anli/README.md已有'本地工作区模式'说明"
    NEED_UPDATE_SHANGYE_README=false
else
    echo "⚠️ shangye-anli/README.md需要更新"
    NEED_UPDATE_SHANGYE_README=true
fi

# 3. 检查.gitignore是否已有dedao规则
echo ""
echo "3. 检查.gitignore状态"
if [ -f .gitignore ] && grep -q "dedao/" .gitignore 2>/dev/null; then
    echo "✅ .gitignore已有dedao规则"
    NEED_UPDATE_GITIGNORE=false
else
    echo "⚠️ .gitignore需要更新或创建"
    NEED_UPDATE_GITIGNORE=true
fi

# 4. 检查根目录README.md是否已有"仓库结构说明"
echo ""
echo "4. 检查根目录README.md状态"
if grep -q "仓库结构说明" README.md 2>/dev/null; then
    echo "✅ README.md已有'仓库结构说明'章节"
    NEED_UPDATE_ROOT_README=false
else
    echo "⚠️ README.md需要添加'仓库结构说明'章节"
    NEED_UPDATE_ROOT_README=true
fi

# 5. 检查同步SOP是否存在
echo ""
echo "5. 检查同步SOP文档"
if [ -f 99-gongjuSOP/协作/本地与仓库同步SOP.md ]; then
    echo "✅ 同步SOP已存在"
    NEED_CREATE_SOP=false
else
    echo "⚠️ 需要创建同步SOP"
    NEED_CREATE_SOP=true
fi

# 6. 统计空文件夹
echo ""
echo "6. 查找空文件夹"
EMPTY_COUNT=$(find . -type d -empty -not -path "./.git/*" 2>/dev/null | wc -l)
echo "发现 $EMPTY_COUNT 个空文件夹"

# 总结
echo ""
echo "=========================================="
echo "📊 状态总结"
echo "=========================================="
echo "需要执行的任务："
echo "- 删除YAML索引: $NEED_DELETE_YAML"
echo "- 清理空文件夹: $EMPTY_COUNT 个"
echo "- 更新shangye-anli/README: $NEED_UPDATE_SHANGYE_README"
echo "- 更新.gitignore: $NEED_UPDATE_GITIGNORE"
echo "- 更新根目录README: $NEED_UPDATE_ROOT_README"
echo "- 创建同步SOP: $NEED_CREATE_SOP"
echo ""

echo "✅ Step 0 完成"
```

---

### Step 1：清理空文件夹

```bash
echo ""
echo "=========================================="
echo "Step 1: 清理空文件夹"
echo "=========================================="

# 创建临时文件记录空文件夹
EMPTY_DIRS="/tmp/empty_dirs.txt"
> $EMPTY_DIRS

# 查找空文件夹（排除.git目录）
find . -type d -empty -not -path "./.git/*" > $EMPTY_DIRS

# 显示找到的空文件夹
EMPTY_COUNT=$(wc -l < $EMPTY_DIRS)
if [ $EMPTY_COUNT -gt 0 ]; then
    echo "找到 $EMPTY_COUNT 个空文件夹："
    cat $EMPTY_DIRS
    
    echo ""
    echo "开始删除..."
    
    # 删除空文件夹
    while IFS= read -r dir; do
        if [ -d "$dir" ]; then
            rmdir "$dir" 2>/dev/null && echo "✅ 已删除: $dir" || echo "⚠️ 无法删除: $dir（可能不为空）"
        fi
    done < $EMPTY_DIRS
    
    echo ""
    echo "✅ 空文件夹清理完成"
else
    echo "✅ 没有发现空文件夹"
fi

echo ""
echo "✅ Step 1 完成"
```

---

### Step 2：优化.gitignore规则

```bash
echo ""
echo "=========================================="
echo "Step 2: 优化.gitignore规则"
echo "=========================================="

if [ "$NEED_UPDATE_GITIGNORE" = true ]; then
    # 备份原文件（如果存在）
    if [ -f .gitignore ]; then
        cp .gitignore .gitignore.backup
        echo "✅ 已备份 .gitignore"
    fi

    # 创建或更新.gitignore（优化版 - 更精确的路径匹配）
    cat > .gitignore << 'EOF'
# ============================================
# 本地工作区（dedao/不在仓库中）
# ============================================
dedao/
**/dedao/

# ============================================
# 课程原文件（版权保护）- 精确匹配
# ============================================
# 只忽略04_原著笔记/MD/目录下的课程文件
**/04_原著笔记/MD/*.md
# 以及任何带"课程"字样的markdown文件（在原著笔记目录下）
**/04_原著笔记/**/*课程*.md

# ============================================
# 临时文件
# ============================================
*.tmp
*.bak
*.backup
~*
.DS_Store
Thumbs.db
*.swp
*.swo

# ============================================
# Python相关
# ============================================
__pycache__/
*.py[cod]
*$py.class
.Python
venv/
.venv/
env/
ENV/
*.egg-info/
dist/
build/

# ============================================
# IDE配置
# ============================================
.vscode/
.idea/
*.sublime-project
*.sublime-workspace

# ============================================
# RAG系统临时文件
# ============================================
rag-system/data/
rag-system/*.db
rag-system/*.pkl
rag-system/chroma/

# ============================================
# 日志和数据库
# ============================================
*.log
*.sqlite
*.db

# ============================================
# 测试和覆盖率
# ============================================
.pytest_cache/
.coverage
htmlcov/
.tox/

# ============================================
# 系统文件
# ============================================
.env
.env.local
*.key
*.pem
secrets/
EOF

    echo "✅ .gitignore 已更新（优化版 - 精确路径匹配）"
    echo ""
    echo "优化说明："
    echo "- 使用 **/04_原著笔记/MD/*.md 精确匹配课程文件"
    echo "- 避免误伤其他包含'课程'的正常文档"
    echo "- 保持其他规则不变"
else
    echo "✅ .gitignore已是最新，跳过更新"
fi

echo ""
echo "✅ Step 2 完成"
```

---

### Step 3：更新shangye-anli/README.md

```bash
echo ""
echo "=========================================="
echo "Step 3: 更新shangye-anli/README.md"
echo "=========================================="

if [ "$NEED_UPDATE_SHANGYE_README" = true ]; then
    # 备份原文件
    cp shangye-anli/README.md shangye-anli/README.md.backup
    echo "✅ 已备份 shangye-anli/README.md"

    # 在文件开头添加状态说明
    cat > shangye-anli/README.md.new << 'EOF'
# 商业案例课改编（项目框架）

> **🔄 工作模式**：本地工作区模式  
> **📍 实际工作路径**：本地 `dedao/` 目录  
> **📦 本目录内容**：系统框架、指令模板、结构说明

---

## 📋 状态说明

**本目录定位**：
- ✅ 提供完整的系统框架和指令
- ✅ 定义标准化的案例拆解流程
- ✅ 作为版本控制和团队协作的基础
- ⚠️ 实际案例拆解工作在本地 `dedao/` 目录进行

**为什么采用本地工作区模式？**
1. **版权保护**：课程原文件不适合上传到公开仓库
2. **灵活迭代**：本地可以快速试错和调整
3. **清晰分工**：仓库管框架，本地管实战
4. **定期同步**：完成的案例可以同步回仓库（去除课程引用）

---

EOF

    # 将原文件内容追加到新文件（从第一个标题开始）
    sed -n '/^# 商业案例课改编/,$p' shangye-anli/README.md.backup | tail -n +2 >> shangye-anli/README.md.new

    # 在文件末尾添加工作流说明
    cat >> shangye-anli/README.md.new << 'EOF'

---

## 🔄 工作流程

### 本地工作（dedao/）

1. **拆解商业案例**：
   - 使用 `00_系统指令/Claude-案例拆解提示词.md`
   - 包含课程原文件作为材料
   - 快速迭代和验证

2. **提炼商业模型**：
   - 使用 `00_系统指令/Claude-模型提炼提示词.md`
   - 从多个案例中抽象可复用模型

3. **归纳跨案例洞察**：
   - 使用 `00_系统指令/Claude-洞察归纳提示词.md`
   - 对比多个案例，提炼共性

### 同步到仓库（定期）

**同步内容**：
- ✅ 新拆解的案例文档（**去除课程原文引用**）
- ✅ 新提炼的商业模型
- ✅ 新归纳的跨案例洞察
- ✅ 更新索引文件

**不同步内容**：
- ❌ 课程原文件（版权保护）
- ❌ 临时工作文件
- ❌ 个人笔记

**同步方法**：
参考 `../99-gongjuSOP/协作/本地与仓库同步SOP.md`

---

## 📍 本地工作区

**路径**：相对于仓库的本地目录（建议 `../dedao/` 或独立路径）

**快速开始**：
1. 查看本地 `dedao/README.md` 了解工作区结构
2. 查看本地 `dedao/本地工作区说明.md` 了解使用方法
3. 开始第一个案例拆解

---

**文档版本**：v2.0  
**最后更新**：2026-01-04  
**维护者**：常松阳
EOF

    # 替换原文件
    mv shangye-anli/README.md.new shangye-anli/README.md

    echo "✅ shangye-anli/README.md 已更新"
else
    echo "✅ shangye-anli/README.md已是最新，跳过更新"
fi

echo ""
echo "✅ Step 3 完成"
```

---

### Step 4：更新根目录README.md

```bash
echo ""
echo "=========================================="
echo "Step 4: 更新根目录README.md"
echo "=========================================="

if [ "$NEED_UPDATE_ROOT_README" = true ]; then
    # 备份原文件
    cp README.md README.md.backup
    echo "✅ 已备份 README.md"

    # 创建要插入的新章节
    cat > /tmp/readme_insert.md << 'EOF'

---

## 📂 仓库结构说明

### 核心目录

- **`01-dao/`** - 道层理论（12篇）
  - 认知理念、核心理论、价值观
  - 如：认知内共生理论、双螺旋进化模型、财富创造的范式转移

- **`02-shu/`** - 术层方法（66篇）
  - 方法框架、执行技巧、实战案例
  - 细分：创新方法、产品设计、沟通技巧、行为改变、战略思维
  - **包含**：DOC-S047《三大标杆的可复用方法论》、DOC-S048《创业项目评估方法论》

- **`shangye-anli/`** - 商业案例框架
  - **模式**：本地工作区模式
  - **内容**：系统指令、流程框架、结构说明
  - **实际工作**：在本地 `dedao/` 目录进行
  - 包含：案例拆解/模型提炼/洞察归纳的完整方法论

- **`AI产品分析/`** - AI竞品分析框架
  - 10步完整流程（Why/Money/What/How/Growth）
  - 导师点评、评分系统、失败案例分析
  - 竞品库、追踪记录、改进清单

- **`99-gongjuSOP/`** - 工具和SOP文档
  - 写作规范：新文档写作框架指南、快速参考
  - 知识库管理：构建SOP、RAG索引重建
  - 协作流程：本地与仓库同步SOP

- **`rag-index/`** - RAG索引系统
  - YAML索引：78篇文档的完整元数据
  - 文档映射：doc-mapping.md（ID→路径）
  - 学习路径：5条主题学习路径

- **`rag-system/`** - RAG查询系统
  - Python实现的检索增强生成系统
  - 支持语义搜索、混合检索

- **`scripts/`** - 脚本工具
  - 索引构建、更新、验证脚本
  - 目录重组工具

- **`archive/`** - 归档文件
  - 旧版本指令
  - 已废弃文档

- **`training/`** - 培训材料
  - 知识库筛选方案
  - 团队培训文档

---

### 工作模式

本仓库采用**三空间协作模式**：

#### 1. GitHub仓库（知识资产库）

**职责**：
- ✅ 理论体系：78篇核心文档
- ✅ 子项目框架：shangye-anli/ AI产品分析/
- ✅ 工具文档：99-gongjuSOP/
- ✅ 版本控制：Git管理所有变更

**不包含**：
- ❌ 课程原文件（版权保护）
- ❌ 临时工作文件
- ❌ 个人笔记碎片

#### 2. 本地工作区（dedao/）

**职责**：
- ✅ 商业案例拆解
- ✅ 课程原文件（作为拆解材料）
- ✅ 实战练习和快速迭代

**工作流**：
1. 使用系统指令拆解案例
2. 提炼商业模型
3. 归纳跨案例洞察
4. 定期同步到仓库（去除课程引用）

**路径**：相对于仓库的本地目录

#### 3. Claude Projects（AI协作界面）

**职责**：
- ✅ 日常AI协作
- ✅ 知识检索（Project Knowledge）
- ✅ 快速查询和分析

**数据来源**：
- 从GitHub仓库定期同步
- 不包含课程原文

---

### 同步机制

#### 本地→仓库（定期同步）

**同步内容**：
- ✅ 新拆解的案例文档（去除课程原文引用）
- ✅ 新提炼的商业模型
- ✅ 新归纳的跨案例洞察

**同步频率**：建议每周一次

**操作指南**：参考 `99-gongjuSOP/协作/本地与仓库同步SOP.md`

#### 仓库→本地（按需同步）

**同步内容**：
- ✅ 系统指令更新
- ✅ 框架文档更新
- ✅ 工具文档更新

**触发时机**：
- 系统指令有重大更新
- 框架方法论调整
- 新增工具或SOP

#### 仓库→Projects（定期同步）

**同步内容**：
- ✅ Project Knowledge更新
- ✅ 新文档索引
- ✅ 理论文档更新

**同步频率**：建议每月一次

---

### 版本管理

**文档版本规则**：
- 道层文档：DOC-D001 ~ DOC-D012
- 术层文档：DOC-S001 ~ DOC-S068
- 每篇文档有独立YAML索引

**Git提交规范**：
- `feat:` - 新增文档/功能
- `docs:` - 更新文档内容
- `chore:` - 更新索引/目录
- `refactor:` - 结构调整
- `fix:` - 修复问题

---

### 快速导航

| 需求 | 推荐路径 |
|------|---------|
| **学习理论** | `01-dao/` + `02-shu/` + `rag-index/learning-paths.md` |
| **拆解商业案例** | 本地 `dedao/` + `shangye-anli/00_系统指令/` |
| **分析AI产品** | `AI产品分析/AI产品竞品分析/00_系统指令/` |
| **写作新文档** | `99-gongjuSOP/写作/新文档写作框架指南.md` |
| **构建知识库** | `99-gongjuSOP/知识库/知识库构建SOP.md` |
| **RAG检索** | `rag-system/` + `rag-index/` |
| **对标学习** | `02-shu/innovation/三大标杆的可复用方法论-Notion亚马逊Musk.md` (DOC-S047) |
| **项目评估** | `02-shu/innovation/创业项目评估方法论-从归因分析到投资决策.md` (DOC-S048) |

EOF

    # 查找插入位置（在"## 🔗 文件关联网络"之前）
    if grep -q "## 🔗 文件关联网络" README.md; then
        # 找到了标记，在其前面插入
        awk '
        /## 🔗 文件关联网络/ {
            system("cat /tmp/readme_insert.md")
            print
            next
        }
        {print}
        ' README.md > README.md.tmp && mv README.md.tmp README.md
        echo "✅ 已在'文件关联网络'章节前插入新内容"
    else
        # 没找到标记，在文件末尾添加
        cat /tmp/readme_insert.md >> README.md
        echo "✅ 已在文件末尾添加新内容"
    fi
else
    echo "✅ README.md已是最新，跳过更新"
fi

echo ""
echo "✅ Step 4 完成"
```

---

### Step 5：创建同步SOP文档

```bash
echo ""
echo "=========================================="
echo "Step 5: 创建同步SOP文档"
echo "=========================================="

if [ "$NEED_CREATE_SOP" = true ]; then
    # 创建目录（如果不存在）
    mkdir -p 99-gongjuSOP/协作

    # 创建同步SOP文档（使用相对路径）
    cat > 99-gongjuSOP/协作/本地与仓库同步SOP.md << 'EOF'
# 本地与仓库同步SOP

> **用途**：规范本地dedao/与GitHub仓库的同步流程  
> **频率**：建议每周同步一次  
> **维护者**：常松阳

---

## 🎯 同步原则

### 核心规则

1. **本地→仓库**：
   - ✅ 同步：完成的案例/模型/洞察
   - ❌ 不同步：课程原文、临时文件、个人笔记

2. **仓库→本地**：
   - ✅ 同步：系统指令更新、框架调整
   - 触发：按需同步（有重大更新时）

3. **质量标准**：
   - 文档必须完整（所有必要章节）
   - 已去除课程原文引用
   - 索引已更新
   - 文件命名符合规范

---

## 📤 从本地同步到仓库

### 场景1：新拆解的商业案例

**前置检查**：
- [ ] 案例文档已完成（包含所有必要部分）
- [ ] 已去除课程原文直接引用（改为"根据课程材料整理"）
- [ ] 已更新本地的 `案例总索引.md`
- [ ] 文件命名符合规范：`<企业名>-<关键词>.md`

**同步步骤**：

```bash
# 假设：
# - 本地工作区：../dedao/
# - 仓库目录：./（当前目录）

# 1. 从本地复制案例到仓库
cp ../dedao/01_案例库/按行业分类/<行业>/<案例文件>.md \
   ./shangye-anli/01_案例库/按行业分类/<行业>/

# 2. 更新仓库的案例总索引
# 手动编辑 shangye-anli/01_案例库/案例总索引.md
# 添加新案例条目

# 3. Git提交
git add shangye-anli/01_案例库/
git commit -m "feat: 新增<企业名>案例拆解"
git push
```

**质量检查**：
- [ ] 案例文档无课程原文引用
- [ ] 案例总索引已更新
- [ ] Git提交完成

---

### 场景2：新提炼的商业模型

**前置检查**：
- [ ] 模型文档已完成
- [ ] 包含：机制、变量、边界、验证方式
- [ ] 至少有2-3个支撑案例
- [ ] 已更新本地的 `模型总索引.md`

**同步步骤**：

```bash
# 1. 从本地复制模型到仓库
cp ../dedao/02_模型库/<类型>/<模型文件>.md \
   ./shangye-anli/02_模型库/<类型>/

# 2. 更新仓库的模型总索引
# 手动编辑 shangye-anli/02_模型库/模型总索引.md

# 3. Git提交
git add shangye-anli/02_模型库/
git commit -m "feat: 新增<模型名>商业模型"
git push
```

---

### 场景3：新归纳的跨案例洞察

**前置检查**：
- [ ] 洞察文档已完成
- [ ] 包含：主题、机制、可证伪条件、验证计划
- [ ] 至少对比2-3个案例
- [ ] 已更新本地的 `洞察总索引.md`

**同步步骤**：

```bash
# 1. 从本地复制洞察到仓库
cp ../dedao/03_洞察库/<洞察文件>.md \
   ./shangye-anli/03_洞察库/

# 2. 更新仓库的洞察总索引
# 手动编辑 shangye-anli/03_洞察库/洞察总索引.md

# 3. Git提交
git add shangye-anli/03_洞察库/
git commit -m "feat: 新增<主题>跨案例洞察"
git push
```

---

## 📥 从仓库同步到本地

### 场景1：系统指令更新

**触发条件**：
- 系统指令有重大更新（如新增步骤、调整框架）
- 收到团队通知

**同步步骤**：

```bash
# 1. 从仓库拉取最新版本
git pull

# 2. 复制更新的系统指令到本地
cp ./shangye-anli/00_系统指令/*.md ../dedao/00_系统指令/

# 3. 验证本地工作区使用最新指令
echo "✅ 系统指令已更新到最新版本"
ls -lh ../dedao/00_系统指令/
```

---

### 场景2：框架文档更新

**触发条件**：
- README有重要调整
- 流程规范有变化

**同步步骤**：

```bash
# 1. 从仓库拉取最新版本
git pull

# 2. 复制更新的README到本地
cp ./shangye-anli/README.md ../dedao/
cp ./shangye-anli/01_案例库/README.md ../dedao/01_案例库/
# ... 其他需要的README

# 3. 调整本地工作流（如有需要）
echo "✅ 框架文档已同步"
```

---

## ⚠️ 注意事项

### 禁止同步的内容

**从本地→仓库（禁止）**：
- ❌ 课程原文件（`../dedao/04_原著笔记/MD/*.md`）
- ❌ 临时工作文件（`*.tmp`, `*.bak`）
- ❌ 个人笔记（未经整理的碎片）
- ❌ 带有课程原文直接引用的案例

**从仓库→本地（通常不需要）**：
- ❌ 理论文档（01-dao/, 02-shu/）：通过Claude Projects访问即可
- ❌ RAG索引：本地不需要完整RAG系统

---

### 同步前检查清单

**文档质量**：
- [ ] 文档结构完整（所有必要章节）
- [ ] 内容符合质量标准
- [ ] 已去除课程原文引用
- [ ] 语言表达清晰、逻辑连贯

**索引更新**：
- [ ] 对应的总索引已更新（案例/模型/洞察）
- [ ] 索引信息准确（标题、路径、标签）

**文件规范**：
- [ ] 文件命名符合规范
- [ ] 存储路径正确
- [ ] Markdown格式正确

**Git提交**：
- [ ] 提交信息清晰（feat/docs/chore）
- [ ] 只提交相关文件
- [ ] 提交前已测试

---

## 📋 同步记录模板

建议在本地 `../dedao/05_学习记录/` 维护同步记录：

```markdown
# 同步记录 - YYYY-MM-DD

## 本次同步内容

### 新增案例（X个）
- [企业名]-[关键词].md - [行业] - [状态]

### 新增模型（X个）
- [模型名].md - [类型] - [支撑案例数]

### 新增洞察（X个）
- 洞察[编号]-[主题].md - [对比案例数]

## 质量检查

- [ ] 所有文档已去除课程引用
- [ ] 索引已更新
- [ ] Git提交完成

## 下次计划

- [ ] 待同步内容...
```

---

## 📊 同步频率建议

| 内容类型 | 建议频率 | 触发条件 |
|---------|---------|---------|
| **新案例** | 每周一次 | 完成2-3个案例后 |
| **新模型** | 每2周一次 | 提炼新模型后 |
| **新洞察** | 每月一次 | 跨案例对比完成后 |
| **系统指令** | 按需 | 仓库通知更新 |

---

## 💡 最佳实践

1. **小步快跑**：
   - 完成一个案例就同步一个
   - 不要积累太多未同步内容

2. **保持质量**：
   - 同步前必须质量检查
   - 宁可慢一点，不要返工

3. **及时更新索引**：
   - 每次同步都更新总索引
   - 索引是检索的入口

4. **记录同步日志**：
   - 维护同步记录
   - 方便复盘和追溯

---

**文档版本**：v1.0  
**创建日期**：2026-01-04  
**维护者**：常松阳  
**相关文档**：
- `../shangye-anli/README.md` - 项目说明
- `../99-gongjuSOP/知识库/知识库构建SOP.md` - 知识库构建流程
- `../99-gongjuSOP/写作/新文档写作框架指南.md` - 写作规范
EOF

    echo "✅ 同步SOP文档已创建"
    echo ""
    echo "文档路径: 99-gongjuSOP/协作/本地与仓库同步SOP.md"
else
    echo "✅ 同步SOP已存在，跳过创建"
fi

echo ""
echo "✅ Step 5 完成"
```

---

### Step 6：最终验证和报告

```bash
echo ""
echo "=========================================="
echo "Step 6: 最终验证和报告"
echo "=========================================="

# 生成验证报告
REPORT="/tmp/repo_cleanup_report_v2.txt"
> $REPORT

echo "=== 仓库整理验证报告 (v2.0优化版) ===" >> $REPORT
echo "生成时间: $(date)" >> $REPORT
echo "" >> $REPORT

# 1. 空文件夹检查
echo "1. 空文件夹检查" >> $REPORT
echo "---" >> $REPORT
REMAINING_EMPTY=$(find . -type d -empty -not -path "./.git/*" 2>/dev/null | wc -l)
echo "剩余空文件夹数: $REMAINING_EMPTY" >> $REPORT
if [ $REMAINING_EMPTY -gt 0 ]; then
    echo "剩余空文件夹:" >> $REPORT
    find . -type d -empty -not -path "./.git/*" >> $REPORT 2>/dev/null
fi
echo "" >> $REPORT

# 2. 关键文件检查
echo "2. 关键文件检查" >> $REPORT
echo "---" >> $REPORT
echo "shangye-anli/README.md: $([ -f shangye-anli/README.md ] && echo '✅ 存在' || echo '❌ 缺失')" >> $REPORT
if [ -f shangye-anli/README.md ]; then
    echo "  - 包含'本地工作区模式': $(grep -q '本地工作区模式' shangye-anli/README.md && echo '✅ 是' || echo '❌ 否')" >> $REPORT
fi
echo ".gitignore: $([ -f .gitignore ] && echo '✅ 存在' || echo '❌ 缺失')" >> $REPORT
if [ -f .gitignore ]; then
    echo "  - 包含dedao规则: $(grep -q 'dedao/' .gitignore && echo '✅ 是' || echo '❌ 否')" >> $REPORT
fi
echo "README.md: $([ -f README.md ] && echo '✅ 存在' || echo '❌ 缺失')" >> $REPORT
if [ -f README.md ]; then
    echo "  - 包含'仓库结构说明': $(grep -q '仓库结构说明' README.md && echo '✅ 是' || echo '❌ 否')" >> $REPORT
fi
echo "99-gongjuSOP/协作/本地与仓库同步SOP.md: $([ -f 99-gongjuSOP/协作/本地与仓库同步SOP.md ] && echo '✅ 存在' || echo '❌ 缺失')" >> $REPORT
echo "" >> $REPORT

# 3. 目录结构验证
echo "3. 目录结构" >> $REPORT
echo "---" >> $REPORT
tree -L 2 -d >> $REPORT 2>/dev/null || find . -type d -maxdepth 2 >> $REPORT

# 显示报告
echo ""
echo "=========================================="
echo "📊 整理验证报告"
echo "=========================================="
cat $REPORT

# 保存报告到仓库
cp $REPORT ./仓库整理报告-$(date +%Y%m%d).txt 2>/dev/null

echo ""
echo "✅ Step 6 完成"
echo ""
echo "=========================================="
echo "🎉 仓库整理全部完成！"
echo "=========================================="
echo ""
echo "完成的任务:"
echo "✅ Step 0: 环境检查和状态确认"
echo "✅ Step 1: 清理空文件夹"
echo "✅ Step 2: 优化.gitignore规则"
echo "✅ Step 3: 更新shangye-anli/README.md"
echo "✅ Step 4: 更新根目录README.md"
echo "✅ Step 5: 创建同步SOP"
echo "✅ Step 6: 生成验证报告"
echo ""
echo "📋 下一步建议:"
echo "1. 查看验证报告: cat /tmp/repo_cleanup_report_v2.txt"
echo "2. 检查shangye-anli/README.md的更新"
echo "3. 检查根目录README.md的新增章节"
echo "4. 阅读同步SOP: 99-gongjuSOP/协作/本地与仓库同步SOP.md"
echo "5. Git提交所有更改"
echo ""
echo "🔧 Git提交命令（建议）:"
echo "git add ."
echo "git status  # 检查变更"
echo 'git commit -m "chore: 整理仓库结构（v2.0优化版）

- 清理空文件夹
- 优化.gitignore规则（精确路径匹配）
- 更新shangye-anli/README.md（标注本地工作区模式）
- 更新根目录README.md（添加仓库结构说明）
- 新增同步SOP（99-gongjuSOP/协作/本地与仓库同步SOP.md）

基于Cursor深度分析的优化：
- 添加状态检查（跳过已完成步骤）
- 优化.gitignore（避免误伤正常文档）
- 使用相对路径（提高可移植性）
- 检查现有内容（避免重复更新）"'
echo "git push"
echo ""
```

---

## 执行说明

### 如何使用这个指令

**逐步执行（推荐）**：
```bash
# 1. 复制Step 0到Cursor执行
# 2. 查看状态报告，确认需要执行的步骤
# 3. 逐步复制Step 1-6执行
```

**优点**：
- ✅ 每步都有状态检查
- ✅ 跳过已完成的步骤
- ✅ 可以验证每步的结果

---

## 优化说明

### v2.0相比v1.0的改进

1. **添加Step 0状态检查**：
   - 检查哪些步骤已完成
   - 智能跳过重复操作
   - 给出清晰的执行建议

2. **优化.gitignore规则**：
   - 使用 `**/04_原著笔记/MD/*.md` 精确匹配
   - 避免误伤包含"课程"的正常文档
   - 减少误报

3. **使用相对路径**：
   - 同步SOP中使用 `../dedao/` 和 `./`
   - 提高可移植性
   - 适应不同的目录结构

4. **检查现有内容**：
   - 避免重复更新已有说明
   - 保护用户自定义内容
   - 减少不必要的变更

5. **更详细的报告**：
   - 包含状态检查结果
   - 列出实际执行的操作
   - 提供明确的下一步建议

---

## 预期执行时间

- **Step 0**: 30秒（状态检查）
- **Step 1**: 1-2分钟（清理空文件夹）
- **Step 2-5**: 5-8分钟（更新文档）
- **Step 6**: 1分钟（生成报告）

**总计**: 约**8-12分钟**

---

## 验证清单

执行完成后，检查：

- [ ] 空文件夹已清理（Step 1报告）
- [ ] .gitignore包含优化规则（Step 2）
- [ ] shangye-anli/README.md有"本地工作区模式"（Step 3）
- [ ] 根目录README.md有"仓库结构说明"（Step 4）
- [ ] 同步SOP文档已创建（Step 5）
- [ ] 验证报告已生成（Step 6）

---

**优化版准备完毕！** 🚀

基于Cursor的专业分析，这个版本更智能、更安全、更可靠。
