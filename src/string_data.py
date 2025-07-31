# -*- coding: UTF-8 -*-
"""
PROJECT_NAME Python_projects
PRODUCT_NAME PyCharm
NAME string_data
AUTHOR Pfolg
TIME 2025/7/18 21:02
"""
"""用于储存常量的文件"""
import os
from dataclasses import dataclass, field


class Data:
    app_name = "Quick Tray"
    bing = "https://cn.bing.com/search?q={}"
    version = "ver1.12.0-20250730"
    website = "https://github.com/Pfolg/QuickTray"
    user_folder = "app_config"
    config_file = os.path.join(user_folder, "basic_config.json")  # user_folder + "/basic_config.json"
    lines_file = os.path.join(user_folder, "lines.json")
    appList_file = os.path.join(user_folder, "applist.json")
    port = 20082
    isautorun = True
    string_on = "on"
    string_off = "off"

    asset_folder = "assets"
    picture_windows = os.path.join(asset_folder, "windows.png")
    picture_preferences_other = os.path.join(asset_folder, "preferences-other.ico")
    picture_power_off = os.path.join(asset_folder, "power-off.svg")
    picture_circle_question = os.path.join(asset_folder, "circle-question.svg")
    picture_circle_exclamation = os.path.join(asset_folder, "circle-exclamation.svg")
    picture_github = os.path.join(asset_folder, "github.svg")
    picture_heading = os.path.join(asset_folder, "heading.svg")
    picture_search = os.path.join(asset_folder, "preferences-desktop-search.ico")
    picture_star = os.path.join(asset_folder, "preferences-desktop-default-applications.ico")
    picture_app = os.path.join(asset_folder, "applications-all.ico")
    picture_link = os.path.join(asset_folder, "applications-internet.ico")
    picture_scripts = os.path.join(asset_folder, "application-vnd.nokia.xml.qt.resource.ico")
    picture_c_star = None
    picture_c_app = None
    picture_c_link = os.path.join(asset_folder, "arrow-up-right-from-square.svg")
    picture_c_scripts = os.path.join(asset_folder, "code.svg")
    picture_luabackend = os.path.join(asset_folder, "luabackend.ico")

    font_myu = "Microsoft YaHei UI"
    font_mmnc = "Maple Mono NF CN"

    s_tool_Items = "Items:"


@dataclass
class LanguageFormat:
    string_quit: str = "Quit"
    string_text: str = "Text"
    string_copy: str = "Copy"
    string_edit: str = "Edit"
    string_search: str = "Search"

    string_about: str = "About"
    string_update: str = "Update"
    string_setting: str = "Setting"
    string_github: str = "GitHub"
    string_settingw: str = "Setting Window"
    string_e_menu: str = "Editing menus"
    string_e_setting: str = "Editing setting"
    string_folder_program: str = "Program\'s folder"
    string_u_menu: str = "Update menus"
    string_c_update: str = "Check update"
    string_change_language: str = "Change Language"
    language_en: str = "English"
    language_zh: str = "Chinese"
    language_changed_tip: str = "The changes can only be fully applied after a restart"

    input_placeholder: str = "Enter..."
    failed_open_file: str = "File not exists\n"
    unknown_error: str = "can not open the path, unknown issue\n"
    unable_open_file: str = "can not open the path\n"
    children_menu: dict = field(
        default_factory=lambda: {
            "star": "star",
            "app": "app",
            "link": "link",
            "scripts": "scripts"
        }
    )


Language_EN = LanguageFormat()

Language_ZH = LanguageFormat(
    string_quit="退出",
    string_text="美句",
    string_copy="复制",
    string_edit="编辑",
    string_search="搜索",

    string_about="关于",
    string_update="刷新",
    string_setting="设置",
    string_github="GitHub",
    string_settingw="设定窗口",
    string_e_menu="编辑菜单",
    string_e_setting="编辑设定",
    string_folder_program="打开目录",
    string_u_menu="刷新菜单",
    string_c_update="检查更新",
    string_change_language="切换语言",
    language_en="英语",
    language_zh="中文",
    language_changed_tip="重启后才能完全应用更改",

    input_placeholder="请输入……",
    failed_open_file="文件不存在！\n",
    unknown_error="无法打开路径，未知问题\n",
    unable_open_file="无法打开路径\n",
    children_menu={
        "star": "收藏",
        "app": "应用",
        "link": "链接",
        "scripts": "脚本"
    }
)


def getLanguage(mark: str) -> LanguageFormat:
    """返回语言：数据类"""
    match mark:
        case "en":
            return Language_EN
        case "zh":
            return Language_ZH
        case _:
            return Language_EN
