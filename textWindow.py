# -*- coding: utf-8 -*-
# Environment    PyCharm
# File_name   textWindow |User    Pfolg
# 2024/11/18 12:25
import time
import tkinter as tk
import requests
import threading


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
                content = requests.get(url)
                if content:
                    tx.set(content.text)
            except BaseException:
                tx.set("")
            finally:
                print(tx.get())
            time.sleep(600)

    threading.Thread(target=getText, daemon=True).start()
    # win.attributes('-alpha', 0.9)  # 透明度
    win.attributes("-transparent", bg)  # 对bg透明
    win.mainloop()


textWindow()