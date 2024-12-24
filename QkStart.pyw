# -*- coding: utf-8 -*-
# Editor    PyCharm
# File   QkStart |Author    Pfolg
# 2024/12/23 17:36
import sys
import pystray
from pystray import MenuItem, Menu
from PIL import Image
import os
import threading
import json
import time
import psutil
import pygame
import tkinter as tk
import requests
from tkinter import messagebox

version = 6
config_file = ".\\config.json"
setting_program = ".\\setting.pyw"
description = "快捷方式的替代：快捷托盘"

if not os.path.exists(config_file):
    messagebox.showerror("Error", f"未发现config_file：{config_file}\n运行设置程序！")
    os.system(f"start {setting_program}")
    sys.exit()
else:
    with open(config_file, "r", encoding="utf-8") as file:
        content = json.load(file)
        if not content:
            messagebox.showerror("Error", "您的配置似乎为空，程序无法运行！")
            sys.exit()

# 读取配置
main_keys = list(content.keys())
other_function = content.get(main_keys[4])


def open_program(icon, item):  # 使用类的默认传参来传递参数，然后检索程序并执行
    name = all_target.get(item.text)
    last_name = name.split(".")[-1]
    try:
        if last_name == "exe":
            os.startfile(name)
        elif last_name == "pyw" or last_name == "py":
            os.system("start {}".format(name))
        else:
            icon.notify("程序格式有误，请检查给点路径或代码！", "QkStart")
    except BaseException:
        icon.notify("{0}启动失败".format(item.text), "QkStart")


def open_link(icon, item):
    os.system("start {}".format(all_target.get(item.text)))
    # webbrowser.open_new_tab(all_target.get(item.text))  # 减少模块使用


all_target = {}
menu1 = []
menu2 = []
menu3 = []
menu4 = []
for key in content:
    value = content.get(key)
    try:
        for a in value:
            all_target[a] = value.get(a)
    except AttributeError:
        pass
    if key == main_keys[0]:
        for i in value:
            menu1.append(MenuItem(i, action=open_program))
    elif key == main_keys[1]:
        for i in value:
            menu2.append(MenuItem(i, action=open_link))
    elif key == main_keys[2]:
        for i in value:
            menu3.append(MenuItem(i, action=open_program))
    elif key == main_keys[3]:
        for i in value:
            menu4.append(MenuItem(i, action=open_program))
    else:
        pass

# 创建菜单项

menu = (
    MenuItem(main_keys[0], pystray.Menu(*menu1)),
    MenuItem(main_keys[1], pystray.Menu(*menu2)),
    MenuItem(main_keys[2], pystray.Menu(*menu3)),
    MenuItem(main_keys[3], pystray.Menu(*menu4)),
    Menu.SEPARATOR,
    MenuItem("Setting", action=lambda: os.system(f"start {setting_program}")),
    MenuItem(text=f"DesktopLabel {other_function.get('DesktopLabel')}", action=None),
    MenuItem(text='Quit', action=lambda: icon.stop()),
    MenuItem(
        text="", action=lambda: os.system(f"start {other_function.get('Default')}"), default=True,
        visible=False)
    # 双击图标动作
)


def textWindow():
    bg = "#d2e6f8"
    win = tk.Tk()
    s_w, s_h = win.winfo_screenwidth(), win.winfo_screenheight()
    win.geometry(f"{int(s_w / 4)}x{int(s_h / 2)}+{int(s_w / 1.4)}+{int(s_h / 12)}")  # 定义窗口大小和位置
    win.resizable(False, False)
    win.overrideredirect(True)
    win.config(background=bg)  # 背景为黑色
    tx = tk.StringVar()
    label = tk.Label(
        win, foreground="#FFFFFF", background=bg, justify=tk.LEFT, font=("simsun.ttc", 16),
        wraplength=int(s_w / 4), textvariable=tx
    )  # 左对齐，填充，字体不管怎么调好像都不会变化
    label.pack()

    def getText():
        while True:
            # 获取文字
            try:
                url = "https://tenapi.cn/v2/yiyan"
                webText = requests.get(url)
                if content:
                    tx.set(webText.text)
            except BaseException:
                tx.set("")
            finally:
                print(tx.get())
            time.sleep(600)  # 请求间隔不宜过短

    threading.Thread(target=getText, daemon=True).start()
    # win.attributes('-alpha', 0.9)  # 透明度
    win.attributes("-transparent", bg)  # 对bg透明
    win.mainloop()


the_win = threading.Thread(target=textWindow, daemon=True)


def auto_run():
    battery = psutil.sensors_battery()
    plugged = battery.power_plugged
    if plugged and other_function.get("StartupApp"):  # 检测是否连接电源
        time.sleep(60)
        if other_function.get("music"):
            pygame.mixer.init()
            pygame.mixer.Sound(other_function.get("music")).play()  # 播放音频
        if other_function.get("DesktopLabel"):
            the_win.start()
        for exe in content["Startup"].values():
            try:
                os.startfile(exe)
            except BaseException:
                continue
            time.sleep(5)


# 载入图片
picture = other_function.get("ico_path")
image = Image.open(picture)
# 创建托盘图标
icon = pystray.Icon("QkStart", image, description, menu)
# 运行托盘图标
threading.Thread(target=auto_run, daemon=True).start()
icon.run()
