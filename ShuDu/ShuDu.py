# -*- coding: utf-8 -*-
import random
from PIL import Image, ImageDraw, ImageFont
import os
from datetime import datetime


def generate_sudoku(size):
    """生成指定大小的数独"""
    if size not in [4, 6, 9]:
        raise ValueError("尺寸必须是4、6或9")

    # 初始化空棋盘
    board = [[0 for _ in range(size)] for _ in range(size)]

    # 生成第一行
    first_row = list(range(1, size + 1))
    random.shuffle(first_row)
    board[0] = first_row

    # 使用回溯法填充其余部分
    if solve_sudoku(board, size):
        return board
    return None


def is_valid(board, row, col, num, size):
    """检查在给定位置放置数字是否有效"""
    # 检查行
    for x in range(size):
        if board[row][x] == num:
            return False

    # 检查列
    for x in range(size):
        if board[x][col] == num:
            return False

    # 检查方块
    block_size = 2 if size == 4 else (2 if size == 6 else 3)
    box_row = row - row % block_size
    box_col = col - col % block_size

    for i in range(box_row, box_row + block_size):
        for j in range(box_col, box_col + block_size):
            if board[i][j] == num:
                return False

    return True


def solve_sudoku(board, size):
    """使用回溯法解决数独"""
    empty = find_empty(board, size)
    if not empty:
        return True

    row, col = empty
    numbers = list(range(1, size + 1))
    random.shuffle(numbers)  # 随机尝试数字，使生成的数独更随机

    for num in numbers:
        if is_valid(board, row, col, num, size):
            board[row][col] = num
            if solve_sudoku(board, size):
                return True
            board[row][col] = 0

    return False


def find_empty(board, size):
    """找到棋盘上的空位置"""
    for i in range(size):
        for j in range(size):
            if board[i][j] == 0:
                return (i, j)
    return None


def create_puzzle(board, size):
    """创建谜题"""
    puzzle = [row[:] for row in board]
    cells_to_remove = {
        4: random.randint(6, 8),  # 减少4x4的移除数量
        6: random.randint(15, 20),  # 减少6x6的移除数量
        9: random.randint(30, 40)  # 减少9x9的移除数量
    }[size]

    positions = [(i, j) for i in range(size) for j in range(size)]
    random.shuffle(positions)

    for i, j in positions[:cells_to_remove]:
        puzzle[i][j] = 0

    return puzzle


