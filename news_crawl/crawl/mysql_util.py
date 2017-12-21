__author__ = 'Administrator'


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