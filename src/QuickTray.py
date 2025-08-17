# -*- coding: UTF-8 -*-
"""
PROJECT_NAME Python_projects
PRODUCT_NAME PyCharm
NAME main
AUTHOR Pfolg
TIME 2025/3/10 10:14
"""
import json
import os.path
import random
import socket
import sys
import time
import urllib.parse
import webbrowser
import pyperclip
import psutil
from PySide6 import QtWidgets, QtGui
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QIcon, QAction
from PySide6.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QLabel, QLineEdit
import win32com.client
from Extend.QuickTrayExtend import EWidget
from Extend.check_version import check_version_match
from Extend.string_data import Data, getLanguage


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
        self.setGeometry(500, 500, 500, 60)
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
        self.setPlaceholderText(app_language.input_placeholder)
        # 初始不可见
        self.setVisible(False)
        self.returnPressed.connect(self.search_in_browser)

    # 忽略关闭事件
    def closeEvent(self, event):
        self.hide()
        event.ignore()


class BeautifulSentence(QLabel):
    def __init__(self):
        super().__init__()
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
        if os.path.exists(lines_file):
            with open(lines_file, "r", encoding="utf-8") as file:
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


class Tray(QSystemTrayIcon):
    def __init__(self):
        super().__init__()
        self.menu_setting = QMenu()
        self.language = app_language
        self.childMenus = {}
        # 报时
        self.hourTimer = QTimer()
        self.lastMin = ""
        self.isHourAlarm = appConfig.get("hourAlarm")
        self.hourTimer.timeout.connect(self.hourAlarm)
        # 设定窗口
        self.action_setting0 = QAction(parent=self.menu_setting)
        # 编辑menu-json
        self.action_setting1 = QAction(parent=self.menu_setting)
        # 编辑setting-json
        self.action_setting2 = QAction(parent=self.menu_setting)
        # 打开所在文件夹
        self.action_setting3 = QAction(parent=self.menu_setting)
        # 刷新菜单
        self.action_setting4 = QAction(parent=self.menu_setting)
        # 改变语言
        self.change_language = QMenu()
        self.language_en = QAction(parent=self.change_language)
        self.language_zh = QAction(parent=self.change_language)
        # 自启动
        self.self_start = QAction()

        self.action_quit = QAction()
        # 关于：官网，更新
        self.menu_about = QMenu()
        self.action_update = QAction(parent=self.menu_about)
        self.action_website = QAction(parent=self.menu_about)
        # 文字标签菜单
        self.menu_text = QMenu()
        self.action_updateText = QAction(parent=self.menu_text)
        self.action_copyText = QAction(self.menu_text)
        self.action_editText = QAction(self.menu_text)
        # 加入搜索动作
        self.action_search = QAction()

        self.__bind_functions()
        self.hot_boot()
        self.hourTimer.start(1000)
        self.show()

    def hourAlarm(self) -> None:
        if not self.isHourAlarm and self.hourTimer:
            self.hourTimer.stop()
            self.hourTimer = None
            return
        now = time.strftime("%H:%M")
        if now.split(":")[1] == "00" and now != self.lastMin:
            self.lastMin = now
            self.showMessage(
                "Hour Alarm",
                self.language.tip_hour_alarm + now
            )

    def hot_boot(self):
        menu = self._addActions()
        self.setContextMenu(menu)
        self.set_tray()
        self.setMenuLanguage()

    def changeMenuLanguage(self, mark: str):
        self.language = getLanguage(mark)
        write_config_json("language", mark)
        self.setMenuLanguage()
        self.showMessage(
            "Tip",
            self.language.language_changed_tip
        )

    def shortcut_option(self):
        if self.self_start.text() == self.language.self_start_off:
            makeShortcut(
                apppath=getPath(),
                icoPath=appConfig.get("logo"),
                workingDirectory=getDirName(),
                pathName=Data.start_link
            )
        else:
            delete_shortcut(Data.start_link)

        self.self_start.setText(self.language.self_start_on if os.path.exists(
            Data.start_link) else self.language.self_start_off)

    def setMenuLanguage(self) -> None:
        """设置语言和切换语言"""
        self.menu_setting.setTitle(self.language.string_setting)
        self.action_setting0.setText(self.language.string_settingw)
        self.action_setting1.setText(self.language.string_e_menu)
        self.action_setting2.setText(self.language.string_e_setting)
        self.action_setting3.setText(self.language.string_folder_program)
        self.action_setting4.setText(self.language.string_u_menu)
        self.change_language.setTitle(self.language.string_change_language)
        self.language_en.setText(self.language.language_en)
        self.language_zh.setText(self.language.language_zh)
        self.action_quit.setText(self.language.string_quit)
        self.menu_about.setTitle(self.language.string_about)
        self.action_update.setText(self.language.string_c_update)
        self.action_website.setText(self.language.string_github)
        self.menu_text.setTitle(self.language.string_text)
        self.action_updateText.setText(self.language.string_update)
        self.action_copyText.setText(self.language.string_copy)
        self.action_editText.setText(self.language.string_edit)
        self.action_search.setText(self.language.string_search)
        for k, v in self.childMenus.items():
            v.setTitle(self.language.children_menu.get(k))
        self.self_start.setText(self.language.self_start_on if os.path.exists(
            os.path.expandvars(Data.start_link)) else self.language.self_start_off)

    def __bind_functions(self) -> None:
        # 设定窗口
        self.action_setting0.triggered.connect(lambda: EWidget().show())
        # 编辑menu-json
        self.action_setting1.triggered.connect(self.setting)
        # 编辑setting-json
        self.action_setting2.triggered.connect(lambda: self.openTarget(config_file))
        # 打开所在文件夹
        self.action_setting3.triggered.connect(lambda: os.startfile(getDirName()))
        # 刷新菜单
        self.action_setting4.triggered.connect(self.hot_boot)
        # ---------
        self.language_en.triggered.connect(lambda: self.changeMenuLanguage("en"))
        self.language_zh.triggered.connect(lambda: self.changeMenuLanguage("zh"))
        # ---------
        # 操作快捷方式
        self.self_start.triggered.connect(self.shortcut_option)
        self.action_quit.triggered.connect(sys.exit)
        self.action_update.triggered.connect(check_update)
        self.action_website.triggered.connect(lambda: self.openTarget(Data.website))
        # 更新标签
        self.action_updateText.triggered.connect(lambda: TextLabel.textGetSet())
        # 复制文本
        self.action_copyText.triggered.connect(lambda: pyperclip.copy(TextLabel.text()))
        # 编辑内容
        self.action_editText.triggered.connect(lambda: self.openTarget(lines_file))
        # ---------
        self.action_search.triggered.connect(lambda: searchBox.show())

    def _addActions(self) -> QMenu:
        menu = QMenu()
        # 设定设置菜单
        self.menu_setting.setIcon(QIcon(Data.picture_preferences_other))
        # ---------
        self.action_quit.setParent(menu)
        self.action_quit.setIcon(QIcon(Data.picture_power_off))
        # ---------
        # 关于：官网，更新
        self.menu_about.setIcon(QIcon(Data.picture_circle_question))
        self.action_update.setIcon(QIcon(Data.picture_circle_exclamation))
        self.action_website.setIcon(QIcon(Data.picture_github))
        # ---------
        # 文字标签菜单
        self.menu_text.setIcon(QIcon(Data.picture_heading))
        # 加入搜索动作
        self.action_search.setParent(menu)
        self.action_search.setIcon(QIcon(Data.picture_search))

        self.change_language.addActions([self.language_en, self.language_zh])
        self.menu_setting.addActions([
            self.action_setting0, self.action_setting4, self.action_setting3, self.action_setting2,
            self.action_setting1, self.self_start])
        self.menu_setting.addMenu(self.change_language)
        self.menu_about.addActions([self.action_website, self.action_update])
        self.menu_text.addActions([self.action_updateText, self.action_copyText, self.action_editText])
        menu.addAction(self.action_search)
        menu.addSeparator()
        # ---------
        self.update_child_menus()
        for i in self.childMenus.values():
            menu.addMenu(i)
        # ---------
        # 添加分割线
        menu.addSeparator()
        # 添加设置菜单
        menu.addMenu(self.menu_setting)
        # 添加文字标签菜单
        menu.addMenu(self.menu_text)
        # 添加关于菜单
        menu.addMenu(self.menu_about)
        # 添加基本动作
        menu.addActions([self.action_quit])
        print("menu set.")
        return menu

    def update_child_menus(self) -> None:
        # 设定子菜单
        menus_info = {
            "star": Data.picture_star,
            "app": Data.picture_app,
            "link": Data.picture_link,
            "scripts": Data.picture_scripts,
        }
        children_icon = {
            "star": Data.picture_c_star,
            "app": Data.picture_c_app,
            "link": Data.picture_c_link,
            "scripts": Data.picture_c_scripts
        }
        _menu_info = {}
        for i in menus_info.keys():
            # 定义子菜单
            this_menu = QMenu()
            # 设置子菜单名称
            this_menu.setTitle(self.language.children_menu.get(i))
            # 设置图标
            icon = menus_info.get(i)
            this_menu.setIcon(QIcon(icon))
            # 更新子菜单字典信息
            _menu_info[i] = {
                "menu_icon": icon,
                "menu": this_menu,
                "children_icon": children_icon.get(i)
            }
            # 保存引用
            self.childMenus[i] = this_menu
        data = self.readSetting()
        # 排序
        data.reverse()
        if data:
            for i in data:
                action = QAction()
                action_type = i.get("type")
                action_name = i.get("name")
                action_path = i.get("path")
                action_icon = i.get("icon")
                if action_type and action_name and action_path:
                    # print(action_name, action_path, action_icon)
                    action.setText(action_name)
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

    @staticmethod
    def setting() -> None:
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
    def readSetting() -> list:
        if os.path.exists(appList_file):
            with open(appList_file, "r", encoding="utf-8") as file:
                data: list = json.load(file)
            if data:
                return sorted(data, key=lambda x: x["name"].lower(), reverse=True)
            else:
                return []
        else:
            return []

    def openTarget(self, p: str) -> None:
        if p:
            print("Will open", p)
            try:
                if os.path.exists(p):
                    if p.split(".")[-1] == "py":
                        os.startfile("python.exe", arguments=p)
                    elif p.split(".")[-1] == "pyw":
                        os.startfile("pythonw.exe", arguments=p)
                    else:
                        os.startfile(p)
                elif p.split(":")[0] in ["http", "https"]:
                    webbrowser.open(p)
                elif not os.path.exists(p) and p.split(":") not in ["http", "https"]:
                    self.showMessage(
                        "Warning",
                        self.language.failed_open_file + p)
                else:
                    self.showMessage("Warning", self.language.unknown_error + p)
            except Exception as _evt:
                self.showMessage("Error", self.language.unable_open_file + p + str(_evt))

    def set_tray(self) -> None:
        item_num = len(self.readSetting())
        info = (
            f"{appConfig.get('tip')} "
            f"{Data.version}\n"
            f"{Data.s_tool_Items} {item_num}\n"
            f"Autorun: {appConfig.get('autorun')}\n"
            f"HourAlarm: {appConfig.get('hourAlarm')}"
        )
        self.setToolTip(info)
        self.setIcon(QIcon(appConfig.get("logo")))


