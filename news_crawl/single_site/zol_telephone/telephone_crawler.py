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
    "Host": "detail.zol.com.cn",
    "Cookie": "z_pro_city=s_provice%3Dbeijing%26s_city%3Dchaoyangqu; userProvinceId=1; userCityId=478; userCountyId=0; userLocationId=1; realLocationId=1; userFidLocationId=1; ip_ck=5MWG4P/0j7QuMzI3NzUzLjE0OTkzMzE5NzY%3D; lv=1499389798; vn=2; __adm__=1; _ga=GA1.3.1017104092.1499390236; _gid=GA1.3.1043543699.1499390236; Hm_lvt_36599089aeb36f4923b9b9c9bfa76ac1=1499390236; Hm_lpvt_36599089aeb36f4923b9b9c9bfa76ac1=1499390450; _smt_uid=595ee11b.160bb695; _ga=GA1.4.1017104092.1499390236; _gid=GA1.4.1043543699.1499390236; Adshow=3; Hm_lvt_ae5edc2bc4fc71370807f6187f0a2dd0=1499332149,1499389971; Hm_lpvt_ae5edc2bc4fc71370807f6187f0a2dd0=1499392779; visited_subcateId=57|0|758|485|223; visited_serachKw=%u5E7F%u5DDE%u91D1%u9E4F%2CS1898%7Cabc%2CS1898%7C%u7EA2%u7C73%uFF0C1s%7C%u5E7F%u5DDE%u91D1%u9E4F%2CA5882%7CEnfora%2CGSM0204%7CEliya%2CPD101a; listSubcateId=57; visited_subcateProId=57-366544%2C198460%2C85829%2C384973%2C138214%7C16-1172843%2C1173124%2C1173647%2C389677",
}


def get_telephone(keyword):

    url = 'http://detail.zol.com.cn/index.php?c=SearchList&keyword=' + keyword
    response = requests.get(url, headers=defalut_headers, timeout=60)
    html = response.text
    soup = BeautifulSoup(html, 'lxml')

    div = soup.find('div', class_='list-item clearfix')
    if div is not None:
        try:
            telephone = {'price': div.find('b', class_='price-type').text}
            url = div.find('ul', class_='param clearfix').find_all('li')[7].find('a')['href']
            url = 'http://detail.zol.com.cn' + url

            response = requests.get(url, headers=defalut_headers, timeout=60)
            html = response.text
            soup = BeautifulSoup(html, 'lxml')
            ps = soup.find('ul', class_='product-param-item').find_all('p')
            for p in ps:
                if '分辨率' in p.text:
                    telephone['主屏分辨率'] = p['title']
                elif '尺寸' in p.text:
                    telephone['主屏尺寸'] = p['title']
                elif '内存' in p.text:
                    telephone['内存'] = p['title']
                elif '后置摄像头' in p.text:
                    telephone['后置摄像头'] = p['title']
                elif '前置摄像头' in p.text:
                    telephone['前置摄像头'] = p['title']
                elif '电池容量' in p.text:
                    telephone['电池容量'] = p['title']
                elif '核心数' in p.text:
                    telephone['核心数'] = p['title']

            return telephone
        except:
            pass


#telephone = get_telephone('华硕,T00F')
#print(1)

