#!/bin/bash
# 自动修复乱码提交脚本
# 注意：此脚本会修改Git历史，需要force push

# 修复提交 9e2f1e5
git rebase -i 9e2f1e5^
# 在编辑器中，将'pick'改为'reword'，然后修改message为：
# chore: remove duplicate Claude_Projects指令V3.4.md file...

# 修复提交 a41b73a
git rebase -i a41b73a^
# 在编辑器中，将'pick'改为'reword'，然后修改message为：
# docs: 添加仓库清理分析报告 - 识别与仓库定位不符的内容...

# 修复提交 c4c1a3b
git rebase -i c4c1a3b^
# 在编辑器中，将'pick'改为'reword'，然后修改message为：
# chore: 清理案例文档和更新README...

# 修复提交 f1f6032
git rebase -i f1f6032^
# 在编辑器中，将'pick'改为'reword'，然后修改message为：
# 归档：将商业案例拆解内容移至_to_move/，准备移出到aichajie...

# 修复提交 b822d43
git rebase -i b822d43^
# 在编辑器中，将'pick'改为'reword'，然后修改message为：
# chore: 删除临时重组脚本...

# 修复提交 af371f3
git rebase -i af371f3^
# 在编辑器中，将'pick'改为'reword'，然后修改message为：
# chore: 删除_to_move/README.md...

# 修复提交 9a31712
git rebase -i 9a31712^
# 在编辑器中，将'pick'改为'reword'，然后修改message为：
# 清理：删除临时报告和已移出内容  - 删除临时报告文件（仓库清理分析报告等14个文件） - 删除已移出的目录（shang...

# 修复提交 ddb3da8
git rebase -i ddb3da8^
# 在编辑器中，将'pick'改为'reword'，然后修改message为：
# 清理：删除临时工具脚本  - 删除 cleanup_repo.py（清理任务已完成） - 删除 fix_encoding...


# 最后force push
git push origin master --force
