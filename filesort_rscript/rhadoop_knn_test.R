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

library("rJava")
library("xlsx")
# #读取原始数据,读取excel出现出现
test<-read.xlsx("/home/yimr/R/data/demo_data/sourcedata.xlsx",sheetIndex = 1,encoding = "UTF-8")
type<-as.character(test$type)
txt<-as.character(test$txt)

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
    #row.names test ok
    row.names(data_train)<-c(rep("law",5))
    # key test failed
    # row.names(data_train)<-key
    # cl<-as.factor(key)
    # 
    cl <- factor(c(rep("law",5)))
    
    # mergedata<-data.frame(x=key,y=data_train)
    
    
    predict<-knn(data_train,data_test,cl)
    # val<-predict
    # cl可以输出,key为为为null时data_test可以输出，
    #key不为空时也可以shuchu
    # val<-predict
    # key<-NULL
    
    # val<-mergedata
    val<-data_train
    keyval(key,val)
  }
  
)

from.dfs(m2)




