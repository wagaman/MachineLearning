from bs4 import BeautifulSoup
import requests
import re
from selenium import webdriver
import time

__author__ = 'Administrator'


defalut_headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.104 Safari/537.36",
    "Host": "weixin.sogou.com",
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.8",

    "Cookie":"SUV=0011889C3CA8F7FC58DD006334AD1859; SMYUV=1492327430061771; UM_distinctid=15b75a57978629-0af03cd69053d4-4e45062e-1fa400-15b75a579793f4; SUID=84A405242A0B940A0000000058FB8AA5; GOTO=Af99047; ABTEST=8|1498093726|v1; IPLOC=CN1100; weixinIndexVisited=1; SNUID=CCA264C1AEAAFD7D6C0F1638AF562756; JSESSIONID=aaaXtjSlJvfQ-anNz0IXv; sct=24; LSTMV=486%2C130; LCLKINT=150922",

    "X-Requested-With": "XMLHttpRequest"
}


weixin_headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.104 Safari/537.36",
    "Host": "mp.weixin.qq.com",
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.8",

    "X-Requested-With": "XMLHttpRequest"
}

def extract_num_one(str):
    SEARCH_PAT = re.compile(r'(\d+)')
    pat_search = SEARCH_PAT.search(str)
    if pat_search != None:
        return pat_search.group(0)



def get_category_weixin(category, start_page=1, max_page=10):

    weixins = []
    for page in range(start_page, max_page):
        page = category if page == 0 else page
        url = 'http://weixin.sogou.com/pcindex/pc/' + category + '/' + str(page) + '.html'
        '''测试编码
        print(requests.get(url, headers=defalut_headers, timeout=60).apparent_encoding)
        '''
        time.sleep(0.6)
        response = requests.get(url, headers=defalut_headers, timeout=60)
        response.encoding = 'utf-8'
        html = response.text
        soup = BeautifulSoup(html, 'lxml')
        for div in soup.find_all('div', class_='txt-box'):
            weixin = {}

            weixin['title'] = div.find('h3').find('a').text
            weixin['href'] = div.find('h3').find('a')['href']
            weixin['summary'] = div.find('p', class_='txt-info').text
            weixin['author_name'] = div.find('a', class_='account').text
            weixin['author_url'] = div.find('a', class_='account')['href']

            time.ctime(int(div.find('span', class_='s2')['t']))
            weixin['time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

            weixins.append(weixin)

    return weixins


def get_hotlist():

    hotwords = []
    url = 'http://weixin.sogou.com/'
    time.sleep(0.6)
    response = requests.get(url, headers=defalut_headers, timeout=60)
    response.encoding = 'utf-8'
    html = response.text

    soup = BeautifulSoup(html, 'lxml')
    for li in soup.find('ol', id='topwords').find_all('li'):
        hotword = {}

        hotword['word'] = li.find('a')['title']
        hotword['hot_index'] = extract_num_one(li.find('span', class_='lan-line').find('span')['style'])


        hotwords.append(hotword)

    return hotwords

def get_search_chapter_weixin(searchword, start_page=1, max_page=3):
    chapters = []
    for page in range(start_page, max_page):
        params = {'query': searchword,
                  'type': '2',
                  'ie': 'utf8',
                  'page': page}
        url = 'http://weixin.sogou.com/weixin'
        time.sleep(0.6)
        response = requests.get(url, headers=defalut_headers, params=params, timeout=60)
        response.encoding = 'utf-8'
        html = response.text
        soup = BeautifulSoup(html, 'lxml')

        #文章
        try:
            for li in soup.find('ul', class_='news-list').find_all('li'):
                chapter = {}

                div = li.find('div', class_='txt-box')
                chapter['title'] = div.find('h3').find('a').text
                chapter['url'] = div.find('h3').find('a')['href']
                chapter['summary'] = div.find('p', class_='txt-info').text

                chapter['author_name'] = div.find('a', class_='account').text
                chapter['author_url'] = div.find('a', class_='account')['href']

                time.ctime(int(div.find('div', class_='s-p')['t']))
                chapter['time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                chapters.append(chapter)
        except:
            pass

    return chapters

def get_search_media_weixin(searchword, start_page=1, max_page=3):
    meidias = []
    for page in range(start_page, max_page):
        params = {'query': searchword,
                  'type': '1',
                  'ie': 'utf8',
                  'page': page}
        url = 'http://weixin.sogou.com/weixin'
        time.sleep(0.6)
        response = requests.get(url, headers=defalut_headers, params= params, timeout=60)
        response.encoding = 'utf-8'
        html = response.text
        soup = BeautifulSoup(html, 'lxml')

        #文章
        try:
            for li in soup.find('ul', class_='news-list2').find_all('li'):

                meidia = {}

                meidia['name'] = li.find('div', class_='txt-box').find('p', class_='tit').find('a').text
                meidia['url'] = li.find('div', class_='txt-box').find('p', class_='tit').find('a')['href']
                meidia['id'] = li.find('div', class_='txt-box').find('p', class_='info').find('label').text

                dls = li.find_all('dl')
                meidia['latest_chapter_title'] = dls.pop().find('dd').find('a').text
                meidia['institution'] = dls.pop().find('dd').text
                meidia['intro'] = dls.pop().find('dd').text
                meidias.append(meidia)
        except:
            pass

    return meidias

def get_chapter_by_url(url):

    time.sleep(1.6)
    try:
        response = requests.get(url, headers=weixin_headers, timeout=60)
        response.encoding = 'utf-8'
        html = response.text
        soup = BeautifulSoup(html, 'lxml')
        chapter = soup.find('div', id='js_content').text
        return chapter
    except:
        pass
        return ''



def get_media_by_url(url):
    chapters = []

    chromedriver = "C:\\Users\Administrator\AppData\Local\Google\Chrome\Application\chromedriver.exe"
    driver = webdriver.Chrome(chromedriver)
    driver.get(url)
    driver.page_source
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')

    media = {}
    media['name'] = soup.find('strong', class_='profile_nickname').text
    media['id'] = soup.find('p', class_='profile_account').text
    descs = soup.find_all('div', class_='profile_desc_value')
    media['intro'] = descs.pop().text
    media['institution'] = descs.pop()['title']

    #文章
    try:
        for div in soup.find_all('div', class_='weui_media_box appmsg'):

            chapter = {}
            chapter['title'] = div.find('h4', class_='weui_media_title').text
            chapter['url'] = 'https://mp.weixin.qq.com' + div.find('h4', class_='weui_media_title')['hrefs']
            chapter['summary'] = div.find('p', class_='weui_media_desc').text
            chapter['media'] = media
            chapter['time'] = div.find('p', class_='weui_media_extra_info').text.replace('原创', '')
            chapters.append(chapter)
    except:
        pass

    return chapters



