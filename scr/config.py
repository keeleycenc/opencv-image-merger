# config.py

"""
配置文件
-----------------------

Author: keeleycenc
Created on: 2023-12-29
Last Modified: 2023-12-29

Description:
    可以在项目的任何地方导入这个模块来访问配置

Dependencies:
    none
"""

import json

def load_config(config_file):
    try:
        with open(config_file, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"配置文件 {config_file} 未找到。使用默认配置。")
        return {}
    except json.JSONDecodeError:
        print(f"配置文件 {config_file} 格式错误。")
        return {}

# 加载配置文件
CONFIG = load_config('config.json')
