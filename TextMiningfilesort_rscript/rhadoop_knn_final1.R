#清理内存
rm(list=ls())
gc()

library("rJava")
options(warn = -1)
options(max.print=1000000)
# options(max.print = Inf) 
options(java.parameters = "-Xmx5120m")
.jinit(parameters="-Xmx5120m")

#引入环境变量
Sys.setenv(HADOOP_CMD="/opt/cloudera/parcels/CDH-5.3.3-1.cdh5.3.3.p0.5/bin/hadoop")
Sys.setenv(HADOOP_STREAMING="/opt/cloudera/parcels/CDH-5.3.3-1.cdh5.3.3.p0.5/lib/hadoop-0.20-mapreduce/contrib/streaming/hadoop-streaming-2.5.0-mr1-cdh5.3.3.jar")
Sys.setenv(JAVA_LIBRARY_PATH="/opt/cloudera/parcels/CDH/lib/hadoop/lib/native")
Sys.setenv(HADOOP_HOME="/opt/cloudera/parcels/CDH-5.3.3-1.cdh5.3.3.p0.5")

library(rmr2)
library(rhdfs)


#调用包
libs<- c( 'rJava','Rwordseg','tmcn','tm','rmr2','rhdfs','class')
lapply(libs, require, character.only = TRUE)
require("rJava")
hdfs.init()

library("rJava")
library("xlsx")
# #读取原始数据,读取excel出现出现
# test<-read.xlsx("/home/yimr/R/data/demo_data/sourcedata.xlsx",sheetIndex = 1,encoding = "UTF-8")
# type<-as.character(test$type)
# txt<-as.character(test$txt)

# mylaw<-read.csv("/home/yimr/R/data/output/output4.csv")
# 
# typeof(mylaw)

library("rmr2")
library("rhdfs")

# input_dfs<-to.dfs(keyval(key = mylaw$type,val = mylaw$txt))
# from.dfs(input_dfs)


# mylaw<-read.csv("/home/yimr/R/data/output/output2.csv",header = FALSE)
# input_dfs<-to.dfs(keyval(key = mylaw$V2,val = mylaw))

# from.dfs(input_dfs)

# key为null,val为val$type,val$txt

require("Rwordseg")
require("tm")
require("tmcn")
require("class")


# input_dfs<-to.dfs(keyval(key = test$type,val = test$txt))


#c37 test ok
mylaw<-read.csv("/home/yimr/R/data/demo_data/C37-Military.csv")
input_dfs<-to.dfs(keyval(key = mylaw$type,val = mylaw$txt))

#rahdoopdata test
mylaw<-read.csv("/home/yimr/R/data/demo_data/rhadoopdata.csv")
input_dfs<-to.dfs(keyval(key = mylaw$type,val = mylaw$txt))

#rahdoopdata test
mylaw<-read.csv("/home/yimr/R/data/demo_data/train.csv")
input_dfs<-to.dfs(keyval(key = mylaw$type,val = mylaw$txt))


resultm1<-from.dfs(input_dfs)
#
m2<-mapreduce(
  input = input_dfs,
  map = function(k,v){
    key<-as.factor(k)
    words <- gsub("[0-9]", "", v)
    words<-segmentCN(words)
    # words<-segmentCN(v[2])
    val<-words
    keyval(key,val)
    
  },
  
  reduce = function(k,v){
    key<-as.factor(k)
    corpustest<- Corpus(VectorSource(v))
    dtm<- DocumentTermMatrix(corpustest,control = list(wordLengths=c(2,Inf)))
    dtm_matrix<-as.matrix(dtm)
    data_train<-dtm_matrix[c(1:76),]
    data_test<-dtm_matrix[c(1:5,71:75),]
    row.names(data_train)<-c(rep("energy",33), rep("law",22),rep("military",21))
    
    cl <- factor(c(rep("energy",33), rep("law",22),rep("military",21)))
    predict<-knn(data_train,data_test,cl)
    
    key<-NULL
    # key<-factor(c(rep("energy",33), rep("law",22),rep("military",15)))
    val<-data_train
    
    # key<-factor(c(rep("energy",5), rep("law",5)))
    # val<-predict
    
    
    keyval(key,val)
    
  }
)

from.dfs(m2)
resultm2<-from.dfs(m2)














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
    
  },
  
  reduce = function(k,v){
    key<-as.factor(k)
    corpustest<- Corpus(VectorSource(v))
    dtm<- DocumentTermMatrix(corpustest,control = list(wordLengths=c(2,Inf)))
    dtm_matrix<-as.matrix(dtm)
    # val<-dtm_matrix[c(1:2),]
    # #
    # test ok
    # 为什么多于70输出为kong
    #[ reached getOption("max.print") -- omitted 73 rows ]
    data_train<-dtm_matrix[c(1:70),]
    data_test<-dtm_matrix[c(1:5,71:75),]
    #row.names test ok
    # row.names(data_train)<-c(rep("energy",33), rep("law",52),rep("military",75))
    # key test failed
    # row.names(data_train)<-key
    # cl<-as.factor(key)
    #
    # cl <- factor(c(rep("energy",33), rep("law",52),rep("military",75)))
    # 
    # # mergedata<-data.frame(x=key,y=data_train)
    # 
    # 
    # predict<-knn(data_train,data_test,cl)
    # val<-predict
    # cl可以输出,key为为为null时data_test可以输出，
    #key不为空时也可以shuchu
    # key<-NULL
    # val<-predict
    key<-NULL
    val<-data_train
    
    
    #test result not sure
    # val<-mergedata
    
    #test result ok
    # val<-data_train
    keyval(key,val)
    
    
    
    # # test ok
    # data_train<-dtm_matrix[c(1:70),]
    # data_test<-dtm_matrix[c(1:3,72:76),]
    # #row.names test ok
    # row.names(data_train)<-c(rep("energy",33), rep("law",23),rep("military",14))
    # # key test failed
    # # row.names(data_train)<-key
    # # cl<-as.factor(key)
    # #
    # cl <- factor(c(rep("energy",33), rep("law",23),rep("military",14)))
    # 
    # # mergedata<-data.frame(x=key,y=data_train)
    # 
    # 
    # predict<-knn(data_train,data_test,cl)
    # # val<-predict
    # # cl可以输出,key为为为null时data_test可以输出，
    # #key不为空时也可以shuchu
    # val<-predict
    # # key<-NULL
    # 
    # #test result not sure
    # # val<-mergedata
    # 
    # #test result ok
    # # val<-data_train
    # keyval(key,val)

    
  }
)

from.dfs(m1)
segdata<-from.dfs(m1)


# 测试哈希key、val，主要是测试keyval和count函数用法结合
require("plyr")
hashes<-hash::hash(key=letters, values=1:26 )
hashes$key
hashes$values
d<-data.frame(hashes$key,hashes$values)
d
d2<-ddply(d,.(hashes.key,hashes.values),count)
d2<-ddply(d,.(hashes$key,hashes$values),count)
d2










