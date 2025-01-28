import random
from PIL import Image, ImageDraw, ImageFont
import os
import datetime
import textwrap
import platform


def get_font_path():
    system_name = platform.system()
    if system_name == "Windows":
        font_path = "C:/Windows/Fonts/simhei.ttf"
    elif system_name == "Linux":
        font_path = "/usr/share/fonts/wqy-microhei/wqy-microhei.ttc"
    elif system_name == "Darwin":
        font_path = "/System/Library/Fonts/PingFang.ttc"
    else:
        raise Exception("不支持的操作系统，请手动指定字体文件路径。")
    if not os.path.exists(font_path) or not os.access(font_path, os.R_OK):
        raise FileNotFoundError(f"字体文件 {font_path} 不存在或不可读，请检查路径。")
    return font_path


# 生成“有的题型”题目
def generate_custom_problem():
    total_people = random.randint(5, 15)
    target_person = random.randint(1, total_people)
    front_people = random.randint(0, target_person - 1)
    back_people = total_people - target_person - front_people
    problem = f"小明前面有{front_people}个小朋友，后面有{back_people}个小朋友"
    return problem


# 生成“第的题型”题目
def generate_order_custom_problem():
    total_people = random.randint(5, 15)
    front_order = random.randint(1, total_people - 1)
    back_order = random.randint(1, total_people - front_order)
    problem = f"从前往后数小明前面第{front_order}个，从后往前数小明后面第{back_order}个"
    return problem


# 生成混合题型1
def generate_mixed_problem1():
    total_people = random.randint(5, 15)
    target_person = random.randint(1, total_people)
    front_people = random.randint(0, target_person - 1)
    back_order = random.randint(1, total_people - target_person)
    problem = f"小明前面有{front_people}个小朋友，从后往前数小明是第{back_order}个"
    return problem


# 生成混合题型2
def generate_mixed_problem2():
    total_people = random.randint(5, 15)
    target_person = random.randint(1, total_people)
    front_order = random.randint(1, target_person)
    back_people = random.randint(0, total_people - target_person)
    problem = f"从前往后数小明是第{front_order}个，小明后面有{back_people}个小朋友"
    return problem


# 绘制题目到图片
def draw_problem(draw, font, problem, x, y, max_width, max_height):
    parts = problem.split('\n')
    total_height = 0
    for part in parts:
        available_width = max_width - x
        char_width = font.getbbox('A')[2] - font.getbbox('A')[0]
        num_chars = available_width // char_width
        wrapped_part = textwrap.fill(part, width=num_chars)
        bbox = draw.multiline_textbbox((x, y + total_height), wrapped_part, font=font)
        text_height = bbox[3] - bbox[1]
        if y + total_height + text_height > max_height:
            new_font_size = font.size - 5
            new_font = ImageFont.truetype(font.path, new_font_size)
            return draw_problem(draw, new_font, problem, x, y, max_width, max_height)
        draw.multiline_text((x, y + total_height), wrapped_part, fill='black', font=font)
        total_height += text_height
    return total_height


# 主函数
def main():
    # A4纸尺寸（像素，300dpi）
    width, height = 2480, 3508
    # 创建白色背景图片
    image = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(image)

    try:
        font_path = get_font_path()
        # 标题字体大小设为100
        title_font = ImageFont.truetype(font_path, 100)
        # 题目字体大小设为75
        problem_font = ImageFont.truetype(font_path, 75)
    except FileNotFoundError as e:
        print(e)
        return

    # 标题
    title = "排队问题"
    title_bbox = draw.textbbox((0, 0), title, font=title_font)
    title_width = title_bbox[2] - title_bbox[0]
    draw.text((width / 2 - title_width / 2, 50), title, fill='black', font=title_font)

    # 让用户选择题型
    print("请选择题型：")
    print("1. 第的题型")
    print("2. 有的题型")
    print("3. 混合题型")
    try:
        choice = input("请输入你的选择(1/2/3)：")
        choice = int(choice)
        if choice not in [1, 2, 3]:
            raise ValueError
    except ValueError:
        print("无效选择，请输入1、2或3。")
        return

    problem_generators = {
        1: generate_order_custom_problem,
        2: generate_custom_problem,
        3: lambda: random.choice([generate_mixed_problem1, generate_mixed_problem2])()
    }

    # 生成题目数量
    num_problems = 8
    y_position = 200
    max_width = width - 100  # 预留左右边距各50像素

    # 计算剩余高度
    remaining_height = height - y_position

    total_problem_height = 0
    problem_heights = []

    # 先计算所有题目高度
    temp_draw = ImageDraw.Draw(Image.new('RGB', (width, height)))
    for i in range(num_problems):
        problem = problem_generators[choice]()
        # 添加序号、“小朋友们排队” 并换行，以及在问题后添加换行和提问
        numbered_problem = f"题目{i + 1}：小朋友们排队，\n{problem}\n请问一共有几个小朋友？"
        # 计算题目高度
        problem_height = draw_problem(temp_draw, problem_font, numbered_problem, 50, 0, max_width, height)
        problem_heights.append(problem_height)
        total_problem_height += problem_height

    # 计算每题之间的间距
    spacing = (remaining_height - total_problem_height) / (num_problems + 1)

    y_position = 200
    # 绘制题目
    for i in range(num_problems):
        problem = problem_generators[choice]()
        # 添加序号、“小朋友们排队” 并换行，以及在问题后添加换行和提问
        numbered_problem = f"题目{i + 1}：小朋友们排队，\n{problem}\n请问一共有几个小朋友？"
        # 绘制题目
        problem_height = draw_problem(draw, problem_font, numbered_problem, 50, y_position, max_width, height)
        y_position += problem_height + spacing  # 增加间距

    # 生成包含时间的文件名
    current_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"paidui-{current_time}.jpg"
    # 保存图片到images目录
    if not os.path.exists('images'):
        try:
            os.makedirs('images')
        except OSError as e:
            print(f"创建目录失败: {e}")
            return
    try:
        image.save(os.path.join('images', filename))
        print(f"图片已保存为 {filename}")
    except Exception as e:
        print(f"保存图片失败: {e}")


if __name__ == "__main__":
    main()