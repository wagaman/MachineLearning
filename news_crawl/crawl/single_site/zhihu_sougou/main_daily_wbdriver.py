_author__ = 'Administrator'
import re
import time
from single_site.zhihu_sougou import zhihu_crawler
from single_site.weixin import wx_crawler
from single_site.weibo import wb_crawler
import pymysql
from selenium import webdriver

def extract_num_one(str):
    SEARCH_PAT = re.compile(r'(\d+)')
    pat_search = SEARCH_PAT.search(str)
    if pat_search != None:
        return pat_search.group(0)

def db_insert(db, sql, params):
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    try:
        # 执行sql语句
        cursor.execute(sql, params)
        # 提交到数据库执行
        db.commit()
        return 0
    except:
        # 如果发生错误则回滚
        db.rollback()
        return 1


def db_fetch_one(db, sql):
    cursor = db.cursor()
    # 执行sql语句
    cursor.execute(sql)
    data = cursor.fetchone()
    return data[0]

def db_fetch_all(db, sql):
    cursor = db.cursor()
    # 执行sql语句
    cursor.execute(sql)
    data = cursor.fetchall()
    return data


def insert_hotword_db(db, hotword_wx, hotword_zhihu):
    #获取最大批次
    max_batch = db_fetch_one(db, "SELECT MAX(batch) FROM list_hotword")
    max_batch = 1 if max_batch is None else int(max_batch) + 1

    cru_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    day = time.strftime('%Y-%m-%d', time.localtime())
    for wx in hotword_wx:
        # SQL 插入语句
        sql = 'INSERT INTO list_hotword(domain,hotword, hot_index, batch, day, time) VALUES (%s, %s, %s, %s, %s, %s)'
        params = ('weixin', wx['word'], int(wx['hot_index']), max_batch, day, cru_time)
        db_insert(db, sql, params)

    for zh in hotword_zhihu:
        # SQL 插入语句
        sql = 'INSERT INTO list_hotword(domain,hotword, hot_index, batch, day, time) VALUES (%s, %s, %s, %s, %s, %s)'
        params = ('zhihu', zh['word'], zh['hot_index'], max_batch, day, cru_time)
        db_insert(db, sql, params)

def insert_hotword_weibo_db(db, hotword_wb):
    #获取最大批次
    max_batch = db_fetch_one(db, "SELECT MAX(batch) FROM list_hotword where domain = 'weibo'")
    max_batch = 1 if max_batch is None else int(max_batch) + 1

    cru_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    day = time.strftime('%Y-%m-%d', time.localtime())
    for wb in hotword_wb:
        sql = 'INSERT INTO list_hotword(domain,hotword, hot_index,search_index, batch, day, time) VALUES (%s, %s, %s,%s, %s, %s, %s)'
        params = ('weibo', wb['title'], int(wb['hot_index']), int(wb['search_index']), max_batch, day, cru_time)
        db_insert(db, sql, params)

def insert_hotword_search_db(db, hotword_wx, hotword_zhihu):
    #获取最大批次
    cru_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    day = time.strftime('%Y-%m-%d', time.localtime())

    for hotword in hotword_zhihu:
        search_rank = 1
        zhihus = zhihu_crawler.get_search_zhihu(hotword['word'], 1, 5)
        for zhihu in zhihus:
            try:
                # SQL 插入语句
                sql = 'INSERT INTO list_hotword_zhihu(question_title,question_url, answer_author_name, answer_author_url, answer_zan, answer_summary, answer_url, answer_num, hotword, search_rank, crawl_time, crawl_day) values (%s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s)'

                params = (zhihu['question_title'], zhihu['question_url'], zhihu['answer_zan'], zhihu['answer_author_name'], zhihu['answer_author_url'], zhihu['answer_summary'], zhihu['answer_url'], zhihu['answer_num'], hotword['word'], search_rank, cru_time, day)
                db_insert(db, sql, params)
                search_rank += 1
            except:
                pass

    for hotword in hotword_wx:
        search_rank = 1
        chapters = wx_crawler.get_search_chapter_weixin(hotword['word'], 1, 5)
        for chapter in chapters:
            try:
                # SQL 插入语句
                sql = 'INSERT INTO list_hotword_weixin(title, href, summary, author_name, author_url, hotword,search_rank,  time, crawl_time, crawl_day) VALUES (%s, %s, %s, %s, %s, %s,%s, %s, %s, %s)'
                params = (chapter['title'], chapter['url'], chapter['summary'], chapter['author_name'], chapter['author_url'], hotword['word'], search_rank, chapter['time'], cru_time, day)
                db_insert(db, sql, params)
                search_rank += 1
            except:
                pass