def create_sudoku_image(boards, size, is_answer=False, original_boards=None):
    """将多个数独转换为A4大小的图片
    boards: 要显示的数独数组
    size: 数独大小
    is_answer: 是否是答案页
    original_boards: 原始题目数组，用于判断哪些数字是填空的
    """
    # A4纸张尺寸（像素，300DPI）
    width = 2480
    height = 3508

    # 创建白色背景的图片
    image = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(image)

    # 根据数独大小设置布局参数
    layout_config = {
        4: {"puzzles_per_row": 3, "puzzles_per_column": 5},
        6: {"puzzles_per_row": 3, "puzzles_per_column": 5},
        9: {"puzzles_per_row": 3, "puzzles_per_column": 5}
    }

    puzzles_per_row = layout_config[size]["puzzles_per_row"]
    puzzles_per_column = layout_config[size]["puzzles_per_column"]
    margin = 100  # 页面边距

    # 计算每个数独的网格大小
    grid_size = min((width - 2 * margin) // puzzles_per_row,
                    (height - 2 * margin) // puzzles_per_column)
    cell_size = grid_size // size

    # 设置字体大小
    normal_font_size = cell_size // 2
    bold_font_size = int(cell_size * 0.65)  # 粗体字号增大到原来的1.3倍
    try:
        normal_font = ImageFont.truetype("arial.ttf", normal_font_size)
        bold_font = ImageFont.truetype("arialbd.ttf", bold_font_size)
    except:
        normal_font = ImageFont.load_default()
        bold_font = normal_font

    # 计算实际起始位置以居中整体布局
    total_width = puzzles_per_row * grid_size + (puzzles_per_row - 1) * 50  # 50是数独之间的间距
    total_height = puzzles_per_column * grid_size + (puzzles_per_column - 1) * 50
    start_x = (width - total_width) // 2
    start_y = (height - total_height) // 2

    # 绘制多个数独
    for row in range(puzzles_per_column):
        for col in range(puzzles_per_row):
            if row * puzzles_per_row + col >= len(boards):
                break

            board = boards[row * puzzles_per_row + col]

            # 计算当前数独的起始位置
            current_x = start_x + col * (grid_size + 50)
            current_y = start_y + row * (grid_size + 50)

            # 绘制网格线
            block_size = 2 if size == 4 else (2 if size == 6 else 3)
            line_thin = max(1, cell_size // 50)
            line_thick = max(2, cell_size // 25)

            # 绘制所有网格线
            for i in range(size + 1):
                line_width = line_thick if i % block_size == 0 else line_thin
                # 垂直线
                draw.line([(current_x + i * cell_size, current_y),
                           (current_x + i * cell_size, current_y + grid_size)],
                          fill='black', width=line_width)
                # 水平线
                draw.line([(current_x, current_y + i * cell_size),
                           (current_x + grid_size, current_y + i * cell_size)],
                          fill='black', width=line_width)

            # 填写数字
            for i in range(size):
                for j in range(size):
                    if board[i][j] != 0:
                        num = str(board[i][j])
                        # 选择字体：如果是答案页且该位置在原题中是空的，使用粗体
                        if is_answer and original_boards and original_boards[row * puzzles_per_row + col][i][j] == 0:
                            font = bold_font
                        else:
                            font = normal_font

                        # 获取文字大小以居中显示
                        text_bbox = draw.textbbox((0, 0), num, font=font)
                        text_width = text_bbox[2] - text_bbox[0]
                        text_height = text_bbox[3] - text_bbox[1]
                        x = current_x + j * cell_size + (cell_size - text_width) // 2
                        y = current_y + i * cell_size + (cell_size - text_height) // 2
                        draw.text((x, y), num, fill='black', font=font)

    return image


def save_sudoku(boards, solutions, size):
    """保存数独题目和答案为JPG图片"""
    # 确保images文件夹存在
    image_dir = "images"
    if not os.path.exists(image_dir):
        os.makedirs(image_dir)

    # 获取当前时间并格式化为指定格式
    current_time = datetime.now().strftime("%Y%m%d%H%M%S")

    # 保存题目
    image_question = create_sudoku_image(boards, size, is_answer=False)
    filename_question = os.path.join(image_dir, f"shudu-{current_time}.jpg")
    image_question.save(filename_question, "JPEG", quality=95)
    print(f"数独题目已保存为：{filename_question}")

    # 保存答案（传入原始题目用于判断填空位置）
    image_answer = create_sudoku_image(solutions, size, is_answer=True, original_boards=boards)
    filename_answer = os.path.join(image_dir, f"shudu-{current_time}-answer.jpg")
    image_answer.save(filename_answer, "JPEG", quality=95)
    print(f"数独答案已保存为：{filename_answer}")

    return filename_question, filename_answer


if __name__ == "__main__":
    print("请选择数独大小：")
    print("1. 4x4")
    print("2. 6x6")
    print("3. 9x9")
    choice = input("请输入选择（1/2/3）：")

    size_map = {"1": 4, "2": 6, "3": 9}
    if choice in size_map:
        size = size_map[choice]
        print(f"\n正在生成{size}x{size}数独...")

        # 根据大小设置题目数量
        puzzles_count = {
            4: 15,  # 3x5=15个
            6: 15,  # 3x5=15个
            9: 15  # 3x5=15个
        }[size]

        # 生成数独题目和答案
        puzzles = []
        solutions = []
        for _ in range(puzzles_count):
            solution = generate_sudoku(size)
            if solution:
                # 保存完整解答
                solutions.append([row[:] for row in solution])
                # 创建题目
                puzzle = create_puzzle(solution, size)
                puzzles.append(puzzle)
            else:
                print("生成数独失败，请重试！")
                break

        if len(puzzles) == puzzles_count:
            print("正在保存图片...")
            filename_q, filename_a = save_sudoku(puzzles, solutions, size)
            print("生成完成！")
        else:
            print("未能生成足够的数独题目！")
    else:
        print("无效的选择！")




