__author__ = 'Administrator'
import time

print(time.ctime())
print(time.localtime())
print(time.strftime('%Y-%m-%d', time.localtime()))
print(time.strftime('%H:%M:%S', time.localtime()) )


time.ctime(int("1498096151"))
print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))

print(time.mktime(time.strptime('2013-01-01 00:00:00','%Y-%m-%d %H:%M:%S')))