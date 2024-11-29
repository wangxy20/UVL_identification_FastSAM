import os
import cv2
import numpy as np
import shutil
import argparse

# 创建空的txt文件
# Create an empty txt file
def create_empty_txt_file(file_path):
    with open(file_path, 'w') as empty_file:
        pass

# 生成带有标注的图像
# Generate an image with annotations
def generate_image(img_path, txt_path, save_path):
    img = cv2.imread(img_path)  # 读取图像
    img_x, img_y = img.shape[0], img.shape[1]  # 获取图像的高度和宽度

    try:
        with open(txt_path, "r") as f:
            data_lines = f.read().splitlines()  # 读取所有行，每行是一个标注
        print(f"Read data from {txt_path}")  # 打印读取信息

        img_result = np.zeros((img_x, img_y, 3), dtype=np.uint8)  # 创建一个空白图像，用于绘制标注
        
        # 遍历每行标注数据
        # Iterate over each line of annotation data
        for line in data_lines:
            d = line.split(' ', -1)  # 以空格分割每行数据
            data = []
            # 将标注的坐标转换为图像上的坐标
            # Convert annotation coordinates to image coordinates
            for i in range(1, int(len(d) / 2) + 1):
                data.append([img_y * float(d[2 * i - 1]), img_x * float(d[2 * i])])
            data = np.array(data, dtype=np.int32)  # 转换为整数类型的坐标

            # 如果标注数据有效，绘制多边形
            # If the annotation data is valid, draw the polygon
            if data.any():
                color = (250, 250, 250)  # 设置绘制颜色，白色
                cv2.fillPoly(img_result, [data], color=color)  # 在图像上绘制多边形

        cv2.imwrite(save_path, img_result)  # 保存生成的图像

    except FileNotFoundError:
        # 如果标注文件未找到，生成一个空图像并保存
        # If the annotation file is not found, create an empty image and save
        print(f"Warning: {txt_path} not found. Creating an empty data array.")
        img_result = np.zeros((img_x, img_y, 3), dtype=np.uint8)  # 创建空白图像
        cv2.imwrite(save_path, img_result)  # 保存空白图像

# 输入参数配置
# Command line arguments
parser = argparse.ArgumentParser(description='test')
parser.add_argument('--img_dir', type=str, default='./predict/images', help='预测图片的地址')  # 预测图像文件夹路径
parser.add_argument('--txt_dir0', type=str, default='./runs/segment/predict/labels/', help='预测图片的txt原始存储地址')  # 原始标注文件夹路径
parser.add_argument('--save_dir', type=str, default='./predict/output/', help='图片保存地址')  # 保存带标注的图像文件夹路径
parser.add_argument('--txt_dir', type=str, default='./predict/labels/', help='txt文件的移动地址')  # 目标标注文件夹路径
args = parser.parse_args()  # 解析命令行参数

# 如果目标目录不存在，创建它
# Create target directory if it does not exist
if not os.path.exists(args.txt_dir):
    os.makedirs(args.txt_dir)

# 获取源目录中的所有文件并复制到目标目录
# Get all files from source directory and copy to target directory
for filename in os.listdir(args.txt_dir0):
    source_path = os.path.join(args.txt_dir0, filename)
    destination_path = os.path.join(args.txt_dir, filename)
    
    # 复制文件
    # Copy files
    shutil.copy(source_path, destination_path)

# 补全所有txt文件（如果图片中未检测到UVL，下面代码会报错）
# Ensure all txt files exist for the images (if any image is missing a txt file, this will create an empty one)
def match_files(img_dir, txt_dir):
    # 获取img_dir中的所有jpg文件
    # Get all jpg files from img_dir
    img_files = [f.path for f in os.scandir(img_dir) if f.is_file() and f.name.endswith('.jpg')]

    # 获取txt_dir中的所有txt文件
    # Get all txt files from txt_dir
    txt_files = [f.path for f in os.scandir(txt_dir) if f.is_file() and f.name.endswith('.txt')]

    # 获取img_dir中文件名（不包含扩展名）
    # Get filenames from img_dir without extension
    img_filenames = {os.path.splitext(os.path.basename(file))[0] for file in img_files}

    # 获取txt_dir中文件名（不包含扩展名）
    # Get filenames from txt_dir without extension
    txt_filenames = {os.path.splitext(os.path.basename(file))[0] for file in txt_files}

    # 计算差集，即需要在txt_dir中补全的文件名
    # Calculate the missing filenames (those that need a txt file in txt_dir)
    missing_filenames = img_filenames - txt_filenames

    # 遍历需要补全的文件名，创建空的txt文件
    # Iterate over missing filenames and create empty txt files for them
    for filename in missing_filenames:
        empty_txt_path = os.path.join(txt_dir, f'{filename}.txt')
        create_empty_txt_file(empty_txt_path)
        print(f"创建空文件：{empty_txt_path}")  # 打印创建的空文件路径

# 补全txt文件
# Ensure all txt files are present
match_files(args.img_dir, args.txt_dir)

# 正式开始转换
# Start processing the images
files = os.listdir(args.img_dir)
for file in files:
    if file.endswith('.jpg'):  # 只处理jpg文件
        name = file[0:-4]  # 获取文件名（去掉扩展名）
        img_path = os.path.join(args.img_dir, name + '.jpg')  # 图像路径
        txt_path = os.path.join(args.txt_dir, name + '.txt')  # 标注文件路径
        save_path = os.path.join(args.save_dir, name + '.jpg')  # 保存路径
        generate_image(img_path, txt_path, save_path)  # 调用生成图像的函数
    else:
        continue  # 跳过非jpg文件