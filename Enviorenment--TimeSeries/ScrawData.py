# -*- coding: utf-8 -*-
"""
Created on Thu Jul 13 13:00:48 2017

@author: 赵慧
自动抓取物联网数据
"""
import urllib.request
from urllib import parse
from bs4 import BeautifulSoup as bs
import re

# 网址
url = "http://61.148.212.17:8088/health720/logdata/"

# 请求
request = urllib.request.Request(url)

# 爬取结果
response = urllib.request.urlopen(request).read()

soup = bs(response, "html.parser")

# 抓取列表
listFiles = soup.findAll("a", href=re.compile("^FILE"))

# 自动下载
# 自动下载
for link in listFiles:
    x = link.get("href")
    if x not in os.listdir("D:/Programma/Environmental"):
        print(x)
        path = "D:\\Programma\\Environmental\\%s" % x
        url = "http://61.148.212.17:8088/health720/logdata/" + x
        urllib.request.urlretrieve(url, path)
        print(url)

    # if not re.search("\.(jpg|JPG)$",link["href"]):
    # x = link["href"]







































