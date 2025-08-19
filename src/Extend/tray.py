# -*- coding: UTF-8 -*-
"""
PROJECT_NAME QuickTray
PRODUCT_NAME PyCharm
NAME tray
AUTHOR Pfolg
TIME 2025/8/19 11:43
"""
import time
import webbrowser

import psutil
from PySide6.QtCore import QTimer
from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import QMenu

from .QuickTrayExtend import EWidget
from .string_data import getLanguage
from .config_json import *
from .otherFunc import *


class Tray(QSystemTrayIcon):
    def __init__(self, language, config: dict, config_file: str, appList_file: str):
        super().__init__()
        self.menu_setting = QMenu()
        self.appList_file = appList_file
        self.config_file = config_file
        self.language = language
        self.config = config
        self.childMenus = {}
        # 报时
        self.hourTimer = QTimer()
        self.lastMin = ""
        self.isHourAlarm = self.config.get("hourAlarm")
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
        write_config_json(self.config_file, "language", mark)
        self.setMenuLanguage()
        self.showMessage(
            "Tip",
            self.language.language_changed_tip
        )

    def shortcut_option(self):
        if self.self_start.text() == self.language.self_start_off:
            makeShortcut(
                self, self.language,
                apppath=getPath(),
                icoPath=self.config.get("logo"),
                workingDirectory=getDirName(),
                pathName=Data.start_link,
            )
        else:
            delete_shortcut(self, self.language, Data.start_link)

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
        self.action_setting2.triggered.connect(lambda: self.openTarget(self.config_file))
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

    def setting(self) -> None:
        _format = {
            "type": "",
            "name": "",
            "path": "",
            "icon": "",
        }
        if not os.path.exists(self.appList_file):
            with open(self.appList_file, "w", encoding="utf-8") as file:
                json.dump([_format], file, indent=4, ensure_ascii=False)
        os.startfile(self.appList_file)

    def readSetting(self) -> list:
        if os.path.exists(self.appList_file):
            with open(self.appList_file, "r", encoding="utf-8") as file:
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
            f"{self.config.get('tip')} "
            f"{Data.version}\n"
            f"{Data.s_tool_Items} {item_num}\n"
            f"Autorun: {self.config.get('autorun')}\n"
            f"HourAlarm: {self.config.get('hourAlarm')}"
        )
        self.setToolTip(info)
        self.setIcon(QIcon(self.config.get("logo")))

    def td_autorun(self) -> None:
        if self.config.get("autorun"):
            battery = psutil.sensors_battery()
            plugged = battery.power_plugged
            if plugged:
                data = self.readSetting()
                for item in data:
                    if "star" in item.get("type"):
                        p = item.get("path")
                        self.openTarget(p)
                        time.sleep(3)