def td_autorun() -> None:
    if appConfig.get("autorun"):
        battery = psutil.sensors_battery()
        plugged = battery.power_plugged
        if plugged:
            data = tray.readSetting()
            for item in data:
                if "star" in item.get("type"):
                    p = item.get("path")
                    tray.openTarget(p)
                    time.sleep(3)


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
        apppath, icoPath, workingDirectory,
        pathName, description="",
        arguments="", style=1) -> None:
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
            tray.showMessage("tip", app_language.tip_create_shortcut_success)
        else:
            tray.showMessage("tip", app_language.tip_create_shortcut_fail)


def delete_shortcut(path: str) -> None:
    _msg = app_language.tip_delete_shortcut_success
    try:
        if os.path.exists(path):
            os.remove(path)
        else:
            _msg = app_language.tip_delete_shortcut_fail
    except Exception as e:
        _msg = app_language.tip_delete_shortcut_fail + "\n" + str(e)

    tray.showMessage("Tip", _msg)


def check_update() -> None:
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


def read_config_json() -> dict:
    if os.path.exists(config_file):
        with open(config_file, "r", encoding="utf-8") as file1:
            config: dict = json.load(file1)
        if not config:
            print("your config is empty, rewrite……")
            config = setup_config_json()
        config["useCount"] += 1
        config["version"] = Data.version
        with open(config_file, "w", encoding="utf-8") as file2:
            json.dump(config, file2, indent=4, ensure_ascii=False)
        print("config Changed!")
        return config
    else:
        return setup_config_json()


