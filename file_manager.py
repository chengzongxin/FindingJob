import os
from datetime import datetime


def write(data):
    # 获取当前时间并格式化
    current_time = datetime.now()
    formatted_time = current_time.strftime("%Y-%m-%d-%H-%M-%S")
    file_name = f'./send_record/record_{formatted_time}.txt'

    # 创建目录（如果不存在）
    os.makedirs(os.path.dirname(file_name), exist_ok=True)

    # 将内容写入文件
    with open(file_name, "w", encoding="utf-8") as file:
        file.write(data)

    print(f"内容已成功写入文件：{file_name}")


def check_com_in_file(com_name: str) -> bool:
    # 定义过滤文件的相对路径
    file_path = os.path.join(os.getcwd(), 'filter.txt')

    # 初始化一个变量，用于标记是否包含
    is_included = False

    try:
        # 打开文件并读取内容
        with open(file_path, 'r', encoding='utf-8') as file:
            # 逐行读取文件内容并检查是否包含在com_name中
            for line in file:
                # 如果line中的内容在com_name中找到，标记为True并退出循环
                if line.strip() in com_name:
                    is_included = True
                    break
    except FileNotFoundError:
        print(f"文件 {file_path} 未找到。请检查文件路径。")

    return is_included
