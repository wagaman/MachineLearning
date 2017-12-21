__author__ = 'Administrator'
import time
from selenium import webdriver
from selenium.common.exceptions import TimeoutException

chromedriver = "C:\\Users\Administrator\AppData\Local\Google\Chrome\Application\chromedriver.exe"
driver = webdriver.Chrome(chromedriver)

startTime = time.time()
# 设定页面加载限制时间
driver.set_page_load_timeout(7)

try:
    driver.get('http://s.weibo.com/weibo/%E9%BB%84%E7%A3%8A%E5%B0%8F%E5%84%BF%E5%AD%90')
except TimeoutException:
    print('time out after 7 seconds when loading page')
finally:
    print(driver.page_source)