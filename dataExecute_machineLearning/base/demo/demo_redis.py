# -*- coding: utf-8 -*-
__author__ = 'sss'
import redis
'''
在linux中 python redis.py运行会报错，不能叫redis.py。
        在python shell下也会报错

在windows中，python文件名和模块名相同，会出各种问题。改名也不管用，需要改包名
'''
if __name__ == '__main__':
    accumulate = 0
    #r = redis.Redis(host='10.1.131.92', port=6379, db=0)
    r = redis.Redis(host='172.16.2.36', port=10001, db=0)
    #r = redis.Redis(host='172.16.0.89', port=30379, db=0)
    print('redis大小：', r.dbsize())

    r.set('sss', 'xh')
    print('keys sss*', r.keys('sss*'))
    print('delete sss', r.delete('guo'))