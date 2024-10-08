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

import Classes.file_manager

# 全局 WebDriver 实例
# driver = None

CHROME_PATH = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
# current_dir = Path(os.path.dirname(os.path.abspath(__file__)))
# # 谷歌浏览器驱动地址
# CHROMEDRIVER_PATH = str(current_dir / "chromedriver")
# 当前文件所在目录
current_dir = Path(os.path.dirname(os.path.abspath(__file__)))
# 谷歌浏览器驱动地址，位于当前文件的上一层级目录中的 Resources 目录
CHROMEDRIVER_PATH = str(current_dir.parent / "Resources" / "chromedriver")

class WebManager:
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

    def get_item(self, index, page):
        # 生成 item 元素的 XPath
        xpath = f'//li[@ka="search_list_{index + (page - 1) * 30}"]'
        # 查找目标 item 元素
        return self.driver.find_element(By.XPATH, xpath)

    def open_job(self, index, page):
        try:
            xpath_job = f"//*[@id='wrap']/div[2]/div[2]/div/div[1]/div[{1 if page > 1 else 2}]/ul/li[{index}]/div[1]/a/div[1]"
            self.wait_untl_element(xpath_job)
            # open_job = self.driver.find_element(By.XPATH, xpath_job)
            open_job = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpath_job)))
            open_job.click()
            self.wait_page_load()

        except Exception as e:
            # 打印其他异常信息
            print(f"在索引 {index} 处打开工作异常。异常信息：{str(e)}")

    def get_com_name(self, index, page):
        try:
            # 构建动态 XPath
            xpath = f"//*[@id='wrap']/div[2]/div[2]/div/div[1]/div[{1 if page > 1 else 2}]/ul/li[{index}]/div[1]/div/div[2]/h3/a"
            com_name = self.driver.find_element(By.XPATH, xpath)
            return com_name.text

        except NoSuchElementException as e:
            # 打印异常信息
            print(f"get_com_name 元素未找到，索引：{index}，异常信息：{str(e)}")
            return None

        except Exception as e:
            # 打印其他异常信息
            print(f"get_com_name 在索引 {index} 处没有找到工作。异常信息：{str(e)}")
            return None

    def get_job_name(self, index, page):
        try:
            # 查找目标 item 元素
            item_element = self.get_item(index, page)
            # 在 item 元素内查找 <span class="salary"> 元素
            salary_element = item_element.find_element(By.XPATH, './/span[@class="job-name"]')
            # 返回薪资文本
            return salary_element.text
        except NoSuchElementException as e:
            # 打印异常信息
            print(f"get_job_salary 元素未找到，索引：{index}，异常信息：{str(e)}")
            return None

        except Exception as e:
            # 打印其他异常信息
            print(f"get_job_salary 在索引 {index} 处没有找到工作。异常信息：{str(e)}")
            return None

    def get_job_salary(self, index, page):
        try:
            # 查找目标 item 元素
            item_element = self.get_item(index, page)
            # 在 item 元素内查找 <span class="salary"> 元素
            salary_element = item_element.find_element(By.XPATH, './/span[@class="salary"]')
            # 返回薪资文本
            return salary_element.text
        except NoSuchElementException as e:
            # 打印异常信息
            print(f"get_job_salary 元素未找到，索引：{index}，异常信息：{str(e)}")
            return None

        except Exception as e:
            # 打印其他异常信息
            print(f"get_job_salary 在索引 {index} 处没有找到工作。异常信息：{str(e)}")
            return None

    def get_person_count(self, index, page):
        try:
            item_element = self.get_item(index, page)
            # 在 item 元素内查找 <ul class="company-tag-list"> 元素
            ul_element = item_element.find_element(By.XPATH, './/ul[@class="company-tag-list"]')
            # 从 <ul> 元素中查找所有 <li> 元素
            li_elements = ul_element.find_elements(By.XPATH, './li')

            # 获取最后一个 <li> 元素
            if li_elements:
                last_li_element = li_elements[-1]
                return last_li_element.text
            return None
        except NoSuchElementException as e:
            # 打印异常信息
            print(f"get_person_count 元素未找到，索引：{index}，异常信息：{str(e)}")
            return None

        except Exception as e:
            # 打印其他异常信息
            print(f"get_person_count 在索引 {index} 处没有找到工作。异常信息：{str(e)}")
            return None

    def get_job_desc(self):
        try:
            # 获取所有窗口句柄
            window_handles = self.driver.window_handles
            # 切换到新窗口（假设新窗口是最后一个打开的窗口）
            self.driver.switch_to.window(window_handles[-1])

            # 关闭新窗口
            # self.driver.close()

            # 切换回原始窗口
            # self.driver.switch_to.window(window_handles[0])

            # 在原始窗口中继续执行操作
            print(self.driver.title)  # 输出原始窗口的标题

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
            name = self.find_element_by_xpath(xpath=xpath).text
            if len(name) > 0:
                return name[0]
        except Exception:
            return None

    def chat_now(self):
        xpath_chat = "//*[@id='main']/div[1]/div/div/div[1]/div[3]/div[1]/a[2]"
        # 点击按钮
        chat_now = self.driver.find_element(By.XPATH, xpath_chat)
        chat_now.click()

    def send_letter(self, letter):
        # 判断是否跳转页面
        chat_url = 'https://www.zhipin.com/web/geek/chat'
        if chat_url in self.driver.current_url:
            self.send_chat_page_letter(letter=letter)
        else:
            self.send_job_page_letter(letter=letter)

    def send_job_page_letter(self, letter):
        # 输入弹框
        input_xpath = "/html/body/div[12]/div[2]/div[2]/div/div[1]/div[2]/textarea"
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
        try:
            # 关闭新窗口
            if len(self.driver.window_handles) > 2:
                self.driver.close()
        except Exception as e:
            print("关闭窗口异常", e)
        # 切换回原始窗口
        self.driver.switch_to.window(window_handles[0])
        # 在原始窗口中继续执行操作
        print(self.driver.title)  # 输出原始窗口的标题

    def switch_first_window(self):
        # 获取所有窗口句柄
        window_handles = self.driver.window_handles
        # 切换回原始窗口
        self.driver.switch_to.window(window_handles[0])
        # 在原始窗口中继续执行操作
        print(self.driver.title)  # 输出原始窗口的标题

    def scroll_to_next(self):
        self.driver.execute_script("window.scrollBy(0, 80);")  # 向上滚动100像素，公司弹窗会挡住翻页按钮

    def go_next_page(self, page):
        # 滚动到底部
        # self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # 获取 <div class="options-pages"> 下的所有元素
        def go_next_action():
            try:
                elements = self.driver.find_elements_by_css_selector('div.options-pages > *')

                # 如果有元素存在，点击最后一个元素
                if elements:
                    last_element = elements[-1]
                    last_element.click()
                else:
                    print("No elements found under div.options-pages.")
                    # 找到父元素
                    parent_element = self.driver.find_element(By.CLASS_NAME, "options-pages")
                    # 直接使用XPath进行查找
                    target_element = parent_element.find_element(By.XPATH, f".//a[text()='{page}']")
                    target_element.click()

            except Exception as e:
                print(f"发生异常：{str(e)}")

        try:
            go_next_action()

        except Exception as e:
            print(f"发生异常：{str(e)}")

            self.driver.execute_script("window.scrollBy(0, 50);")  # 向下滚动 50 像素，可以根据实际情况调整
            go_next_action()

        self.wait_page_load()

    def scroll_to_element_by_index(self, index, page):
        try:
            # 构建动态 XPath
            xpath = f'//li[@ka="search_list_{index + (page - 1) * 30}"]'

            # 查找目标元素
            element = self.driver.find_element(By.XPATH, xpath)

            # 使用 ActionChains 模拟滚动
            actions = ActionChains(self.driver)
            actions.move_to_element(element).perform()

            # 可选：额外调整滚动位置
            self.driver.execute_script("window.scrollBy(0, 100);")  # 向上滚动100像素

        except Exception as e:
            print(f"发生异常：{str(e)}")
