# -*- coding: UTF-8 -*-
"""
PROJECT_NAME Python_projects
PRODUCT_NAME PyCharm
NAME main
AUTHOR Pfolg
TIME 2025/3/10 10:14
"""
import configparser
# 这个程序没有界面，只有托盘，界面--懒得做 2025/3/10
import json
import os.path
import sys
import threading
import time
import webbrowser

import psutil
import requests
from PySide6 import QtWidgets, QtGui
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QAction
from PySide6.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QWidget, QLabel, QPushButton


class MyQWidget(QWidget):
    def __init__(self):
        super().__init__()

    # 忽略关闭事件
    def closeEvent(self, event):
        event.ignore()


class MyQLabel(QLabel):
    def __init__(self):
        super().__init__()

    # 忽略关闭事件
    def closeEvent(self, event):
        event.ignore()


def set_QWidget(window: QWidget):
    # 设定窗口
    window.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
    # 窗口位置和大小
    window.setGeometry(1250, 720, 600, 100)
    # 定义标签和父级
    label1 = QLabel(parent=window)
    label2 = QLabel(parent=window)
    # 设置标签在Widget中位置
    label1.setGeometry(0, 0, 400, 50)
    label2.setGeometry(0, 20, 400, 50)
    # 设置样式
    label1.setStyleSheet("""
                background-color: rgba(0, 0, 0, 0);
                color: rgba(255, 255, 255, .7);
                font-size: 18px;
                """)  # font-weight: bold;
    label2.setStyleSheet("""
                background-color: rgba(0, 0, 0, 0);
                color: rgba(255, 255, 255, .7);
                font-size: 12px;
                """)
    font = QtGui.QFont()
    font.setFamily("Microsoft YaHei UI")
    font.setBold(False)
    label1.setFont(font)
    label2.setFont(font)
    # 设置文本
    label1.setText("Windows Hacked")
    label2.setText("Go to http://127.0.0.1/ to pay the ransom.")
    # 启用透明度
    window.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
    # 窗口顶置，去标题栏，去除任务栏图标
    window.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.Tool)


def textGetSet():
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

    print(sentence)
    TextLabel.setText(sentence)


def td_getText():
    while True:
        textGetSet()
        # 20min
        time.sleep(1200)


def set_QLabel(label: QLabel):
    # 设置位置和大小
    label.setGeometry(50, 50, 600, 540)
    label.setStyleSheet("""
                background-color: rgba(0, 0, 0, 0);
                color: rgba(255, 255, 255, .7);
                font-size: 18px;
                font-weight: bold;
                """)
    # 换行
    label.setWordWrap(True)
    sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
    label.setSizePolicy(sizePolicy)
    # 文本对齐方式
    label.setAlignment(Qt.AlignmentFlag.AlignLeading | Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
    # 启用透明度
    label.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
    # 去标题栏，去任务栏图标
    label.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Tool)


def td_autorun():
    if eval(appConfig.get("infor").get("autorun")):
        tray.tray_icon.showMessage(
            "Quick Tray",
            "辅助自启动 True Running",
            QIcon(appConfig.get("tray").get("logo")),
        )
        battery = psutil.sensors_battery()
        plugged = battery.power_plugged
        if plugged:
            data = tray.readSetting()
            # print(appConfig.get("infor").get("autorun"))
            for item in data:
                if "star" in item.get("type"):
                    p = item.get("path")
                    tray.openTarget(p)
                    time.sleep(3)
    else:
        tray.tray_icon.showMessage(
            "Quick Tray",
            "辅助自启动 False",
            QIcon(appConfig.get("tray").get("logo")),
        )


def open_ini():
    if not os.path.exists("config.ini"):
        setup_ini()
    os.startfile("config.ini")


