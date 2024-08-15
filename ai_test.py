import unittest

import ai_manager
from web_manager import WebManager


class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, True ,"test_something")  # add assertion here

    def test_something_else(self):
        web_manager = WebManager()
        web_manager.load_first_page("https://www.zhipin.com/job_detail/3493d7cd51b72eea1XVy3d-7FFRR.html?securityId=RMzZ2DIzHqEt5-y1BpCpK6eOtyg-UgQLJfWXy-qmHwtw7QOhFxiPvY_cuRbJIuXJgY0CfeY4yuqXs9S1tYq0flO-7ov7LFTcLDp9nAts1eBl5Ik746YifRM~")
        job_desc = web_manager.get_job_desc()
        letter = ai_manager.generate_letter(job_desc)
        print(letter)

if __name__ == '__main__':
    unittest.main()
