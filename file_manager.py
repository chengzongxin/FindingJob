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
