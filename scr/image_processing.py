# image_processing.py

"""
图像处理模块
-----------------------

Author: keeleycenc
Created on: 2023-12-27
Last Modified: 2023-12-30

Description:
    该模块提供了处理图像的功能，包括背景删除、调整大小和颜色转换。
    它与各种图像格式一起使用，并支持单个和批量处理图像。

Dependencies:
    - OpenCV
"""

import cv2


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
    # 反转掩码，以便保留非指定颜色的部分
    mask_inv = cv2.bitwise_not(mask)
    # 应用掩码，只保留颜色在指定范围内的部分
    res = cv2.bitwise_and(image, image, mask=mask_inv)
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