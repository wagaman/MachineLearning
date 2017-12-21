# -*- coding: UTF-8 -*-

__author__ = 'sss'
from pyspark import SparkConf, SparkContext
from operator import add
import sys

'''
    pyspark对sparkconf 已经实例化了
        所以SparkConf().setMaster(master).setAppName(appName)是不起作用的
            SparkSession.builder().appName().getOrCreate() 也是不起作用

sh /opt/spark2/bin/spark-submit --master spark://10.1.131.71:7077 /home/yimr/sss/wordcount.py


sh /opt/cloudera/parcels/CDH/bin/spark-submit --master spark://172.16.2.31:7077 /home/yimr/sss/wordcount.py

'''


if __name__ == "__main__":
    input = "hdfs://172.16.2.31:8020/user/yimr/YiMR/publicdict/ip_area.data"
    output = "hdfs://172.16.2.31:8020/tmp/aaa"

    conf = SparkConf()
    sc = SparkContext(conf=conf)
    lines = sc.textFile(input)

    words = lines.flatMap(lambda line: line.split(' '))

    wc = words.map(lambda x: (x, 1))

    counts = wc.reduceByKey(add)

    counts.saveAsTextFile(output)
