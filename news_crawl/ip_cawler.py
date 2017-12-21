from bs4 import BeautifulSoup
import requests
import pymysql
import time

__author__ = 'sss'

# 打开数据库连接
db = pymysql.connect("127.0.0.1", "root", "root", "ip", charset="utf8")

def db_insert(db, sql, params):
    cursor = db.cursor()
    try:
        # 执行sql语句
        cursor.execute(sql, params)
        # 提交到数据库执行
        db.commit()
    except Exception as e:
        # 如果发生错误则回滚
        print(e)
        db.rollback()

def getProv(phone_num):
    url = 'http://ip.cn/db.php?num='+phone_num
    time.sleep(0.2)
    try:
        response = requests.get(url, timeout=60)
        response.encoding = 'utf-8'
        html = response.text
        soup = BeautifulSoup(html, 'lxml')
        str = soup.find('div', class_='well').text
    except:
        str = ''
    try:
        prov = str[str.find('在城市:') + 4:str.find('基础数据库')].strip()
    except:
        prov = str
    return prov

def generate_num(prefix):
    all_num = []
    for index in range(3236, 10000):

        if index < 10:
            num = prefix + '000' + str(index)
        elif 10 <= index < 100:
            num = prefix + '00' + str(index)
        elif 100 <= index < 1000:
            num = prefix + '0' + str(index)
        elif 1000 <= index < 10000:
            num = prefix + str(index)
        all_num.append(num)
    return all_num

def insert_into(prefix):
    nums = generate_num(prefix)
    for num in nums:
        prov = getProv(num)
        sql = "insert into num_address(number, address) values (%s, %s)"
        params = (num, prov)
        db_insert(db, sql, params)




insert_into('176')
print( getProv('1300001') )


