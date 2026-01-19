#!/bin/bash
# 修复Git提交历史中的作者信息
# 将"康康康"统一改为"MRYGP"

git filter-branch --env-filter '
OLD_NAME="康康康"
NEW_NAME="MRYGP"
NEW_EMAIL="a44425874@gmail.com"

if [ "$GIT_AUTHOR_NAME" = "$OLD_NAME" ]; then
    export GIT_AUTHOR_NAME="$NEW_NAME"
    export GIT_AUTHOR_EMAIL="$NEW_EMAIL"
fi
if [ "$GIT_COMMITTER_NAME" = "$OLD_NAME" ]; then
    export GIT_COMMITTER_NAME="$NEW_NAME"
    export GIT_COMMITTER_EMAIL="$NEW_EMAIL"
fi
' --tag-name-filter cat -- --branches --tags

echo ""
echo "修复完成！"
echo "请检查结果: git log --format='%H|%an|%ae' -10"
echo "如果满意，运行: git push origin master --force"
