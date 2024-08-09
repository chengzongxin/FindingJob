from web_manager import WebManager
import ai_manager
import time

index = 1

# test
def loop_find():
    global index
    print(f"当前投递第[{index}]个")
    web_manager.open_job(index)
    job_desc = web_manager.get_job_desc()
    letter = ai_manager.generate_letter(job_desc)
    if letter is None:
        print("The function returned None (empty).")
        web_manager.close_current()
    else:
        print(f"The function returned: {letter}")
        # 开始聊天
        web_manager.chat_now(letter)
        web_manager.close_current()
    index += 1
    time.sleep(2)


if __name__ == '__main__':
    web_manager = WebManager()
    web_manager.load_first_page()

    while True:
        try:
            loop_find()
        except Exception:
            continue



