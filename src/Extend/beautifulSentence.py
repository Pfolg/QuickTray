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

from PySide6 import QtGui
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QVBoxLayout, QHBoxLayout, QWidget, QSizePolicy
from .string_data import Data
from .otherFunc import get_screen_info


class BeautifulSentence(QWidget):
    def __init__(self, lines_file):
        super().__init__()
        self.lines_file = lines_file
        self.label = QLabel(self)
        self.max_width = 0
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
        # 2. 创建字体度量对象
        font_metrics = QtGui.QFontMetrics(self.label.font())
        # 3. 计算原始文本宽度
        text_width = font_metrics.horizontalAdvance(sentence)
        # 动态宽度
        if text_width <= self.max_width:
            self.label.setMinimumWidth(text_width)
        else:
            self.label.setMinimumWidth(self.max_width)
        print(sentence)
        self.label.setText(sentence)

    def init(self) -> None:
        # 设置位置和大小
        sw, sh = get_screen_info()
        self.max_width, height = int(sw / 2.5), int(sh / 1.4)
        self.setGeometry(50, 50, self.max_width, height)
        self.label.setMaximumWidth(self.max_width)

        main_layout = QVBoxLayout(self)
        # 上方空白
        main_layout.addStretch(0)
        # 水平布局容器
        h_container = QHBoxLayout()
        # 左侧空白
        h_container.addStretch(0)

        # 文字容器
        text_layout = QVBoxLayout()
        text_layout.addWidget(self.label)
        h_container.addLayout(text_layout)

        # 右侧空白
        h_container.addStretch(1)

        # 添加水平容器到主布局
        main_layout.addLayout(h_container)

        # 下方空白
        main_layout.addStretch(1)

        self.label.setStyleSheet("""
                    background-color: rgba(0, 0, 0, 60);
                    color: rgba(255, 255, 255, .7);
                    font-size: 20px;
                    """)
        # 定义字体
        font = QtGui.QFont()
        font.setFamily(Data.font_mmnc)
        font.setBold(True)  # 加粗
        font.setItalic(True)  # 倾斜
        self.label.setFont(font)
        # 换行
        sizePolicy = QSizePolicy(
            QSizePolicy.Policy.Preferred,  # 水平方向扩展
            QSizePolicy.Policy.Preferred  # 垂直方向根据内容调整
        )
        sizePolicy.setHeightForWidth(True)  # 高度可以根据宽度调整
        self.label.setSizePolicy(sizePolicy)
        self.label.setWordWrap(True)  # 换行

        # 启用透明度
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        # 去标题栏，去任务栏图标，鼠标穿透
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.ToolTip |
            Qt.WindowType.WindowTransparentForInput |
            Qt.WindowType.WindowStaysOnBottomHint
        )

    # 忽略关闭事件
    def closeEvent(self, event):
        event.ignore()
