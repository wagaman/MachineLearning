
rm(list=ls())
gc()
## classic wordcount 
## input can be any text file
## inspect output with from.dfs(output) -- this will produce an R list watch out with big datasets
Sys.setenv(HADOOP_CMD="/opt/cloudera/parcels/CDH-5.3.3-1.cdh5.3.3.p0.5/bin/hadoop")
Sys.setenv(HADOOP_STREAMING="/opt/cloudera/parcels/CDH-5.3.3-1.cdh5.3.3.p0.5/lib/hadoop-0.20-mapreduce/contrib/streaming/hadoop-streaming-2.5.0-mr1-cdh5.3.3.jar")
Sys.setenv(JAVA_LIBRARY_PATH="/opt/cloudera/parcels/CDH/lib/hadoop/lib/native")
Sys.setenv(HADOOP_HOME="/opt/cloudera/parcels/CDH-5.3.3-1.cdh5.3.3.p0.5")
#加载rmr2包
library(rmr2)
library(hdfs)
#输入数据文件
#/home/yimr/R/data/demo_data
train<-read.csv(file="/home/yimr/R/data/demo_data/small.csv",header=FALSE)
names(train)<-c("user","item","pref")

#使用rmr的hadoop格式，hadoop是默认设置。
rmr.options(backend = 'hadoop')

#把数据集存入HDFS
train.hdfs = to.dfs(keyval(train$user,train))
from.dfs(train.hdfs)
#STEP 1, 建立物品的同现矩阵
# 1) 按用户分组，得到所有物品出现的组合列表。
#测试成功
train.mr<-mapreduce(
  train.hdfs, 
  map = function(k, v) {
    keyval(k,v$item)
  },
  reduce=function(k,v){
    m<-merge(v,v)
    keyval(m$x,m$y)
  }
)

from.dfs(train.mr)

# 2) 对物品组合列表进行计数，建立物品的同现矩阵，失败,在应用require之后成功
# ddply()函数位于plyr包，用于对data.frame进行分组统计，与tapply有些类似
require("plyr")
# require("tmcn")
require(rmr2)
step2.mr<-mapreduce(
  train.mr,
  map = function(k, v) {
    d<-data.frame(k,v)
    # d2<-ddply(d,.(k,v),count)
    # d2<-count(d,c("k", "v"))

    key<-d$k
    val<-d
    keyval(key,val)
  },
  
  reduce = function(k,v){
    d2<-ddply(d,.(k,v),count,c("k", "v"))
    key<-d2$k
    val<-d2
    keyval(key,val)
  }
  
)
from.dfs(step2.mr)


# 2. 建立用户对物品的评分矩阵
#测试成功
train2.mr<-mapreduce(
  train.hdfs, 
  map = function(k, v) {
    #df<-v[which(v$user==3),]
    df<-v
    key<-df$item
    val<-data.frame(item=df$item,user=df$user,pref=df$pref)
    keyval(key,val)
  }
)
from.dfs(train2.mr)

#3. 合并同现矩阵 和 评分矩阵
require("rmr2")
eq.hdfs<-equijoin(
  left.input=step2.mr, 
  #left.input = train2.mr,
  right.input=train2.mr,
  map.left=function(k,v){
    keyval(k,v)
  },
  map.right=function(k,v){
    keyval(k,v)
  },
  outer = c("left")
)
from.dfs(eq.hdfs)

#4. 计算推荐结果列表
cal.mr<-mapreduce(
  input=eq.hdfs,
  map=function(k,v){
    val<-v
    na<-is.na(v$user.r)
    if(length(which(na))>0) val<-v[-which(is.na(v$user.r)),]
    keyval(val$k.l,val)
  },
  reduce=function(k,v){
    val<-ddply(v,.(k.l,v.l,user.r),summarize,v=freq.l*pref.r)
    keyval(val$k.l,val)
  }
)
from.dfs(cal.mr)

#5. 按输入格式得到推荐评分列表
result.mr<-mapreduce(
  input=cal.mr,
  map=function(k,v){
    keyval(v$user.r,v)
  },
  reduce=function(k,v){
    val<-ddply(v,.(user.r,v.l),summarize,v=sum(v))
    val2<-val[order(val$v,decreasing=TRUE),]
    names(val2)<-c("user","item","pref")
    keyval(val2$user,val2)
  }
)
from.dfs(result.mr)



require("plyr")
hashes<-hash::hash(key=letters, values=1:26 )
hashes$key
hashes$values
d<-data.frame(hashes$key,hashes$values)
d
d2<-ddply(d,.(hashes.key,hashes.values),count)
d2<-ddply(d,.(hashes$key,hashes$values),count)
d2




