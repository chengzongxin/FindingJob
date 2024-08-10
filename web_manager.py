import os
import time
import subprocess
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException

from pathlib import Path

import file_manager

# 全局 WebDriver 实例
# driver = None

CHROME_PATH = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
current_dir = Path(os.path.dirname(os.path.abspath(__file__)))
# 谷歌浏览器驱动地址
CHROMEDRIVER_PATH = str(current_dir / "chromedriver")
ZHIPIN_URL = "https://www.zhipin.com/web/geek/job?query=iOS&city=101280600"


class WebManager:
    def __init__(self) -> None:
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
        chrome_options.binary_location = CHROME_PATH
        self.driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, options=chrome_options)

    def load_first_page(self):
        self.driver.get(url=ZHIPIN_URL)
        self.driver.set_page_load_timeout(30)
        print("open finish===================>", self.driver.title)

    def get_driver(self):
        return self.driver

    def wait_page_load(self):
        self.driver.set_page_load_timeout(30)

    def wait_untl_element(self, xpath):
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )

    def find_element_by_xpath(self, xpath) -> WebElement:
        return self.driver.find_element(By.XPATH, xpath)

    def get(self, url):
        self.driver.get(url)
        self.driver.set_page_load_timeout(30)
        xpath_locator = "//*[@id='header']/div[1]/div[3]/ul/li[2]"
        WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.XPATH, xpath_locator))
        )

    def open_job(self, index):
        com_name = ""
        isInclude = file_manager.check_com_in_file(com_name)
        xpath_job = f"//*[@id='wrap']/div[2]/div[2]/div/div[1]/div[2]/ul/li[{index}]/div[1]/a/div[1]"
        self.wait_untl_element(xpath_job)
        open_job = self.driver.find_element(By.XPATH, xpath_job)
        open_job.click()
        self.wait_page_load()
        # time.sleep(10)

    def get_com_name(self, index):
        try:
            # 构建动态 XPath
            xpath = f"//*[@id='wrap']/div[2]/div[2]/div/div[1]/div[2]/ul/li[{index}]/div[1]/div/div[2]/h3/a"
            com_name = self.driver.find_element(By.XPATH, xpath)
            return com_name.text

        except NoSuchElementException as e:
            # 打印异常信息
            print(f"元素未找到，索引：{index}，异常信息：{str(e)}")
            return None

        except Exception as e:
            # 打印其他异常信息
            print(f"在索引 {index} 处没有找到工作。异常信息：{str(e)}")
            return None

    def get_job_desc(self):
        # 获取所有窗口句柄
        window_handles = self.driver.window_handles
        # 切换到新窗口（假设新窗口是最后一个打开的窗口）
        self.driver.switch_to.window(window_handles[-1])

        # 在新窗口中执行操作
        print(self.driver.title)  # 输出新窗口的标题

        # 关闭新窗口
        # self.driver.close()

        # 切换回原始窗口
        # self.driver.switch_to.window(window_handles[0])

        # 在原始窗口中继续执行操作
        # print(self.driver.title)  # 输出原始窗口的标题

        print('self.driver.title', self.driver.title)
        try:
            description_selector = "//*[@id='main']/div[3]/div/div[2]/div[1]/div[3]"
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.XPATH, description_selector))
            )
            job_description_element = self.driver.find_element(By.XPATH, description_selector)
            return job_description_element.text

        except Exception:
            print(f"No job found at index.")
            return None

    def get_hr_name(self):
        try:
            xpath = "//*[@id='main']/div[3]/div/div[2]/div[1]/div[4]/h2"
            name = self.find_element_by_xpath(xpath=xpath)
            if len(name) > 0:
                return name[0]
        except Exception:
            return None

    def chat_now(self, letter):
        xpath_chat = " //*[@id='main']/div[1]/div/div/div[1]/div[3]/div[1]/a[2]"
        # 点击按钮
        chat_now = self.driver.find_element(By.XPATH, xpath_chat)
        if chat_now.text == '立即沟通':
            chat_now.click()
            self.send_letter(letter=letter)
        else:
            print("已沟通过，pass")

    def send_letter(self, letter):
        input_xpath = "/html/body/div[12]/div[2]/div[2]/div/div[1]/div[2]/textarea"
        self.wait_untl_element(input_xpath)
        input = self.find_element_by_xpath(input_xpath)
        input.click()
        input.send_keys(letter)

    def close_current(self):
        # 获取所有窗口句柄
        window_handles = self.driver.window_handles
        # 关闭新窗口
        self.driver.close()
        # 切换回原始窗口
        self.driver.switch_to.window(window_handles[0])
        # 在原始窗口中继续执行操作
        print(self.driver.title)  # 输出原始窗口的标题

    def go_next_page(self, page):
        xpath = f"//*[@id='wrap']/div[2]/div[2]/div/div[1]/div[2]/div/div/div/a[{page}]"
        self.wait_untl_element(xpath)
        open_job = self.find_element_by_xpath(xpath)
        open_job.click()
        self.wait_page_load()
