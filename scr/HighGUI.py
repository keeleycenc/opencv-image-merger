# HighGUI.py

"""
高级图形用户界面
-----------------------

Author: keeleycenc
Created on: 2023-12-30
Last Modified: 2023-12-30

Description:
    使用OpenCV的图形用户界面

Dependencies:
    - OpenCV
"""

import cv2
import numpy as np
from image_processing import remove_backgrounds
from image_merging import merge_images_overlap
from config import save_config_to_json, load_config_from_json, CONFIG
from rich.console import Console

console = Console()

# 轨迹条初始化的问题，需要使用标志表示已完成才能调用on_trackbar_change函数，不然会报错
trackbars_created = False

def on_trackbar_change(image_paths, _):
    """
    响应轨迹条值变化，更新图像的颜色阈值，并展示处理后的图像。

    Args:
        image_paths (list of str): 要处理的图像路径列表。
        _: 未使用的参数，通常是轨迹条的当前值。
    """
    global lower_bound, upper_bound, trackbars_created

    if not trackbars_created:
        return
    
    config = CONFIG.get('MERGE_METHOD', 'weighted')

    # 获取轨迹条当前位置作为颜色边界值
    lower_bound = [cv2.getTrackbarPos('LowerBound' + ch, 'Adjust Colors') for ch in ['B', 'G', 'R']]
    upper_bound = [cv2.getTrackbarPos('UpperBound' + ch, 'Adjust Colors') for ch in ['B', 'G', 'R']]

    # 用于展示处理结果的临时变量
    temp_foregrounds = remove_backgrounds(image_paths, np.array(lower_bound), np.array(upper_bound))
    temp_merged_image = merge_images_overlap(temp_foregrounds, method=config)
    
    # 显示处理后的图像
    cv2.imshow('Adjusted Merged Image', temp_merged_image)

def adjust_colors_and_preview(image_paths):
    """
    创建一个窗口和轨迹条，允许用户实时调整颜色阈值，并展示处理后的图像效果。

    Args:
        image_paths (list of str): 要处理的图像路径列表。
    """
    global lower_bound, upper_bound, trackbars_created

    # 加载配置
    config = load_config_from_json()
    lower_bound = config.get("LOWER_BOUND_COLOR", [0, 0, 0])
    upper_bound = config.get("UPPER_BOUND_COLOR", [255, 255, 255])

    # 创建窗口和轨迹条
    cv2.namedWindow('Adjust Colors')
    for i, ch in enumerate(['B', 'G', 'R']):
        cv2.createTrackbar('LowerBound' + ch, 'Adjust Colors', lower_bound[i], 255, lambda _: on_trackbar_change(image_paths, _))
        cv2.createTrackbar('UpperBound' + ch, 'Adjust Colors', upper_bound[i], 255, lambda _: on_trackbar_change(image_paths, _))

     # 设置标志，表示所有轨迹条已创建
    trackbars_created = True

    # 初始调用一次以更新显示
    on_trackbar_change(image_paths, None)

    instructions = [
        ("[bold green]'s' 键[/bold green]", "保存设置"),
        ("[bold red]'ESC' 键[/bold red]", "退出程序"),
    ]

    console.print("[bold underline]key[/bold underline]", justify="center")
    for key, action in instructions:
        console.print(f"{key} : [bold]{action}[/bold]")

    while True:
        # 按键检测
        key = cv2.waitKey(1) & 0xFF

        # 检查窗口是否关闭
        if cv2.getWindowProperty('Adjust Colors', cv2.WND_PROP_VISIBLE) < 1:  
            break

        if key == ord('s'):  # 按 's' 键保存设置
            save_config_to_json(lower_bound, upper_bound)
            print("Settings saved.")
        elif key == 27:  # 按 'ESC' 键退出
            break



