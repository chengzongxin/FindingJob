import unittest

import ai_manager
from web_manager import WebManager


class MyTestCase(unittest.TestCase):
    # def test_something(self):
    #     self.assertEqual(True, True ,"test_something")  # add assertion here

    def test_something_else(self):
        web_manager = WebManager()
        web_manager.load_first_page("https://www.zhipin.com/job_detail/da4b44ec8894a02e1HNy3d-8EFRY.html?lid=1KPVQLy5faG.search.9&securityId=eYR5Vd3GuPqIv-e19IDtlll_ja-5y9cxSek9AGspNmJezVNdj8wkn9fRBsUw_ObkDI2vPEMes1GKz8b9kC-A57jb45mkQ5psguRC1ann2et4yaK-hjFzGDMJtZggWThPslB0RSvFCb4H1CLwWwrTN483_JFasRgv6VidLEXocd7r2cL53P0~&sessionId=")
        job_desc = web_manager.get_job_desc()
        letter = ai_manager.generate_letter(job_desc)
        print(letter)

if __name__ == '__main__':
    unittest.main()
