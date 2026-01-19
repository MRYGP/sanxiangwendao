#!/bin/sh
# 修复剩余的乱码提交
export FILTER_BRANCH_SQUELCH_WARNING=1

git filter-branch -f --msg-filter '
case "$GIT_COMMIT" in
    506c6732b648994a05faef8c292062d323506dc1)
        printf "新增：产品设计的三大反人性陷阱 + 社会资源论\n\n- 新增道层理论文档2篇：\n  - DOC-D016: 社会资源论：商业成功的第四维度\n  - DOC-D017: 产品设计的三大反人性陷阱\n- 更新文档映射和RAG配置\n- 更新README统计（86篇文档）\n- 关键洞察：揭示90%产品失败的底层原因（对抗人性）"
        ;;
    9bbe4e5*)
        printf "清理：删除所有临时指令和脚本文件"
        ;;
    *)
        cat
        ;;
esac
' -- --all
