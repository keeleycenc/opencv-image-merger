# image_merging.py

"""
图像合并模块
-----------------------

Author: keeleycenc
Created on: 2023-12-27
Last Modified: 2023-12-30

Description:
    将处理后的所有图像进行重叠合并

Dependencies:
    - OpenCV
    - NumPy
"""

import cv2
import numpy as np
from image_processing import resize_image_to_same_size, ensure_color_images
from rich.console import Console

# 创建一个 Console 实例用于打印
console = Console()


def merge_images_weighted(images):
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


def merge_images_simple(images):
    """
    将多张图片通过叠加合并成一张图片。

    Args:
        images (list of numpy.ndarray): 包含图像数组的列表。

    Returns:
        numpy.ndarray: 合并后的图片。
    """
    images = resize_image_to_same_size(images)  # 确保图片大小一致
    images = ensure_color_images(images)        # 确保图片都是彩色的

    # 初始化合并图像为第一张图片
    merged_image = images[0].copy()

    # 逐张图片叠加
    for img in images[1:]:
        merged_image = cv2.add(merged_image, img)

    # 规范化像素值
    merged_image = np.clip(merged_image, 0, 255)

    return merged_image


def merge_images_overlap(images, method='weighted'):
    """
    根据指定的方法合并图像。
    weighted: 为每张图像分配相等的权重
    simple  : 仅简单地叠加图像。

    Args:
        images (list of numpy.ndarray): 需要合并的图像列表。
        method (str, optional): 图像合并的方法。

    Returns:
        numpy.ndarray: 根据指定方法合并后的图像。

    Raises:
        ValueError: 方法未找到或不存在
    """
    if method == 'weighted':
        return merge_images_weighted(images)
    elif method == 'simple':
        return merge_images_simple(images)
    else:
        raise ValueError("Unknown merge method: {}".format(method))





    

