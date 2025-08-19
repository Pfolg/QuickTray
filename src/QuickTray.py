# -*- coding: UTF-8 -*-
"""
PROJECT_NAME Python_projects
PRODUCT_NAME PyCharm
NAME main
AUTHOR Pfolg
TIME 2025/3/10 10:14
"""
import os.path
import sys

import pyperclip
from PySide6.QtCore import QTimer
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication

from Extend.string_data import Data, getLanguage
from Extend.searchbox import SearchBox
from Extend.beautifulSentence import BeautifulSentence
from Extend.config_json import read_config_json
from Extend.otherFunc import single_instance
from Extend.tray import Tray

if __name__ == '__main__':
    config_file = Data.config_file
    lines_file = Data.lines_file
    appList_file = Data.appList_file
    if not os.path.exists(Data.user_folder):
        os.mkdir(Data.user_folder)
    # 是否正在测试
    isTest = True
    # 读取配置
    appConfig = read_config_json(config_file)
    # 设定语言
    app_language = getLanguage(appConfig.get("language"))
    # 初始化app
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(appConfig.get("logo")))
    # 初始化托盘
    tray = Tray(
        language=app_language,
        config_file=config_file,
        config=appConfig,
        appList_file=appList_file
    )
    # 搜索框
    searchBox = SearchBox()
    # 左上角句子
    TextLabel = BeautifulSentence(lines_file)
    TextLabel.show()
    TextLabel.setText("Quick Tray is running.")
    ### 链接动作
    # 更新标签
    tray.action_updateText.triggered.connect(lambda: TextLabel.textGetSet())
    # 复制文本
    tray.action_copyText.triggered.connect(lambda: pyperclip.copy(TextLabel.text()))
    # 编辑内容
    tray.action_editText.triggered.connect(lambda: tray.openTarget(lines_file))
    # 搜索框
    tray.action_search.triggered.connect(lambda: searchBox.show())

    # 设置线程
    time1 = QTimer()
    time1.timeout.connect(tray.td_autorun)
    time1.setSingleShot(True)  # 单次触发

    time2 = QTimer()
    time2.timeout.connect(lambda: TextLabel.textGetSet())
    if not isTest:
        time1.start(3000)  # 3s
        TextLabel.textGetSet()  # 手动调用
        time2.start(30000)  # 5min
        # 占用端口以识别单个实例
        lock_socket = single_instance(appConfig.get("port"), tray)
    sys.exit(app.exec())
    # "pyinstaller.exe -F -w -i .\assets\luabackend.ico .\QuickTray.py"
