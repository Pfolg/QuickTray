# -*- coding: UTF-8 -*-
"""
PROJECT_NAME QuickTray
PRODUCT_NAME PyCharm
NAME searchbox
AUTHOR Pfolg
TIME 2025/8/19 11:03
"""
import urllib.parse
import webbrowser

from PySide6 import QtGui
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLineEdit

from .otherFunc import get_screen_info
from .string_data import Data


class SearchBox(QLineEdit):
    def __init__(self):
        super().__init__()
        self.init()

    def search_in_browser(self) -> None:
        visible = self.isVisible()
        query = self.text()
        if query and visible:
            # 使用必应中国作为搜索引擎
            bing = Data.bing
            # 使用bing搜索指定的查询
            search_url = bing.format(urllib.parse.quote(query))
            # 打开默认浏览器并导航到搜索URL
            webbrowser.open_new_tab(search_url)
        self.setText("")
        self.setVisible(False)

    def init(self) -> None:
        width, height = 700, 60
        screen_width, screen_height = get_screen_info()
        self.setGeometry(int((screen_width - width) / 2), int(screen_height / 2), width, height)
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool)
        self.setStyleSheet("""
                font-size: 24px;
                padding: 15px;
                border-radius: 60px;  # 加大圆角半径
                background: rgba(255, 255, 255, 0.2);
                border: 2px solid #c3daf8;
                """)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)  # 透明背景
        font = QtGui.QFont()
        font.setPointSize(18)
        self.setFont(font)
        # 提醒词
        self.setPlaceholderText("Enter...")
        # 初始不可见
        self.setVisible(False)
        self.returnPressed.connect(self.search_in_browser)

    # 重写关闭事件
    def closeEvent(self, event):
        self.hide()
        event.ignore()
