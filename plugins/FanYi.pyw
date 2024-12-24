# -*- coding: utf-8 -*-
# Editor    PyCharm
# File   FanYi |Author    Pfolg
# 2024/12/13 19:24
import tkinter as tk
import pyperclip
from translate import Translator
from tkinter.scrolledtext import ScrolledText
from tkinter import ttk
import threading

languageDict = {
    "英语": "en",
    "中文": "zh",
    "繁体中文": "zh-TW",
    "日语": "ja",
    "韩语": "ko",
    "法语": "fr",
    "西班牙语": "es",
    "意大利语": "it",
    "德语": "de",
    "土耳其语": "tr",
    "俄语": "ru",
    "葡萄牙语": "pt",
    "越南语": "vi",
    "印尼语": "id",
    "泰语": "th",
    "马来语": "ms",
    "阿拉伯语": "ar",
    "印地语": "hi"}


def frameTran(frm):
    languageList = list(languageDict.keys())

    # 源语言
    source_language = ttk.Combobox(frm, values=languageList, width=8, state="readonly")
    source_language.set("英语")
    source_language.place(relx=.65, rely=0)

    # 目标语言
    target_language = ttk.Combobox(frm, values=languageList, width=8, state="readonly")
    target_language.set("中文")
    target_language.place(relx=.65, rely=.15)

    # 输入框
    source_text = ScrolledText(frm, width=20, height=6)
    source_text.place(relx=0, rely=0)

    # 输出框
    out_text = ScrolledText(frm, width=20, height=7)
    out_text.place(relx=0, rely=.5)

    # 粘贴按钮
    def pasteSourceText():
        source_text.delete("1.0", "end")
        source_text.insert("end", pyperclip.paste())

    ttk.Button(frm, text="粘贴", width=8, command=pasteSourceText).place(relx=.67, rely=.3)

    # 翻译函数，核心代码
    def translate_text(text, sources, target):
        if text and sources and target and (sources != target):
            s = languageDict.get(sources)
            t = languageDict.get(target)
            translator = Translator(from_lang=s, to_lang=t)
            out = translator.translate(text)
            out_text.delete("1.0", "end")
            out_text.insert("end", out)
            print(out)

    # 翻译按钮
    ttk.Button(
        frm, text="翻译", width=8, command=lambda: threading.Thread(
            target=lambda: translate_text(
                source_text.get("1.0", "end").strip(),
                source_language.get(), target_language.get())).start()
    ).place(relx=.67, rely=.6)

    # 清除按钮
    def deleteAll():
        source_text.delete("1.0", "end")
        out_text.delete("1.0", "end")

    ttk.Button(frm, text="清除", width=8, command=deleteAll).place(relx=.67, rely=.45)

    # 复制按钮
    ttk.Button(
        frm, text="复制", width=8, command=lambda: pyperclip.copy(out_text.get("1.0", "end"))
    ).place(relx=.67, rely=.75)


if __name__ == '__main__':
    window = tk.Tk()
    window.title("翻译")
    screen_w, screen_h = window.winfo_screenwidth(), window.winfo_screenheight()
    width, height = int(screen_w / 6), int(screen_h / 4)
    window.geometry(f"{width}x{height}+{int(screen_w / 2)}+{int(screen_h / 4)}")
    window.resizable(False, False)

    f = ttk.Frame(window)
    frameTran(f)
    f.place(relx=0, rely=0, width=width, height=height)

    window.mainloop()
