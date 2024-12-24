# -*- coding: utf-8 -*-
# Editor    PyCharm
# File   IntTimeNotify |Author    Pfolg
# 2024/12/16 19:54
import os.path
import time
from win10toast import ToastNotifier
from tkinter import messagebox

notify_title = "整点报时"
toast = ToastNotifier()
flag_file = "notify_int_time.flag"


def judge_program_is_running():
    if os.path.exists(flag_file):
        return False
    else:
        return True


def notify_int_time(text: str):
    toast.show_toast(
        title=notify_title,
        msg=text,
        icon_path=None,
        duration=5,
        threaded=False,
    )


def judge_time():
    with open(flag_file, "w", encoding="utf-8") as file:
        file.write("Delete this file to end the process!")
    while os.path.exists(flag_file):
        if time.localtime().tm_min == 0:
            notify_int_time(time.strftime("%H:%M"))
        time.sleep(10)


def main():
    if judge_program_is_running():
        try:
            print("running program...")
            messagebox.showinfo("整点报时", "running program...")
            judge_time()
        except KeyboardInterrupt:
            pass
        except Exception:
            pass
        finally:
            os.remove(flag_file)
            print("deleted " + flag_file)
    else:
        x = messagebox.askyesno(
            "Error", flag_file + " exists,\nPlease delete it to start new process!\nDelete it?")
        if x:
            os.remove(flag_file)


if __name__ == "__main__":
    main()
