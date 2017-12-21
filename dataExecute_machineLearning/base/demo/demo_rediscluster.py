# -*- coding: utf-8 -*-
__author__ = 'sss'
from rediscluster import StrictRedisCluster

'''

pip install redis-py-cluster
    1. 连接master节点
    2. 使用cli连接，集群中单个节点时，有些key时设置不进去的
    3. redis使用docker组建集群，不能使用docker内网IP地址

'''

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

if __name__=='__main__':

    redisClient = conredis()
    redis_expiretime = 1200
    redisClient.set('testkey', 12, redis_expiretime)
    redisClient.incr('testkey', 13)

    print(redisClient.get('testkey'))

    redisClient.keys("*")
    redisClient.flushall()