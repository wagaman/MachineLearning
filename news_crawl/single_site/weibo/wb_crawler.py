from bs4 import BeautifulSoup
from selenium.common.exceptions import TimeoutException
import requests
import re
from selenium import webdriver
import time

__author__ = 'Administrator'


defalut_headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.104 Safari/537.36",
    "Host": "weibo.com",
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.8",
    "Cookie": "SINAGLOBAL=56924263082.47178.1490961570261; un=18810046675; YF-Ugrow-G0=169004153682ef91866609488943c77f; _s_tentry=-; Apache=1280022376460.9653.1498005913271; ULV=1498005913290:13:6:4:1280022376460.9653.1498005913271:1497930000591; login_sid_t=b1dd8e0e56eeaca308c1bd7087a8302a; YF-V5-G0=8a3c37d39afd53b5f9eb3c8fb1874eec; SCF=Aqytu0ELBvn8W7wF5yl7Mq3jrQnc2GSFI2WUL3qoQ2kWQaEJlhVcnGZM2W-sajT5IObgHVaq9YTVjqCjSsipie4.; SUHB=0ElaweFjilL5LF; YF-Page-G0=35f114bf8cf2597e9ccbae650418772f; SUB=_2AkMuFU0CdcPxrAVQmvwSzW3la4pH-jydwCT0An7uJhMyAxh87gcjqSUpvu651fvfbp-l5MANDhIjCjQTTg..; SUBP=0033WrSXqPxfM72wWs9jqgMF55529P9D9WWnJaf0YJ7vRa.hzKEd1XNG5JpVF02R1h27ehBcSoMf; UOR=cuiqingcai.com,widget.weibo.com,login.sina.com.cn; appkey=; WB_register_version=dd90749cc052f754; TC-Ugrow-G0=370f21725a3b0b57d0baaf8dd6f16a18; TC-V5-G0=a472c6c9af48bc4b9df1f924ca5cce70; TC-Page-G0=0cd4658437f38175b9211f1336161d7d",
    "X-Requested-With": "XMLHttpRequest"
}

def extract_num_one(str):
    SEARCH_PAT = re.compile(r'(\d+)')
    pat_search = SEARCH_PAT.search(str)
    if pat_search != None:
        return pat_search.group(0)



def get_category_weibo(category, start_page=1, max_page=10):

    weibos = []
    for page in range(start_page, max_page):
        url = 'http://weibo.com/a/aj/transform/loadingmoreunlogin?ajwvr=6&category=' + category + '&page=' + str(page) +'&lefnav=0'
        html = requests.get(url, headers=defalut_headers, timeout=60).text.encode('latin-1').decode('unicode_escape').replace('\/', '/')
        soup = BeautifulSoup(html, 'lxml')
        for div in soup.find_all('div', attrs={'action-type': 'feed_list_item'}):
            weibo = {}

            weibo['title'] = div.text.strip().split('\n')[0]

            author_time = div.find('div', class_='subinfo_box clearfix').text
            weibo['author'] = author_time.split('\n')[2]
            weibo['time'] = author_time.split('\n')[3]

            div.find_all().pop()
            praise_repeat_forward = div.find_all('span', class_='subinfo_rgt S_txt2')
            weibo['praise'] = extract_num_one( praise_repeat_forward.pop().text)
            weibo['repeat'] = extract_num_one(praise_repeat_forward.pop().text)
            weibo['forward'] = extract_num_one(praise_repeat_forward.pop().text)
            weibos.append(weibo)

    return weibos


def get_hotlist_weibo(category, driver=None):

    weibos = []
    url = 'http://s.weibo.com/top/summary?cate=' + category
    if driver is None:
        chromedriver = "C:\\Users\Administrator\AppData\Local\Google\Chrome\Application\chromedriver.exe"
        driver = webdriver.Chrome(chromedriver)
    driver.get(url)
    html = driver.page_source

    soup = BeautifulSoup(html, 'lxml')
    for tr in soup.find_all('tr', attrs={'action-type': 'hover'}):
        weibo = {}

        weibo['title'] = tr.find('td', class_='td_02').find('a').text
        weibo['href'] = 'http://s.weibo.com'+tr.find('td', class_='td_02').find('a')['href']
        weibo['search_index'] = tr.find('td', class_='td_03').text
        weibo['hot_index'] = extract_num_one(tr.find('td', class_='td_04').find('span')['style'])

        weibos.append(weibo)

    return weibos

def get_search_weibo(searchword, driver=None):

    weibos = []
    url = 'http://s.weibo.com/weibo/' + searchword
    if driver is None:
        chromedriver = "C:\\Users\Administrator\AppData\Local\Google\Chrome\Application\chromedriver.exe"
        driver = webdriver.Chrome(chromedriver)
    driver.get(url)
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    for div in soup.find_all('div', class_='WB_cardwrap S_bg2 clearfix'):
        try:
            weibo = {}

            weibo['author_name'] = div.find('a', class_='W_texta W_fb')['nick-name']
            weibo['author_url'] = div.find('a', class_='W_texta W_fb')['href']

            weibo['title'] = div.find('p', attrs={'node-type': 'feed_list_content'}).text
            weibo['time'] = div.find('div', class_='feed_from W_textb').find('a').text
            weibo['crawl_time'] = time.strftime('%H:%M:%S', time.localtime())
            weibos.append(weibo)
        except Exception:
            pass

    #热门文章
    chapters = []
    for div in soup.find_all('div', class_='shortlink_feed feed_list_web2 '):
        try:
            chapter = {}

            chapter['title'] = div.find('a', class_='W_texta W_fb')['title']
            chapter['url'] = div.find('a', class_='W_texta W_fb')['href']
            chapter['intro'] = div.find('p', class_='link_info W_textb').text

            chapter['author_name'] = div.find('span', class_='linkAC_from').find('a').text
            chapter['author_url'] = div.find('span', class_='linkAC_from').find('a')['href']

            chapter['time'] = div.find_all('span', class_='linkAC_from')[1].text
            chapter['crawl_time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            chapters.append(chapter)
        except:
            pass

    #相关人物
    persons = []
    for div in soup.find_all('div', class_='rela_person2 clearfix'):
        try:
            person = {}

            person['name'] = div.find('p', class_='name').find('a').text
            person['url'] = div.find('p', class_='name').find('a')['href']
            person['intro'] = div.find('p', class_='intro').text

            persons.append(person)
        except:
            pass

    return weibos, chapters, persons




