# -*- coding: utf-8 -*-
import time
__author__ = 'sss'
import os
'''

nohup python rename.py > /home/yimr/tmp.log &

linux查看所有python进程ps -ef |grep python

kafka生成的文件目录
    /user/yimr/sss/tmp5/018
    /user/yimr/sss/tmp5/018/0180
    /user/yimr/sss/tmp5/018/0182
    /user/yimr/sss/tmp5/018/0183

    ...
    /user/yimr/sss/tmp5/018/0180/1505178810000/
    /user/yimr/sss/tmp5/018/0180/1505178815000/
    /user/yimr/sss/tmp5/018/0180/1505178820000/
    /user/yimr/sss/tmp5/018/0180/1505178825000/
    ...

    /user/yimr/sss/tmp5/018/0180/1505178810000/_SUCESSS
    /user/yimr/sss/tmp5/018/0180/1505178810000/part-00000
    ...

    使用hadoop脚本合并成

    /user/yimr/sss/kafka_out/018
    /user/yimr/sss/kafka_out/018/0180-1505178810000.txt
    /user/yimr/sss/kafka_out/018/0180-1505178815000.txt


'''
if __name__ == '__main__':
        cru_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        print(cru_time)
    #while True:
        output = os.popen("hadoop fs -ls /user/yimr/sss/tmp2/018")
        arr = output.read()

        arr = arr.split("\n")
        accumulate = 0
        for file in arr:
            try:
                if len(file.split("    ")[2].split(" ")) > 5:
                    file_dir = file.split("    ")[2].split(" ")[5]
                    #/user/yimr/sss/tmp5/018/0180
                    output = os.popen("hadoop fs -ls " + file_dir)
                    area_id = file_dir.split("/")[len(file_dir.split("/")) - 1]
                    arr_son = output.read()

                    timestamp_files = arr_son.split("\n")
                    for timestamp_file in timestamp_files:
                        try:
                            if len(timestamp_file.split("    ")[2].split(" ")) > 5:
                                timestamp_file_file_dir = timestamp_file.split("    ")[2].split(" ")[5]
                                output = os.popen("hadoop fs -ls " + timestamp_file_file_dir)
                                timestamp_file_son = output.read()

                                timestamp = timestamp_file_file_dir.split("-")[1]

                                if "_SUCCESS" in timestamp_file_son:
                                    os.popen("hadoop fs -mv " + timestamp_file_file_dir + "/part-00000 /user/yimr/sss/kafka_out/018/018-" + area_id + "-" + timestamp + "-" + accumulate)
                                    accumulate += 1

                                    #os.popen("hadoop fs -rm -r " + timestamp_file_file_dir)
                        except:
                            pass
            except:
                pass

cru_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
print(cru_time)
print(111)