class Tray:
    def __init__(self):
        self.tray_icon = QSystemTrayIcon()
        self.set_tray()
        self._addActions()
        self.tray_icon.show()

    @staticmethod
    def setting():
        _format = {
            "type": "",
            "name": "",
            "path": "",
            "icon": "",
        }
        if not os.path.exists("applist.json"):
            with open("applist.json", "w", encoding="utf-8") as file:
                json.dump([_format], file, indent=4, ensure_ascii=False)
        os.startfile("applist.json")

    @staticmethod
    def readSetting():
        if os.path.exists("applist.json"):
            with open("applist.json", "r", encoding="utf-8") as file:
                data: [] = json.load(file)
            if data:
                return data
            else:
                return []
        else:
            return []

    def openTarget(self, p: str):
        print("Will open", p)
        try:
            if os.path.exists(p):
                os.startfile(p)
            if p.split(":")[0] in ["http", "https"]:
                webbrowser.open(p)
        except Exception:
            self.tray_icon.showMessage("Error", "未能打开 {}".format(p))

    def _addActions(self):
        menu = QMenu()
        # 设定设置菜单
        menu_setting = QMenu()
        menu_setting.setTitle("set")
        menu_setting.setIcon(QIcon("assets/Tile_Folders/preferences/preferences-other.ico"))
        # 编辑json
        action_setting1 = QAction(parent=menu_setting)
        action_setting1.setText("editing in json")
        action_setting1.triggered.connect(self.setting)
        action_setting2 = QAction(parent=menu_setting)
        # 编辑ini
        action_setting2.setText("editing in ini")
        action_setting2.triggered.connect(open_ini)
        action_setting3 = QAction(parent=menu_setting)
        # 打开所在文件夹
        action_setting3.setText("program\'s folder")
        action_setting3.triggered.connect(lambda: os.startfile(os.getcwd()))
        menu_setting.addActions([action_setting1, action_setting2, action_setting3])

        action_quit = QAction(parent=menu)
        action_quit.setIcon(QIcon("assets/solid/power-off.svg"))
        action_quit.setText("quit")
        action_quit.triggered.connect(sys.exit)

        action_updateText = QAction(parent=menu)
        action_updateText.setIcon(QIcon("assets/Tile_Folders/preferences/preferences-desktop-search.ico"))
        action_updateText.setText("update text")
        action_updateText.triggered.connect(textGetSet)
        # 设定子菜单
        menus_infor = {
            "star": "assets/Tile_Folders/preferences/preferences-desktop-default-applications.ico",
            "app": "assets/Tile_Folders/categories/applications-all.ico",
            "link": "assets/Tile_Folders/categories/applications-internet.ico",
            "scripts": "assets/Tile_Folders/mimetypes/application-vnd.nokia.xml.qt.resource.ico",
        }
        children_icon = {
            "star": None,
            "app": None,
            "link": "assets/solid/arrow-up-right-from-square.svg",
            "scripts": "assets/solid/code.svg"
        }
        for i in menus_infor.keys():
            # 定义子菜单
            this_menu = QMenu()
            # 设置子菜单名称
            this_menu.setTitle(i)
            # 设置图标
            icon = menus_infor.get(i)
            this_menu.setIcon(QIcon(icon))
            # 更新子菜单字典信息
            menus_infor[i] = {
                "menu_icon": icon,
                "menu": this_menu,
                "children_icon": children_icon.get(i)
            }
            # 加入主菜单中
            menu.addMenu(this_menu)

        # 添加分割线
        menu.addSeparator()
        # 添加设置菜单
        menu.addMenu(menu_setting)
        # 添加基本动作
        menu.addActions([action_updateText, action_quit])
        data = self.readSetting()
        # 排序
        data.reverse()
        if data:
            for i in data:
                action = QAction()
                action_type, action_name, action_path, action_icon = i.get("type"), i.get("name"), i.get("path"), i.get(
                    "icon")
                # print(action_name, action_path, action_icon)
                if action_name:
                    action.setText(action_name)
                if action_path:
                    # 通过默认参数传递当前值 c，解决作用域问题——by DeepSeek
                    action.triggered.connect(lambda checked, p=action_path: self.openTarget(p))
                for m in menus_infor.keys():
                    if m in action_type:
                        tm = menus_infor.get(m).get("menu")
                        action.setParent(tm)
                        tm.addAction(action)
                        if menus_infor.get(m).get("children_icon"):
                            action.setIcon(QIcon(menus_infor.get(m).get("children_icon")))
                if action_icon:
                    action.setIcon(QIcon(action_icon))
        self.tray_icon.setContextMenu(menu)

    def set_tray(self):
        self.tray_icon.setToolTip(appConfig.get("tray").get("tip"))
        self.tray_icon.setIcon(QIcon(appConfig.get("tray").get("logo")))


def read_ini():
    this_config = {}
    if os.path.exists("config.ini"):
        config = configparser.ConfigParser()
        config.read('config.ini')
        # 读取所有配置
        for section in config.sections():
            this_section = {}
            for key in config[section]:
                this_section[key] = config[section][key]
            this_config[section] = this_section
        print(this_config)
        if not this_config:
            print("your config is empty, rewrite……")
            config["tray"] = {
                "tip": "QkStart With WaterMark",
                "logo": "assets/snowflake.png"
            }
            config["infor"] = {
                "usecount": "0",
                "autorun": False,
            }
            this_config = {
                'tray': {'tip': 'QkStart With WaterMark', 'logo': 'assets/snowflake.png'},
                'infor': {'usecount': '0', "autorun": False, }}

        config["infor"]["useCount"] = str(eval(config["infor"]["useCount"]) + 1)
        with open('config.ini', 'w', encoding="utf-8") as file:
            config.write(file)
            print("config.ini Changed!")
        return this_config
    else:
        setup_ini()
        return {'tray': {'tip': 'QkStart With WaterMark', 'logo': 'assets/snowflake.png'},
                'infor': {'usecount': '0', "autorun": False, }}


def setup_ini():
    config = configparser.ConfigParser()
    config["tray"] = {
        "tip": "QkStart With WaterMark",
        "logo": "assets/snowflake.png"
    }
    config["infor"] = {
        "usecount": "0",
        "autorun": False,
    }
    with open('config.ini', 'w', encoding="utf-8") as file:
        config.write(file)


if __name__ == '__main__':
    appConfig = read_ini()
    app = QApplication(sys.argv)
    tray = Tray()
    # 右下角标签
    Widget = MyQWidget()
    set_QWidget(Widget)
    Widget.show()

    # 左上角句子
    TextLabel = MyQLabel()
    set_QLabel(TextLabel)
    TextLabel.show()
    TextLabel.setText("正在初始化……")
    threading.Thread(target=td_autorun, daemon=True).start()
    threading.Thread(target=td_getText, daemon=True).start()

    sys.exit(app.exec())
