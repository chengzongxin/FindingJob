import time

import ai_manager
import file_manager
from web_manager import WebManager
import asyncio

index = 1
page = 1

ZHIPIN_URL = "https://www.zhipin.com/web/geek/job?query=iOS&city=101280600&scale=302,303,304"

# /html/body/div[12]/div[2] 超过限制弹窗
def loop_find() -> bool:
    global page
    global index
    if index > 30:
        page += 1
        web_manager.go_next_page(page)
        index = 1
        time.sleep(10)

    com_name = web_manager.get_com_name(index, page)
    web_manager.scroll_to_element_by_index(index)
    print(f"当前投递第[{index}]个,公司名：[{com_name}]")
    if com_name is None:
        index += 1
        # return True
        loop_find()
    is_include = file_manager.check_com_in_file(com_name)
    if is_include:
        print(f"当前投递的公司：[{com_name}] 被过滤，跳过执行下一个")
        index += 1
        # return True
        loop_find()
    is_include = file_manager.check_com_in_today_send(com_name)
    if is_include:
        print(f"当前投递的公司：[{com_name}] 已投递，跳过执行下一个")
        index += 1
        # return True
        loop_find()
    print("打开公司页面")
    web_manager.open_job(index, page)
    print("获取职位描述")
    job_desc = web_manager.get_job_desc()
    if job_desc is None:
        print("获取职位描述失败")
        index += 1
        # return True
        web_manager.close_current()
        loop_find()
    print("开始聊天")
    web_manager.chat_now()
    letter = ai_manager.generate_letter(job_desc)
    if letter is None:
        print("The function returned None (empty).")
        web_manager.close_current()
    else:
        print(f"The function returned:\n {letter}")
        web_manager.send_letter(letter)
        file_manager.write_send_com(com_name)
        time.sleep(2)
        # 开始聊天
        web_manager.close_current()
    index += 1

    # return False
    loop_find()


if __name__ == '__main__':
    web_manager = WebManager()
    web_manager.load_first_page(ZHIPIN_URL)

    loop_find()
    # while True:
    #     try:
    #         isContinue = loop_find()
    #         if isContinue:
    #             continue
    #     except Exception:
    #         continue