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
import math
from image_processing import resize_image_to_same_size, ensure_color_images
from rich.console import Console
from config import CONFIG

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


def merge_images_grid(images, placeholder_image_path, output_size=(1024, 1024)):
    """
    将图像拼接成网格, 为保证视觉均衡不足部分将使用占位图像填充。

    Args:
        images (list of numpy.ndarray): 需要拼接的图像列表。
        placeholder_image_path (str): 占位图像的路径。
        output_size (tuple, optional): 拼接后的图像大小，格式为(width, height)。

    Returns:
        numpy.ndarray: 拼接后的图像。

    Raises:
        ValueError: 如果图像数量不在1到9之间
    """
    num_images = len(images)
    if num_images < 1 or num_images > 9:
        raise ValueError("图像数量不符")

    # 加载占位图像
    placeholder_image = cv2.imread(placeholder_image_path)
    if placeholder_image is None:
        raise ValueError("无法加载占位图像")

    # 确定网格大小
    grid_size = math.ceil(math.sqrt(num_images))
    if grid_size < 1:
        grid_size = 1

    # 确保图像大小一致
    images = resize_image_to_same_size(images)

    # 获取图像宽度和高度
    height, width = images[0].shape[:2]

    # 调整占位图像尺寸以匹配其他图像
    placeholder_image = cv2.resize(placeholder_image, (width, height), interpolation=cv2.INTER_AREA)

    # 创建一个空白画布
    grid_height = height * grid_size
    grid_width = width * grid_size
    grid = np.zeros((grid_height, grid_width, 3), dtype=np.uint8)

    # 将图像和占位图像放置在正确的位置
    for i in range(grid_size * grid_size):
        row = i // grid_size
        col = i % grid_size
        if i < num_images:
            grid[row * height:(row + 1) * height, col * width:(col + 1) * width] = images[i]
        else:
            grid[row * height:(row + 1) * height, col * width:(col + 1) * width] = placeholder_image

    # 调整图像大小以匹配输出尺寸
    grid = cv2.resize(grid, output_size, interpolation=cv2.INTER_AREA)

    return grid


def merge_images_overlap(images, method='weighted'):
    """
    根据指定的方法合并图像。
    weighted: 为每张图像分配相等的权重
    simple  : 仅简单地叠加图像。
    grid    : 通过网格拼接

    Args:
        images (list of numpy.ndarray): 需要合并的图像列表。
        method (str, optional): 图像合并或拼接的方法。

    Returns:
        numpy.ndarray: 根据指定方法合并后的图像。

    Raises:
        ValueError: 方法未找到或不存在
    """

    placeholder_image_path = CONFIG.get('PLACEHOLDER', 'images/missing.jpg')

    if method == 'weighted':
        return merge_images_weighted(images)
    elif method == 'simple':
        return merge_images_simple(images)
    elif method == 'grid' :
        return merge_images_grid(images, placeholder_image_path, output_size=(1024, 1024))
    else:
        raise ValueError("Unknown merge method: {}".format(method))







    

