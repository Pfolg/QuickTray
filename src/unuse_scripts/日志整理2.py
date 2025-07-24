# -*- coding: UTF-8 -*-
"""
PROJECT_NAME Python_projects
PRODUCT_NAME PyCharm
NAME 日志整理2
AUTHOR Pfolg
TIME 2025/4/6 11:56
"""
import json
import time

with open("request.log", "r", encoding="utf-8") as file:
    content = file.readlines()

# print(content)
req = []
for item in content:
    x = json.loads(item.split(">")[1])
    # print(x)
    if x.get("hitokoto") and x.get("hitokoto") not in req:
        req.append(x.get("hitokoto"))
    elif x.get("data") and x.get("data").get("content") not in req:
        req.append(x.get("data").get("content"))

time.sleep(3)
with open("lines.txt", "r", encoding="utf-8") as lin:
    old_data = lin.readlines()

for i in old_data:
    j = i.strip()
    if not j in req:
        req.append(j)

print(req)
with open("lines.json", "w", encoding="utf-8") as file1:
    json.dump(req, file1, indent=4, ensure_ascii=False)
