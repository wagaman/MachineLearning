# -*- coding: utf-8 -*-
import os
import time
from rediscluster import StrictRedisCluster

__author__ = 'sss'


'''
nohup python demo_redis.py > /home/yimr/tmp.log &

linux查看所有python进程
ps -ef |grep python
'''

def get_FileSize_byte(filePath):
    fsize = os.path.getsize(filePath)
    return fsize

def conredis():

    #redis cluster的nodes
    REDIS_NODES=[
        {'host': '172.16.0.91', 'port': 6379},
        {'host': '172.16.0.93', 'port': 6379},
        {'host': '172.16.0.88', 'port': 6379},
        {'host': '172.16.0.89', 'port': 6379},
        {'host': '172.16.0.94', 'port': 6379},
        {'host': '172.16.0.92', 'port': 6379}
    ]

    redis_nodes = REDIS_NODES
    #redis的key的过期时间,单位s
    # redis_expiretime= 1200
    maxconnections = 50
    redisClient = StrictRedisCluster(startup_nodes=redis_nodes, max_connections=maxconnections)

    return redisClient

if __name__ == '__main__':
    accumulate = 0
    r = conredis()
    while True:
        cru_time = round(time.time())
        print(r.dbsize())
        keys = r.keys('*')

        area_set = {'0187', '0181', '0180', '0186', '0720', '0183', '0188', '0185', '0182', '018'}
        area_files = {}
        for area_id in area_set:
            area_files[area_id] = open('/home/yimr/sss/data/redis/018-' + area_id + '-' + str(cru_time) + '-' + str(accumulate), 'w')
            accumulate += 1

        for key in keys:
            try:
                area_id = key.split("|")[18]
                if area_id in area_set:
                    file_ptr = area_files[area_id]
                    new_line = key + '\n'
                    file_ptr.write(new_line)
            except:
                pass

        for area_id in area_set:
            area_files[area_id].close()

        for area_id in area_set:
            if get_FileSize_byte(area_files[area_id]) < 10:
                os.remove(area_files[area_id])

        os.popen('hadoop fs -put /home/yimr/sss/data/redis/* /user/yimr/sss/kafka_out/018 ')
        os.popen('rm -f /home/yimr/sss/data/redis/* ')
        r.flushall()
        time.sleep(60)







