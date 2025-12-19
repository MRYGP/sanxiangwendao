# Cursor指令：修复GitHub Commit Message乱码

## 问题描述

GitHub仓库显示部分commit message出现乱码，如：
- "æ,...ç�†è¾...åŠ©æ—†æ¡£å¤' é™¤å†—æž©æŠ¾å'Šï¼Œæ›..."

这是UTF-8编码被错误解释为其他编码（如Latin-1）导致的。

## 诊断步骤

### 1. 检查Git全局配置

```bash
# 查看当前编码配置
git config --global --list | grep -i encoding

# 查看commit.encoding
git config --global commit.encoding

# 查看i18n.commitencoding
git config --global i18n.commitencoding

# 查看i18n.logoutputencoding
git config --global i18n.logoutputencoding
```

### 2. 检查仓库级配置

```bash
# 进入仓库目录
cd /path/to/sanxiangwendao

# 查看仓库级编码配置
git config --local --list | grep -i encoding
```

### 3. 查看最近的commit message编码

```bash
# 查看最近10个commit的message（看是否乱码）
git log --oneline -10

# 查看详细信息
git log -5
```

## 修复步骤

### 方案A：设置正确的Git编码配置

```bash
# 设置全局编码为UTF-8
git config --global i18n.commitencoding utf-8
git config --global i18n.logoutputencoding utf-8
git config --global core.quotepath false

# 如果使用Windows，还需要设置
git config --global core.autocrlf true
```

### 方案B：修复终端编码（如果是终端问题）

**macOS/Linux:**
```bash
# 在 ~/.bashrc 或 ~/.zshrc 中添加
export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8
```

**Windows (PowerShell):**
```powershell
# 设置控制台输出编码
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
```

### 方案C：重写乱码的commit message（如果需要）

**警告：这会改变commit历史，如果已经push到远程，需要force push**

```bash
# 交互式rebase，修改最近N个commit
git rebase -i HEAD~N

# 在打开的编辑器中，将需要修改的commit前面的 'pick' 改为 'reword'
# 保存退出后，会依次弹出编辑器让你修改commit message
```

**如果只修改最近一个commit:**
```bash
git commit --amend -m "新的commit message（中文）"
```

### 方案D：检查是否是GitHub显示问题

有时候本地没问题，但GitHub显示乱码，可能是：
1. GitHub页面编码识别问题（刷新或换浏览器试试）
2. 文件名包含特殊字符

## 预防措施

### 1. 确保每次commit前编码正确

在仓库根目录创建 `.gitattributes` 文件：

```
# 设置所有文本文件使用LF换行符
* text=auto

# 明确指定某些文件类型的编码
*.md text encoding=utf-8
*.yaml text encoding=utf-8
*.json text encoding=utf-8
*.py text encoding=utf-8
```

### 2. 提交时使用英文commit message（最保险）

如果中文经常出问题，考虑使用英文commit message：
- `feat: add value chain innovation document`
- `docs: update README with new learning path`
- `fix: correct encoding in metadata files`

## 验证修复

```bash
# 修复后，创建一个测试commit
echo "test" >> test.txt
git add test.txt
git commit -m "测试中文commit message是否正常"

# 查看是否正常显示
git log -1

# 如果正常，删除测试文件
git reset --hard HEAD~1

# push到GitHub后检查显示是否正常
```

## 如果以上都不行

可能是某些commit在创建时就是乱码的，需要：

1. 找出所有乱码的commit
2. 决定是否需要重写历史（如果历史不重要，可以重写）
3. 或者接受历史乱码，只确保未来的commit正常

---

*执行完成后，请反馈诊断结果和修复情况*
