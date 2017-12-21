import random
from bs4 import BeautifulSoup
import requests
import re
from selenium import webdriver
import time
import json

__author__ = 'Administrator'


defalut_headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.104 Safari/537.36",
    "Host": "zhihu.sogou.com",
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.8",

    "X-Requested-With": "XMLHttpRequest"
}

zhihu_headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.104 Safari/537.36",
    "Host": "www.zhihu.com",
    "Accept": "application/json, text/plain, */*",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.8",

    "cookie": 'q_c1=9f49f26933c24cd1bdae547b02cfef6b|1499304485000|1499304485000; q_c1=bf83564bb35740129b750640a29bd37b|1499304485000|1499304485000; _zap=b8733d60-fd56-4366-91c5-2daf9d396332; d_c0="AHCCvU-0BQyPTl8bJudFItgJXhrRr4bZ-n4=|1499321242"; __utma=51854390.2130606608.1499321243.1499321243.1499321243.1; __utmz=51854390.1499321243.1.1.utmcsr=zhihu.com|utmccn=(referral)|utmcmd=referral|utmcct=/question/30532407; __utmv=51854390.100--|2=registration_date=20170706=1^3=entry_date=20170706=1; aliyungf_tc=AQAAANULYnxHfQQAYQzLb6C4sfRMIeuN; r_cap_id="YTJhYzNlZDM3YmVlNGE2NDk1ZTJlMTE2NTU1NjI1YzM=|1499646648|05b69285c2651a30d97a87301b40c6a8ff9e6041"; cap_id="ZTM5ZGVlZjY2MTkwNDM4MThkMTEyM2MwYzE3YmI5Mjk=|1499646648|0740aad2c45f14d990c536c9de566d155058a104"; capsion_ticket="2|1:0|10:1499656617|14:capsion_ticket|44:ODQzNjZkN2ExYmM0NDEzOGExYmU4OGJiZWI3YWY0ZGU=|a62a8ff35981526f56b3facf899778ab46667846d31529e38c46938e44024f90"; z_c0="2|1:0|10:1499656629|4:z_c0|92:Mi4wQUFCQ05FNjBCUXdBY0lLOVQ3UUZEQ1lBQUFCZ0FsVk50WDZLV1FDaFBUMWlrTm4wcDBUYkw0XzhaMk9rWmZwb1d3|208fd8afa5044b7ea415d3bdfc14413005d6b8021fb27777891dbb6127029383"; _xsrf=66cdee21-99fa-487b-894d-e1f069d5da74',

    "X-Requested-With": "XMLHttpRequest"
}

def extract_num_one(str):
    SEARCH_PAT = re.compile(r'(\d+)')
    pat_search = SEARCH_PAT.search(str)
    if pat_search != None:
        return pat_search.group(0)

def get_category_zhihu(category, start_page=1, max_page=10, key='今日最热'):

    zhihus = []
    '''
    http://zhihu.sogou.com/include/pc/pc/hot/hot0.html
    http://zhihu.sogou.com/include/pc/5/hot/hot1.html
    http://zhihu.sogou.com/include/pc/5/hot/hot2.html
    '''
    for page in range(start_page, max_page):
        if page == 0:
            url = 'http://zhihu.sogou.com/include/pc/pc/' + category[key] + '0.html'
        else:
            url = 'http://zhihu.sogou.com/include/pc/0/' + category[key] + str(page) + '.html'

        '''测试编码
        print(requests.get(url, headers=defalut_headers, timeout=60).apparent_encoding)
        '''
        time.sleep(0.6)
        response = requests.get(url, headers=defalut_headers, timeout=60)
        response.encoding = 'utf-8'
        html = response.text
        soup = BeautifulSoup(html, 'lxml')
        for li in soup.find_all('li'):
            zhihu = {}

            zhihu['title'] = li.find('p', class_='tit').find('a').text
            zhihu['href'] = li.find('p', class_='tit').find('a')['href']
            zhihu['answer_author_name'] = li.find('p', class_='p1').find('a').text
            zhihu['answer_author_url'] = li.find('p', class_='p1').find('a')['href']
            zhihu['answer_zan'] = li.find('p', class_='p1').find('span', class_='zan').text
            zhihu['answer_summary'] = li.find('p', class_='p2').text

            zhihus.append(zhihu)

    return zhihus


def get_hotlist():

    hotwords = []
    url = 'http://zhihu.sogou.com/'
    time.sleep(0.6)
    response = requests.get(url, headers=defalut_headers, timeout=60)
    response.encoding = 'utf-8'
    html = response.text

    soup = BeautifulSoup(html, 'lxml')
    for li in soup.find('ol', class_='hot-news').find_all('li'):
        hotword = {}

        hotword['word'] = li.find('a').text
        hotword['hot_index'] = extract_num_one(li.find('span', class_='lan-line').find('span')['style'])


        hotwords.append(hotword)

    return hotwords

