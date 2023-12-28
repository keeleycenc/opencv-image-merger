# image_processing.py

"""
图像处理模块
-----------------------

Author: keeleycenc
Created on: 2023-12-27
Last Modified: 2023-12-28

Description:
    该模块提供了处理图像的功能，包括背景删除、调整大小和颜色转换。
    它与各种图像格式一起使用，并支持单个和批量处理图像。

Dependencies:
    - OpenCV
"""

import cv2
import os
from datetime import datetime

def get_image_paths(folder_path, max_images=5):
    """
    获取指定文件夹下的图像文件路径，支持多种图像格式，最多返回 max_images 数量的图像路径。

    Args:
        folder_path (str): 图像文件夹的路径。
        max_images (int): 最大获取的图像数量。

    Returns:
        list: 包含图像路径的列表。
    """
    # 支持的图像文件扩展名
    supported_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.gif']

    # 获取文件夹中所有文件
    all_files = os.listdir(folder_path)

    # 筛选出图像文件
    image_files = [file for file in all_files if os.path.splitext(file)[1].lower() in supported_extensions]

    # 获取前 max_images 张图像的路径
    image_paths = [os.path.join(folder_path, file) for file in image_files[:max_images]]

    return image_paths


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

def remove_background(image_path, lower_bound_color, upper_bound_color):
    """
    移除图片中特定颜色范围的背景。

    Args:
        image_path (str): 图片的路径。
        lower_bound_color (numpy.ndarray): 要移除的颜色范围的下界（HSV格式）。
        upper_bound_color (numpy.ndarray): 要移除的颜色范围的上界（HSV格式）。

    Returns:
        numpy.ndarray: 移除特定颜色背景后的图片。
    """
    # 读取图片
    image = cv2.imread(image_path)
    # 将图片从BGR颜色空间转换到HSV颜色空间
    hsv_img = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    # 创建一个掩码，仅保留指定颜色范围内的区域
    mask = cv2.inRange(hsv_img, lower_bound_color, upper_bound_color)
    # 应用掩码，只保留颜色在指定范围内的部分
    res = cv2.bitwise_and(image, image, mask=mask)
    return res


def remove_backgrounds(image_paths, lower_bound_color, upper_bound_color):
    """
    对多张图片应用背景移除。

    Args:
        image_paths (list of str): 图片路径的列表。
        lower_bound_color (numpy.ndarray): 要移除的颜色范围的下界（HSV格式）。
        upper_bound_color (numpy.ndarray): 要移除的颜色范围的上界（HSV格式）。

    Returns:
        list of numpy.ndarray: 移除背景后的图片列表。
    """
    foregrounds = []
    for path in image_paths:
        # 对每张图片应用背景移除
        fg = remove_background(path, lower_bound_color, upper_bound_color)
        foregrounds.append(fg)
    return foregrounds



def resize_image_to_same_size(images):
    """
    调整一组图片的尺寸，使它们具有相同的宽度和高度。

    Args:
        images (list of numpy.ndarray): 包含图像数组的列表。

    Returns:
        list of numpy.ndarray: 尺寸调整后的图片列表。
    """
    # 找到最小的宽度和高度
    min_height = min(image.shape[0] for image in images)
    min_width = min(image.shape[1] for image in images)
    # 调整所有图片到相同的尺寸
    resized_images = [cv2.resize(image, (min_width, min_height)) for image in images]
    return resized_images


def ensure_color_images(images):
    """
    确保所有图片都是彩色的（BGR格式）。

    Args:
        images (list of numpy.ndarray): 包含图像数组的列表。

    Returns:
        list of numpy.ndarray: 转换为彩色后的图片列表。
    """
    color_images = []
    for image in images:
        # 如果是灰度图像，转换为彩色图像
        if len(image.shape) == 2:  
            color_image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
        else:
            color_image = image
        color_images.append(color_image)
    return color_images