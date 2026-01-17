# -*- coding: utf-8 -*-
"""
仓库重组脚本：将商业案例拆解相关内容归档到 _to_move/ 目录
"""
import os
import shutil
from pathlib import Path

base_dir = Path(r'e:\sanxiangwendao')
os.chdir(base_dir)

print("=" * 60)
print("开始执行仓库重组任务")
print("=" * 60)

# Step 1: 创建存档目录结构
print("\n[Step 1] 创建存档目录结构...")
to_move_dir = base_dir / '_to_move'
dirs_to_create = [
    to_move_dir / 'shangye-anli',
    to_move_dir / '99-gongjuSOP-协作',
    to_move_dir / '88-案例库'
]

for dir_path in dirs_to_create:
    dir_path.mkdir(parents=True, exist_ok=True)
    print(f'  [OK] 已创建: {dir_path.relative_to(base_dir)}')

# Step 2: 移动 shangye-anli/
print("\n[Step 2] 移动 shangye-anli/ 到 _to_move/shangye-anli/...")
shangye_anli_src = base_dir / 'shangye-anli'
shangye_anli_dst = to_move_dir / 'shangye-anli'

if shangye_anli_src.exists():
    for item in shangye_anli_src.iterdir():
        dst_path = shangye_anli_dst / item.name
        if item.is_dir():
            if dst_path.exists():
                shutil.rmtree(dst_path)
            shutil.copytree(item, dst_path)
        else:
            shutil.copy2(item, dst_path)
        print(f'  [OK] 已移动: {item.name}')
    print(f'  [INFO] shangye-anli/ 内容已复制到 _to_move/shangye-anli/')
    print(f'  [NOTE] 原目录保留，稍后需要手动删除')
else:
    print(f'  [WARN] shangye-anli/ 目录不存在')

# Step 3: 移动 99-gongjuSOP/协作/
print("\n[Step 3] 移动 99-gongjuSOP/协作/ 到 _to_move/99-gongjuSOP-协作/...")
collab_src = base_dir / '99-gongjuSOP' / '协作'
collab_dst = to_move_dir / '99-gongjuSOP-协作'

if collab_src.exists():
    for item in collab_src.iterdir():
        dst_path = collab_dst / item.name
        if item.is_dir():
            if dst_path.exists():
                shutil.rmtree(dst_path)
            shutil.copytree(item, dst_path)
        else:
            shutil.copy2(item, dst_path)
        print(f'  [OK] 已移动: {item.name}')
    print(f'  [INFO] 99-gongjuSOP/协作/ 内容已复制到 _to_move/99-gongjuSOP-协作/')
else:
    print(f'  [WARN] 99-gongjuSOP/协作/ 目录不存在')

# Step 4: 移动 88/
print("\n[Step 4] 移动 88/ 到 _to_move/88-案例库/...")
case88_src = base_dir / '88'
case88_dst = to_move_dir / '88-案例库'

if case88_src.exists():
    for item in case88_src.iterdir():
        dst_path = case88_dst / item.name
        if item.is_dir():
            if dst_path.exists():
                shutil.rmtree(dst_path)
            shutil.copytree(item, dst_path)
        else:
            shutil.copy2(item, dst_path)
        print(f'  [OK] 已移动: {item.name}')
    print(f'  [INFO] 88/ 内容已复制到 _to_move/88-案例库/')
else:
    print(f'  [WARN] 88/ 目录不存在')

# Step 5: 创建 02-shu/cases/ 目录结构
print("\n[Step 5] 创建 02-shu/cases/ 目录结构...")
cases_dir = base_dir / '02-shu' / 'cases'
subdirs = ['跨案例对比', '科技互联网', '金融投资']

for subdir in subdirs:
    subdir_path = cases_dir / subdir
    subdir_path.mkdir(parents=True, exist_ok=True)
    print(f'  [OK] 已创建: {subdir_path.relative_to(base_dir)}')

# Step 6: 复制案例文档
print("\n[Step 6] 复制案例文档到 02-shu/cases/...")

# 从 _to_move/88-案例库/ 复制案例
case_source = to_move_dir / '88-案例库' / '01_案例库'

# 复制 Musk 跨案例对比
musk_src = case_source / '跨案例对比' / 'Musk-商业模式跨案例对比.md'
musk_dst = cases_dir / '跨案例对比' / 'Musk-商业模式跨案例对比.md'
if musk_src.exists():
    shutil.copy2(musk_src, musk_dst)
    print(f'  [OK] 已复制: Musk-商业模式跨案例对比.md -> 跨案例对比/')
else:
    print(f'  [WARN] 未找到: {musk_src}')

# 复制 Tesla 案例
tesla_src = case_source / '按行业分类' / '科技互联网' / 'Tesla-创办电动汽车公司是蠢上加蠢.md'
tesla_dst = cases_dir / '科技互联网' / 'Tesla-创办电动汽车公司是蠢上加蠢.md'
if tesla_src.exists():
    shutil.copy2(tesla_src, tesla_dst)
    print(f'  [OK] 已复制: Tesla-创办电动汽车公司是蠢上加蠢.md -> 科技互联网/')
else:
    print(f'  [WARN] 未找到: {tesla_src}')

# 复制亚马逊案例
amazon_src = case_source / '按企业生命周期分类' / '成长期' / '亚马逊-三大支柱业务与飞轮效应.md'
amazon_dst = cases_dir / '科技互联网' / '亚马逊-三大支柱业务与飞轮效应.md'
if amazon_src.exists():
    shutil.copy2(amazon_src, amazon_dst)
    print(f'  [OK] 已复制: 亚马逊-三大支柱业务与飞轮效应.md -> 科技互联网/')
else:
    print(f'  [WARN] 未找到: {amazon_src}')

# 复制 Buffett 案例
buffett_src = case_source / '按行业分类' / '科技互联网' / 'Buffett-股神从投资大师格雷厄姆身上学到了什么.md'
buffett_dst = cases_dir / '金融投资' / 'Buffett-股神从投资大师格雷厄姆身上学到了什么.md'
if buffett_src.exists():
    shutil.copy2(buffett_src, buffett_dst)
    print(f'  [OK] 已复制: Buffett-股神从投资大师格雷厄姆身上学到了什么.md -> 金融投资/')
else:
    print(f'  [WARN] 未找到: {buffett_src}')

# 复制 Alibaba 案例（如果有）
alibaba_src = case_source / '按行业分类' / '科技互联网' / 'Alibaba-业务财务宏观纵览.md'
alibaba_dst = cases_dir / '科技互联网' / 'Alibaba-业务财务宏观纵览.md'
if alibaba_src.exists():
    shutil.copy2(alibaba_src, alibaba_dst)
    print(f'  [OK] 已复制: Alibaba-业务财务宏观纵览.md -> 科技互联网/')

print("\n" + "=" * 60)
print("仓库重组任务执行完成！")
print("=" * 60)
print("\n下一步：")
print("1. 检查 _to_move/ 目录内容")
print("2. 检查 02-shu/cases/ 目录内容")
print("3. 创建 _to_move/README.md 说明文档")
print("4. Git 提交变更")
