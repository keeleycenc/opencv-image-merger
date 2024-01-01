# 图像处理和合并项目

这个项目包括处理和合并图像的功能。它使用OpenCV进行图像操作，支持背景移除和图像重叠合并。

## 系统环境

确保你的系统已安装[Python](https://www.python.org/)并添加环境变量

## 项目依赖

本项目依赖于`OpenCV` | `NumPy` | `Rich`。在开始之前，请确保安装了这些库。你可以使用以下命令进行安装：  

```bash
pip install opencv-python numpy

pip install rich
```

**注意事项:** 在windows下可能需要以管理员方式运行，有时候会权限不足无法写入文件

## 使用方法

运行main.py以启动应用程序。确保images及combined_image文件夹在项目根目录下，并且包含要处理的图像。

```bash
python src/main.py
```

## 脚本打包

1.安装PyInstaller：

```bash
pip install pyinstaller
```

2.脚本打包

```bash
pyinstaller --onefile scr/main.py
```

3.在 dist 文件夹能看到生成的 EXE 文件

- 在当前目录中创建一个文件夹用于放置合成所需的照片，文件夹名为“images”
- 在当前目录中创建一个文件夹用于生成合成照片的存放地，文件夹名为“combined_image”
- 双击运行exe
  
## 更新日志

<details>
    <summary>2024-01-01 [1.2.2]</summary>

1.新增函数 `timeit_decorator` 装饰器
  
</details>

<details>
    <summary>2023-12-31 [1.2.1]</summary>

1.新增 `Rich` 库，美化终端输出
  
</details>

<details>
    <summary>2023-12-30 [1.2.0]</summary>

1.新增opencv图形界面UI，详见 `HighGUI.py` 文件

2.新增 `cv2.bitwise_not` 来反转掩码，保留非指定颜色的部分

*反转前*

![反转前][1]

*反转后*

![反转后][2]

3.新增图片合并方法

4.其它优化

</details>

<details>
    <summary>2023-12-29 [1.1.0]</summary>

1.新增函数 `select_image_paths_gui`  

- 使用图形界面选择图像文件

2.新增 `config.json` 配置文件

</details>

<details>
    <summary>2023-12-28 [1.0.0]</summary>

1.新增函数 `get_image_paths`  

- 功能：获取指定文件夹下的图像文件路径，支持多种图像格式。如果该文件夹中的图像数量超过 *max_images* 指定的数量，它将只返回最前面的 *max_images* 张图像的路径。

2.新增函数 `save_image`  

- 功能：保存图像到指定文件夹，文件名以当前时间命名。
  
</details>

[1]: img/20231230_192923.jpg
[2]: img/20231230_192936.jpg
