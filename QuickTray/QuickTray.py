# -*- coding: UTF-8 -*-
"""
PROJECT_NAME Python_projects
PRODUCT_NAME PyCharm
NAME main
AUTHOR Pfolg
TIME 2025/3/10 10:14
"""
# 这个程序没有界面，只有托盘，界面--懒得做 2025/3/10
import json
import os.path
import random
import socket
import sys
import time
import urllib.parse
import webbrowser

import psutil
from PySide6 import QtWidgets, QtGui
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QIcon, QAction
from PySide6.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QWidget, QLabel, QLineEdit

from get_windows_menus import *


class MyQWidget(QWidget):
    def __init__(self):
        super().__init__()

    # 忽略关闭事件
    def closeEvent(self, event):
        event.ignore()


class MyQLineEdit(QLineEdit):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("""
        font-size: 24px;
        padding: 15px;
        border-radius: 60px;  # 加大圆角半径
        background: rgba(255, 255, 255, 0.2);
        border: 2px solid #c3daf8;
        """)

    # 忽略关闭事件
    def closeEvent(self, event):
        self.hide()
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
    # 窗口顶置，去标题栏，去除任务栏图标，鼠标穿透
    window.setWindowFlags(
        Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.Tool | Qt.WindowType.WindowTransparentForInput)


def textGetSet():
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
    if os.path.exists(lines_file):
        with open(lines_file, "r", encoding="utf-8") as file:
            content: list = json.load(file)

        sentence = content[random.randint(0, len(content))]
    else:
        sentence = "Wish you hava a good day!"
    print(sentence)
    TextLabel.setText(sentence)


