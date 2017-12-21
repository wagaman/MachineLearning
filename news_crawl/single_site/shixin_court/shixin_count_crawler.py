from urllib.request import urlretrieve
import uuid
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
    "Host": "shixin.court.gov.cn",
    "Origin": "http://shixin.court.gov.cn",

    "Cookie": "_gscs_2025930969=09928799rtb5tx11|pv:1; _gscbrs_2025930969=1; JSESSIONID=406D94C0EABD377CA529B94285D5BC9E; _gscu_2025930969=09618250ualvq911",

    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Connection": "keep-alive",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.8",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
}

def get_result(name, code, uuid_, image_code):

    url = 'http://shixin.court.gov.cn/findDisNew'

    params = {'pName': name,
              'pCardNum': code,
              'pProvince': '0',
              'pCode': image_code,
              'captchaId': uuid_}

    response = requests.post(url, headers=defalut_headers, data=params, timeout=60)
    response.encoding = 'utf-8'
    response.text
    html = response.text


    return html

def get_captchaNew():
    uuid_tmp = uuid.uuid4().__str__().replace('-', '')
    url = 'http://shixin.court.gov.cn/captchaNew.do?captchaId=' + uuid_tmp

    filename = 'C:\\Users\sss\Desktop\code.jpg'

    ir = requests.get(url, headers=defalut_headers)
    if ir.status_code == 200:
        open(filename, 'wb').write(ir.content)

    return uuid_tmp


#uuid = get_captchaNew()

wenshus = get_result('薛豪', '142727199008221556', 'ebde29a793c34183bc1468047be3ab3f', 'na7j')

print(1)



