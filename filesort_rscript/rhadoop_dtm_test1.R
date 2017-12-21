#清理内存
rm(list=ls())
gc()

library("rJava")
options(warn = -1)
options(java.parameters = "-Xmx4096m")
.jinit(parameters="-Xmx4096m")

#引入环境变量
Sys.setenv(HADOOP_CMD="/opt/cloudera/parcels/CDH-5.3.3-1.cdh5.3.3.p0.5/bin/hadoop")
Sys.setenv(HADOOP_STREAMING="/opt/cloudera/parcels/CDH-5.3.3-1.cdh5.3.3.p0.5/lib/hadoop-0.20-mapreduce/contrib/streaming/hadoop-streaming-2.5.0-mr1-cdh5.3.3.jar")
Sys.setenv(JAVA_LIBRARY_PATH="/opt/cloudera/parcels/CDH/lib/hadoop/lib/native")
Sys.setenv(HADOOP_HOME="/opt/cloudera/parcels/CDH-5.3.3-1.cdh5.3.3.p0.5")

library(rmr2)
library(rhdfs)


#调用包
libs<- c( 'rJava','Rwordseg','tmcn','tm','rmr2','rhdfs')
lapply(libs, require, character.only = TRUE)
require("rJava")
hdfs.init()

#替代for循环的paste txt程序
##批量读入txt文件，并将文本放入同一个数据框
###结果部分成功
# 
# ###test1——读取预处理文件，并分词
# library("xlsx")
# #读取原始数据
# test<-read.xlsx("/home/yimr/R/data/demo_data/sourcedata.xlsx",sheetIndex = 1,encoding = "UTF-8")
# #test[1:2]
# 
# test$type<-as.character(test$type)
# test$txt<-as.character(test$txt)
# length(test)
# 
# table(test$type)
# 
# # typeof(table(test$type))
# # "integer"
# 
# test
# input_dfs<-to.dfs(test)
# from.dfs(input_dfs)
# # key为null,val为val$type,val$txt
# 
# require("Rwordseg")
# m1<-mapreduce(
#   input = input_dfs,
#   map = function(k,v){
#     # key<-v$type
#     # val<-v$txt
#     key<-v[1]
#     # val<-v[2]
#     words <- gsub("[0-9]", "", v[2])
#     words<-segmentCN(words)
#     # words<-segmentCN(v[2])
#     
#     val<-words
#     
#     keyval(key,val)
#     
#   }
# )
# 
# from.dfs(m1)
# ###测试成功，是不是对单篇文章进行的分词？gsub是对单篇文章进行的处理
# ###能不能



# ###test——能不能使用自己写的去停词函数，还是需要在mapreduce中重写此函数？
# test2<-from.dfs(m1)
# test2$key
# test2$val[1]
# 
# 
# 
# files<-dir("/home/yimr/R/data/test/C35-Law",full.names = TRUE)
# files
# types<-c("law","medical","military","sports")
# #file1<-dir(files[1])
# #a<-data.frame()
# #a<-NULL
# txtcontents<-as.character(0)
# len_law<-length(files)
# #len_law<-52
# for (j in 1:length(files)) {
#   
#   txts<-iconv(readLines(files[j],n=-1,skipNul = TRUE),"gb2312","utf-8")
#   ald<-NULL
#   len<-length(txts)
#   for (i in 1:len) {
#     ald<-paste(txts[len+1-i],ald)
#   }
#   
#   txtcontents[j]<-ald
#   #b<-data.frame(txt=ald)
#   #a<-rbind(a,b)
# }
# 
# type<-c(rep(types[1],length(files)))
# mylist<-list(type=type,txt=txtcontents)
# 
# write.csv(mylist,file = "/home/yimr/R/data/output/output2.csv",na=" ", fileEncoding = "utf-8",col.names = FALSE)
# 
# 
# 
# 




###还是只能通过R读取csv文件在加载到hdoop的dfs文件中
# mylaw<-read.csv("/home/yimr/R/data/output/output2.csv",header = FALSE)
mylaw<-read.csv("/home/yimr/R/data/output/output2.csv")

typeof(mylaw)

library("rmr2")
library("rhdfs")

input_dfs<-to.dfs(keyval(key = mylaw$type,val = mylaw$txt))
from.dfs(input_dfs)