def setup_config_json() -> dict:
    config = {
        "tip": Data.app_name,
        "version": Data.version,
        "logo": Data.picture_luabackend,
        "useCount": 0,
        "port": Data.port,
        "autorun": Data.isautorun,
        "language": "en",  # en zh
        "hourAlarm": False
    }
    with open(config_file, "w", encoding="utf-8") as file:
        json.dump(config, file, ensure_ascii=False, indent=4)
    return config


def write_config_json(key: str, value) -> None:
    if os.path.exists(config_file):
        try:
            with open(config_file, "r", encoding="utf-8") as f1:
                org: dict = json.load(f1)

            if org.get(key):
                # 使用isinstance会发生错误
                if type(value) == type(org.get(key)):
                    org[key] = value
                    with open(config_file, "w", encoding="utf-8") as f2:
                        json.dump(org, f2, indent=4, ensure_ascii=False)
                else:
                    print("instance is not suitable.")
        except Exception as e:
            print("an error happened in writing config: ", e)
            setup_config_json()
    else:
        setup_config_json()


def single_instance(port: int) -> socket.socket:
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


if __name__ == '__main__':
    config_file = Data.config_file
    lines_file = Data.lines_file
    appList_file = Data.appList_file
    if not os.path.exists(Data.user_folder):
        os.mkdir(Data.user_folder)
    # 是否正在测试
    isTest = True
    # 读取配置
    appConfig = read_config_json()
    # 设定语言
    app_language = getLanguage(appConfig.get("language"))

    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(appConfig.get("logo")))
    tray = Tray()

    # 搜索框
    searchBox = SearchBox()
    # 左上角句子
    TextLabel = BeautifulSentence()
    TextLabel.show()
    TextLabel.setText("Quick Tray is running.")
    # 设置线程
    time1 = QTimer()
    time1.timeout.connect(td_autorun)
    time1.setSingleShot(True)  # 单次触发

    time2 = QTimer()
    time2.timeout.connect(lambda: TextLabel.textGetSet())
    if not isTest:
        time1.start(3000)  # 3s
        TextLabel.textGetSet()  # 手动调用
        time2.start(30000)  # 5min
        # 占用端口以识别单个实例
        lock_socket = single_instance(appConfig.get("port"))
    sys.exit(app.exec())
    # "pyinstaller.exe -F -w -i .\assets\luabackend.ico .\QuickTray.py"
