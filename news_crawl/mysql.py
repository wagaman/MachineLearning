__author__ = 'Administrator'

import pymysql

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

def db_fetch_one(db, sql):
    cursor = db.cursor()
    # 执行sql语句
    cursor.execute(sql)
    data = cursor.fetchone()
    return data[0]

sql = "insert into num_address(number, address) values (%s, %s)"
params = ('13000161', '山东烟台 联通')
db_insert(db, sql, params)

db.close()