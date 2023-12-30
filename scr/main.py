# main.py

"""
Main Module
-----------

Author: keeleycenc
Created on: 2023-12-27
Last Modified: 2023-12-30

Description:
    This is the main entry point of the application. 

Usage:
    Run this script to start the application. Ensure all dependencies are
    installed and necessary files are in place.

Dependencies:
    - OpenCV
    - NumPy
"""

import cv2
import numpy as np
from image_merging import merge_images_overlap
from file_utils import save_image, select_image_paths_gui
from image_processing import remove_backgrounds
from config import CONFIG
from HighGUI import adjust_colors_and_preview


def main():
    # 读取配置文件，如果不存在，则使用默认配置
    config = CONFIG.get('MERGE_METHOD', 'simple')
    folder_path = CONFIG.get('IMAGES', 'images')
    combined_image = CONFIG.get('COMBINED_IMAGE', 'combined_image')
    lower_bound_color = np.array(CONFIG.get('LOWER_BOUND_COLOR', [0, 0, 0]))
    upper_bound_color = np.array(CONFIG.get('UPPER_BOUND_COLOR', [255, 75, 255]))

    # 获取图片文件
    image_paths = select_image_paths_gui(folder_path)

    # 移除每张图片的背景
    foregrounds = remove_backgrounds(image_paths, lower_bound_color, upper_bound_color)

    # 合并图片
    merged_image = merge_images_overlap(foregrounds, method=config)

    # 保存图片
    save_image(merged_image, combined_image)

    # GUI
    adjust_colors_and_preview(image_paths)

    # 关闭OpenCV窗口
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
