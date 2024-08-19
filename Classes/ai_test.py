import unittest
from datetime import time

from Classes.ai_manager import AiManager
from Classes.web_manager import WebManager


class MyTestCase(unittest.TestCase):
    # def test_something(self):
    #     self.assertEqual(True, True ,"test_something")  # add assertion here

    def test_send_collect_1(self):
        first_page = "https://www.zhipin.com/web/geek/recommend?tab=4&sub=1&page=1&tag=4"
        web_manager = WebManager()
        web_manager.load_first_page(first_page)
        xpath = "//*[@id='container']/div[2]/div/ul/li[1]/div/div[2]/div[2]/div/div/a/span[1]"
        web_manager.wait_untl_element(xpath)
        job_ele = web_manager.find_element_by_xpath(xpath)
        if job_ele is not None:
            job_ele.click()
            web_manager.wait_page_load()
            job_desc = web_manager.get_job_desc()
            web_manager.chat_now()
            ai_manager = AiManager()
            letter = ai_manager.generate_letter(job_desc)
            # 发送消息
            web_manager.send_letter(letter)
            print(letter)


    def test_send_job_detail(self):
        web_manager = WebManager()
        job_detail_page_url = "https://www.zhipin.com/job_detail/7c19086d04fef4811HNz3967EVpZ.html?securityId=RPcu-dJ5VaRyk-f10eHyTVDMMp3XjnCvQUbt16nP2HUv-Q9mW84wBaFwmBiOwo9906a1vsxGUk9NAPYJJ99a7tbpexZ3LOg_0qRukO7ZhsZ7RQlUCzWjWw~~&ka=personal_interest_job_7c19086d04fef4811HNz3967EVpZ"
        web_manager.load_first_page(job_detail_page_url)
        job_desc = web_manager.get_job_desc()
        web_manager.chat_now()
        ai_manager = AiManager()
        letter = ai_manager.generate_letter(job_desc)
        # 发送消息
        # web_manager.send_letter(letter)
        print(letter)

if __name__ == '__main__':
    unittest.main()
