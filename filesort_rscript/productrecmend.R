#引用plyr包
library(plyr)
setwd("D:\\chinaunicom\\R\\data\\demo_csv")
#读取数据集
train<-read.csv(file="./small.csv",header=FALSE)
names(train)<-c("user","item","pref") 

 train
# user item pref
# 1 1 101 5.0
# 2 1 102 3.0
# 3 1 103 2.5
# 4 2 101 2.0
# 5 2 102 2.5
# 6 2 103 5.0
# 7 2 104 2.0
# 8 3 101 2.0
# 9 3 104 4.0
# 10 3 105 4.5
# 11 3 107 5.0
# 12 4 101 5.0
# 13 4 103 3.0
# 14 4 104 4.5
# 15 4 106 4.0
# 16 5 101 4.0
# 17 5 102 3.0
# 18 5 103 2.0
# 19 5 104 4.0
# 20 5 105 3.5
# 21 5 106 4.0

 merge(train$item,train$item)
 
 
 
 
 
#计算用户列表
usersUnique<-function(){
  users<-unique(train$user)
  users[order(users)]
}

#计算商品列表方法
itemsUnique<-function(){
  items<-unique(train$item)
  items[order(items)]
}

# 用户列表
users<-usersUnique() 
 users
# [1] 1 2 3 4 5

# 商品列表
items<-itemsUnique() 
 items
# [1] 101 102 103 104 105 106 107

#建立商品列表索引
index<-function(x) which(items %in% x)
data<-ddply(train,.(user,item,pref),summarize,idx=index(item)) 

 data
# user item pref idx
# 1 1 101 5.0 1
# 2 1 102 3.0 2
# 3 1 103 2.5 3
# 4 2 101 2.0 1
# 5 2 102 2.5 2
# 6 2 103 5.0 3
# 7 2 104 2.0 4
# 8 3 101 2.0 1
# 9 3 104 4.0 4
# 10 3 105 4.5 5
# 11 3 107 5.0 7
# 12 4 101 5.0 1
# 13 4 103 3.0 3
# 14 4 104 4.5 4
# 15 4 106 4.0 6
# 16 5 101 4.0 1
# 17 5 102 3.0 2
# 18 5 103 2.0 3
# 19 5 104 4.0 4
# 20 5 105 3.5 5
# 21 5 106 4.0 6

#同现矩阵
cooccurrence<-function(data){
  n<-length(items)
  co<-matrix(rep(0,n*n),nrow=n)
  for(u in users){
    idx<-index(data$item[which(data$user==u)])
    m<-merge(idx,idx)
    for(i in 1:nrow(m)){
      co[m$x[i],m$y[i]]=co[m$x[i],m$y[i]]+1
    }
  }
  return(co)
}

#推荐算法
recommend<-function(udata=udata,co=coMatrix,num=0){
  n<-length(items)
  
  # all of pref
  pref<-rep(0,n)
  pref[udata$idx]<-udata$pref
  
  # 用户评分矩阵
  userx<-matrix(pref,nrow=n)
  
  # 同现矩阵*评分矩阵
  r<-co %*% userx
  
  # 推荐结果排序
  r[udata$idx]<-0
  idx<-order(r,decreasing=TRUE)
  topn<-data.frame(user=rep(udata$user[1],length(idx)),item=items[idx],val=r[idx])
  #topn0),]

# 推荐结果取前num个
if(num>0){
  topn<-head(topn,num)
}

#返回结果
return(topn)
}

#生成同现矩阵
co<-cooccurrence(data) 
 co
# [,1] [,2] [,3] [,4] [,5] [,6] [,7]
# [1,]  5    3    4    4    2    2    1
# [2,]  3    3    3    2    1    1    0
# [3,]  4    3    4    3    1    2    0
# [4,]  4    2    3    4    2    2    1
# [5,]  2    1    1    2    2    1    1
# [6,]  2    1    2    2    1    2    0
# [7,]  1    0    0    1    1    0    1

#计算推荐结果
recommendation<-data.frame()
for(i in 1:length(users)){
  udata<-data[which(data$user==users[i]),]
  recommendation<-rbind(recommendation,recommend(udata,co,0)) 
} 

 recommendation
# user item val
# 1 1 104 33.5
# 2 1 106 18.0
# 3 1 105 15.5
# 4 1 107 5.0
# 5 2 106 20.5
# 6 2 105 15.5
# 7 2 107 4.0
# 8 3 103 24.5
# 9 3 102 18.5
# 10 3 106 16.5
# 11 4 102 37.0
# 12 4 105 26.0
# 13 4 107 9.5
# 14 5 107 11.5