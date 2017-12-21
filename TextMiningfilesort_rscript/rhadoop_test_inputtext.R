

rm(list=ls())
gc()

#引入环境变量
Sys.setenv(HADOOP_CMD="/opt/cloudera/parcels/CDH-5.3.3-1.cdh5.3.3.p0.5/bin/hadoop")
Sys.setenv(HADOOP_STREAMING="/opt/cloudera/parcels/CDH-5.3.3-1.cdh5.3.3.p0.5/lib/hadoop-0.20-mapreduce/contrib/streaming/hadoop-streaming-2.5.0-mr1-cdh5.3.3.jar")
Sys.setenv(JAVA_LIBRARY_PATH="/opt/cloudera/parcels/CDH/lib/hadoop/lib/native")
Sys.setenv(HADOOP_HOME="/opt/cloudera/parcels/CDH-5.3.3-1.cdh5.3.3.p0.5")



#调用包
libs<- c( 'rJava','Rwordseg','tmcn','tm','rmr2','rhdfs')
lapply(libs, require, character.only = TRUE)

# library(rJava)
# library("Rwordseg")
# library("tmcn")
# library("tm")
# #rhadoop初始化
# library('rmr2')
# library('rhdfs')

hdfs.init()

#ebookLocation<-"/user/yimr/Rhadoop/test/securecrt.txt"时，测试成功；
#ebookLocation <- "/user/yimr/Rhadoop/test/C35-Law/C35-Law002.txt"时，测试为null；
# ebookLocation<-"/user/yimr/Rhadoop/test/small.csv"
ebookLocation <- "/user/yimr/Rhadoop/test/C35-Law/C35-Law002.txt"
#ebookLocation<-"/user/yimr/Rhadoop/test/securecrt.txt"
require("Rwordseg")
require("tmcn")
require("tm")


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




