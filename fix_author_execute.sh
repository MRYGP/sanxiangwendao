#!/bin/bash
# 修复Git提交历史中的作者信息（非交互式版本）

OLD_NAME="康康康"
OLD_EMAIL="924630554@qq.com"
NEW_NAME="MRYGP"
NEW_EMAIL="a44425874@gmail.com"

echo "============================================================"
echo "修复Git提交历史中的作者信息"
echo "============================================================"
echo ""
echo "将修复: $OLD_NAME <$OLD_EMAIL>"
echo "改为:   $NEW_NAME <$NEW_EMAIL>"
echo ""
echo "开始修复..."

export FILTER_BRANCH_SQUELCH_WARNING=1

git filter-branch --env-filter "
if [ \"\$GIT_AUTHOR_NAME\" = \"$OLD_NAME\" ] || [ \"\$GIT_AUTHOR_EMAIL\" = \"$OLD_EMAIL\" ]; then
    export GIT_AUTHOR_NAME=\"$NEW_NAME\"
    export GIT_AUTHOR_EMAIL=\"$NEW_EMAIL\"
fi
if [ \"\$GIT_COMMITTER_NAME\" = \"$OLD_NAME\" ] || [ \"\$GIT_COMMITTER_EMAIL\" = \"$OLD_EMAIL\" ]; then
    export GIT_COMMITTER_NAME=\"$NEW_NAME\"
    export GIT_COMMITTER_EMAIL=\"$NEW_EMAIL\"
fi
" --tag-name-filter cat -- --branches --tags

echo ""
echo "============================================================"
echo "修复完成！"
echo "============================================================"
echo ""
echo "检查修复结果:"
git log --format="%H|%an|%ae" -10
echo ""
