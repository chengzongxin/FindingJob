import time

import ai_manager
import file_manager
from web_manager import WebManager

index = 1
page = 1

ZHIPIN_URL = "https://www.zhipin.com/web/geek/job?query=iOS&city=101280600&scale=302,303,304"


def loop_find() -> bool:
    global page
    global index
    com_name = web_manager.get_com_name(index)
    web_manager.scroll_to_element_by_index(index)
    print(f"当前投递第[{index}]个,公司名：[{com_name}]")
    if com_name is None:
        index += 1
        return True
    is_include = file_manager.check_com_in_file(com_name)
    if is_include:
        print(f"当前投递的公司：[{com_name}] 被过滤，跳过执行下一个")
        index += 1
        return True
    print("打开公司页面")
    web_manager.open_job(index)
    print("获取职位描述")
    job_desc = web_manager.get_job_desc()
    print("开始聊天")
    web_manager.chat_now()
    letter = ai_manager.generate_letter(job_desc)
    if letter is None:
        print("The function returned None (empty).")
        web_manager.close_current()
    else:
        print(f"The function returned: {letter}")
        web_manager.send_letter(letter)
        time.sleep(2)
        # 开始聊天
        web_manager.close_current()
    index += 1
    if index > 30:
        page += 1
        web_manager.go_next_page(page)
        index = 1
    time.sleep(2)
    return False


if __name__ == '__main__':
    web_manager = WebManager()
    web_manager.load_first_page(ZHIPIN_URL)

    while True:
        try:
            isContinue = loop_find()
            if isContinue:
                continue
        except Exception:
            continue
