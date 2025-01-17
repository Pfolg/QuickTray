# -*- coding: utf-8 -*-
# Editor    PyCharm
# File   setting |Author    Pfolg
# 2024/12/21 22:18
"""
需要一个线程读取文件，然后反馈到程序中  文件监视线程
提供一个窗口，给用户更改设置   窗口线程
自动保存用户更改
启动日志记录
"""
# 导入第三方库
import os.path  # 需要对路径进行判断
import tkinter as tk  # 主窗口库
import webbrowser
from tkinter import ttk, messagebox, filedialog  # 实现窗口功能的库
import threading  # 实现多线程的库
import json  # 实现文件读写的库
import time  # 管理时间的库

# name
program_name = "QkStart控制面板"
# 定义配置文件
config_file = ".\\QkStart_config.json"
# 定义日志文件
log_file = ".\\QkStartLog.log"
# 默认图标
default_ico = ".\\QkStart.ico"
# 默认提示音
default_music = ".\\machao.mp3"
# 定义版本
version = 1
# 许可证
LICENSE = "MIT"
# 默认标签
default_label = "重启主程序以应用更改"


# 定义查找文件的函数
def find_files(x, limit=None):
    if limit is None:
        limit = [("所有文件", "*.*"), ]
    win = tk.Tk()
    win.withdraw()
    file_path = filedialog.askopenfilename(filetypes=limit)
    if file_path:
        x.set(file_path)
    win.destroy()


def find_directory(x):
    win = tk.Tk()
    win.withdraw()
    file_path = filedialog.askdirectory()
    if file_path:
        x.set(file_path)
    win.destroy()


