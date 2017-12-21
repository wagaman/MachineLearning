import time

__author__ = 'Administrator'

from single_site.zol_telephone import telephone_crawler
import mysql_util
import pymysql

db = pymysql.connect("127.0.0.1", "root", "root", "ip", charset="utf8")

datas = mysql_util.db_fetch_all(db, "select DISTINCT(CONCAT(brand,',',model)), brand,model from telephone_info_2 where brand != 'EMULATIONAL' and update_time is null")

for data in datas:
    telephone = telephone_crawler.get_telephone(data[0])
    sql = "update telephone_info_2 set price = %s, resolution_power = %s, size = %s, camera = %s, camera_front = %s," \
          " memory = %s, core_num = %s, battery_capacity = %s, update_time = %s where brand = %s and model = %s"
    time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    if telephone is None:
        params = ('', '', '', '', '', '', '', '', time, data[1], data[2])
    else:
        params = (telephone['price'], telephone.get('主屏分辨率', ''), telephone.get('主屏尺寸', ''), telephone.get('后置摄像头', ''), telephone.get('前置摄像头', ''), telephone.get('内存', ''), telephone.get('核心数', ''), telephone.get('电池容量', ''), time, data[1], data[2])

    mysql_util.db_insert(db, sql, params)


print(1)