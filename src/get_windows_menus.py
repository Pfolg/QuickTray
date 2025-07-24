# -*- coding: UTF-8 -*-
"""
PROJECT_NAME Python_projects
PRODUCT_NAME PyCharm
NAME get_windows_menus
AUTHOR Pfolg
TIME 2025/4/19 18:27
"""
from pypinyin import pinyin, Style
import os


def get_lnk_pure_name(lnk_path):
    # 提取纯净文件名
    target_name = os.path.basename(lnk_path)  # 获取目标文件名（含扩展名）
    pure_name = os.path.splitext(target_name)[0]  # 去掉所有扩展名
    return pure_name


# 使用示例
if __name__ == '__main__':
    lnk_path = r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\ArcGIS\ArcMap 10.2.lnk"
    print(get_lnk_pure_name(lnk_path))  # 输出: ArcMap 10.2


def get_lnk_classified_dict(target_dir):
    classified = {}
    for root, _, files in os.walk(target_dir):
        for file in files:
            if not file.lower().endswith('.lnk'):
                continue

            # 获取完整路径
            full_path = os.path.join(root, file)

            # 提取文件名首字符
            filename = os.path.splitext(file)[0]
            if not filename:
                continue

            first_char = filename[0]
            # 处理中文首字符
            if '\u4e00' <= first_char <= '\u9fff':
                initial = pinyin(first_char, style=Style.FIRST_LETTER)[0][0].upper()
            else:
                initial = first_char.upper() if first_char.isalpha() else '#'

            # 分类键处理
            key = initial if initial.isalpha() else '#'
            classified.setdefault(key, []).append(full_path)

    # 按 a-z 顺序整理字典
    sorted_keys = sorted([k for k in classified.keys() if k != '#']) + ['#']
    return {k: sorted(classified.get(k, [])) for k in sorted_keys}


if __name__ == '__main__':
    pass
