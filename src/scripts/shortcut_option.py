# -*- coding: UTF-8 -*-
"""
PROJECT_NAME QuickTray
PRODUCT_NAME PyCharm
NAME shortcut_option
AUTHOR Pfolg
TIME 2025/8/1 19:23
"""
import os
import sys

import win32com.client


def getDirName():
    # 判断是否打包环境
    if getattr(sys, 'frozen', False):
        base_path = os.path.dirname(sys.executable)  # exe所在目录
    else:
        base_path = os.path.dirname(__file__)  # 脚本所在目录

    return base_path


def getPath():
    if getattr(sys, 'frozen', False):
        return sys.executable  # exe所在目录
    else:
        return __file__  # 脚本所在目录


# 定义创建的函数
def makeShortcut(
        apppath, icoPath, workingDirectory,
        pathName, description="",
        arguments="", style=1):
    if pathName and apppath:
        try:
            # 创建WScript.Shell对象
            shell = win32com.client.Dispatch("WScript.Shell")

            # 指定快捷方式保存的位置和名称
            pathName = os.path.expandvars(pathName)
            icoPath = os.path.join(getDirName(), icoPath)
            # 删除可能存在的快捷方式
            if os.path.exists(pathName):
                os.remove(pathName)
            print(pathName)
            print(icoPath)

            # 创建快捷方式
            shortcut = shell.CreateShortcut(pathName)

            # 设置快捷方式的属性
            shortcut.TargetPath = apppath  # 应用程序路径
            shortcut.IconLocation = icoPath  # 图标路径
            shortcut.WindowStyle = style  # 1 表示正常窗口，其他值根据需要设置
            """
            "正常窗口（程序正常运行，窗口可见）": 1,
            "最小化窗口（程序运行，窗口最小化到任务栏）": 3,
            "最大化窗口（程序运行，窗口最大化）": 7
            """
            shortcut.Arguments = arguments  # 程序启动参数
            shortcut.Description = description  # 快捷方式描述
            shortcut.WorkingDirectory = workingDirectory  # 工作目录

            # 保存快捷方式
            shortcut.Save()
        except Exception as e:
            print("Error", str(e))
            print(str(e))

        if os.path.exists(pathName):
            print("tip", "success")
        else:
            print("tip", "fail")


def delete_shortcut(path):
    _msg = "success"
    path = os.path.expandvars(path)
    try:
        if os.path.exists(path):
            os.remove(path)
        else:
            _msg = "fail"
    except Exception as e:
        _msg = "fail" + "\n" + str(e)

    print("Tip", _msg)