def insert_hotword_search_weibo_db(db, hotword_weibo, driver=None):
    cru_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    day = time.strftime('%Y-%m-%d', time.localtime())

    for hotword in hotword_weibo:
        search_rank = 1
        weibos, chapters, persons = wb_crawler.get_search_weibo(hotword['title'], driver)
        for weibo in weibos:
            try:
                # SQL 插入语句
                sql = 'INSERT INTO list_hotword_weibo(title, author_name,author_url,hotword, search_rank,time, crawl_time, crawl_day) values (%s, %s, %s, %s, %s, %s,%s, %s)'

                params = (weibo['title'], weibo['author_name'], weibo['author_url'], hotword, search_rank, weibo['time'], cru_time, day)
                db_insert(db, sql, params)
                search_rank += 1
            except:
                pass
    search_rank = 1
    for chapter in chapters:
        try:
            # SQL 插入语句
            sql = 'INSERT INTO list_hotword_weibo(title, author_name,author_url,hotword, search_rank,time, crawl_time, crawl_day, summary, url) values (%s, %s, %s, %s, %s, %s,%s, %s, %s, %s)'

            params = (chapter['title'], chapter['author_name'], chapter['author_url'], hotword, search_rank, chapter['time'], cru_time, day, chapter['intro'], chapter['url'])
            db_insert(db, sql, params)
            search_rank += 1
        except:
            pass
    search_rank = 1
    for person in persons:

        try:
            # SQL 插入语句
            sql = 'INSERT INTO list_hotword_weibo(author_name,author_url,hotword, search_rank, crawl_time, crawl_day, summary) values (%s, %s, %s, %s, %s, %s,%s)'

            params = (person['title'], person['url'], hotword, search_rank, cru_time, day, person['intro'])
            db_insert(db, sql, params)
            search_rank += 1
        except:
            pass


def insert_category_weixin(db):
    category = {}
    category['热门'] = 'pc_0'
    category['推荐'] = 'pc_1'
    category['段子手'] = 'pc_2'
    category['养生堂'] = 'pc_3'
    category['私房活'] = 'pc_4'
    category['八卦精'] = 'pc_5'
    category['爱生活'] = 'pc_6'
    category['财经迷'] = 'pc_7'
    category['汽车迷'] = 'pc_8'
    category['科技咖'] = 'pc_9'
    category['潮人帮'] = 'pc_10'
    category['辣妈帮'] = 'pc_11'
    category['点赞党'] = 'pc_12'
    category['旅行家'] = 'pc_13'
    category['职场人'] = 'pc_14'
    category['美食家'] = 'pc_15'
    category['古今通'] = 'pc_16'
    category['学霸族'] = 'pc_17'
    category['星座控'] = 'pc_18'
    category['体育迷'] = 'pc_19'
    for key, value in category.items():
        weixins = wx_crawler.get_category_weixin(value, start_page=0, max_page=10)
        crawl_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        crawl_day = time.strftime('%Y-%m-%d', time.localtime())
        for weixin in weixins:
            sql = 'INSERT INTO list_category_weixin(title, href, summary, author_name, author_url, label, time, crawl_time, crawl_day) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)'
            params = (weixin['title'], weixin['href'], weixin['summary'], weixin['author_name'], weixin['author_url'], key, weixin['time'], crawl_time, crawl_day)
            db_insert(db, sql, params)


