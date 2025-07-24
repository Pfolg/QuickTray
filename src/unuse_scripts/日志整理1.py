# -*- coding: UTF-8 -*-
"""
PROJECT_NAME Python_projects
PRODUCT_NAME PyCharm
NAME 日志整理1
AUTHOR Pfolg
TIME 2025/3/23 19:44
"""
with open("request.log", "r", encoding="utf-8") as file:
    c = file.read()
# print(c)
c2 = c.replace("type", "hitokoto").split("hitokoto")
txt = []
for i in c2:
    if "from" in i:
        continue
    else:
        x = i.replace(",", ":").split(":")[1].strip("\"")
        if not x in txt:
            txt.append(x)
print(txt)
with open("lines1.txt", "w", encoding="utf-8") as file:
    for i in txt:
        file.writelines(i + "\n")
