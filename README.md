给孩子用的一些题型生成小工具

一、ShuDu.py
  1、主要功能
    数独生成：支持生成不同尺寸（4x4、6x6、9x9）的数独。
    图片生成：将多个数独题目和答案以 A4 纸张大小的图片形式输出，图片格式为 JPEG。
    用户交互：允许用户选择数独的尺寸，根据用户的选择生成相应数量的数独题目和答案。
  2、实现步骤
    2.1、数独生成部分
      generate_sudoku(size)：生成指定大小的数独棋盘，首先初始化空棋盘，随机填充第一行，然后使用回溯法填充其余部分。
      is_valid(board, row, col, num, size)：检查在数独棋盘的指定位置放置指定数字是否合法，会检查所在行、列和方块是否有重复数字。
      solve_sudoku(board, size)：使用回溯法解决数独问题，通过递归尝试不同数字来填充棋盘的空位置。
      find_empty(board, size)：找到数独棋盘中的空位置（值为 0 的位置）。
      create_puzzle(board, size)：根据完整的数独棋盘创建数独谜题，随机移除一定数量的数字。
    2.2、图片生成部分
      create_sudoku_image(boards, size, is_answer=False, original_boards=None)：将多个数独棋盘转换为 A4 大小的图片，可指定是否为答案页。图片中会绘制数独的网格线，并根据情况使用不同字体填充数字。
      save_sudoku(boards, solutions, size)：保存数独题目和答案为 JPG 图片，会创建images文件夹（如果不存在），并以当前时间命名图片文件。
    2.3、主程序部分
      用户可以选择数独的尺寸（4x4、6x6、9x9）。
      根据用户选择的尺寸生成相应数量的数独题目和答案。
      调用save_sudoku函数将生成的数独题目和答案保存为图片。
  3、注意事项
    程序使用了 Python 的PIL库（即Pillow）来处理图片，确保该库已安装。
    字体文件使用了arial.ttf和arialbd.ttf，如果找不到这些字体文件，会使用默认字体。
