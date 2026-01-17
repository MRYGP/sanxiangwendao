# -*- coding: utf-8 -*-
import subprocess
import sys
import os
from pathlib import Path

os.chdir(Path(__file__).parent.parent)
subprocess.run(['git', 'commit', '-m', 'docs: 添加乱码修复工具和指南'])