def get_search_zhihu(searchword, start_page=1, max_page=3):
    zhihus = []
    for page in range(start_page, max_page):
        params = {'query': searchword,
                  '_sug_type_': 1,
                  'sut': 1245,
                  'ie': 'utf8',
                  'lkt': '0,0,0',
                  'page': page}
        url = 'http://zhihu.sogou.com/zhihu'
        time.sleep(0.6)
        response = requests.get(url, headers=defalut_headers, params=params, timeout=60)
        response.encoding = 'utf-8'
        html = response.text
        soup = BeautifulSoup(html, 'lxml')

        #文章

        for div in soup.find_all('div', class_='result-about-list'):
            zhihu = {}
            try:
                zhihu['question_title'] = div.find('h4').find('a').text
                zhihu['question_url'] = div.find('h4').find('a')['href']
                zhihu['answer_zan'] = extract_num_one(div.find('p', class_='about-answer').find('span').text)
                if div.find('p', class_='about-answer').find('a') is None:
                    zhihu['answer_author_name'] = '匿名/知乎用户'
                    zhihu['answer_author_url'] = ''
                else:
                    zhihu['answer_author_name'] = div.find('p', class_='about-answer').find('a').text
                    zhihu['answer_author_url'] = div.find('p', class_='about-answer').find('a')['href']
                zhihu['answer_summary'] = div.find('p', class_='summary-answer-num').find('a').text
                zhihu['answer_url'] = div.find('p', class_='summary-answer-num').find('a')['href']
                zhihu['answer_num'] = extract_num_one(div.find('span', class_='answer-num').text)
            except:
                pass
            zhihus.append(zhihu)


    return zhihus

def get_question_selenium(question_id):

    url = 'http://www.zhihu.com/question/%d' % (question_id)
    time.sleep(0.6)
    response = requests.get(url, headers=defalut_headers, timeout=60)
    if response.status_code == 404:
        return None
    soup = BeautifulSoup(response.text, 'lxml')
    question = {}
    question['id'] = question_id
    # 标题
    question['title'] = soup.find('h1', class_='QuestionHeader-title').text.strip()
    # 内容
    question['detail'] = soup.find('div', class_='QuestionRichText').text.strip()

    # 所属的话题标签
    question['tags'] = [a.string.strip() for a in soup.find_all("a", class_='TopicLink')]

    def _extract_answer(block):
        answer = {}
        answer['id'] = block['name']
        responder_block = block.find('a', class_='UserLink-link')
        # /people/<responder> or 匿名用户
        answer['responder'] = responder_block['href'][8:] if responder_block else -1
        # 日期
        answer['created'] = block.find('div', class_='ContentItem-time').text.strip().replace('发布于', '')
        # 内容
        answer['content'] = block.find('div', class_='RichContent-inner').text.strip()
        # 赞同数
        answer['upvote'] = block.find('button', class_='VoteButton--up').text.strip()
        return answer

    def _get_all_html(url):
        chromedriver = "C:\\Users\Administrator\AppData\Local\Google\Chrome\Application\chromedriver.exe"
        driver = webdriver.Chrome(chromedriver)
        driver.get(url)
        time.sleep(0.6)
        driver.execute_script("window.scrollBy(0,10500)")
        try:
            while driver.find_element_by_class_name('QuestionMainAction') is not None:
                driver.find_element_by_class_name('QuestionMainAction').click()
                time.sleep(0.6)
        except:
            print('抓取完成')
        finally:
            html = driver.page_source

            return html

    # 回答数目
    answers_count = extract_num_one(soup.find('div', id='QuestionAnswers-answers').text)
    answers_count = int(answers_count)

    if answers_count > 23:
        url = 'https://www.zhihu.com/question/' + str(question_id)
        html = _get_all_html(url)
        soup = BeautifulSoup(html, 'lxml')
    print('答案数：' + str(len(soup.find_all('div', class_='ContentItem AnswerItem'))) )
    # 答案
    answers = []
    for block in soup.find_all('div', class_='ContentItem AnswerItem'):
        if block.find('div', class_='answer-status') is not None:
            continue  # 忽略建议修改的答案
        answers.append(_extract_answer(block))

    question['answers'] = answers
    return question


def get_question_json(question_id):

    url = 'https://www.zhihu.com/api/v4/questions/' + str(question_id) +'/answers'
    params = {'sort_by': 'default',
              'include': 'data[*].is_normal,is_collapsed,collapse_reason,is_sticky,collapsed_by,suggest_edit,comment_count,can_comment,content,editable_content,voteup_count,reshipment_settings,comment_permission,mark_infos,created_time,updated_time,review_info,relationship.is_authorized,is_author,voting,is_thanked,is_nothelp,upvoted_followees;data[*].author.follower_count,badge[?(type=best_answerer)].topics',
              'limit': 20,
              'offset': 0}
    time.sleep(2.6)
    response = requests.get(url, headers=zhihu_headers, params=params, timeout=60)
    if response.status_code == 404:
        return None
    json_data = json.loads(response.text)
    question = json_data['data'][0]['question']
    question['answer_num'] = json_data['paging']['totals']
    question['answers'] = json_data['data']

    page_num = int(question['answer_num'] / 20) + 1

    for page_index in range(1, 5):
        url = 'https://www.zhihu.com/api/v4/questions/' + str(question_id) +'/answers'
        params = {'sort_by': 'default',
                  'include': 'data[*].is_normal,is_collapsed,collapse_reason,is_sticky,collapsed_by,suggest_edit,comment_count,can_comment,content,editable_content,voteup_count,reshipment_settings,comment_permission,mark_infos,created_time,updated_time,review_info,relationship.is_authorized,is_author,voting,is_thanked,is_nothelp,upvoted_followees;data[*].author.follower_count,badge[?(type=best_answerer)].topics',
                  'limit': page_index * 20 + 20,
                  'offset': page_index * 20}
        time.sleep(30 * random.random())
        response = requests.get(url, headers=zhihu_headers, params=params, timeout=60)
        if response.status_code == 404:
            return None
        json_data = json.loads(response.text)
        question['answers'].extend(json_data['data'])


    return question




