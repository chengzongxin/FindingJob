import unittest

import ai_manager
from web_manager import WebManager


class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, True ,"test_something")  # add assertion here

    def test_something_else(self):
        web_manager = WebManager()
        web_manager.load_first_page("https://www.zhipin.com/job_detail/ab0101d62a2d37321HV93dm1FltT.html?lid=3Td10QA59il.search.1&securityId=hkunk2SJZeHLo-2187h-yvZkRFH0FrHvQ6pZ5jn0KbjTo7aOlfHtdoHN_TAXBaMNF34ishlcGhd1u6NkZ3zNrnA9iykMbXQjlerrjHAcySv3BVGgq3sZSu0cgu5xRisBGGtx9KpAExJcjw~~&sessionId=")
        job_desc = web_manager.get_job_desc()
        letter = ai_manager.generate_letter(job_desc)
        print(letter)

if __name__ == '__main__':
    unittest.main()
