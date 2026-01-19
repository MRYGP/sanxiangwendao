#!/bin/bash
# 修复Git提交历史中的作者信息
# 将"康康康"统一改为"MRYGP"

echo "============================================================"
echo "修复Git提交历史中的作者信息"
echo "============================================================"
echo ""
echo "当前配置:"
echo "  新用户名: MRYGP"
echo "  新邮箱: a44425874@gmail.com"
echo ""
echo "⚠️  警告: 这会重写Git历史！"
echo "请确保已备份仓库或已推送到远程！"
echo ""
read -p "是否继续? (yes/no): " confirm

if [ "$confirm" != "yes" ]; then
    echo "已取消"
    exit 1
fi

echo ""
echo "开始修复..."

git filter-branch --env-filter '
OLD_NAME="康康康"
OLD_EMAIL="924630554@qq.com"
NEW_NAME="MRYGP"
NEW_EMAIL="a44425874@gmail.com"

if [ "$GIT_AUTHOR_NAME" = "$OLD_NAME" ] || [ "$GIT_AUTHOR_EMAIL" = "$OLD_EMAIL" ]; then
    export GIT_AUTHOR_NAME="$NEW_NAME"
    export GIT_AUTHOR_EMAIL="$NEW_EMAIL"
fi
if [ "$GIT_COMMITTER_NAME" = "$OLD_NAME" ] || [ "$GIT_COMMITTER_EMAIL" = "$OLD_EMAIL" ]; then
    export GIT_COMMITTER_NAME="$NEW_NAME"
    export GIT_COMMITTER_EMAIL="$NEW_EMAIL"
fi
' --tag-name-filter cat -- --branches --tags

echo ""
echo "============================================================"
echo "修复完成！"
echo "============================================================"
echo ""
echo "检查修复结果:"
git log --format="%H|%an|%ae" -10
echo ""
echo "如果满意，运行: git push origin master --force"
echo "如果不满意，运行: git filter-branch --force --index-filter 'git rm --cached --ignore-unmatch -r .' --prune-empty --tag-name-filter cat -- --all"
echo "然后: git reset --hard refs/original/refs/heads/master"
