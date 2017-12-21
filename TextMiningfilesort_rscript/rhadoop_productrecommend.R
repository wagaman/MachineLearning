#引入yinru引入引入huanjingbianliang
Sys.setenv(HADOOP_CMD="/opt/cloudera/parcels/CDH-5.3.3-1.cdh5.3.3.p0.5/bin/hadoop")
Sys.setenv(HADOOP_STREAMING="/opt/cloudera/parcels/CDH-5.3.3-1.cdh5.3.3.p0.5/lib/hadoop-0.20-mapreduce/contrib/streaming/hadoop-streaming-2.5.0-mr1-cdh5.3.3.jar")
Sys.setenv(JAVA_LIBRARY_PATH="/opt/cloudera/parcels/CDH/lib/hadoop/lib/native")
Sys.setenv(HADOOP_HOME="/opt/cloudera/parcels/CDH-5.3.3-1.cdh5.3.3.p0.5")
# setwd("/opt/cloudera/parcels/CDH-5.3.3-1.cdh5.3.3.p0.5")

rm(list=ls())
gc()
#加载rmr2包
library(rmr2)
library(rhdfs)
hdfs.init()

#输入数据文件 test ok
#/home/yimr/R/data/demo_data
train<-read.csv(file="/home/yimr/R/data/demo_data/small.csv",header=FALSE)
names(train)<-c("user","item","pref")

#使用rmr的hadoop格式，hadoop是默认设置。
rmr.options(backend = 'hadoop')

testinput<-mapreduce(
  input = '/user/yimr/Rhadoop/test/small.csv',
  input.format = "text",
  map = function(k,v){
    key<-k
    val<-v
    keyval(key,val)
    
  }
)

from.dfs(testinput)

train.hdfs<-mapreduce(
  input = testinput,
  map = function(k,v){
    key<-k
    v<-strsplit(v,",")
    
    v1<-sapply(v,function(v) return(v[1]))
    v2<-sapply(v,function(v) return(v[2]))
    v3<-sapply(v,function(v) return(v[3]))
    
    val<-data.frame(v1=v1,v2=v2,v3=v3)
    names(val)<-c("user","item","pref")
    
    # val<-v
    keyval(val$user,val)
  }
) 
from.dfs(train.hdfs)
###

### hash's key-val test
# > hdfs.ls("/user/yimr/Rhadoop")
# permission owner      group size          modtime                      file
# 1 drwxr-xr-x  yimr supergroup    0 2016-12-29 13:40 /user/yimr/Rhadoop/result
# 2 drwxr-xr-x  yimr supergroup    0 2016-12-27 13:44   /user/yimr/Rhadoop/test

hashes<-hash::hash(key=1:5, values=c("1,101,5.0","1,102,5.0","1,103,5.0","1,104,5.0","1,105,5.0") )
hashes
hashes$values
typeof(hashes$values)
unlist(strsplit(hashes$values,","))
unlist(strsplit(hashes$values,","))[1]
typeof(strsplit(hashes$values,","))


strsplit(hashes$values,",")
val<-strsplit(hashes$values,",")
hashval<-sapply(val,function(v) return(v[2]))
typeof(hashval)


strsplit(hashes$values,",")[1]
strsplit(hashes$values,",")[[1]][1]
###

### test ok,the same with the prefer
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
library(rmr2)
step1.mr<-mapreduce(
  train.mr,
  map = function(k, v) {
    d<-data.frame(k,v)
    d1<-ddply(d,.(k,v),count,c("k", "v"))
    # d2<-count(d,c("k", "v"))
    # d2<-ddply(d,.(k,v),summarize,freq=length(k))
    
    key<-d
    val<-d1$freq
    keyval(key,val)
  },
  reduce=function(k,v){
    # d2<-ddply(d,.(k,v),count,c(k, v))
    # d2<-ddply(d,.(k,v),summarise,freq=length(k))
    d2<-sum(v)
    key<-k
    val<-d2
    keyval(key,val)
  }
  
)
from.dfs(step1.mr)

step2.mr<-mapreduce(
  step1.mr,
  map = function(k, v) {
    d3<-data.frame(k,v)
    # d1<-ddply(d,.(k,v),count,c("k", "v"))
    # d2<-count(d,c("k", "v"))
    # d2<-ddply(d,.(k,v),summarize,freq=length(k))
    
    key<-k$k
    val<-data.frame(k=d3$k,v=d3$v,freq=d3$v.1)
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

eq1.hdfs<-mapreduce(
  input = eq.hdfs,
  map = function(k,v){
    key<-NULL
    val<-v
    keyval(key,val)
    
  }
)
result1<-from.dfs(eq1.hdfs)
length(result1$val[,1])
result1$val[1,]


#4. 计算推荐结果列表
cal.mr<-mapreduce(
  input=eq1.hdfs,
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


# 测试哈希key、val，主要是测试keyval和count函数用法结合
require("plyr")
hashes<-hash::hash(key=letters, values=1:26 )
hashes$key
hashes$values
length(hashes$values)

d<-data.frame(hashes$key,hashes$values)
d
d2<-ddply(d,.(hashes.key,hashes.values),count)
d2<-ddply(d,.(hashes$key,hashes$values),count)
d2

hashes<-hash::hash(key=1, values="1,101,5.0" )
hashes
hashes$values
unlist(strsplit(hashes$values,","))
unlist(strsplit(hashes$values,","))[1]