def set_QLabel(label: QLabel):
    # 设置位置和大小
    label.setGeometry(50, 50, 600, 540)
    label.setStyleSheet("""
                background-color: rgba(0, 0, 0, 0);
                color: rgba(255, 255, 255, .7);
                font-size: 18px;
                font-weight: bold;
                """)
    # 定义字体
    font = QtGui.QFont()
    font.setFamily("Maple Mono NF CN")
    font.setBold(True)  # 加粗
    font.setItalic(True)  # 倾斜
    label.setFont(font)
    # 换行
    label.setWordWrap(True)
    sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
    label.setSizePolicy(sizePolicy)
    # 文本对齐方式
    label.setAlignment(Qt.AlignmentFlag.AlignLeading | Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
    # 启用透明度
    label.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
    # 去标题栏，去任务栏图标，鼠标穿透
    label.setWindowFlags(
        Qt.WindowType.FramelessWindowHint | Qt.WindowType.Tool | Qt.WindowType.WindowTransparentForInput)


def td_autorun():
    if appConfig.get("autorun"):
        tray.tray_icon.showMessage(
            "Quick Tray",
            "辅助自启动 True Running",
            QIcon(appConfig.get("logo")),
        )
        battery = psutil.sensors_battery()
        plugged = battery.power_plugged
        if plugged:
            data = tray.readSetting()
            for item in data:
                if "star" in item.get("type"):
                    p = item.get("path")
                    tray.openTarget(p)
                    time.sleep(3)
    else:
        tray.tray_icon.showMessage(
            "Quick Tray",
            "辅助自启动 False",
            QIcon(appConfig.get("logo")),
        )


def search_in_browser(box: QLineEdit):
    visible = box.isVisible()
    query = box.text()
    if query and visible:
        # 使用必应中国作为搜索引擎
        bing = "https://cn.bing.com/search?q={}"
        # 使用bing搜索指定的查询
        search_url = bing.format(urllib.parse.quote(query))
        # 打开默认浏览器并导航到搜索URL
        webbrowser.open_new_tab(search_url)
    box.setText("")
    box.setVisible(False)


def set_searchBox(box: QLineEdit):
    box.setGeometry(500, 500, 500, 60)
    box.setWindowFlags(
        Qt.WindowType.FramelessWindowHint |
        Qt.WindowType.WindowStaysOnTopHint |
        Qt.WindowType.Tool)
    box.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)  # 透明背景
    font = QtGui.QFont()
    font.setPointSize(18)
    box.setFont(font)
    # 提醒词
    box.setPlaceholderText("Enter...")
    # 初始不可见
    box.setVisible(False)
    box.returnPressed.connect(lambda: search_in_browser(box))


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
        if not os.path.exists(appList_file):
            with open(appList_file, "w", encoding="utf-8") as file:
                json.dump([_format], file, indent=4, ensure_ascii=False)
        os.startfile(appList_file)

    @staticmethod
    def readSetting():
        if os.path.exists(appList_file):
            with open(appList_file, "r", encoding="utf-8") as file:
                data: list = json.load(file)
            if data:
                return sorted(data, key=lambda x: x["name"].lower(), reverse=True)
            else:
                return []
        else:
            return []

    def openTarget(self, p: str):
        if p:
            print("Will open", p)
            try:
                if os.path.exists(p):
                    os.startfile(p)
                elif p.split(":")[0] in ["http", "https"]:
                    webbrowser.open(p)
                elif not os.path.exists(p) and p.split(":") not in ["http", "https"]:
                    self.tray_icon.showMessage("Warning", f"未能打开 {p}，因为文件不存在。")
                else:
                    self.tray_icon.showMessage("Warning", f"未能打开{p}，未知的问题。")
            except Exception as _evt:
                self.tray_icon.showMessage("Error", f"未能打开 {p}，详情：{_evt}")

    def set_windows_menu(self, father_menu: QMenu):
        # windows菜单内容
        target_dir = os.path.expandvars(r'%ProgramData%\Microsoft\Windows\Start Menu\Programs')
        windows_menus = get_lnk_classified_dict(target_dir)
        menu_windows = QMenu(parent=father_menu)
        menu_windows.setTitle("Windows Menu")
        menu_windows.setIcon(QIcon("assets/windows.png"))
        for key in windows_menus:
            this_menu = QMenu()
            this_menu.setTitle(key)
            for item in windows_menus.get(key):
                this_action = QAction(parent=this_menu)
                this_action.setText(get_lnk_pure_name(item))
                this_action.triggered.connect(lambda checked, p=item: self.openTarget(p))
                this_menu.addAction(this_action)
            menu_windows.addMenu(this_menu)
        father_menu.addMenu(menu_windows)

    def _addActions(self):
        menu = QMenu()
        # 设定设置菜单
        menu_setting = QMenu()
        menu_setting.setTitle("set")
        menu_setting.setIcon(QIcon("assets/Tile_Folders/preferences/preferences-other.ico"))
        # 编辑json
        action_setting1 = QAction(parent=menu_setting)
        action_setting1.setText("Editing menus")
        action_setting1.triggered.connect(self.setting)
        # 编辑ini
        action_setting2 = QAction(parent=menu_setting)
        action_setting2.setText("Editing setting")
        action_setting2.triggered.connect(open_basic_json)
        # 打开所在文件夹
        action_setting3 = QAction(parent=menu_setting)
        action_setting3.setText("Program\'s folder")
        action_setting3.triggered.connect(lambda: os.startfile(os.getcwd()))
        # 刷新菜单
        action_setting4 = QAction(parent=menu_setting)
        action_setting4.setText("Update menus")
        action_setting4.triggered.connect(self._addActions)

        menu_setting.addActions([action_setting4, action_setting3, action_setting2, action_setting1])

        action_quit = QAction(parent=menu)
        action_quit.setIcon(QIcon("assets/solid/power-off.svg"))
        action_quit.setText("quit")
        action_quit.triggered.connect(sys.exit)

        action_updateText = QAction(parent=menu)
        action_updateText.setIcon(QIcon("assets/solid/heading.svg"))
        action_updateText.setText("update text")
        action_updateText.triggered.connect(textGetSet)

        # 加入搜索动作
        action_search = QAction(parent=menu)
        action_search.setText("Search")
        action_search.setIcon(QIcon("assets/Tile_Folders/preferences/preferences-desktop-search.ico"))
        action_search.triggered.connect(lambda: searchBox.show())
        menu.addAction(action_search)
        menu.addSeparator()
        # 设定Windows应用菜单
        # self.set_windows_menu(father_menu=menu)
        # 设定子菜单
        menus_info = {
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
        _menu_info = {}
        for i in menus_info.keys():
            # 定义子菜单
            this_menu = QMenu()
            # 设置子菜单名称
            this_menu.setTitle(i)
            # 设置图标
            icon = menus_info.get(i)
            this_menu.setIcon(QIcon(icon))
            # 更新子菜单字典信息
            _menu_info[i] = {
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
                if action_type and action_name and action_path:
                    # print(action_name, action_path, action_icon)
                    if action_name:
                        action.setText(action_name)
                    if action_path:
                        # 通过默认参数传递当前值 c，解决作用域问题——by DeepSeek
                        action.triggered.connect(lambda checked, p=action_path: self.openTarget(p))
                    for m in _menu_info.keys():
                        if m in action_type:
                            tm = _menu_info.get(m).get("menu")
                            action.setParent(tm)
                            tm.addAction(action)
                            if _menu_info.get(m).get("children_icon"):
                                action.setIcon(QIcon(_menu_info.get(m).get("children_icon")))
                    if action_icon:
                        action.setIcon(QIcon(action_icon))
        self.tray_icon.setContextMenu(menu)

    def set_tray(self):
        self.tray_icon.setToolTip(f"{appConfig.get('tip')} ver{appConfig.get('version')}")
        self.tray_icon.setIcon(QIcon(appConfig.get("logo")))


def single_instance(port: int):
    print("checking port")
    try:
        # 选择一个不常用的端口
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(("127.0.0.1", port))
    except socket.error:
        print("Another simple is running, quit")
        tray.tray_icon.showMessage(
            "Warning",
            f"port: {port} is using, maybe there is an instance running \nor change the port.")
        sys.exit()
    return sock


def open_basic_json():
    if not os.path.exists(config_file):
        setup_config_json()
    os.startfile(config_file)


def read_config_json() -> dict:
    if os.path.exists(config_file):
        with open(config_file, "r", encoding="utf-8") as file1:
            config: dict = json.load(file1)
        if not config:
            print("your config is empty, rewrite……")
            config = setup_config_json()
        config["usecount"] += 1
        with open(config_file, "w", encoding="utf-8") as file2:
            json.dump(config, file2, indent=4, ensure_ascii=False)
        print("config Changed!")
        return config
    else:
        return setup_config_json()


def setup_config_json() -> dict:
    config = {
        "tip": "Quick Tray",
        "version": version,
        "logo": "assets\luabackend.ico",
        "usecount": 0,
        "port": 20082,
        "autorun": True,
    }
    with open(config_file, "w", encoding="utf-8") as file:
        json.dump(config, file, ensure_ascii=False, indent=4)
    return config


if __name__ == '__main__':
    version = "1.11.0-25614"
    config_file = "app_config/basic_config.json"
    lines_file = "app_config/lines.json"
    appList_file = "app_config/applist.json"
    # 读取配置
    appConfig = read_config_json()

    app = QApplication(sys.argv)
    tray = Tray()

    # 右下角标签
    # Widget = MyQWidget()
    # set_QWidget(Widget)
    # Widget.show()

    # 搜索框
    searchBox = MyQLineEdit()
    set_searchBox(searchBox)
    # 左上角句子
    TextLabel = MyQLabel()
    set_QLabel(TextLabel)
    TextLabel.show()
    TextLabel.setText("正在初始化……")
    # 设置线程
    time1 = QTimer()
    time1.timeout.connect(td_autorun)
    time1.setSingleShot(True)  # 单次触发
    time1.start(3000)

    time2 = QTimer()
    time2.timeout.connect(textGetSet)
    textGetSet()  # 手动调用
    time2.start(5 * 60 * 1000)

    # 占用端口以识别单个实例
    lock_socket = single_instance(appConfig.get("port"))
    sys.exit(app.exec())
    # "pyinstaller.exe -F -w -i .\assets\luabackend.ico .\QuickTray.py"
