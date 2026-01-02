import os
import subprocess

# 切换到项目根目录
os.chdir('.')

# 添加DEDAO文件夹中的所有markdown文件
subprocess.run(['git', 'add', '商业案例课改编/dedao/*.md'])

print("DEDAO files added to git")