###test-inputcsv
ebookLocation<-"/user/yimr/Rhadoop/test/small.csv"
mcsv <- mapreduce(
  input = ebookLocation,
  input.format  =  "csv",
  
  map = function(k, v){
    #以空格和标点符号分割字符串
    # k<-v[1]
    keyval(k,v)
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











###测试2 失败，for循环只循环了2次
#ebookLocation<-"/user/yimr/Rhadoop/test/securecrt.txt"
m1<-mapreduce(
  input = ebookLocation,
  input.format  =  "text",
  map=function(k,v){
    v<-iconv(v,"gb2312","utf-8")#转格式
    # for (i in 1:length(v)) {
    #   ald<-paste(v)
    # 
    # }
    # # print(i)
    # # len<-length(v)
    # # for (i in 1:len) {
    # #   ald<-paste(v[len+1-i],ald)
    # # }
    # v<-ald

    keyval(k,v)
    }
  #,
  # reduce = function(k,v){
  #   len<-length(v)
  #   for (i in 1:len) {
  #     ald<-paste(v[len+1-i],ald)
  #   }
  #   v<-ald
  #   keyval(k,v)
  # }

)

result1<-from.dfs(m1)
result1



###测试3 分词测试
###gsub函数可实现相应功能，输出结果文档中去掉了数字；
###但是添加上segmentCN分词函数，就出问题，输出结果为null；
ebookLocation<-"/home/yimr/R/data/train/C39-Sports/C39-Sports0145.txt"
ebooks<-iconv(readLines(ebookLocation,n=-1,skipNul = TRUE),"gb2312","utf-8")
len<-length(ebooks)
#将单行文字拼接为一篇文章
ald<-NULL
for (i in 1:len) {
  ald<-paste(ebooks[len+1-i],ald)
}
###将相应R对象上传为hdfs文件格式
input.hdfs<-to.dfs(ald)
m1<-mapreduce(
  input = input.hdfs,
  map = function(k,v){
    
    key<-c("sports")
    val<-v
    keyval(key,val)
  }
)
from.dfs(m1)
###在hadoop各个节点上安装了rwordseg分词包后，测试分词成功
require("Rwordseg")
m2<-mapreduce(
  input = m1,
  map = function(k,v){
    words <- gsub("[0-9]", "", v)
    words<-segmentCN(words)
    key<-k
    val<-words
    keyval(key,val)
  }
)
words<-from.dfs(m2)
words

m3<-mapreduce(
  input = m2,
  map=function(k,v){
    
    
  }
  
  
)




#分词测试结果
# > from.dfs(m3)
# $key
# NULL
# 
# $val
# NULL

# m3<-mapreduce(
#   input = m2,
#   map = function(k,v){
#     keyval(k,v)
#     
#   },
#   reduce = function(k,v){
#     segword2<-segmentCN(v)
#     keyval(k,segword2)
#   }
#   
# )
# from.dfs(m3)



segwords<-segmentCN(words$val)
words
segwords
from.dfs(to.dfs(segwords))









mergetxts<- function(x){
  #构建训练样本
  #getwd()
  setwd(x)
  
  #定义路径下训练集的文件夹及文件类型，注意：文件夹名称需要和文件类别对应
  #如C35-Law文件夹存放Law相关的txt文件
  folderlen<-NULL
  folderdirec<-NULL
  folderdirec<-dir("./",full.names = TRUE)
  types<-dir("./")
  
  #获取文件夹个数,得到一重循环的次数
  folderlen<-length(folderdirec)
  num<-0
  filedirec<-NULL
  filelen<-NULL
  txtcontents<-NULL
  #print(txtcontents)
  mytype<-NULL
  #print(mytype)
  test<-NULL
  
  #预定义预分配内存
  length(filelen)<-length(filedirec)
  length(mytype)<-10000
  length(txtcontents)<-10000
  #循环读取测试集中各类别的txt文本文件
  for (k in 1:folderlen) {
    
    filedirec<-dir(folderdirec[k],full.names = TRUE)
    #获取文件夹下文件个数，得到二重循环的次数
    filelen[k]<-length(filedirec)
    
    for (j in 1:filelen[k]) {
      
      txts<-iconv(readLines(filedirec[j],n=-1,skipNul = TRUE),"gb2312","utf-8")
      ald<-NULL
      len<-length(txts)
      #将单行文字拼接为一篇文章
      for (i in 1:len) {
        ald<-paste(txts[len+1-i],ald)
      }
      
      num<- num+1
      #print(num)
      txtcontents[num]<-ald
      #print(txtcontents)
      #mytype[num]<-c(rep(types[k],filelen[k]))
      mytype[num]<-c(types[k])
      
      rm(ald)
      rm(txts)
      gc()
      
    }
    
  }
  num<-0
  #获得测试集，并整合成矩阵
  test<-list(type=mytype,txt=txtcontents)
  
  rm(mytype)
  rm(txtcontents)
  gc()
  return(test) 
}

testinputdirc<-"/home/yimr/R/data/test/"
test<-mergetxts(testinputdirc)
test$type<-as.character(test$type)
test$txt<-as.character(test$txt)
table(test$type)

table1<-table(test$type)
table1

test



#去除分词、停词后对train和test进行矩阵汇总
#运用knn算法时需要维度相同
stopwords<-stopwordsCN()
removeStopWords <- function(x,stopwords) {  
  temp <- character(0)  
  index <- 1  
  xLen <- length(x)  
  while (index <= xLen) {  
    if (length(stopwords[stopwords==x[index]]) <1)  
      temp<- c(temp,x[index])  
    index <- index +1  
  }  
  temp  
}
#分词并转换为语料矩阵
segdtm<-function(stddata){
  
  #添加停词,可构建自己的停词库
  #去除文本中的特殊字符
  testtemp<- gsub("[0-9 < > ~]"," ",stddata)
  #testtemp还未分词，是整篇的文章
  #testtemp[1]
  segwords1<- segmentCN(testtemp)
  #取第一篇和第二篇文本查看效果
  #segwords1[1:2]
  #构建停用词算法
  #删除停用词
  #apply(x,function,..参数..)
  segwords2 <- lapply(segwords1,removeStopWords,stopwords)
  #segwords2[1:2]
  rm(testtemp,segwords1)
  gc()
  return(segwords2)
}
#对测试集和训练集进行分词
# traintemp<-segdtm(train$txt)
testtemp<-segdtm(test$txt)
testtemp
#testtemp已分词
mtest<-to.dfs(testtemp)
mresult<-from.dfs(mtest)
mresult$key
mresult$val


###测试4——语料矩阵、分词矩阵转换测试
###测试结果，还是无法val可以是分词后的值，但是还是无法进行语料转换、合并矩阵等操作；
require("tm")
m3<-mapreduce(
  input = mtest,
  map = function(k,v){
    
    # corpustest<- Corpus(VectorSource(v))
    # #创建文档-条目矩阵
    # dtm<- DocumentTermMatrix(corpustest,control = list(wordLengths=c(2,Inf)))
    # #矩阵转换
    # #dtm_matrix横轴为分隔词，纵轴为出现的频率
    # dtm_matrix<-as.matrix(dtm)
    # 
    key<-k
    val<-v
    keyval(key,val)

  }
  # ,
  # reduce = function(k,v){
  #   corpustest<- Corpus(VectorSource(v))
  #   #创建文档-条目矩阵
  #   dtm<- DocumentTermMatrix(corpustest,control = list(wordLengths=c(2,Inf)))
  #   #矩阵转换
  #   #dtm_matrix横轴为分隔词，纵轴为出现的频率
  #   dtm_matrix<-as.matrix(dtm)
  #   keyval(k,dtm_matrix)
  #   
  # }
  # 
  
  # ,
  # reduce = function(k,v){
  #   segword2<-segmentCN(v)
  #   keyval(k,segword2)
  # }

)
from.dfs(m3)



###测试5——将分词、矩阵转换后的矩阵作为knn输入集，测试knn分类算法
###借鉴filesort.R,原始版的文本分类脚本
library("xlsx")
#读取原始数据
test<-read.xlsx("sourcedata.xlsx",sheetIndex = 1,encoding = "UTF-8")
#test[1:2]

test$type<-as.character(test$type)
test$txt<-as.character(test$txt)
length(test)

table(test$type)

library(tmcn)#添加停词,可构建自己的停词库
#如stopwords<- unlist(read.table("D:\\R\\RWorkspace\\StopWords.txt",stringsAsFactors=F))  
stopwords<-stopwordsCN()

length(stopwords)
#stopwords[1:10]

#加载Rwordseg程序包
library(Rwordseg)
testtemp<- gsub("[0-9 < > ~]"," ",test$txt)
#testtemp
#删除文本中的特殊字符
segwords1<- segmentCN(testtemp)
segwords1[1:2]

#构建停用词算法
removeStopWords <- function(x,stopwords) {  
  temp <- character(0)  
  index <- 1  
  xLen <- length(x)  
  while (index <= xLen) {  
    if (length(stopwords[stopwords==x[index]]) <1)  
      temp<- c(temp,x[index])  
    index <- index +1  
  }  
  temp  
} 

#删除停用词
segwords2 <- lapply(segwords1,removeStopWords,stopwords)
segwords2[1:2]

library(tm)
#创建corpus语料库对象
corpustest<- Corpus(VectorSource(segwords2))
#创建文档-条目矩阵
dtm<- DocumentTermMatrix(corpustest,control = list(wordLengths=c(2,Inf)))
#矩阵转换
#dtm_matrix横轴为分隔词，纵轴为出现的频率
dtm_matrix<-as.matrix(dtm)
dim(dtm_matrix)

#构建训练样本和测试样本
data.train<-dtm_matrix[c(1:65,83:220,241:280),]
data.test<-dtm_matrix[c(66:82,221:240,281:300),]
#为训练样本指定类别
row.names(data.train)<- test$type[c(1:65,83:220,241:280)]
#测试样本的类别为空
row.names(data.test)<- NULL
#指定要预测的类别
testclass<-as.factor(row.names(data.train))
#加载class程序包
input<-list(train=data.train,test=data.test,type=testclass)
input
library(class)
require("class")
input_dfs<-to.dfs(input)
m5<-mapreduce(
  input = input_dfs,
  map = function(k,v){
    key<-k
    val<-v
    keyval(key,val)
  }
  # ,
  # reduce = function(k,v){
  #   # predict<-knn(v$train,v$test,v$type)
  #   key<-k
  #   val<-v
  #   # val<-data.frame(predict)
  #   keyval(key,val)
  # }

)

result5<- from.dfs(m5)

predict<-knn(result5$val$train,result5$val$test,testclass)
result5$key
result5$val$test


library(class)
#用knn模型对文档进行分类
predict<-knn(data.train,data.test,testclass)

shiji<-test$type[c(66:82,221:240,281:300)]
table(predict,shiji)




# 测试6——将输入路径作为hdfs
###hdfs路径，然后readLines，结果为空
ebookLocation <- "/user/yimr/Rhadoop/test/C35-Law/C35-Law002.txt"
ebookLocation<-"/user/yimr/Rhadoop/test/securecrt.txt"


###本地路径，然后将本地路径上传为hdfs文件，然后readLines，结果为null
ebookLocation<-"/home/yimr/R/data/train/C39-Sports/C39-Sports0145.txt"
ebooks<-iconv(readLines(ebookLocation,n=-1,skipNul = TRUE),"gb2312","utf-8")

ebookLocation<-"/user/yimr/Rhadoop/test/securecrt.txt"
input6<-to.dfs(ebookLocation)
require("Rwordseg")
require("tmcn")
require("tm")
m <- mapreduce(
  input = input6,
  map = function(k, v){
    #以空格和标点符号分割字符串
    words<-hdfs.cat(v)
    # words<-readLines(v,n=-1,skipNul = TRUE)
    # words<-iconv(words,"gb2312","utf-8")
    
    key<-k
    val<-words
    keyval(key,val)
  }
 
)
x <- from.dfs(m)
x


file1<-from.dfs(input6)
cat1<-hdfs.cat(file1$val)
cat1



cat1<-hdfs.cat("/user/yimr/Rhadoop/test/securecrt.txt")
typeof(cat1)

















###测试dtm函数和corpus函数，均来自于tm包
docs <- c("This is a text.", "This another one.")
#vs是list类型,源自tm
vs <- VectorSource(docs)
inspect(VCorpus(vs))
# library("tmcn")
# library("Rwordseg")
library(tm)
dtm<- DocumentTermMatrix(vs,control = list(wordLengths=c(2,Inf)))


crude<-data("crude")
dtm <- DocumentTermMatrix(crude,
                          control = list(weighting =
                                           function(x)
                                             weightTfIdf(x, normalize =
                                                           FALSE),
                                         stopwords = TRUE))
as.matrix(dtm)
inspect(dtm[1:5, 237:242])




###测试随机森林，randomforest
iris
typeof(iris)
library("randomForest")
iris.rf <- randomForest(Species ~ ., data=iris, importance=TRUE,proximity=TRUE)##分类
iris.rf
predict(iris.rf,iris[1,1:4])##预测
print(iris.rf)  
## Look at variable importance:  
round(importance(iris.rf), 2) 


library("randomForest") 
data(iris) 
set.seed(100) 
ind=sample(2,nrow(iris),replace=TRUE,prob=c(0.8,0.2)) 
iris.rf=randomForest(Species~.,iris[ind==1,],ntree=50,nPerm=10,mtry=3,proximity=TRUE,importance=TRUE) 
print(iris.rf) 
iris.pred=predict( iris.rf,iris[ind==2,] ) 
table(observed=iris[ind==2,"Species"],predicted=iris.pred ) 
#length(iris[ind==2,])
# 一些重要参数说明
# randomForest()对训练集的数据进行处理，生成决策树
# iris.rf=randomForest(Species~.,iris[ind==1,],ntree=50,nPerm=10,mtry=3,proximity=TRUE,importance=TRUE)
# Species~.:代表需要预测的列，species是列的名称。
# iris[ind==1,]：生成决策树的训练集
# ntree：生成决策树的数目
# nperm：计算importance时的重复次数
# mtry：选择的分裂属性的个数
# proximity=TRUE：表示生成临近矩阵
# importance=TRUE：输出分裂属性的重要性
# predict（）

# iris.pred=predict( iris.rf,iris[ind==2,] )
# iris.rf：表示生成的随机森林模型
# iris[ind==2,] ：进行预测的测试集
# 






