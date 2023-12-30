# config.py

"""
配置文件
-----------------------

Author: keeleycenc
Created on: 2023-12-29
Last Modified: 2023-12-30

Description:
    可以在项目的任何地方导入这个模块来访问配置
    MAX_IMAGES: 合图像的数量
    IMAGES: 合并图像文件的路径
    COMBINED_IMAGE: 保持合并图像文件路径
    MERGE_METHOD: 不同的图片合并方法，"weighted" 或者 "simple" 可选
    LOWER_BOUND_COLOR: 要移除的颜色范围的下界（HSV格式）
    UPPER_BOUND_COLOR: 要移除的颜色范围的上界（HSV格式）

Dependencies:
    none
"""

import json

def load_config(config_file):
    """
    从指定的文件中加载配置。

    Args:
        config_file (str): JSON 配置文件的路径。

    Returns:
        dict: 解析后的配置数据。
    """
    try:
        with open(config_file, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"配置文件 {config_file} 未找到。程序将终止。")
        input("按任意键退出...")
        exit(1)  # 使用非零值表示错误退出
    except json.JSONDecodeError:
        print(f"配置文件 {config_file} 格式错误。程序将终止。")
        input("按任意键退出...")
        exit(1)


def load_config_from_json(filepath='config.json', default_config=None):
    """
    从 JSON 文件中加载配置

    Args:
        filepath (str): JSON 文件的路径。默认为 'config.json'。
        default_config (dict, optional): 当文件不存在时使用的默认配置。如果为 None，
                                         则使用预定义的默认配置。

    Returns:
        dict: 解析后的配置数据，或默认配置。
    """
    if default_config is None:
        default_config = {
            "LOWER_BOUND_COLOR": [0, 0, 0],
            "UPPER_BOUND_COLOR": [255, 255, 255]
        }

    try:
        with open(filepath, 'r') as file:
            config_data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        config_data = default_config

    return config_data


def save_config_to_json(lower_bound, upper_bound, filepath='config.json'):
    """
    读取现有的 JSON 配置文件, 将当前的颜色阈值保存到 JSON 文件。

    Args:
        lower_bound (list): 颜色的下界值。
        upper_bound (list): 颜色的上界值。
        filepath (str): JSON 文件的保存路径。默认为 'config.json'。
    """
    try:
        # 首先读取现有配置
        with open(filepath, 'r') as file:
            config_data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        config_data = {}

    # 更新颜色阈值
    config_data["LOWER_BOUND_COLOR"] = lower_bound
    config_data["UPPER_BOUND_COLOR"] = upper_bound

    # 将更新后的配置写回文件
    with open(filepath, 'w') as file:
        json.dump(config_data, file, indent=4)


# 加载配置文件
CONFIG = load_config('config.json')
