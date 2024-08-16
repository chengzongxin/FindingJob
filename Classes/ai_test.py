import unittest

from Classes.ai_manager import AiManager
from Classes.web_manager import WebManager


class MyTestCase(unittest.TestCase):
    # def test_something(self):
    #     self.assertEqual(True, True ,"test_something")  # add assertion here

    def test_something_else(self):
        web_manager = WebManager()
        job_detail_page_url = "https://www.zhipin.com/job_detail/ea122426861464111HB43t65EFJY.html?securityId=oLEyyuAqWsIc0-t1GzaMJzv7XU65-XUP-EDBQR7pAieGOVBdTMAWq7CQUtPEnXDDPIFB9El_hywBPvcHqibkeDFySFxYmYqnrkwPZMhMzimFj6KN2IOr0Q%7E%7E&ka=personal_interest_job_ea122426861464111HB43t65EFJY"
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