# mylaw<-read.csv("/home/yimr/R/data/output/output2.csv",header = FALSE)
# input_dfs<-to.dfs(keyval(key = mylaw$V2,val = mylaw))

from.dfs(input_dfs)

# key为null,val为val$type,val$txt

require("Rwordseg")

#编码问题会导致val分词后为空
m1<-mapreduce(
  input = input_dfs,
  map = function(k,v){
    # key<-v$type
    # val<-v$txt
    key<-as.factor(k)
    # val<-v[3]
    words <- gsub("[0-9]", "", v)
    
    
    words<-segmentCN(words)
    # words<-segmentCN(v[2])
    
    val<-words
    keyval(key,val)
    
  }
)

from.dfs(m1)
segdata<-from.dfs(m1)
###test-添加dtm相关包
###首先需要在集群中各个节点安装相关程序包
###在reducer中汇总词频？尝试下

# r中实现语料库和dtm方法
# #library(tm)
# #创建corpus语料库对象
# corpustest<- Corpus(VectorSource(segdata$val))
# #创建文档-条目矩阵
# dtm<- DocumentTermMatrix(corpustest,control = list(wordLengths=c(2,Inf)))
# #矩阵转换
# #dtm_matrix横轴为分隔词，纵轴为出现的频率
# dtm_matrix<-as.matrix(dtm)
# #dtm_matrix[1,]
# dim(dtm_matrix)



install.packages("tm","/usr/lib64/R/library/")

# /usr/lib64/R/library/class/libs
# 'https://cran.rstudio.com/src/contrib/pack_0.1-1.tar.gz'
###测试成功
require("tm")
require("tmcn")
require("class")

m2<-mapreduce(
  input = m1,
  map = function(k,v){
    key<-as.factor(k)
    
    val<-v
    keyval(key,val)
  },
  reduce = function(k,v){
    key<-as.factor(k)
    corpustest<- Corpus(VectorSource(v))
    dtm<- DocumentTermMatrix(corpustest,control = list(wordLengths=c(2,Inf)))
    dtm_matrix<-as.matrix(dtm)
    # val<-dtm_matrix[c(1:2),]
    # 
    data_train<-dtm_matrix[c(1:5),]
    data_test<-dtm_matrix[c(1:2),]
    # cl<-as.factor(key)
    # 
    cl <- factor(c(rep("law",5)))
    
    # mergedata<-data.frame(x=key,y=data_train)
    
    
    predict<-knn(data_train,data_test,cl)
    # val<-predict
    # cl可以输出,data_test可以输出，
    
    val<-predict
    key<-NULL
    # val<-mergedata
    keyval(key,val)
  }
  
)

from.dfs(m2)


# 测试哈希key、val，主要是测试keyval和count函数用法结合
require("plyr")
hashes<-hash::hash(key=letters, values=1:26 )
hashes$key
hashes$values
hashes$key[1:4]

d<-data.frame(hashes$key,hashes$values)
d
d2<-ddply(d,.(hashes.key,hashes.values),count)
d2<-ddply(d,.(hashes$key,hashes$values),count)
d2



















# 运行knn后的结果，感觉用testclass也可以成功
# $key
# [1] law law
# Levels: law
# 
# $val
# [1] law law
# Levels: law
#当输出testclass时，结果如下
# $key
# [1] law
# Levels: law
# 
# $val
# [1] law
# Levels: law


train <- rbind(iris3[1:25,,1], iris3[1:25,,2], iris3[1:25,,3])
test <- rbind(iris3[26:50,,1], iris3[26:50,,2], iris3[26:50,,3])
cl <- factor(c(rep("s",25), rep("c",25), rep("v",25)))
predics<- knn(train, test, cl, k = 3)
typeof(predics)

table(predics)
typeof(table(predics))



attributes(.Last.value)









###测试knn算法能否应用
require("class")
m3<-mapreduce(
  input = m2,
  map = function(k,v){
    key<-k
    val<-v
    keyval(key,val)
  },
  reduce = function(k,v){
    key<-k
    testclass<-as.factor(key)
    
    
    
  }
  
)

