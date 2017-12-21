import time

__author__ = 'sss'


print(" 0 2017-09-08 13:22 /user/yimr/sss/tmp7/-1504848120000".split(" "))

str = "/user/yimr/sss/tmp5/018/0180"
print(str.split("/"))
area_id = str.split("/")[len(str.split("/")) - 1]
print(area_id)

while True:
    time.sleep(60)
    print(1)