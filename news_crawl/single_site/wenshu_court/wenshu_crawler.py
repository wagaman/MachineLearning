from bs4 import BeautifulSoup
from selenium.common.exceptions import TimeoutException
import requests
import re
from selenium import webdriver
import time
import json

__author__ = 'Administrator'


defalut_headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.104 Safari/537.36",
    "Host": "wenshu.court.gov.cn",
    "Origin": "http://wenshu.court.gov.cn",

    "Cookie": "FSSBBIl1UgzbN7N80S=xqJQi.g2ay3FKEb6uAeVgtcC85vMX32R.yNiulR8Hg.PEr8P5z2njTI_EuEpntxe; ASP.NET_SessionId=fookphukvxslwghztak3muki; wzwsconfirm=377796e93293633a991dd5a499cdb7ee; wzwstemplate=MTA=; ccpassport=caffae62f1bd0fb1df2b4cf4cd0f7a21; wzwschallenge=-1; wzwsvtime=1501746539; Hm_lvt_3f1a54c5a86d62407544d433f6418ef5=1501551011,1501722196,1501746519,1501750504; Hm_lpvt_3f1a54c5a86d62407544d433f6418ef5=1501751588; _gscu_2116842793=014889188asn2e58; _gscs_2116842793=t01746519z81wza58|pv:19; _gscbrs_2116842793=1; FSSBBIl1UgzbN7N80T=1Tmiusj2jduM6UwvMUvKYvi4D.T_dbK4Ok4DTLF.RGqGiQ2C3s845ukxrNIR8rtt711ZSaTSkkMoo_BMq2.kwsQxS3lhVxa6hc1jGE3naPyqXoFM9mhhH.TxRNNlE_UKBcQnPC8LPZoIUMT9Xz5T6JtxgkPGtgCCxX5KYTTHVWgoyJxyNy1PzZlMfP3EGj8yq1olgqUQvlYlG7ry7JjQo9HY6cvjq8wjvr02RHRU56nIbLLRfE84jyjVBcD7Hl0NNQ87VzfGTfLsJKjss2ISQKPCz_sZxt1C_LdjKFIkwMhWq7bAgu2FeZ_M9Um5DVT8gZiyO8jcPefIzHcDuKcNZI4JI",

    "Accept": "*/*",
    "Connection": "keep-alive",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.8",
    "Content-Length": "331",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
}


def get_list_driver(keyword, driver=None):

    wenshus = []
    url = 'http://wenshu.court.gov.cn/list/list/?sorttype=1&conditions=searchWord+QWJS+++' + keyword
    if driver is None:
        chromedriver = "C:\\Users\sss\AppData\Local\Google\Chrome\Application\chromedriver.exe"
        driver = webdriver.Chrome(chromedriver)
    driver.get(url)
    time.sleep(5)
    driver.find_element_by_id('12_button').click()
    driver.find_element_by_id('12_input_20').click()

    def getHtml(driver):
        driver.find_elements_by_link_text('下一页').click()
        time.sleep(5)
        html = driver.page_source
        return html

    def append_wenshu_from(html):
        soup = BeautifulSoup(html, 'lxml')
        for div in soup.find_all('div', attrs={'class': 'dataItem'}):
            wenshu = {}

            wenshu['title'] = div.find('input', class_='DocIds')['value'].split('|')[1]
            wenshu['id'] = div.find('input', class_='DocIds')['value'].split('|')[0]
            wenshu['date_day'] = div.find('input', class_='DocIds')['value'].split('|')[2]

            wenshus.append(wenshu)

    time.sleep(5)
    html = driver.page_source
    append_wenshu_from(html)
    while driver.find_element_by_link_text('下一页') is not None:
        html = getHtml(driver)
        append_wenshu_from(html)

    return wenshus


#抓不下来
def get_list(keyword, start_page=2, max_page=3):

    wenshus = []
    for page in range(start_page, max_page):

        url = 'http://wenshu.court.gov.cn/List/ListContent?MmEwMD=1yDikIN2FuaMoM8v.M9K2.J4CvC_HjY4sHgDm9R.N7kG5AbCLIw4idqxS2QRXJxtQ8pZrZCSuH3o6C7MaNLkzIIxrg3RnDNh2vUKoZZn.5YAoKmO0Gn.ZbicH7mRZrjT1jArxgZN2QRME.Rtzuy3DPgJbiL6F7GNmQ8YHDFJYjCnNXuZBnDZyYFlzVWGUzFLHB44p3TnLvuqCH9RrqNwWnjyBdU1GQx6Ee1J445WbshoUo88g4sgXCPvpjZLL19RAwqW.QxHQqvMFgyiqNuiDu2sV63nohcFDfKpREw7..A7t2fIY5EV3dKoul_hJ9dfKBL6LnayXeQaO9sOPK44sH4Yd6R7.0KR7DMUTm7SZlSC4HKahzjU8nW5qo_d8wr_eoj0T0L4tQuw8.fXa6SKIOHTEWALjmhvFh5Q'

        params = {'Param': '全文检索:' + keyword + ',裁判年份:2017,审判程序:一审',
                  'Index': page,
                  'Page': '5',
                  'Direction': 'asc',
                  'Order': '法院层级'}

        response = requests.post(url, headers=defalut_headers, data=params, timeout=60)
        response.encoding = 'utf-8'
        response.text
        json_data = response.json()


    return json_data

get_list_driver('中国联合网络通信有限公司')

wenshus = get_list('中国联合网络通信有限公司')
print(1)