def insert_category_zhihu(db):
    category = {}
    category['今日最热'] = 'hot/hot'
    category['编辑推荐'] = 'recommend/recommend'
    category['运动'] = 'topic/topic1_'
    category['互联网'] = 'topic/topic2_'
    category['艺术'] = 'topic/topic3_'
    category['阅读'] = 'topic/topic4_'
    category['美食'] = 'topic/topic5_'
    category['动漫'] = 'topic/topic6_'
    category['汽车'] = 'topic/topic7_'
    category['生活方式'] = 'topic/topic8_'
    category['教育'] = 'topic/topic9_'
    category['摄影'] = 'topic/topic10_'
    category['历史'] = 'topic/topic11_'
    category['文化'] = 'topic/topic12_'
    category['旅行'] = 'topic/topic13_'
    category['职业发展'] = 'topic/topic14_'
    category['经济学'] = 'topic/topic15_'
    category['足球'] = 'topic/topic16_'
    category['篮球'] = 'topic/topic17_'
    category['投资'] = 'topic/topic18_'
    category['音乐'] = 'topic/topic19_'
    category['电影'] = 'topic/topic20_'
    category['法律'] = 'topic/topic21_'
    category['自然科学'] = 'topic/topic22_'
    category['设计'] = 'topic/topic23_'
    category['创业'] = 'topic/topic24_'
    category['健康'] = 'topic/topic25_'
    category['商业'] = 'topic/topic26_'
    category['体育'] = 'topic/topic27_'
    category['科技'] = 'topic/topic28_'
    category['化学'] = 'topic/topic29_'
    category['物理学'] = 'topic/topic30_'
    category['生物学'] = 'topic/topic31_'
    category['金融'] = 'topic/topic32_'

    for key, value in category.items():
        if key == '今日最热' or key == '编辑推荐':
            zhihus = zhihu_crawler.get_category_zhihu(category, start_page=0, max_page=50, key=key)
        else:
            zhihus = zhihu_crawler.get_category_zhihu(category, start_page=0, max_page=10, key=key)
        crawl_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        crawl_day = time.strftime('%Y-%m-%d', time.localtime())
        for zhihu in zhihus:
            sql = 'INSERT INTO list_category_zhihu(title, href, answer_author_name, answer_author_url, answer_zan, answer_summary, label, crawl_time, crawl_day) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)'
            params = (zhihu['title'], zhihu['href'], zhihu['answer_author_name'], zhihu['answer_author_url'], zhihu['answer_zan'], zhihu['answer_summary'], key, crawl_time, crawl_day)
            db_insert(db, sql, params)


def insert_hotword_weixin_chapter_db(db, crawl_day=None):
    hrefs = db_fetch_all(db, "select href from `list_hotword_weixin` where have_content is null and crawl_day = '" + crawl_day + "'")
    for data in hrefs:
        href = data[0]
        chapter = wx_crawler.get_chapter_by_url(href)
        sql = 'update list_hotword_weixin set text = %s , have_content = %s where href = %s'
        params = (chapter, 'yes', data[0]) if len(chapter) > 0 else (chapter, 'none', data[0])
        db_insert(db, sql, params)

def insert_category_weixin_chapter_db(db, crawl_day=None):
    hrefs = db_fetch_all(db, "select href from `list_category_weixin` where have_content is null and crawl_day = '" + crawl_day + "'")
    for data in hrefs:
        href = data[0]
        chapter = wx_crawler.get_chapter_by_url(href).strip()
        sql = "update list_category_weixin set text = %s , have_content = %s where href = %s"
        params = (chapter, 'yes', href)
        db_insert(db, sql, params)

