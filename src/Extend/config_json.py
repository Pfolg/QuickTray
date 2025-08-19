# -*- coding: UTF-8 -*-
"""
PROJECT_NAME QuickTray
PRODUCT_NAME PyCharm
NAME config_json
AUTHOR Pfolg
TIME 2025/8/19 11:19
"""
import json
import os

from .string_data import Data


def read_config_json(config_file:str) -> dict:
    if os.path.exists(config_file):
        with open(config_file, "r", encoding="utf-8") as file1:
            config: dict = json.load(file1)
        if not config:
            print("your config is empty, rewrite……")
            config = setup_config_json(config_file)
        config["useCount"] += 1
        config["version"] = Data.version
        with open(config_file, "w", encoding="utf-8") as file2:
            json.dump(config, file2, indent=4, ensure_ascii=False)
        print("config Changed!")
        return config
    else:
        return setup_config_json(config_file)


def setup_config_json(config_file:str) -> dict:
    config = {
        "tip": Data.app_name,
        "version": Data.version,
        "logo": Data.picture_luabackend,
        "useCount": 0,
        "port": Data.port,
        "autorun": Data.isautorun,
        "language": "en",  # en zh
        "hourAlarm": False
    }
    with open(config_file, "w", encoding="utf-8") as file:
        json.dump(config, file, ensure_ascii=False, indent=4)
    return config


def write_config_json(config_file:str,key: str, value) -> None:
    if os.path.exists(config_file):
        try:
            with open(config_file, "r", encoding="utf-8") as f1:
                org: dict = json.load(f1)

            if org.get(key):
                # 使用isinstance会发生错误
                if type(value) == type(org.get(key)):
                    org[key] = value
                    with open(config_file, "w", encoding="utf-8") as f2:
                        json.dump(org, f2, indent=4, ensure_ascii=False)
                else:
                    print("instance is not suitable.")
        except Exception as e:
            print("an error happened in writing config: ", e)
            setup_config_json(config_file)
    else:
        setup_config_json(config_file)

