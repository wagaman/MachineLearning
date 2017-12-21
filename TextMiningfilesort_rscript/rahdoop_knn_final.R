#清理内存
rm(list=ls())
gc()

#调用包
libs<- c( 'rJava','Rwordseg','tmcn','tm','class','rmr2','rhdfs','xlsx')
lapply(libs, require, character.only = TRUE)
# require("rJava")
# library("rJava")
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
library("rJava")

hdfs.init()


test<-read.xlsx("/home/yimr/R/data/demo_data/sourcedata.xlsx",sheetIndex = 1,encoding = "UTF-8")
# type<-as.character(test$type)
# txt<-as.character(test$txt)

input_dfs<-to.dfs(keyval(key = test$type,val = test$txt))
from.dfs(input_dfs)

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

resultm1<- from.dfs(m1)
resultm1$key


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
    
    # data_train<-dtm_matrix[c(1:300),]
    # mergedata<-data.frame(x=key,y=data_train)
    
    # data_train<-dtm_matrix[c(1:300),]
    # data_test<-dtm_matrix[c(46:50,96:100,186:190,265:270),]
    # row.names(data_train)<-k
    # cl<-as.factor(row.names(data_train))
    # predict<-knn(data_train,data_test,cl)
    # 
    # # cl<-as.factor(key)
    # # 
    # cl <- factor(c(rep("law",58),rep("medical",126),rep("military",58),rep("sports",58)))
    #
    
    # mergedata<-data.frame(x=key,y=data_train)
    
    data_train<-dtm_matrix[c(1:300),]
    data_test<-dtm_matrix[c(265:270),]
    row.names(data_train)<-c(rep("military",58),rep("sports",58),rep("law",58),rep("medical",126))
    
    # cl <- factor(c(rep("military",58),rep("sports",58),rep("law",58),rep("medical",126)))
    # 
    # predict<-knn(data_train,data_test,cl)
    # key<-NULL
    val<-data_train
    keyval(key,val)
  }
  
)

resultdtm<-from.dfs(m2)
resultdtm$key

# data_train<-dtm_matrix[c(1:300),]
# data_test<-dtm_matrix[c(46:50,96:100,186:190,265:270),]
# row.names(data_train)<-k
# cl<-as.factor(row.names(data_train))
# predict<-knn(data_train,data_test,cl)
# 




# cl <- factor(c(rep("law",13),rep("Medical",36),rep("Military",14),rep("Sports",12)))

cl <- factor(c(rep("military",58),rep("sports",58),rep("law",58),rep("medical",126)))





