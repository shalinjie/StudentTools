# -*- coding: utf-8 -*-
from PIL import Image, ImageDraw, ImageFont
import random
import os
import datetime

# 设置A4纸尺寸 (2480x3508 pixels, 300dpi)
A4_WIDTH = 2480
A4_HEIGHT = 3508
MARGIN = 100  # 页边距
TABLE_SPACING = 50  # 表格之间的间距

# 字体路径 (根据系统选择合适的字体路径)
FONT_PATH = "arial.ttf"  # Windows系统
# FONT_PATH = "/Library/Fonts/Arial.ttf"  # macOS系统
# FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"  # Linux系统

# 表格参数
TABLE_ROWS = 4
TABLE_COLS = 9
CELL_WIDTH = 150
CELL_HEIGHT = 100
FONT_SIZE = 30

# 创建 images 目录（如果不存在）
if not os.path.exists("images"):
    os.makedirs("images")


# 随机生成第一行和第一列的数字
def generate_table_data():
    # 第一行 (1到8列)
    first_row = [random.randint(1, 9) for _ in range(TABLE_COLS - 1)]
    first_row.insert(0, "+")  # 第一列第一行是 "+"

    # 第一列 (2到4行)
    first_col = [random.randint(1, 9) for _ in range(TABLE_ROWS - 1)]
    first_col.insert(0, "+")  # 第一行第一列是 "+"

    return first_row, first_col


# 计算表格中某个空格的值
def calculate_cell_value(row, col, first_row, first_col):
    if row == 0 or col == 0:  # 第一行或第一列
        return first_row[col] if row == 0 else first_col[row]
    else:  # 其他空格
        return first_row[col] + first_col[row]


# 绘制一个表格
def draw_table(draw, start_x, start_y, first_row, first_col):
    font = ImageFont.truetype(FONT_PATH, FONT_SIZE)

    for row in range(TABLE_ROWS):
        for col in range(TABLE_COLS):
            # 计算单元格的坐标
            x = start_x + col * CELL_WIDTH
            y = start_y + row * CELL_HEIGHT

            # 绘制单元格边框
            draw.rectangle([x, y, x + CELL_WIDTH, y + CELL_HEIGHT], outline="black")

            # 如果是第一行或第一列，填充数字
            if row == 0 or col == 0:
                cell_value = calculate_cell_value(row, col, first_row, first_col)
                text = str(cell_value) if cell_value != "+" else "+"

                # 计算文本尺寸
                text_bbox = font.getbbox(text)
                text_width = text_bbox[2] - text_bbox[0]
                text_height = text_bbox[3] - text_bbox[1]

                # 居中绘制文本
                draw.text(
                    (x + (CELL_WIDTH - text_width) // 2, y + (CELL_HEIGHT - text_height) // 2),
                    text,
                    fill="black",
                    font=font
                )


# 随机选择两个空格并填写答案
def fill_example_answers(draw, start_x, start_y, first_row, first_col):
    font = ImageFont.truetype(FONT_PATH, FONT_SIZE)

    # 随机选择两个空格（排除第一行和第一列）
    example_cells = random.sample(
        [(row, col) for row in range(1, TABLE_ROWS) for col in range(1, TABLE_COLS)],
        2
    )

    for row, col in example_cells:
        # 计算单元格的坐标
        x = start_x + col * CELL_WIDTH
        y = start_y + row * CELL_HEIGHT

        # 计算单元格的值
        cell_value = calculate_cell_value(row, col, first_row, first_col)
        text = str(cell_value)

        # 计算文本尺寸
        text_bbox = font.getbbox(text)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]

        # 居中绘制文本
        draw.text(
            (x + (CELL_WIDTH - text_width) // 2, y + (CELL_HEIGHT - text_height) // 2),
            text,
            fill="black",
            font=font
        )


# 生成一页A4纸的图片
def generate_a4_page():
    # 创建空白A4纸图片
    image = Image.new("RGB", (A4_WIDTH, A4_HEIGHT), "white")
    draw = ImageDraw.Draw(image)

    # 计算每个表格的宽度和高度
    table_width = CELL_WIDTH * TABLE_COLS
    table_height = CELL_HEIGHT * TABLE_ROWS

    # 计算每行和每列可以放置的表格数量
    tables_per_row = (A4_WIDTH - 2 * MARGIN) // (table_width + TABLE_SPACING)
    tables_per_col = (A4_HEIGHT - 2 * MARGIN) // (table_height + TABLE_SPACING)

    # 计算表格的起始坐标（居中）
    start_x = (A4_WIDTH - (tables_per_row * table_width + (tables_per_row - 1) * TABLE_SPACING)) // 2
    start_y = (A4_HEIGHT - (tables_per_col * table_height + (tables_per_col - 1) * TABLE_SPACING)) // 2

    # 生成并绘制多个表格
    for i in range(tables_per_row):
        for j in range(tables_per_col):
            # 计算当前表格的起始坐标
            table_start_x = start_x + i * (table_width + TABLE_SPACING)
            table_start_y = start_y + j * (table_height + TABLE_SPACING)

            # 生成表格数据
            first_row, first_col = generate_table_data()

            # 绘制表格
            draw_table(draw, table_start_x, table_start_y, first_row, first_col)

            # 填写两个空格的答案
            fill_example_answers(draw, table_start_x, table_start_y, first_row, first_col)

    # 保存图片
    current_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    image_path = os.path.join("images", f"biaogeguilv-{current_time}.jpg")
    image.save(image_path)
    print(f"A4纸图片已生成：{image_path}")


# 运行代码
generate_a4_page()