"""
Dry-run测试：不安装依赖，验证代码逻辑和配置
"""
import sys
import io
from pathlib import Path

# 设置UTF-8编码（Windows兼容）
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "rag-system"))

print("=" * 60)
print("RAG系统 Dry-Run 测试")
print("=" * 60)
print("\n此测试不安装依赖，仅验证代码逻辑和配置...\n")

# 测试1: 配置文件
print("[测试1] 配置文件加载...")
try:
    from config import DOC_MAPPING, get_doc_file_path, INDEX_DIR, VECTOR_DB_DIR
    print(f"  ✅ DOC_MAPPING: {len(DOC_MAPPING)} 篇文档")
    print(f"  ✅ INDEX_DIR: {INDEX_DIR}")
    print(f"  ✅ VECTOR_DB_DIR: {VECTOR_DB_DIR}")
except Exception as e:
    print(f"  ❌ 配置加载失败: {e}")
    sys.exit(1)

# 测试2: 文档路径查找
print("\n[测试2] 文档路径查找...")
test_docs = ["DOC-D001", "DOC-S001", "DOC-S039"]
all_found = True
for doc_id in test_docs:
    try:
        file_path = get_doc_file_path(doc_id)
        exists = file_path.exists()
        status = "✅" if exists else "❌"
        print(f"  {status} {doc_id}: {file_path.name}")
        if not exists:
            all_found = False
    except Exception as e:
        print(f"  ❌ {doc_id}: {e}")
        all_found = False

if not all_found:
    print("  ⚠️  部分文档路径查找失败")
else:
    print("  ✅ 所有测试文档路径正确")

# 测试3: 索引文件检查
print("\n[测试3] 索引文件检查...")
index_files = list(INDEX_DIR.glob("*.yaml"))
print(f"  ✅ 找到 {len(index_files)} 个索引文件")
if len(index_files) != len(DOC_MAPPING):
    print(f"  ⚠️  索引文件数量 ({len(index_files)}) 与文档映射 ({len(DOC_MAPPING)}) 不一致")

# 测试4: 代码结构检查
print("\n[测试4] 代码结构检查...")
modules = [
    "rag-system/embedding.py",
    "rag-system/document_loader.py",
    "rag-system/vector_store.py",
    "rag-system/retriever.py",
    "rag-system/query_processor.py",
    "rag-system/rag_chain.py",
    "scripts/build_index.py",
    "scripts/test_query.py",
]

all_exist = True
for module in modules:
    file_path = project_root / module
    exists = file_path.exists()
    status = "✅" if exists else "❌"
    print(f"  {status} {module}")
    if not exists:
        all_exist = False

# 测试5: 目录结构检查
print("\n[测试5] 新目录结构检查...")
dao_dirs = [
    "01-dao/theory",
    "01-dao/framework",
    "01-dao/philosophy",
]
shu_dirs = [
    "02-shu/innovation",
    "02-shu/communication",
    "02-shu/behavior-change",
    "02-shu/strategy",
    "02-shu/execution",
    "02-shu/psychology",
]

all_dirs_exist = True
for dir_path in dao_dirs + shu_dirs:
    full_path = project_root / dir_path
    exists = full_path.exists()
    status = "✅" if exists else "❌"
    print(f"  {status} {dir_path}/")
    if not exists:
        all_dirs_exist = False

# 总结
print("\n" + "=" * 60)
print("测试总结")
print("=" * 60)

issues = []
if not all_found:
    issues.append("部分文档路径查找失败")
if not all_exist:
    issues.append("部分代码文件缺失")
if not all_dirs_exist:
    issues.append("部分目录缺失")

if issues:
    print("⚠️  发现以下问题：")
    for issue in issues:
        print(f"  - {issue}")
    print("\n建议：修复上述问题后再继续")
else:
    print("✅ 所有基础检查通过！")
    print("\n下一步：")
    print("  1. 安装依赖：pip install -r requirements.txt")
    print("  2. 重建索引：python scripts/build_index.py --reset")
    print("  3. 测试查询：python scripts/test_query.py \"什么是价值链创新\"")

print("=" * 60)

