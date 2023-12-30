# main.py

"""
文件处理模块
-----------------------

Author: keeleycenc
Created on: 2023-12-30
Last Modified: 2023-12-30

Description:
    此模块提供文件处理相关功能，包括获取图像文件路径和使用图形界面选择图像文件。
    它支持多种图像格式，并允许用户指定最大图像数量限制。

Dependencies:
    - OpenCV
"""

import cv2
import os
import tkinter as tk
from datetime import datetime
from tkinter import filedialog
from config import CONFIG


def get_image_paths(folder_path):
    """
    获取指定文件夹下的图像文件路径。支持多种图像格式，最多返回配置文件中设置的最大图像数量。

    Args:
        folder_path (str): 图像文件夹的路径。

    Returns:
        list: 包含图像路径的列表。
    """
    MAX_IMAGES = CONFIG.get('MAX_IMAGES', 4)
    supported_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.gif']

    try:
        # 获取文件夹中所有文件
        all_files = os.listdir(folder_path)

        # 筛选出图像文件
        image_files = [file for file in all_files if os.path.splitext(file)[1].lower() in supported_extensions]

        # 检查是否有图像文件
        if not image_files:
            raise ValueError("未找到支持的图像文件。")

        # 获取前 MAX_IMAGES 张图像的路径
        image_paths = [os.path.join(folder_path, file) for file in image_files[:MAX_IMAGES]]

        return image_paths

    except FileNotFoundError:
        print(f"无法找到文件夹: {folder_path}")
    except ValueError as e:
        print(e)
    except Exception as e:
        print(f"处理文件夹时遇到错误: {e}")

    print("请按任意键退出程序...")
    input()  # 等待用户按键
    exit()   # 退出程序


def select_image_paths_gui(folder_path):
    """
    使用图形界面选择图像文件。最多返回配置文件中设置的最大图像数量。

    Args:
        folder_path (str): 图像文件夹的默认路径。

    Returns:
        list: 包含用户选择的图像路径列表。
    """
    MAX_IMAGES = CONFIG.get('MAX_IMAGES',4)
    root = tk.Tk()
    root.withdraw()  # 不显示主窗口

    # 让用户选择图像文件
    file_paths = filedialog.askopenfilenames(
        initialdir=folder_path, 
        title="请选择图像文件",
        filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif")],
        multiple=True
    )

      # 如果用户没有选择任何文件，则默认 get_image_paths
    if not file_paths:
        return get_image_paths(folder_path)

    return list(file_paths)[:MAX_IMAGES]


def save_image(image, folder_path):
    """
    保存图像到指定文件夹，文件名以当前时间命名。

    Args:
        image (numpy.ndarray): 要保存的图像。
        folder_path (str): 图像要保存的文件夹路径。
    
    Returns:
        str: 保存的文件路径。
    """
    # 获取当前时间作为文件名，格式为 'YYYYMMDD_HHMMSS.jpg'
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = f"{folder_path}/{current_time}.jpg"

    # 保存图像
    cv2.imwrite(file_path, image)
    return file_path
