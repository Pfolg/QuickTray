# -*- coding: UTF-8 -*-
"""
PROJECT_NAME QuickTray
PRODUCT_NAME PyCharm
NAME beautifulSentence
AUTHOR Pfolg
TIME 2025/8/19 11:15
"""
import json
import os
import random

from PySide6 import QtWidgets, QtGui
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel
from .string_data import Data


class BeautifulSentence(QLabel):
    def __init__(self,lines_file):
        super().__init__()
        self.lines_file=lines_file
        self.init()

    def textGetSet(self) -> None:
        """
        # https://v1.hitokoto.cn/?c=a&c=g&c=b&c=d&c=i&c=j&c=k
        # url = "https://v1.hitokoto.cn/"
        url = "https://animechan.io/api/v1/quotes/random"
        try:
            content = requests.get(url)
            print(content.status_code)
            if content.status_code == 200:
                print(content.json())
                sentence = content.json().get("data").get("content")
            else:
                sentence = "status_code={}，请求失败".format(content.status_code)
            # 记录日志
            with open("request.log", "a", encoding="utf-8") as file:
                file.write(f'{time.strftime("%Y/%m/%d %H:%M:%S")}->{content.text}\n')
        except NameError:
            sentence = "可能频繁的请求，请求失败"
        except requests.exceptions.ConnectionError:
            sentence = "网络连接问题，请求失败"
        except Exception:
            sentence = "未知问题，请求失败"
            """
        if os.path.exists(self.lines_file):
            with open(self.lines_file, "r", encoding="utf-8") as file:
                content: list = json.load(file)

            sentence = content[random.randint(0, len(content))]
        else:
            sentence = "Quick Tray is running."
        print(sentence)
        self.setText(sentence)

    def init(self) -> None:
        # 设置位置和大小
        self.setGeometry(50, 50, 600, 540)
        self.setStyleSheet("""
                    background-color: rgba(0, 0, 0, 0);
                    color: rgba(255, 255, 255, .7);
                    font-size: 18px;
                    font-weight: bold;
                    """)
        # 定义字体
        font = QtGui.QFont()
        font.setFamily(Data.font_mmnc)
        font.setBold(True)  # 加粗
        font.setItalic(True)  # 倾斜
        self.setFont(font)
        # 换行
        self.setWordWrap(True)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding
        )
        self.setSizePolicy(sizePolicy)
        # 文本对齐方式
        self.setAlignment(Qt.AlignmentFlag.AlignLeading | Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        # 启用透明度
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        # 去标题栏，去任务栏图标，鼠标穿透
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint | Qt.WindowType.ToolTip | Qt.WindowType.WindowTransparentForInput | Qt.WindowType.WindowStaysOnBottomHint)

    # 忽略关闭事件
    def closeEvent(self, event):
        event.ignore()