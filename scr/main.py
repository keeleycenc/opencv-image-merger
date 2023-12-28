# main.py

"""
Main Module
-----------

Author: keeleycenc
Created on: 2023-12-27
Last Modified: 2023-12-28

Description:
    This is the main entry point of the application. 

Usage:
    Run this script to start the application. Ensure all dependencies are
    installed and necessary files are in place.

Dependencies:
    - OpenCV
    - NumPy
    - Other modules: image_processing, image_merging
"""

import cv2
import numpy as np
from image_merging import merge_images_overlap
from image_processing import get_image_paths, remove_backgrounds, save_image

def main():
    # 图片路径列表
    folder_path = 'images'  # 文件夹路径
    image_paths = get_image_paths(folder_path)

    # 设置颜色范围（黑到白）
    lower_bound_color = np.array([0, 0, 0])
    upper_bound_color = np.array([255, 255, 255])

    # 移除每张图片的背景
    foregrounds = remove_backgrounds(image_paths, lower_bound_color, upper_bound_color)

    # 合并图片并保存
    merged_image = merge_images_overlap(foregrounds)
    save_image(merged_image, "combined_image")

    # 显示合并后的图片
    cv2.imshow('Merged Image', merged_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
