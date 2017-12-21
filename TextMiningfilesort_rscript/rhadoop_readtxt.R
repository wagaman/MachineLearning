## classic wordcount 
## input can be any text file
## inspect output with from.dfs(output) -- this will produce an R list watch out with big datasets
Sys.setenv(HADOOP_CMD="/opt/cloudera/parcels/CDH-5.3.3-1.cdh5.3.3.p0.5/bin/hadoop")
Sys.setenv(HADOOP_STREAMING="/opt/cloudera/parcels/CDH-5.3.3-1.cdh5.3.3.p0.5/lib/hadoop-0.20-mapreduce/contrib/streaming/hadoop-streaming-2.5.0-mr1-cdh5.3.3.jar")
Sys.setenv(JAVA_LIBRARY_PATH="/opt/cloudera/parcels/CDH/lib/hadoop/lib/native")
Sys.setenv(HADOOP_HOME="/opt/cloudera/parcels/CDH-5.3.3-1.cdh5.3.3.p0.5")
# setwd("/opt/cloudera/parcels/CDH-5.3.3-1.cdh5.3.3.p0.5")

rm(list=ls())
gc()


library('rmr2')
library('rhdfs')
library('Rwordseg')
hdfs.init()

## @knitr wordcount-signature
wordcount = 
  function(
    input, 
    # output = NULL, 
    output,
    pattern = " "){
    
    ## @knitr wordcount-map
    wc.map = 
      function(., lines) {
        keyval(unlist(strsplit(x = lines,split = pattern)),1)}
    
    ## @knitr wordcount-reduce
    wc.reduce =
      function(word, counts ) {
        keyval(word, sum(counts))}
    
    ## @knitr wordcount-mapreduce
    mapreduce(
      input = input,
      output = output,
      input.format = "text",
      map = wc.map,
      reduce = wc.reduce,
      combine = TRUE)}
## @knitr end

ebook<-"/user/yimr/Rhadoop/test/C39-Sports/C39-Sports2506.txt"
ebook<-"/user/yimr/Rhadoop/test/C35-Law.csv"


#output路径不能是已经存在的hdfs文件路径
output<-"/user/yimr/Rhadoop/result/C35-Law.csv"


wc2<-wordcount(ebook,output)
#wc1<-wordcount("/user/yimr/Rhadoop/test/securecrt.txt")
from.dfs(wc2)

#from.dfs()语句不支持输入路径这样的参数？为什么又可以啦

from.dfs(output)
# 报错说是output不是一个file
# hdfs.cat(output)


# 
# hdfs.mkdir("/user/yimr/Rhadoop/result/C35-Law.csv")
# hdfs.ls("/user/yimr/Rhadoop/result/C35-Law.csv")
# hdfs.rm("/user/yimr/Rhadoop/result/C35-Law.csv")





###
##
#以下是测试文件
require('Rwordseg')
#segmentCN(lines)

wordcount = 
  function(
    input, 
    # output = NULL, 
    output,
    pattern = " "){
    
    ## @knitr wordcount-map
    wc.map = 
      function(., lines) {
        # keyval(unlist(strsplit(x = lines,split = pattern)),1)}
        keyval(segmentCN(lines),1)}
    
    
    ## @knitr wordcount-reduce
    wc.reduce =
      function(word, counts ) {
        keyval(word, sum(counts))}
    
    ## @knitr wordcount-mapreduce
    mapreduce(
      input = input,
      output = output,
      input.format = "text",
      map = wc.map,
      reduce = wc.reduce,
      combine = TRUE)}
## @knitr end

ebook<-"/user/yimr/Rhadoop/test/C35-Law.csv"

#output路径不能是已经存在的hdfs文件路径
output<-"/user/yimr/Rhadoop/result/C35-Law-test.csv"

wc2<-wordcount(ebook,output)
from.dfs(wc2)

#from.dfs()语句不支持输入路径这样的参数？为什么又可以啦
from.dfs(output)

###
##
#
#程序测试成功
ebook<-"/user/yimr/Rhadoop/test/C35-Law.csv"
length(file(ebook))
#当map中的val<-v时，程序测试成功。
require('Rwordseg')
require("Rwordseg")
readtxt<-mapreduce(
  input = ebook,
  input.format = "text",
  map = function(k,v){
    key<-k
    # val<- segmentCN(v)
    val<-v
    keyval(key,val)
    
  }
)
from.dfs(readtxt)
#成功添加key值
addkey<-mapreduce(
  input = readtxt,
  map = function(k,v){
    key<-c(rep("law",53))
    val<-v
    keyval(key,val)
  }
  
)
from.dfs(addkey)


# rm(addkey)
# rm(readtxt)
# gc()
#失败
require("Rwordseg")
require("tmcn")
require("tm")
segwords<-mapreduce(
  input = addkey,
  map = function(k,v){
    key<-k
    val<-segmentCN(v)
    keyval(key,val)
  }
)
from.dfs(segwords)

