# -*- coding: UTF-8 -*-
"""
PROJECT_NAME QuickTray
PRODUCT_NAME PyCharm
NAME otherFunc
AUTHOR Pfolg
TIME 2025/8/19 11:24
"""
import os
import socket
import sys
import win32com.client
from PySide6.QtWidgets import QSystemTrayIcon, QApplication
import requests

from .string_data import Data, LanguageFormat


def get_screen_info() -> tuple:
    """读取屏幕长宽，用于窗口定位"""
    # 获取现有的 QApplication 实例
    _app = QApplication.instance()
    if _app is not None:
        # 获取显示器数据
        screen = _app.primaryScreen().geometry()
        # 返回长宽
        return screen.width(), screen.height()
    else:
        return 800, 600


def get_latest_github_version(owner, repo):
    """从GitHub API获取最新Release版本号"""
    url = f"https://api.github.com/repos/{owner}/{repo}/releases/latest"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()["tag_name"]
    except requests.exceptions.RequestException as e:
        raise Exception(f"GitHub API error: {str(e)}")


def check_version_match(local_ver):
    """主检查函数"""
    # 配置参数
    REPO_OWNER = "Pfolg"
    REPO_NAME = "QuickTray"

    try:
        remote_ver = get_latest_github_version(REPO_OWNER, REPO_NAME)
        if remote_ver == local_ver:
            print(f"✅ 版本一致 (本地: {local_ver}, GitHub: {remote_ver})")
            return True, f"当前版本 {remote_ver} 已是最新版！"
        else:
            print(f"❌ 版本不一致 (本地: {local_ver}, GitHub最新: {remote_ver})")
            return False, f"GitHub 最新发布 {remote_ver} \n当前 {local_ver}"

    except Exception as e:
        print(f"⚠️ 检查失败: {str(e)}")
        return False, str(e)


def getDirName() -> str:
    # 判断是否打包环境
    if getattr(sys, 'frozen', False):
        base_path = os.path.dirname(sys.executable)  # exe所在目录
    else:
        base_path = os.path.dirname(__file__)  # 脚本所在目录

    return base_path


def getPath() -> str:
    if getattr(sys, 'frozen', False):
        return sys.executable  # exe所在目录
    else:
        return __file__  # 脚本所在目录


# 定义创建的函数
def makeShortcut(
        tray: QSystemTrayIcon,
        language: LanguageFormat,
        apppath,
        icoPath,
        workingDirectory,
        pathName,
        description="",
        arguments="",
        style=1
) -> None:
    if pathName and apppath:
        try:
            # 创建WScript.Shell对象
            shell = win32com.client.Dispatch("WScript.Shell")

            # 指定快捷方式保存的位置和名称
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
            tray.showMessage("Error", str(e))
            print(str(e))

        if os.path.exists(pathName):
            tray.showMessage("tip", language.tip_create_shortcut_success)
        else:
            tray.showMessage("tip", language.tip_create_shortcut_fail)


def delete_shortcut(tray: QSystemTrayIcon, language: LanguageFormat, path: str) -> None:
    _msg = language.tip_delete_shortcut_success
    try:
        if os.path.exists(path):
            os.remove(path)
        else:
            _msg = language.tip_delete_shortcut_fail
    except Exception as e:
        _msg = language.tip_delete_shortcut_fail + "\n" + str(e)

    tray.showMessage("Tip", _msg)


def check_update(tray: QSystemTrayIcon) -> None:
    b, flag = check_version_match(Data.version)
    if b:
        tray.showMessage(
            Data.app_name,
            flag,
        )
    else:
        tray.showMessage(
            Data.app_name,
            flag,
        )


def single_instance(port: int, tray: QSystemTrayIcon) -> socket.socket:
    try:
        # 选择一个不常用的端口
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(("127.0.0.1", port))
    except socket.error:
        print("Another simple is running, quit")
        tray.showMessage(
            "Warning",
            f"port: {port} is using, maybe there is an instance running \nor change the port.")
        sys.exit()
    return sock
