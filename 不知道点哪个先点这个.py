# -*- coding: utf-8 -*-
# Editor    PyCharm
# File   不知道点哪个先点这个 |Author    Pfolg
# 2024/12/24 16:59
# 标记为必须文件
import json
import winreg as reg
import os
import tkinter as tk
from tkinter import ttk, messagebox


def modify_startup(file_path="", startup_name=""):
    if not file_path:
        file_path = os.path.abspath(__file__)
    if not startup_name:
        startup_name = "My Python Program"

    # 打开注册表键
    reg_key = reg.HKEY_CURRENT_USER
    reg_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
    try:
        registry_key = reg.OpenKey(reg_key, reg_path, 0, reg.KEY_SET_VALUE)
    except FileNotFoundError:
        registry_key = reg.CreateKey(reg_key, reg_path)

    # 修改键值
    try:
        reg.SetValueEx(registry_key, startup_name, 0, reg.REG_SZ, file_path)
        messagebox.showinfo("QkStart", f"已成功修改启动项 '{startup_name}' 的路径。")
        print(f"已成功修改启动项 '{startup_name}' 的路径。")
    except FileNotFoundError:
        messagebox.showerror("QkStart", f"启动项 '{startup_name}' 不存在。")
        print(f"启动项 '{startup_name}' 不存在。")
    finally:
        reg.CloseKey(registry_key)


def delete_startup(startup_name=""):
    if not startup_name:
        startup_name = "My Python Program"

    # 打开注册表键
    reg_key = reg.HKEY_CURRENT_USER
    reg_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
    try:
        registry_key = reg.OpenKey(reg_key, reg_path, 0, reg.KEY_SET_VALUE)
    except FileNotFoundError:
        registry_key = reg.CreateKey(reg_key, reg_path)

    # 删除键值
    try:
        reg.DeleteValue(registry_key, startup_name)
        messagebox.showinfo("QkStart", f"已成功删除启动项 '{startup_name}'。")
        print(f"已成功删除启动项 '{startup_name}'。")
    except FileNotFoundError:
        messagebox.showerror("QkStart", f"启动项 '{startup_name}' 不存在。")
        print(f"启动项 '{startup_name}' 不存在。")
    finally:
        reg.CloseKey(registry_key)


# 读取插件
def readPlugins():
    if os.path.exists(".\\plugins"):
        files = os.walk(".\\plugins")
        if files:
            for i, j, k in files:
                if k:
                    return k
                else:
                    return False
            else:
                return False
        else:
            return False


# 读取配置文件
def readConfig():
    if os.path.exists(config_file):
        print("Found the config file!")
        with open(config_file, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        return False


# 写入配置
def writeConfig(plugins, configDict):
    # 替换内容
    if plugins and configDict:
        scripts = {}
        # 获取父目录
        father_path = os.getcwd()
        # print(plugins, configDict)
        # 修改格式
        for item in plugins:
            scripts[item.split(".")[0]] = father_path + "\\plugins\\" + item
        print("plugins：", scripts)
        configDict["QuickScripts"] = scripts
        # 写入配置
        with open(config_file, "w", encoding="utf-8") as cf:
            json.dump(configDict, cf, ensure_ascii=False, indent=4)
        messagebox.showinfo("QkStart", "已将更改的内容写入配置文件！")
        print("已将更改的内容写入配置文件" + config_file + "\n[回车退出……]")
    else:
        messagebox.showerror("QkStart", "读取失败！")
        input("读取失败！\n[回车退出……]")


# 设置 主程序 更新plugins 添加/移除-开机自启动 打开日志 打开配置文件 打开官网
class Direction:
    def __init__(self, name):
        self.root = tk.Tk()
        self.name = name

    def window(self):
        self.root.title(self.name)
        screen_w, screen_h = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        width, height = int(screen_w / 6), int(screen_h / 4)
        self.root.geometry(f"{width}x{height}+{int(screen_w / 2)}+{int(screen_h / 4)}")
        self.root.resizable(False, False)

        tk.Label(self.root, text=self.name + "程序", ).pack()
        frame = ttk.Frame(self.root, borderwidth=2, relief="groove", padding=1)
        ttk.Button(
            frame, text="设置", command=lambda: os.system("start {}".format(setting_file)), width=12
        ).place(relx=.05, rely=.02)
        ttk.Button(
            frame, text="打开主程序", command=lambda: os.system("start {}".format(main_program)), width=12
        ).place(relx=.5, rely=.02)

        ttk.Button(
            frame, text="Website", command=lambda: os.system("start {}".format(website)), width=12
        ).place(relx=.05, rely=.2)
        ttk.Button(
            frame, text="查看日志", command=lambda: os.system("start {}".format(log_file)), width=12
        ).place(relx=.5, rely=.2)
        ttk.Button(
            frame, text="更新plugins", command=lambda: writeConfig(readPlugins(), readConfig()), width=24
        ).place(relx=0.1, rely=.4)
        ttk.Button(
            frame, text="添加开机自启", command=lambda: modify_startup(main_program, "QkStart"), width=24
        ).place(relx=.1, rely=.6)
        ttk.Button(
            frame, text="移除开机自启", command=lambda: delete_startup("QkStart"), width=24
        ).place(relx=.1, rely=.8)

        frame.place(x=10, y=20, width=238, height=185)
        self.root.mainloop()


if __name__ == '__main__':
    setting_file = "setting.pyw"
    main_program = "QkStart.pyw"
    config_file = "config.json"
    log_file = "QkStartLog.log"
    website = "https://github.com/Pfolg/QkStart"
    d = Direction("QkStart导航")
    d.window()