def insert_category_zhihu_answer_db(db):
    hrefs = db_fetch_all(db, "select href,update_count from list_category_zhihu where have_content is null ")
    hrefs = set(hrefs)
    for data in hrefs:
        href = data[0]
        if str(href).__contains__('question'):
            question_id = extract_num_one(href)
            question_data = zhihu_crawler.get_question_json(question_id)

            try:
                for answer in question_data['answers']:
                    sql = "insert into list_zhihu_answer(question_id,question_title,excerpt,id,content,voteup_count,comment_count,updated_time,author_id,author_name,author_headline,author_gender) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                    params = (question_data['id'], question_data['title'],answer['excerpt'],answer['id'],answer['content'],answer['voteup_count'],answer['comment_count'],answer['updated_time'],answer['author']['id'],answer['author']['name'],answer['author']['headline'],answer['author']['gender'])
                    db_insert(db, sql, params)

                if len(question_data['answers']) > 0:
                    update_count = 0 if data[1] is None else int(data[1]) + 1
                    sql = "update list_category_zhihu set update_count = %s, have_content = %s where href = %s"
                    params = (update_count, 'yes', href)
                    db_insert(db, sql, params)
            except:
                sql = "update list_category_zhihu set update_count = %s, have_content = %s where href = %s"
                params = (update_count, 'no', href)
                db_insert(db, sql, params)


def insert_hotword_zhihu_answer_db(db):
    hrefs = db_fetch_all(db, "select question_url,update_count from list_hotword_zhihu where have_content is null ")
    hrefs = set(hrefs)
    for data in hrefs:
        href = data[0]
        if str(href).__contains__('question'):
            question_id = extract_num_one(href)
            question_data = zhihu_crawler.get_question_json(question_id)

        try:
            for answer in question_data['answers']:
                sql = "insert into list_zhihu_answer(question_id,question_title,excerpt,id,content,voteup_count,comment_count,updated_time,author_id,author_name,author_headline,author_gender) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                params = (question_data['id'], question_data['title'],answer['excerpt'],answer['id'],answer['content'],answer['voteup_count'],answer['comment_count'],answer['updated_time'],answer['author']['id'],answer['author']['name'],answer['author']['headline'],answer['author']['gender'])
                db_insert(db, sql, params)

            if len(question_data['answers']) > 0:
                update_count = 0 if data[1] is None else int(data[1]) + 1
                sql = "update list_hotword_zhihu set update_count = %s, have_content = %s where question_url = %s"
                params = (update_count, 'yes', href)
                db_insert(db, sql, params)
        except:
            sql = "update list_hotword_zhihu set update_count = %s, have_content = %s where question_url = %s"
            params = (update_count, 'no', href)
            db_insert(db, sql, params)



if __name__ == '__main__':
    # 打开数据库连接
    db = pymysql.connect("127.0.0.1", "root", "root", "news", charset="utf8")

    day = time.strftime('%Y-%m-%d', time.localtime())

    #微信热词文章抓取
    insert_hotword_weixin_chapter_db(db, crawl_day=day)
    #知乎各个类别的动态
    insert_category_zhihu(db)
    #微信各个类别的动态
    insert_category_weixin(db)
    #微信类别文章抓取
    insert_category_weixin_chapter_db(db, crawl_day=day)

    # 每天的搜索热词
    hotword_zhihu = zhihu_crawler.get_hotlist()
    hotword_wx = wx_crawler.get_hotlist()
    insert_hotword_search_db(db, hotword_wx, hotword_zhihu)
    insert_hotword_db(db, hotword_wx, hotword_zhihu)

    #知乎类别动态问题更新，添加一个字段更新次数
    insert_category_zhihu_answer_db(db)
    #知乎热搜词问题更新，添加一个字段更新次数
    insert_hotword_zhihu_answer_db(db)



    db.close()

