# image_merging.py

"""
图像合并模块
-----------------------

Author: keeleycenc
Created on: 2023-12-27
Last Modified: 2023-12-28

Description:
    将处理后的所有图像进行重叠合并

Dependencies:
    - OpenCV
    - NumPy
"""

import cv2
import numpy as np
from image_processing import resize_image_to_same_size, ensure_color_images

def merge_images_overlap(images):
    """
    将多张图片通过加权重叠合并成一张图片。

    Args:
        images (list of numpy.ndarray): 包含图像数组的列表。

    Returns:
        numpy.ndarray: 合并后的图片。
    """
    images = resize_image_to_same_size(images)
    images = ensure_color_images(images)

    # 初始化合并图像为全黑图像
    height, width, channels = images[0].shape
    merged_image = np.zeros((height, width, channels), dtype=np.uint8)

    # 计算每张图像的权重
    alpha = 1.0 / len(images)

    for img in images:
        # 将每张图片加权后叠加到合并图像上
        merged_image = cv2.addWeighted(merged_image, 1.0, img, alpha, 0)

    return merged_image
