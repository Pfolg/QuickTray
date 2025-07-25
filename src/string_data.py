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


class Data:
    version = "ver1.11.3-20250725"
    website = "https://github.com/Pfolg/QuickTray"
    user_folder = "app_config"
    config_file = os.path.join(user_folder, "basic_config.json")  # user_folder + "/basic_config.json"
    lines_file = os.path.join(user_folder, "lines.json")
    appList_file = os.path.join(user_folder, "applist.json")
    port = 20082
    isautorun = True
    string_autorun = "autorun"
    string_type = "type"
    string_star = "star"
    string_app = "app"
    string_link = "link"
    string_scripts = "scripts"
    string_on = "on"
    string_off = "off"
    str_tip = "tip"
    str_logo = "logo"
    str_version = "version"
    str_usecount = "usecount"
    str_port = "port"

    timer1_timeout = 30000
    timer2_timeout = 300000

    s_tool_Items = "Items:"

    string_path = "path"
    string_name = "name"
    string_icon = "icon"
    string_quit = "Quit"
    string_text = "Text"
    string_copy = "Copy"
    string_edit = "Edit"
    string_search = "Search"
    string_menu_icon = "menu_icon"
    string_menu = "menu"
    string_children_icon = "children_icon"

    string_about = "About"
    string_update = "Update"
    string_setting = "Setting"
    string_github = "GitHub"
    string_settingw = "Setting Window"
    string_e_menu = "Editing menus"
    string_e_setting = "Editing setting"
    string_folder_program = "Program\'s folder"
    string_u_menu = "Update menus"
    string_c_update = "Check update"

    font_myu = "Microsoft YaHei UI"
    font_mmnc = "Maple Mono NF CN"

    watermark1 = "Windows Hacked"
    watermark2 = "Go to http://127.0.0.1/ to pay the ransom."
    default_sentence = "Wish you hava a good day!"
    default_sentence2 = "QuickTray is Testing..."

    app_name = "Quick Tray"
    local_link = "127.0.0.1"
    bing = "https://cn.bing.com/search?q={}"
    input_placeholder = "Enter..."
    keyword_web: list = ["http", "https"]
    failed_open_file = "文件不存在！\n"
    unknown_error = "无法打开路径，未知问题\n"
    unable_open_file = "无法打开路径\n"
    Programs_folder = r'%ProgramData%\Microsoft\Windows\Start Menu\Programs'
    Windows_Menu = "Windows Menu"

    asset_folder = "assets"
    picture_windows = asset_folder + "/windows.png"
    picture_preferences_other = asset_folder + "/preferences-other.ico"
    picture_power_off = asset_folder + "/power-off.svg"
    picture_circle_question = asset_folder + "/circle-question.svg"
    picture_circle_exclamation = asset_folder + "/circle-exclamation.svg"
    picture_github = asset_folder + "/github.svg"
    picture_heading = asset_folder + "/heading.svg"
    picture_search = asset_folder + "/preferences-desktop-search.ico"
    picture_star = asset_folder + "/preferences-desktop-default-applications.ico"
    picture_app = asset_folder + "/applications-all.ico"
    picture_link = asset_folder + "/applications-internet.ico"
    picture_scripts = asset_folder + "/application-vnd.nokia.xml.qt.resource.ico"
    picture_c_star = None
    picture_c_app = None
    picture_c_link = asset_folder + "/arrow-up-right-from-square.svg"
    picture_c_scripts = asset_folder + "/code.svg"
    picture_luabackend = asset_folder + "luabackend.ico"
