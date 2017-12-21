# -*- coding: UTF-8 -*-

__author__ = 'sss'
from pyspark import SparkConf, SparkContext
from operator import add
import sys

'''
    pyspark对sparkconf 已经实例化了
        所以SparkConf().setMaster(master).setAppName(appName)是不起作用的
            SparkSession.builder().appName().getOrCreate() 也是不起作用

sh /opt/spark2/bin/spark-submit --executor-memory 3g --master spark://10.1.131.71:7077 /home/yimr/sss/select_column.py

13001489999|31192120|6941550mpy4|12744|29614|8604710057196401|101|311921365758030|2480|46876|2|200|5|460011480058683|http://10.17.170.2/fT2L5b+fpLND|0||018|0180|10.91.128.19|10.0.0.172|220.206.133.68|220.206.133.131|1026|80|Zte-tu235_TD/1.0 ThreadX/4.0b Larena/2.40 Release/4.15.2010 Browser/NetFront3.5 Profile/MIDP-2.0 Configuration/CLDC-1.1|application/vnd.wap.mms-message

13001489999|31192137|1652910J71n|12744|29614|8604710057196401|100|311921384923120|676|292|2|200|5|460011480058683|http://mmsc.monternet.com/|0||018|0180|10.91.128.19|10.0.0.172|220.206.133.68|220.206.133.131|1027|80|Zte-tu235_TD/1.0 ThreadX/4.0b Larena/2.40 Release/4.15.2010 Browser/NetFront3.5 Profile/MIDP-2.0 Configuration/CLDC-1.1|application/vnd.wap.mms-message

(u'31235920', u'57437105ca9')
(u'31235920', u'5745550DloR')
(u'31235920', u'5925380d8Qn')

'''


if __name__ == "__main__":
    input = "hdfs://10.1.131.72:8020/user/yimr/Modeler/flux-hb/once/1300140.txt.gz"
    output = "hdfs://10.1.131.72:8020/user/yimr/sss/tmp6"

    conf = SparkConf()
    sc = SparkContext(conf=conf)
    lines = sc.textFile(input)

    lines.map(lambda line: (line.split('|')[1], line.split('|')[2])).saveAsTextFile(output)
