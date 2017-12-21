__author__ = 'Administrator'
import time
from selenium import webdriver

chromedriver = "C:\\Users\Administrator\AppData\Local\Google\Chrome\Application\chromedriver.exe"
driver = webdriver.Chrome(chromedriver)


driver.get("https://www.zhihu.com/question/19794858")
time.sleep(0.6)
driver.execute_script("window.scrollBy(0,10500)")
try:
    while driver.find_element_by_class_name('QuestionMainAction') is not None:
        driver.find_element_by_class_name('QuestionMainAction').click()
        time.sleep(0.6)
except:
    print('抓取完成')
finally:
    print(driver.page_source)