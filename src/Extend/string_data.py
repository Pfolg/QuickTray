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


def locate_assets_files(file: str) -> str:
    assets = "assets"
    return os.path.join(assets, file)


class Data:
    app_name = "Quick Tray"
    bing = "https://cn.bing.com/search?q={}"
    version = "ver1.12.2-dev"
    website = "https://github.com/Pfolg/QuickTray"
    # 解析环境变量
    start_link = os.path.expandvars("%AppData%\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\Quick Tray.lnk")
    user_folder = "app_config"
    config_file = os.path.join(user_folder, "basic_config.json")  # user_folder + "/basic_config.json"
    lines_file = os.path.join(user_folder, "lines.json")
    appList_file = os.path.join(user_folder, "applist.json")
    port = 20082
    isautorun = True
    string_on = "on"
    string_off = "off"

    asset_folder = "assets"
    picture_windows = locate_assets_files("windows.png")
    picture_preferences_other = locate_assets_files("preferences-other.ico")
    picture_power_off = locate_assets_files("power-off.svg")
    picture_circle_question = locate_assets_files("circle-question.svg")
    picture_circle_exclamation = locate_assets_files("circle-exclamation.svg")
    picture_github = locate_assets_files("github.svg")
    picture_heading = locate_assets_files("heading.svg")
    picture_search = locate_assets_files("preferences-desktop-search.ico")
    picture_star = locate_assets_files("preferences-desktop-default-applications.ico")
    picture_app = locate_assets_files("applications-all.ico")
    picture_link = locate_assets_files("applications-internet.ico")
    picture_scripts = locate_assets_files("application-vnd.nokia.xml.qt.resource.ico")
    picture_c_star = None
    picture_c_app = None
    picture_c_link = locate_assets_files("arrow-up-right-from-square.svg")
    picture_c_scripts = locate_assets_files("code.svg")
    picture_luabackend = locate_assets_files("luabackend.ico")

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
    string_u_menu: str = "Reload menus"
    string_c_update: str = "Check update"
    string_change_language: str = "Language"
    language_en: str = "English"
    language_zh: str = "Chinese"
    language_changed_tip: str = "The changes can only be fully applied after a restart"
    tip_create_shortcut_success: str = "Self-start setting successful"
    tip_create_shortcut_fail: str = "Self-starting setting failed"
    tip_delete_shortcut_success: str = "The self-start has been successfully canceled"
    tip_delete_shortcut_fail: str = "Failed to cancel self-starting"
    tip_hour_alarm: str = "Now is: "
    self_start_on: str = "Self-start ✅"
    self_start_off: str = "Self-start ❌"

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
    string_u_menu="重载菜单",
    string_c_update="检查更新",
    string_change_language="语言",
    language_en="英语",
    language_zh="中文",
    language_changed_tip="重启后才能完全应用更改",
    tip_create_shortcut_success="自启动设置成功",
    tip_create_shortcut_fail="自启动设置失败",
    tip_delete_shortcut_success="取消自启动成功",
    tip_delete_shortcut_fail="取消自启动失败",
    tip_hour_alarm="现在是：",
    self_start_on="自启动 ✅",
    self_start_off="自启动 ❌",

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
