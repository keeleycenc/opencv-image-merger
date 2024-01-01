# main.py

"""
Main Module
-----------

Author: keeleycenc
Created on: 2023-12-27
Last Modified: 2023-12-31

Description:
    This is the main entry point of the application. 

Usage:
    Run this script to start the application. Ensure all dependencies are
    installed and necessary files are in place.

Dependencies:
    - OpenCV
    - NumPy
    - Rich
"""

import cv2
import numpy as np
import json
import time
import random
from image_merging import merge_images_overlap
from file_utils import save_image, select_image_paths_gui
from image_processing import remove_backgrounds
from config import CONFIG
from HighGUI import adjust_colors_and_preview, type_print
from rich.console import Console
from rich.traceback import install
from rich.table import Table
from rich.progress import Progress

# 安装全局异常处理器
install()

# 创建一个 Console 实例用于打印
console = Console()

# 创建 Table 实例
table = Table(show_header=True, header_style="bold magenta")
table.add_column("ID", style="dim", width=6)
table.add_column("name", min_width=12)
table.add_column("Description")

# 向表格中添加行
table.add_row("1", "MAX_IMAGES", "需要合并的图像数量")
table.add_row("2", "IMAGES", "需要合并图像的文件路径")
table.add_row("3", "COMBINED_IMAGE", "保存合并图像文件路径")
table.add_row("4", "MERGE_METHOD", "图片合并方法weighted or simple")
table.add_row("5", "LOWER_BOUND_COLOR", "要移除的颜色范围的下界（HSV格式）")
table.add_row("6", "UPPER_BOUND_COLOR", "要移除的颜色范围的上界（HSV格式）")

# http://patorjk.com/software/taag/
MAS = """
███╗   ███╗     █████╗     ███████╗
████╗ ████║    ██╔══██╗    ██╔════╝
██╔████╔██║    ███████║    ███████╗
██║╚██╔╝██║    ██╔══██║    ╚════██║
██║ ╚═╝ ██║    ██║  ██║    ███████║
╚═╝     ╚═╝    ╚═╝  ╚═╝    ╚══════╝
"""

def print_json_file(file_path):
    """
    打印获取json文件的状态

    Args:
        file_path (str): json文件路径
    """
    try:
        with open(file_path, 'r') as file:
            # 读取 JSON 数据
            data = json.load(file)

            # 将 JSON 数据转换为字符串，以便格式化输出
            json_str = json.dumps(data, indent=4)

            # 打印 JSON 字符串
            console.print(json_str)

    except FileNotFoundError:
        console.print(f"[bold red]Error: File '{file_path}' does not exist. Using default configuration.[/bold red]")
    except json.JSONDecodeError:
        console.print(f"[bold red]Error: Unable to parse the JSON file '{file_path}'. Using default configuration.[/bold red]")


def text_progress_bar(duration):
    """
    加载动画

     Args:
        duration: 持续时间（秒）  
    """
    progress_list = ["\\", "|", "/", "—"]
    start_time = time.time()

    while time.time() - start_time < duration:
        for symbol in progress_list:
            print(f"\r{symbol}", end="")
            time.sleep(duration / len(progress_list) / 5)  # 控制旋转速度
    
    print("\n", end="")


def display_progress(min_duration, max_duration):
    """
    使用Rich库的进度条。 持续给定的时间（秒）。好让客户给钱优化

     Args:
        param min_duration: 最小持续时间（秒）
        param max_duration: 最大持续时间（秒）
    """
    duration = random.uniform(min_duration, max_duration)
    with Progress() as progress:
        task = progress.add_task("[red]Loading...", total=100)

        for i in range(100):
            time.sleep(duration / 100)
            progress.update(task, advance=1)

    console.print(f"Progress completed in {duration:.2f} seconds!")



def main():
    """
    主程序入口
    """
    console.rule("[bold red]Ver1.2.1",align='center')
    type_print(console, MAS, delay=0.01, style="red")
    # 加载动画
    text_progress_bar(1.88)
    # 打印表格
    console.print(table)
    # 读取配置文件，如果不存在，则使用默认配置
    console.print("Load configuration file...")
    config_file = 'config.json'
    print_json_file(config_file)
    config = CONFIG.get('MERGE_METHOD', 'simple')
    folder_path = CONFIG.get('IMAGES', 'images')
    combined_image = CONFIG.get('COMBINED_IMAGE', 'combined_image')
    lower_bound_color = np.array(CONFIG.get('LOWER_BOUND_COLOR', [0, 0, 0]))
    upper_bound_color = np.array(CONFIG.get('UPPER_BOUND_COLOR', [255, 75, 255]))
    
    # 获取图片文件
    console.print("Execution:[italic green] Get picture file [/italic green]")
    display_progress(0.1,0.5) 
    image_paths = select_image_paths_gui(folder_path)

    # 移除每张图片的背景
    console.print("Execution: [italic green] Remove the background of each image [/italic green]")
    display_progress(0.5, 1.5)
    foregrounds = remove_backgrounds(image_paths, lower_bound_color, upper_bound_color)

    # 合并图片
    console.print("Execution: [italic green] Picture merge [/italic green]")
    display_progress(0.5, 2)
    merged_image = merge_images_overlap(foregrounds, method=config)

    # 保存图片
    console.print("Execution: [italic green] Saving image [/italic green]")
    display_progress(0.1, 0.5)
    save_image(merged_image, combined_image)    

    # GUI
    console.print("Execution: [italic green] load GUI [/italic green]")
    display_progress(1, 2)
    adjust_colors_and_preview(image_paths)

    console.rule("[bold red]Cutting line",align='center')

    # 关闭OpenCV窗口
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
