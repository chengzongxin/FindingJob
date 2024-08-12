import os
import time
import subprocess
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from pathlib import Path

import file_manager

# 全局 WebDriver 实例
# driver = None

CHROME_PATH = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
current_dir = Path(os.path.dirname(os.path.abspath(__file__)))
# 谷歌浏览器驱动地址
CHROMEDRIVER_PATH = str(current_dir / "chromedriver")


class LiepinWebManager:
    def __init__(self) -> None:
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
        chrome_options.binary_location = CHROME_PATH
        self.driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, options=chrome_options)

    def load_first_page(self, url):
        self.driver.get(url)
        self.wait_page_load()
        print("open finish===================>", self.driver.title)

    def get_driver(self):
        return self.driver

    def wait_page_load(self):
        # 设置隐式等待时间为10秒
        self.driver.implicitly_wait(10)  # 设置隐式等待时间为10秒
        # 等待页面完全加载
        WebDriverWait(self.driver, 10).until(
            lambda driver: driver.execute_script("return document.readyState") == "complete"
        )
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

    def get_job_name(self, index, page):
        try:
            # 构建动态 XPath
            xpath = f"//*[@id='lp-search-job-box']/div[3]/section[1]/div[2]/div[{index}]/div/div[1]/div/a/div[1]/div/div[1]"
            job_name = self.driver.find_element(By.XPATH, xpath)
            return job_name.text

        except NoSuchElementException as e:
            # 打印异常信息
            print(f"元素未找到，索引：{index}，异常信息：{str(e)}")
            return None

        except Exception as e:
            # 打印其他异常信息
            print(f"在索引 {index} 处没有找到工作。异常信息：{str(e)}")
            return None

    def get_job_city(self, index, page):
        try:
            # 构建动态 XPath
            xpath = f"//*[@id='lp-search-job-box']/div[3]/section[1]/div[2]/div[{index}]/div/div[1]/div/a/div[1]/div/div[2]"
            job_city = self.driver.find_element(By.XPATH, xpath)
            return job_city.text

        except NoSuchElementException as e:
            # 打印异常信息
            print(f"元素未找到，索引：{index}，异常信息：{str(e)}")
            return None

        except Exception as e:
            # 打印其他异常信息
            print(f"在索引 {index} 处没有找到工作。异常信息：{str(e)}")
            return None

    def get_com_name(self, index, page):
        try:
            # 构建动态 XPath
            xpath = f"//*[@id='home-main-box-container']/div[2]/div/ul/li[{index}]/div/div[1]/div[1]/div/div[1]/div/span"
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

    def open_job(self, index, page):
        xpath = f"//*[@id='lp-search-job-box']/div[3]/section[1]/div[2]/div[{index}]/div/div[1]/div/a/div[1]/div/div[1]"
        job_name = self.driver.find_element(By.XPATH, xpath)
        job_name.click()
        self.wait_page_load()

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
            description_selector = "/html/body/main/content/section[2]/dl/dd"
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
            name = self.find_element_by_xpath(xpath=xpath).text
            if len(name) > 0:
                return name[0]
        except Exception:
            return None

    def chat_now(self):
        xpath_chat = "/html/body/main/content/section[1]/a"
        # 点击按钮
        chat_now = self.driver.find_element(By.XPATH, xpath_chat)
        chat_now.click()

    def send_letter(self, letter):
        # 输入弹框
        input_xpath = "//*[@id='im-chatwin']/div/div[2]/div[3]/div[1]/textarea"
        self.wait_untl_element(input_xpath)
        input = self.find_element_by_xpath(input_xpath)
        input.click()
        input.send_keys(letter)

    def send_job_page_letter(self, letter):
        # 输入弹框
        input_xpath = "//*[@id='im-chatwin']/div/div[2]/div[3]/div[1]/textarea"
        self.wait_untl_element(input_xpath)
        input = self.find_element_by_xpath(input_xpath)
        input.click()
        input.send_keys(letter)

    def send_chat_page_letter(self, letter):
        input_xpath = '//*[@id="chat-input"]'
        self.wait_untl_element(input_xpath)
        input = self.find_element_by_xpath(input_xpath)
        input.click()
        input.send_keys(letter)
        # 模拟按回车键
        input.send_keys(Keys.RETURN)  # 或者使用 Keys.ENTER

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

    # def scroll_to_element_by_index(self, index):
    #     try:
    #         # 构建动态 XPath
    #         xpath = f'//li[@ka="search_list_{index}"]'
    #
    #         # 查找目标元素
    #         element = self.driver.find_element(By.XPATH, xpath)
    #
    #         # 使用 JavaScript 滚动到该元素
    #         self.driver.execute_script("arguments[0].scrollIntoView();", element)
    #
    #         # 选做：可选地，添加等待时间，以确保页面滚动完成
    #         # import time
    #         # time.sleep(2)
    #
    #     except Exception as e:
    #         print(f"发生异常：{str(e)}")

    def scroll_to_element_by_index(self, index):
        try:
            # 构建动态 XPath
            xpath = f'//li[@ka="search_list_{index}"]'

            # 查找目标元素
            element = self.driver.find_element(By.XPATH, xpath)

            # 使用 ActionChains 模拟滚动
            actions = ActionChains(self.driver)
            actions.move_to_element(element).perform()

            # 可选：额外调整滚动位置
            # self.driver.execute_script("window.scrollBy(0, 100);")  # 向上滚动100像素

        except Exception as e:
            print(f"发生异常：{str(e)}")

    def get_com_city(self, index, page):
        pass
