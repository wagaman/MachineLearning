## classic wordcount 
## input can be any text file
## inspect output with from.dfs(output) -- this will produce an R list watch out with big datasets
Sys.setenv(HADOOP_CMD="/opt/cloudera/parcels/CDH-5.3.3-1.cdh5.3.3.p0.5/bin/hadoop")
Sys.setenv(HADOOP_STREAMING="/opt/cloudera/parcels/CDH-5.3.3-1.cdh5.3.3.p0.5/lib/hadoop-0.20-mapreduce/contrib/streaming/hadoop-streaming-2.5.0-mr1-cdh5.3.3.jar")
Sys.setenv(JAVA_LIBRARY_PATH="/opt/cloudera/parcels/CDH/lib/hadoop/lib/native")
Sys.setenv(HADOOP_HOME="/opt/cloudera/parcels/CDH-5.3.3-1.cdh5.3.3.p0.5")
setwd("/opt/cloudera/parcels/CDH-5.3.3-1.cdh5.3.3.p0.5")
library('rmr2')
library('rhdfs')
hdfs.init()
## @knitr wordcount-signature
wordcount = 
  function(input,output = NULL,pattern = " "){
    
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

ebookLocation <- "/user/yimr/Rhadoop/test/C35-Law/C35-Law002.txt"
ebookLocation<-"/user/yimr/Rhadoop/test/small.csv"
###
##
#以下程序测试成功
ebookLocation <- "/user/yimr/Rhadoop/test/C35-Law/C35-Law002.txt"

ebookLocation<-"/user/yimr/Rhadoop/test/securecrt.txt"
require("Rwordseg")
require("tmcn")
require("tm")
m <- mapreduce(
               input = ebookLocation,
               input.format  =  "text",
               
               map = function(k, v){
                 #以空格和标点符号分割字符串
                 words <- unlist(strsplit(v, split = "[[:space:][:punct:]]"))
                 # words<-segmentCN(v)
                 words <- tolower(words)
                 words <- gsub("[0-9]", "", words)
                 words <- words[words != ""]
                 wordcount <- table(words)
                 keyval(
                   key = names(wordcount),
                   val = as.numeric(wordcount)
                 )
               },
               
               reduce = function(k, counts){
                 keyval(key = k,
                        val = sum(counts))
               }
)
x <- from.dfs(m)
x


library(tm)
#加载Rwordseg程序包
library(Rwordseg)
segwords1<- segmentCN(ebooks)



ebookLocation<-"/home/yimr/R/data/train/C39-Sports/C39-Sports0145.txt"
ebooks<-iconv(readLines(ebookLocation,n=-1,skipNul = TRUE),"gb2312","utf-8")
ebooks
segwords1<- segmentCN(ebooks)
segwords1
typeof(segwords1)

ebooks.hdfs<-to.dfs(segwords1)
ebooks.hdfs <- from.dfs(ebooks.hdfs)
ebooks.hdfs

#可以将r对象写入\读取dfs文件
ebooks.hdfs<-to.dfs(ebooks)

ebooks_hdfs<-from.dfs(ebooks.hdfs)
ebooks_hdfs
ebookLocation1<-"/user/yimr/Rhadoop/test/C39-Sports/C39-Sports2506.txt"


m <- mapreduce(
  input = ebookLocation1,
  # map = function(k,v){
  #     txts<-segmentCN(v)
  # 
  # }
  # input.format  =  "text",
  # 
  map = function(k, v){
    #以空格和标点符号分割字符串
    words <- unlist(strsplit(v, split = "[[:space:][:punct:]]"))
    # words<-segmentCN(v)
    words <- tolower(words)
    words <- gsub("[0-9]", "", words)
    words <- words[words != ""]
    wordcount <- table(words)
    keyval(
      key = names(wordcount),
      val = as.numeric(wordcount)
    )
  },

  reduce = function(k, counts){
    keyval(key = k,
           val = sum(counts))
  }
)
x <- from.dfs(m)
x

from.dfs(mapreduce(input = to.dfs(1:100),map = function(k, v) cbind(v, mean(v))))
cbind(0, matrix(1, nrow = 0, ncol = 4))
m <- cbind(1, 1:7) # the '1' (= shorter vector) is recycled
m
m <- cbind(m, 8:14)[, c(1, 3, 2)] # insert a column
m