# 定义 setting 类
class Setting:

    # 定义日志写入函数
    def write_log(self, keyword=""):
        if self.running and self.count == 0:  # 最开始运行的时候，定义 keyWord 为 start
            keyword = "start"
        elif not self.running:  # 程序结束运行之后，定义 keyword 为 end
            keyword = "end"
        with open(log_file, "a", encoding="utf-8") as file:  # 写入日志，除了以上两种情况，其他情况需要自定义 keyword
            file.writelines(f'{time.strftime("%Y/%m/%d %H:%M:%S")} {keyword}\n')
        # messagebox.showinfo(self.name, keyword)

    # 定义配置文件阅读程序&有保存功能
    def readConfigFile(self):
        while self.running:  # 无限循环，当 self.running 等于 false 时退出
            if os.path.exists(config_file) and self.running==True:  # 判断配置文件是否存在
                with open(config_file, "r", encoding="utf-8") as file1:
                    data = json.load(file1)  # 如果配置文件存在，则读入数据
                if self.count == 0 and self.running==True:  # 初次读入数据时，读入数据等于 date
                    self.data = data
                if self.data != data and self.count != 0 and self.running==True:  # 如果程序里的数据不等于读入数据，且不是第一次循环，则覆写配置
                    with open(config_file, "w", encoding="utf-8") as file2:
                        json.dump(self.data, file2, ensure_ascii=False, indent=4)#覆写配置
            else:  # 不存在，询问用户是否需要创建，同意则创建，不同意则退出程序
                if messagebox.askyesno(
                        "Error",
                        "未发现配置文件，创建配置文件？\n若创建配置文件，请不要随意更改配置文件！！！"):
                    with open(config_file, "w", encoding="utf-8") as file1:
                        json.dump(self.data, file1, ensure_ascii=False, indent=4)
                    self.write_log("created config_file：" + config_file)
                else:
                    self.running = False
                    self.window.destroy()
            self.count = 1  # 不使用加等于是为了优化
            time.sleep(2)  # 睡两秒钟也是为了优化

    # 定义标签页通用布局函数
    def setTabProperty(self, tab: ttk.Frame, name: str):
        # 定义删除选定的列表中的值的函数
        def delete_selection():
            try:
                num = listbox.curselection()[0]
                key0 = listbox.get(0, tk.END)[num]
                key = key0.split("  |  ")[0]
                # print(key)
                del self.data[name][key]
                listbox.delete(num)
                print(self.data)
                update_listBox()  # 更新列表
                self.write_log("deleted " + key0)  # 运行日志写入函数
            except IndexError:
                print("没有指定的值，无法进行删除！")

        # 定义添加值的函数
        def add_item():
            i1, i2 = v1.get(), v2.get()  # 获取用户输入
            # 判断用户输入的标签是否在 listbox 里面存在键
            boxList = list(listbox.get(0, tk.END))
            judge = True
            for i in boxList:
                if i1 in i:
                    judge = False
            if i1 and i2 and judge:
                listbox.insert(tk.END, i1 + "  |  " + i2)
                self.data[name][i1] = i2
                print(self.data)
                update_listBox()  # 更新列表
                self.write_log("added " + i1 + "  |  " + i2)  # 运行日志写入函数
            else:
                print("添加失败")
                messagebox.showerror("Error", "添加失败！")  # 弹窗提醒，添加失败

        # 定义删除所有值的函数
        def delete_all():
            listbox.delete(0, tk.END)
            v = self.data[name]
            self.data[name] = {}
            print(self.data)
            update_listBox()  # 更新列表
            self.write_log("cleared " + str(v))  # 运行日志写入函数

        # 定义更新列表的函数
        def update_listBox():
            try:
                listbox.delete(0, tk.END)  # 删除所有数据
                items = list(self.data[name].keys())  # 获取最新数据
                for item in items:  # 循环插入数据
                    v = self.data[name].get(item)
                    listbox.insert(tk.END, item + "  |  " + v)
            except BaseException:
                pass

        ttk.Label(tab, text=default_label).place(relx=.4, rely=.02)
        # 添加 标签：路径 的框架
        frame1 = ttk.Frame(tab, borderwidth=2, relief="groove", padding=1)
        v1, v2 = tk.StringVar(), tk.StringVar()
        ttk.Label(frame1, text="标签").place(relx=.02, rely=.02)
        ttk.Entry(frame1, textvariable=v1, width=30).place(relx=.1, rely=.02)
        ttk.Label(frame1, text="路径").place(relx=0.02, rely=.3)
        ttk.Entry(frame1, textvariable=v2, width=40).place(relx=.1, rely=.3)
        ttk.Button(frame1, text="浏览", width=8, command=lambda: find_files(v2)).place(relx=.6, rely=.3)
        ttk.Button(frame1, text="添加", command=add_item).place(relx=.45, rely=.7)
        frame1.place(x=40, y=40, width=680, height=140)

        # 展示&删除 标签：路径
        frame2 = ttk.Frame(tab, borderwidth=2, relief="groove", padding=1)
        ttk.Label(frame2, text="已经添加的[标签  |  路径]，选定删除", font=("微软雅黑", 12)).place(relx=.02, rely=.02)
        listbox = tk.Listbox(frame2, width=90, height=7)
        ttk.Button(frame2, text="删除选定", command=delete_selection).place(relx=.8, rely=.02)
        ttk.Button(frame2, text="删除全部", command=delete_all).place(relx=.6, rely=.02)
        # ttk.Button(frame2, text="保存当前页更改").place(relx=.8, rely=.02)
        update_listBox()  # 更新列表
        listbox.place(relx=.02, rely=.3)
        frame2.place(x=40, y=200, width=680, height=200)

    # 定义第5标签页的设定函数
    def setTab5Property(self):
        the_data = self.data["OtherFunction"]

        # 测试用函数
        def save_change(msg=None):
            if self.running==True:
                if default_func.get() == "None" or not default_func.get():
                    x1 = None
                else:
                    x1 = default_func.get()
                if ico_path.get().split(".")[-1] != "ico" or not ico_path.get():
                    x2 = default_ico
                else:
                    x2 = ico_path.get()
                if music_path.get().split(".")[-1] not in [ "mp3","wav"] or not music_path.get() :
                    x3 = default_music
                else:
                    x3 = music_path.get()
                changed_data = {
                    "StartupApp": bool_value1.get(),
                    "Startup": bool_value2.get(),
                    "DesktopLabel": bool_value3.get(),
                    "Default": x1,
                    "ico_path": x2,  # 绝对不能为空
                    "music": x3
                }

                self.data["OtherFunction"] = changed_data
                self.write_log(msg)
                print("Change saved"+msg)

        tab5 = ttk.Frame(self.notebook)
        tab5Name = list(self.data.keys())[4]
        # 定义标签
        ttk.Label(tab5, text=default_label).place(relx=.4, rely=.02)
        frame1 = ttk.Frame(tab5, borderwidth=2, relief="groove", padding=1)
        # bool变量
        bool_value1, bool_value2, bool_value3 = tk.BooleanVar(), tk.BooleanVar(), tk.BooleanVar()
        default_func, ico_path, music_path = tk.StringVar(), tk.StringVar(), tk.StringVar()
        # 赋初值 使用.get()更安全 找不到就是none
        bool_value1.set(the_data.get("StartupApp"))
        bool_value2.set(the_data.get("Startup"))
        bool_value3.set(the_data.get("DesktopLabel"))
        default_func.set(the_data.get("Default"))
        ico_path.set(the_data.get("ico_path"))
        music_path.set(the_data.get("music"))

        ttk.Checkbutton(
            frame1, text="帮助自启动APP", onvalue=True, offvalue=False, variable=bool_value1,
            command=lambda: save_change("Changed 启动APP to " + str(bool_value1.get())), width=20
        ).place(relx=.02, rely=.02)
        ttk.Checkbutton(
            frame1, text="开机自启动", onvalue=True, offvalue=False, variable=bool_value2,
            command=lambda: save_change("Changed 开机自启动 to " + str(bool_value2.get())), width=20
        ).place(relx=.52, rely=.02)
        ttk.Checkbutton(
            frame1, text="桌面标签", onvalue=True, offvalue=False, variable=bool_value3,
            command=lambda: save_change("Changed 桌面标签 to " + str(bool_value3.get())), width=20
        ).place(relx=.02, rely=.22)

        def midFun5_music():
            find_files(music_path, limit=[("mp3文件", "*.mp3"),("wav文件","*.wav"), ])
            save_change("Changed music_path " + music_path.get())

        # 提示音设定
        ttk.Label(frame1, text="自定义提示音[.mp3]").place(relx=.02, rely=.4)
        ttk.Entry(frame1, width=40, textvariable=music_path).place(relx=.22, rely=.4)
        ttk.Button(
            frame1, text="选择",
            command=midFun5_music, width=6
        ).place(relx=.67, rely=.395)
        # 托盘图标设定
        ttk.Label(frame1, text="自定义托盘图标[.ico]").place(relx=.02, rely=.6)
        ttk.Entry(frame1, width=40, textvariable=ico_path).place(relx=.22, rely=.6)

        def midFun1_ico():
            find_files(ico_path, limit=[(".ico文件", "*.ico"), ])
            save_change("Changed ico_path " + ico_path.get())

        ttk.Button(
            frame1, text="选择",
            command=midFun1_ico, width=6
        ).place(relx=.67, rely=.595)

        # 默认点击功能设定
        ttk.Label(frame1, text="默认打开[路径/链接]").place(relx=.02, rely=.8)
        ttk.Entry(frame1, width=40, textvariable=default_func).place(relx=.22, rely=.8)

        def midFun2_default():
            find_files(default_func)
            save_change("Changed default " + default_func.get())

        def midFun3_default():
            find_directory(default_func)
            save_change("Changed default " + default_func.get())

        def midFun4_default():
            default_func.set("")
            save_change("Cleared default " + default_func.get())

        ttk.Button(
            frame1, text="文件", command=midFun2_default, width=6
        ).place(relx=.67, rely=.795)
        ttk.Button(
            frame1, text="文件夹", command=midFun3_default, width=6
        ).place(relx=.77, rely=.795)
        ttk.Button(
            frame1, text="清除", command=midFun4_default, width=6
        ).place(relx=.87, rely=.795)

        # 打开 配置文件 GitHub
        def open_config_file(e):
            os.startfile(config_file)

        def open_GitHub(e):
            # 这个链接需要更改
            webbrowser.open("https://github.com/Pfolg/QkStart")

        ttk.Button(frame1, text="Save", command=lambda: save_change("已手动保存")).place(relx=.85, rely=.02)

        label_color = "#005fb8"
        frame2 = ttk.Frame(tab5, borderwidth=2, relief="groove", padding=1)
        label1 = ttk.Label(frame2, text="打开配置文件", foreground=label_color, cursor="hand2")
        label2 = ttk.Label(frame2, text="GitHub / ISSUE / LICENSE", foreground=label_color, cursor="hand2")
        ttk.Label(
            frame2, text=f"本程序遵循 {LICENSE} 协议，继续使用，代表您同意此协议\n"
                         f"感谢所有本程序涉及的第三方库及Python语言开发者，未能一一致谢，抱歉！\n"
                         f"程序可能无法自行修改自启动，请您手动将程序的本体（QkStart.pyw或QkStart.exe）的快捷方式放到启动文件夹"
        ).place(relx=.02, rely=.42)
        label1.bind("<Button-1>", open_config_file)
        label2.bind("<Button-1>", open_GitHub)
        # 添加到<frame>
        label1.place(relx=.02, rely=.02)
        label2.place(relx=.02, rely=.22)
        frame2.place(x=40, y=250, width=680, height=120)
        frame1.place(x=40, y=40, width=680, height=200)
        self.notebook.add(tab5, text=tab5Name)

    # 定义主窗口函数
    def settingWindow(self):
        self.tdReadConfig.start()  # 读入配置数据线程启动
        # 定义窗口属性
        self.window.title(self.name)
        screen_width, screen_height = self.window.winfo_screenwidth(), self.window.winfo_screenheight()
        window_width, window_height = int(screen_width / 2), int(screen_height / 2)
        self.window.geometry("{0}x{1}+{2}+{3}".format(
            window_width, window_height, int(window_width / 2), int(window_height / 2)))
        try:
            self.window.iconbitmap(default_ico)
        except Exception:
            pass
        self.window.resizable(False, False)

        # 添加标签页到Notebook
        tabs = [ttk.Frame(self.notebook) for _ in range(self.menuCount)]

        # 将标签页添加到Notebook
        for i in range(len(tabs)):
            name = list(self.data.keys())[i]
            self.setTabProperty(tabs[i], name)
            self.notebook.add(tabs[i], text=name)
        self.setTab5Property()
        # 将 notebook 添加到 window
        self.notebook.pack(fill='both', expand=True)
        self.window.mainloop()
        time.sleep(2)  # 睡两秒钟是为了等待读入数据线程将数据保存
        self.running = False  # 运行状态转为 False

    # 初始化的函数
    def __init__(self, menuCount, name):
        self.name = name
        self.window = tk.Tk()  # 定义 tinker 窗口
        self.notebook = ttk.Notebook(self.window)  # 创建一个Notebook控件
        self.count = 0  # 定义循环次数
        self.running = True  # 定义程序运行状态
        self.tdReadConfig = threading.Thread(target=self.readConfigFile, daemon=True)  # 定义读入配置数据线程
        self.data = {
            "Startup": {
            },
            "QuickLinks": {
                "carbon": "https://carbon.now.sh/",
                "Ray.so": "https://ray.so/",
                "Image-to-Braille": "https://505e06b2.github.io/Image-to-Braille/",
                "查汇率": "https://themoneyconverter.com/zh-CN/"
            },
            "Tools": {
                "Calculator": "C:/WINDOWS/system32/calc.exe"
            },
            "QuickScripts": {
                "autoShutdownPro": "D:\\Little_Tools\\QkStart\\plugins\\autoShutdownPro.pyw",
                "FanYi": "D:\\Little_Tools\\QkStart\\plugins\\FanYi.pyw",
                "IntTimeNotify": "D:\\Little_Tools\\QkStart\\plugins\\IntTimeNotify.pyw",
                "makeKey": "D:\\Little_Tools\\QkStart\\plugins\\makeKey.pyw",
                "WaterMark": "D:\\Little_Tools\\QkStart\\plugins\\WaterMark.pyw"
            },
            "OtherFunction": {
                "StartupApp": True,
                "Startup": True,
                "DesktopLabel": False,
                "Default": None,
                "ico_path": default_ico,  # 绝对不能为空
                "music": default_music

            }
        }  # 定义初始 data 数据
        self.menuCount = menuCount  # 定义 tab 数 前4个普通窗口
        self.write_log()  # 运行日志写入函数
        self.settingWindow()  # 运行窗口


if __name__ == '__main__':
    setting = Setting(menuCount=4, name=program_name)  # 创建一个 setting 为 Setting 类的对象
    setting.write_log()  # 运行日志写入函数
