import json
import time
import traceback
import math
import requests
from bs4 import BeautifulSoup
from single_site.zhihu.zh_utils import parse_num
import re
from selenium import webdriver


defalut_headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0",
    "Host": "www.zhihu.com",
    "X-Requested-With": "XMLHttpRequest"
}

def extract_num_one(str):
    SEARCH_PAT = re.compile(r'(\d+)')
    pat_search = SEARCH_PAT.search(str)
    if pat_search != None:
        return pat_search.group(0)


def get_login_session():
    with open('config.json') as f:
        config = json.load(f)
    session = requests.Session()
    login_result = session.post('http://www.zhihu.com/login/email', data=config, headers=defalut_headers).json()
    if login_result['r'] == 1:
        print('登录失败:', login_result['msg'])
        if login_result['errcode'] == 1991829:  # 输入验证码
            r = session.get('http://www.zhihu.com/captcha.gif')
            with open('captcha.gif', 'wb') as f:
                f.write(r.content)
            captcha = input('请输入验证码（当前目录下captcha.gif）：')
            config['captcha'] = captcha
            r = session.post('http://www.zhihu.com/login/email', data=config, headers=defalut_headers)
            login_result = r.json()
            if login_result['r'] == 1:
                print('登录失败:', login_result['msg'])
                exit(1)
            else:
                print('登录成功！')
    else:
        print('登录成功！')
    return session




def get_huati_questions_list(topic_id, output_file, start_page=1, max_page=10, sleep_sec=5, max_try=3):
    '''
    按照时间倒序获取某话题下的问题列表
    爬取的属性：ID，标题，提出时间，来自的子话题，回答数量

    2016年2月后知乎不再提供“全部问题”页面
    2016年2月26日恢复了23日上线时去掉的「全部问题」列表
    参见 https://www.zhihu.com/question/40470324
    '''

    def _get_each_question(page):
        try:
            url = 'http://www.zhihu.com/topic/%d/questions?page=%d' % (topic_id, page)
            html = requests.get(url, headers=defalut_headers, timeout=60).text
            soup = BeautifulSoup(html, 'lxml')
            for div in soup.find_all('div', attrs={'itemprop': 'question'}):
                question = {}

                subtopic = div.find('div', class_='subtopic')
                if subtopic:
                    question['subtopic'] = subtopic.a.text
                question['a_count'] = int(div.find('meta', attrs={'itemprop': 'answerCount'})['content'])
                question['ts'] = int(div.find('span', class_='time')['data-timestamp']) // 1000
                a = div.find('a', class_='question_link')
                question['id'] = int(a['href'][10:])
                question['title'] = a.text.strip()

                json.dump(question, output_file, ensure_ascii=False)
                output_file.write('\n')
            return True
        except Exception:
            traceback.print_exc()
            return False

    cur_page = start_page
    while cur_page < start_page + max_page:
        try_count = 0
        while not _get_each_question(cur_page):
            if try_count > max_try:
                break
            else:
                try_count += 1
            time.sleep(sleep_sec)
        if try_count > max_try:
            print('error occurs in get_questions_list!')
            break
        print('current page: ', cur_page)
        cur_page += 1
        time.sleep(sleep_sec)


def get_search_list(search_word, output_file, start_page=1, max_page=10, sleep_sec=5, max_try=3):
    '''
    问题和优质答案
    '''

    url = 'http://www.zhihu.com/search?type=content&q=' + search_word

    def _get_all_html(url):
        chromedriver = "C:\\Users\Administrator\AppData\Local\Google\Chrome\Application\chromedriver.exe"
        driver = webdriver.Chrome(chromedriver)
        driver.get(url)
        time.sleep(0.6)
        try:
            for i in range(1, max_page):
                driver.find_element_by_class_name('zu-button-more').click()
                time.sleep(0.6)
        except:
            print('抓取完成')
        finally:
            html = driver.page_source
            return html

    html = _get_all_html(url)
    soup = BeautifulSoup(html, 'lxml')
    answers = []
    for li in soup.find_all('li', class_='item clearfix'):
        question = {}
        a = li.find('a', class_='js-title-link')
        question['id'] = int(a['href'][10:])
        question['title'] = a.text.strip()
        json.dump(question, output_file, ensure_ascii=False)
        output_file.write('\n')

        answer = {}
        div = li.find('div', class_='entry answer')
        if div is not None:
            try:
                answer['url'] = div.find('link', attrs={'itemprop': 'url'})['href']
                if div.find('a', class_='js-vote-count') is not None:
                    answer['up'] = div.find('a', class_='js-vote-count').text
                if div.find('span', class_='count') is not None:
                    answer['up'] = div.find('span', class_='count').text
                answer['author'] = div.find('div', class_='entry-content js-collapse-body')['data-author-name']
                answer['content'] = div.find('script', class_='content').text
                answer['time'] = div.find('a', class_='time text-muted').text
                answer['question'] = question['title']
            except:
                print(li)
            finally:
                answers.append(answer)

    return answers


def get_question(question_id):

    url = 'http://www.zhihu.com/question/%d' % (question_id)
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


def get_voters_profile(answer_id):
    voters = []

    def _extract_voters(url):
        r = requests.get(url, headers=defalut_headers, timeout=60).json()
        for div in r['payload']:
            soup = BeautifulSoup(div, 'lxml')
            block = soup.find('a', class_='zm-item-link-avatar')
            if block:
                uid = block['href'][8:]
            else:
                uid = -1  # 匿名投票
                voters.append((uid, [0, 0, 0, 0]))
            block = soup.find('ul', class_='status')
            if block:
                # 赞同数, 感谢数, 提问数, 回答数
                profile = [parse_num(s.partition(' ')[0]) for s in block.text.split('\n') if s.strip() != '']
            else:
                profile = [-1, -1, -1, -1]
            voters.append((uid, profile))

        return r['paging']['next']

    url = 'https://www.zhihu.com/answer/%d/voters_profile' % answer_id
    while True:
        n = _extract_voters(url)
        if n == '':
            break
        url = 'https://www.zhihu.com' + n
    return voters


def get_person(session, person_id):
    # to be implemented
    pass