ebookLocation<-"/user/yimr/Rhadoop/test/small.csv"
wordcount1 = 
  function(
    input, 
    output = NULL, 
    pattern = ","){
    ## @knitr wordcount-map
    wc.map = 
      function(., lines) {
        keyval(
          unlist(
            strsplit(
              x = lines,
              split = pattern)),
          1)}
    ## @knitr wordcount-reduce
    wc.reduce =
      function(word, counts ) {
        keyval(word, sum(counts))}
    
    
    ## @knitr wordcount-mapreduce
    mapreduce(
      input = input,
      output = output,
      input.format = "csv",
      map = wc.map,
      reduce = wc.reduce,
      combine = TRUE)}
## @knitr end
wc3<-wordcount1(ebookLocation)
result3<-from.dfs(wc3) 
result3
#结果为空









###test-inputcsv
ebookLocation<-"/user/yimr/Rhadoop/test/small.csv"
mcsv <- mapreduce(
  input = ebookLocation,
  input.format  =  "csv",
  
  map = function(k, v){
    #以空格和标点符号分割字符串
    # k<-v[1]
    
    keyval(k,v$V1)
    # price<-strsplit(v$V1,",")    
    # v<-price
    # keyval(k,v)
  }
)
x <- from.dfs(mcsv)
x

# unlist(strsplit("a.b.c", ".", fixed = TRUE))

# $key
# NULL
# 
# $val
# V1
# 1    1,101,5.0
# 2    1,102,3.0
# 3    1,103,2.5
# 4    2,101,2.0
# 5    2,102,2.5
# 6    2,103,5.0
# 7    2,104,2.0
# 8    3,101,2.0
# 9    3,104,4.0
# 10   3,105,4.5
# 11   3,107,5.0
# 1.1  4,101,5.0
# 2.1  4,103,3.0
# 3.1  4,104,4.5
# 4.1  4,106,4.0
# 5.1  5,101,4.0
# 6.1  5,102,3.0
# 7.1  5,103,2.0
# 8.1  5,104,4.0
# 9.1  5,105,3.5
# 10.1 5,106,4.0


# keyval(k,v$V1)
# $key
# NULL
# 
# $val
# [1] 1,101,5.0 1,102,3.0 1,103,2.5 2,101,2.0 2,102,2.5 2,103,5.0 2,104,2.0 3,101,2.0 3,104,4.0 3,105,4.5 3,107,5.0
# [12] 4,101,5.0 4,103,3.0 4,104,4.5 4,106,4.0 5,101,4.0 5,102,3.0 5,103,2.0 5,104,4.0 5,105,3.5 5,106,4.0



ebookLocation <- "/user/yimr/Rhadoop/test/C35-Law/C35-Law002.txt"
#ebookLocation<-"/user/yimr/Rhadoop/test/securecrt.txt"
require("Rwordseg")
require("tmcn")
require("tm")

# ebookLocation<-"/user/yimr/Rhadoop/test/small.csv"

m <- mapreduce(
  input = ebookLocation,
  input.format  =  "text",
  
  map = function(k, v){
    #以空格和标点符号分割字符串 
    v<-iconv(v,"gb2312","utf-8")# 重新赋值转格式
    words <- unlist(strsplit(v, split = "[[:space:][:punct:]]"))
    #words<-segmentCN(v)
    words <- tolower(words)
    words <- gsub("[0-9]", "", words)#得改 [0-9０１２３４５６７８９]
    words <- words[words != ""]
    wordcount <- table(words)
    #val <- iconv(v,"gb2312","utf-8")# 删 
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

strsp1<-strsplit("a,b,c", ",", fixed = TRUE)
typeof(strsp1)
strsp1[[1]]
# > strsp1[[1]]
# [1] "a" "b" "c"

strsp2<-unlist(strsp1)
# > strsp2[1]
# [1] "a"

#当kv赋值反转时，数据结果为null
mcsv2<-mapreduce(
  input = mcsv,
  map = function(k,v){
    key<-k
    # v<- unlist(strsplit(x=v,split = ","))           
    val<-v
    #
    # val<-v[1:3]
    # > from.dfs(mcsv2)
    # $key
    # NULL
    # 
    # $val
    # [1] 1,101,5.0 1,102,3.0 1,103,2.5 4,101,5.0 4,103,3.0 4,104,4.5
    # Levels: 1,101,5.0 1,102,3.0 1,103,2.5 4,101,5.0 4,103,3.0 4,104,4.5
    # 
    
    keyval(key,val)
  },
  reduce = function(k,v){
    key<-k
    val<-v
    keyval(key,val)
    
  }
)

from.dfs(mcsv2)
rmcsv2<-from.dfs(mcsv2)




