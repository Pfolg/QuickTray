# -*- coding: UTF-8 -*-
"""
PROJECT_NAME Python_projects
PRODUCT_NAME PyCharm
NAME deleted_code
AUTHOR Pfolg
TIME 2025/6/14 12:52
"""
# def read_ini():
#     this_config = {}
#     if os.path.exists("config.ini"):
#         config = configparser.ConfigParser()
#         config.read('config.ini')
#         # 读取所有配置
#         for section in config.sections():
#             this_section = {}
#             for key in config[section]:
#                 this_section[key] = config[section][key]
#             this_config[section] = this_section
#         print(this_config)
#         if not this_config:
#             print("your config is empty, rewrite……")
#             config["tray"] = {
#                 "tip": "QkStart With WaterMark",
#                 "logo": "assets/snowflake.png"
#             }
#             config["infor"] = {
#                 "usecount": "0",
#                 "port": "20082",
#                 "autorun": False,
#             }
#             this_config = {
#                 'tray': {'tip': 'QkStart With WaterMark', 'logo': 'assets/snowflake.png'},
#                 'infor': {'usecount': '0', "port": "20082", "autorun": False, }}
#
#         config["infor"]["useCount"] = str(eval(config["infor"]["useCount"]) + 1)
#         with open('config.ini', 'w', encoding="utf-8") as file:
#             config.write(file)
#             print("config.ini Changed!")
#         return this_config
#     else:
#         setup_ini()
#         return {'tray': {'tip': 'QkStart With WaterMark', 'logo': 'assets/snowflake.png'},
#                 'infor': {'usecount': '0', "port": "20082", "autorun": False, }}


# def setup_ini():
#     config = configparser.ConfigParser()
#     config["tray"] = {
#         "tip": "QkStart With WaterMark",
#         "logo": "assets/snowflake.png"
#     }
#     config["infor"] = {
#         "usecount": "0",
#         "port": "20082",
#         "autorun": False,
#     }
#     with open('config.ini', 'w', encoding="utf-8") as file:
#         config.write(file)
