#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import re
from collections import defaultdict

# 设置UTF-8编码
sys.stdout.reconfigure(encoding='utf-8')

def analyze_dedao_structure():
    dedao_path = '商业案例课改编/dedao'
    files = os.listdir(dedao_path)
    files.sort()

    companies = defaultdict(list)
    themes = defaultdict(int)
    total_files = 0

    for file in files:
        if not file.endswith('.md'):
            continue

        total_files += 1

        # 提取公司和主题
        if '丨' in file:
            parts = file.split('丨')
            company = parts[0].split('.')[1].strip()
            theme = parts[1].replace('.md', '').strip()

            companies[company].append(theme)

            # 统计主题关键词
            if '马斯克' in company or 'Musk' in company:
                theme_key = 'Elon Musk系列'
            elif '巴菲特' in company or 'Buffett' in company:
                theme_key = 'Warren Buffett系列'
            elif '亚马逊' in company or 'Amazon' in company:
                theme_key = 'Amazon系列'
            elif '苹果' in company or 'Apple' in company:
                theme_key = 'Apple系列'
            elif 'Netflix' in company:
                theme_key = 'Netflix系列'
            elif '特斯拉' in company or 'Tesla' in company:
                theme_key = 'Tesla系列'
            elif 'SpaceX' in company:
                theme_key = 'SpaceX系列'
            elif '京东' in company or 'JD' in company:
                theme_key = '京东系列'
            elif '拼多多' in company or 'Pinduoduo' in company:
                theme_key = '拼多多系列'
            elif '美团' in company or 'Meituan' in company:
                theme_key = '美团系列'
            elif '周末互动' in file:
                theme_key = '互动与思考'
            else:
                theme_key = '其他企业'

            themes[theme_key] += 1

    print('商业案例课改编 - dedao文件夹分析')
    print('=' * 50)
    print(f'总文件数: {total_files}')
    print(f'覆盖企业/主题数: {len(companies)}')
    print()
    print('主题分布 (按案例数量排序):')
    for theme, count in sorted(themes.items(), key=lambda x: x[1], reverse=True):
        print(f'  {theme}: {count}篇')

    print()
    print('主要企业 (前10名，按案例数排序):')
    for company, cases in sorted(companies.items(), key=lambda x: len(x[1]), reverse=True)[:10]:
        print(f'  {company}: {len(cases)}篇案例')
        # 显示前3个案例标题
        for i, case in enumerate(cases[:3]):
            print(f'    • {case}')

    # 生成优先级建议
    print()
    print('改编优先级建议:')
    priority_order = [
        ('Elon Musk系列', '创业家思维、科技创新'),
        ('Warren Buffett系列', '投资智慧、价值投资'),
        ('Amazon系列', '平台战略、飞轮效应'),
        ('Tesla系列', '颠覆式创新、电动汽车'),
        ('SpaceX系列', '航天科技、成本创新'),
        ('Apple系列', '产品设计、用户体验'),
        ('Netflix系列', '内容平台、订阅模式'),
        ('京东系列', '物流体系、自营模式'),
        ('美团系列', '本地生活、高频业务'),
        ('拼多多系列', '社交电商、下沉市场')
    ]

    for i, (theme, reason) in enumerate(priority_order, 1):
        if theme in themes:
            print(f'{i}. {theme} ({themes[theme]}篇) - {reason}')

if __name__ == '__main__':
    analyze_dedao_structure()