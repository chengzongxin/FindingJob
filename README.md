---
layout: post
title: "runloop"
date: 2024-8-8
description: "runloop"
tag: runloop
---



## 导读

### Prerequisite: Add Chrome to PATH

Please make sure the path to chrome’s executable is added to the environment variable `PATH`. You can check it by running the command `chrome.exe` (on Windows) or `Google/ Chrome` ( on Mac). It should launch the Chrome browser.

If you get a similar message as below that means Chrome is not added to your system’s path:

```
'chrome' is not recognized as an internal or external command,
operable program or batch file.
```

If this is the case, please feel free to Google [how to add chrome to PATH](https://www.google.com/search?q=how+to+add+chrome+to+PATH)? If you are on Mac, please follow the steps in [This Link](https://apple.stackexchange.com/questions/228512/how-do-i-add-chrome-to-my-path).

### Step 1: Launch browser with custom flags

To enable Chrome to open a port for remote debugging, we need to launch it with a custom flag –

```
chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\selenum\ChromeProfile"
```

For Mac:

```
Google\ Chrome --remote-debugging-port=9222 --user-data-dir="~/ChromeProfile"
```

For `--remote-debugging-port` value you can specify any port that is open.

For `--user-data-dir` flag you need to pass a directory where a new Chrome profile will be created. It is there just to make sure chrome launches in a separate profile and doesn’t pollute your default profile.

> Once Chrome is launched this way it has opened a connection on the given port that any client can connect to for debugging.

You can now play with the browser manually, navigate to as many pages, perform actions and once you need your automation code to take charge, you may run your automation script. You just need to modify your Selenium script to make Selenium connect to that opened browser.

You can verify if the Chrome is launched in the right way:

- Launch a new browser window *normally* (without any flag), and navigate to `http://127.0.0.1:9222`
- Confirm if you see the Google homepage reference in the second browser window

### Step 2: Launch browser with options

Here is that simple but magical Java and Python code. You can easily convert it into a Programming language of your choice.

```
// JAVA Example
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.chrome.ChromeOptions;

//Change chrome driver path accordingly
System.setProperty("webdriver.chrome.driver", "C:\\selenium\\chromedriver.exe");
ChromeOptions options = new ChromeOptions();
options.setExperimentalOption("debuggerAddress", "127.0.0.1:9222");
WebDriver driver = new ChromeDriver(options);
System.out.println(driver.getTitle());
```

```
# PYTHON Example
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
#Change chrome driver path accordingly
chrome_driver = "C:\chromedriver.exe"
driver = webdriver.Chrome(chrome_driver, chrome_options=chrome_options)
print driver.title
﻿
```

What is that value under debuggerAddress?

The URL `127.0.0.1` denotes your localhost. We have supplied the same port, i.e `9222`, that we used to launch Chrome with `--remote-debugging-port` flag. While you can use any port, you need to make sure it is open and available to use.



## selenium  版本不能为4.1x，否则不能指定路径

```python
pip3 uninstall selenium   # 卸载
pip3 install selenium==3.14.0 # 安装指定版本
```

## 下载安装chromedriver

chromedriver版本和chrome版本一致

## 需要先启动窗口

cmd打开命令行

```
chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\selenum\ChromeProfile"
```

## 在调试脚本

```
# 谷歌浏览器位置
CHROME_PATH = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
# 谷歌浏览器驱动地址
# CHROMEDRIVER_PATH = r'.\chromedriver.exe'
current_dir = Path(os.path.dirname(os.path.abspath(__file__)))
CHROMEDRIVER_PATH = str(current_dir / "chromedriver")
 
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
 
chrome_options.binary_location = CHROME_PATH
driver = webdriver.Chrome(executable_path = CHROMEDRIVER_PATH, options=chrome_options)
 
driver.get("https://www.baidu.com/")
print(driver.title)
```







参考:

https://cosmocode.io/how-to-connect-selenium-to-an-existing-browser-that-was-opened-manually/#0-why-do-we-want-selenium-to-connect-to-a-previously-opened-browser