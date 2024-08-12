import sys
import time

import ai_manager
import file_manager
from liepin_web_manager import LiepinWebManager
from web_manager import WebManager
import asyncio

index = 1
page = 1

ZHIPIN_URL = "https://www.zhipin.com/web/geek/job?query=iOS&city=101280600&scale=302,303,304"
LIEPIN_URL = "https://www.liepin.com"


# /html/body/div[12]/div[2] 超过限制弹窗

def loop_find():
    global page
    global index

    while True:
        if index > 30:
            print(f"当前第 {index} 个，去下一页")
            page += 1
            web_manager.go_next_page(page)
            index = 1

        com_name = web_manager.get_com_name(index, page)
        web_manager.scroll_to_element_by_index(index, page)
        print(f"当前投递第[{index}]个, 公司名：[{com_name}]")

        if com_name is None:
            index += 1
            continue

        is_include = file_manager.check_com_in_file(com_name)
        if is_include:
            print(f"当前投递的公司：[{com_name}] 被过滤，跳过执行下一个")
            index += 1
            continue

        is_include = file_manager.check_com_in_today_send("boss", com_name)
        if is_include:
            print(f"当前投递的公司：[{com_name}] 已投递，跳过执行下一个")
            index += 1
            continue

        print("打开公司页面")
        web_manager.open_job(index, page)

        print("获取职位描述")
        job_desc = web_manager.get_job_desc()

        if job_desc is None:
            print("获取职位描述失败")
            index += 1
            web_manager.close_current()
            continue

        print("开始聊天")
        web_manager.chat_now()

        letter = ai_manager.generate_letter(job_desc)

        if letter is None:
            print("The function returned None (empty).")
            web_manager.close_current()
        else:
            print(f"The function returned:\n {letter}")
            web_manager.send_letter(letter)
            file_manager.write_send_com("boss", com_name)
            time.sleep(2)
            web_manager.close_current()

        index += 1


def loop_liepin():
    global page
    global index

    while True:
        job_name = liepin_web_manager.get_job_name(index, page)
        job_city = liepin_web_manager.get_job_city(index, page)
        com_name = liepin_web_manager.get_com_name(index, page)

        if job_name is None or job_city is None or com_name is None:
            index += 1
            continue

        if "iOS" in job_name and "深圳" in job_city:
            web_manager.open_job(index, page)
        else:
            index += 1
            continue

        is_include = file_manager.check_com_in_today_send("liepin", com_name)
        if is_include:
            print(f"当前投递的公司：[{com_name}] 已投递，跳过执行下一个")
            index += 1
            continue

        liepin_web_manager.open_job(index, page)
        print("获取职位描述")
        job_desc = liepin_web_manager.get_job_desc()

        if job_desc is None:
            print("获取职位描述失败")
            index += 1
            liepin_web_manager.close_current()
            continue

        print("开始聊天")
        liepin_web_manager.chat_now()

        letter = ai_manager.generate_letter(job_desc)

        if letter is None:
            print("The function returned None (empty).")
            liepin_web_manager.close_current()
        else:
            print(f"The function returned:\n {letter}")
            liepin_web_manager.send_letter(letter)
            file_manager.write_send_com("liepin", com_name)
            time.sleep(2)
            liepin_web_manager.close_current()

        index += 1


#


# def loop_find_lie_pin:
#     pass

if __name__ == '__main__':
    # print("sys.argv", sys.argv, sys.argv[0], sys.argv[1])
    if sys.argv[1] == "boss":
        web_manager = WebManager()
        web_manager.load_first_page(ZHIPIN_URL)
        loop_find()
    elif sys.argv[1] == "liepin":
        liepin_web_manager = LiepinWebManager()
        liepin_web_manager.load_first_page(LIEPIN_URL)
        loop_liepin()
    # while True:
    #     try:
    #         isContinue = loop_find()
    #         if isContinue:
    #             continue
    #     except Exception:
    #         continue
