#! /usr/bin/env Rscript
#批量注释，选中代码，然后ctrl+shift+c

rm(list=ls())
gc()
#接收调用R脚本的外部参数，其中参数为字符串格式，首先securecrt进入R脚本的存放路径
#Rscript filesort_inout_3args.R "/home/yimr/R/data/train/" " " "/home/yimr/R/data/output/"
argv <- commandArgs(TRUE)
traininputdirc<-as.character(argv[1])
testinputdirc<-as.character(argv[2])
outputdirc<-as.character(argv[3])

#加载库文件，本地相应路径安装有相应的程序包，后期需优化
#或者，运行R脚本的服务器可联网，设置相应R软件的下载镜像，则可应用install.packages("tm")相关函数
install.packages("~/R/packages/tmcn_0.1-4.tar.gz", repos = NULL, type = "source")
install.packages("~/R/packages/Rwordseg_0.2-1.tar.gz", repos = NULL, type = "source")
#install.packages("tm")
install.packages("~/R/packages/tm_0.6-1.tar.gz", repos = NULL, type = "source")
library(class)
library(tmcn)
library(tm)
#加载Rwordseg程序包
library(Rwordseg)
#如stopwords<- unlist(read.table("D:\\R\\RWorkspace\\StopWords.txt",stringsAsFactors=F))  
stopwords<-stopwordsCN()
#length(stopwords)

#加载自定义词典
#添加相关词典
installDict("/home/yimr/R/packages/Dict/Sports.scel",dictname = "Sports")
installDict("/home/yimr/R/packages/Dict/Medical.scel",dictname = "Medical")
installDict("/home/yimr/R/packages/Dict/Law.scel",dictname = "Law")
installDict("/home/yimr/R/packages/Dict/Military.scel",dictname = "Military")
installDict("/home/yimr/R/packages/Dict/mywords.txt",dictname = "Mywords")

# installDict("/home/yimr/R/packages/Dict/电子游戏.txt",dictname = "games")
# installDict("/home/yimr/R/packages/Dict/工程与应用科学.txt",dictname = "engineer")
installDict("/home/yimr/R/packages/Dict/农林渔畜.txt",dictname = "agriculter")
# installDict("/home/yimr/R/packages/Dict/全国.txt",dictname = "country")
# installDict("/home/yimr/R/packages/Dict/人文科学.txt",dictname = "culture")
# 
# installDict("/home/yimr/R/packages/Dict/社会科学.txt",dictname = "scientist")
# installDict("/home/yimr/R/packages/Dict/生活.txt",dictname = "life")
# installDict("/home/yimr/R/packages/Dict/艺术.txt",dictname = "art")
# installDict("/home/yimr/R/packages/Dict/娱乐.txt",dictname = "entertainment")
installDict("/home/yimr/R/packages/Dict/运动休闲.txt",dictname = "leisuretime")
installDict("/home/yimr/R/packages/Dict/自然科学.txt",dictname = "nature")


mergetxts<- function(x){
  #构建训练样本
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


#构建训练样本,traintxts位list结构
#traininputdirc<-"/home/yimr/R/data/test/"
test<-mergetxts(traininputdirc)

# #setwd(traininputdirc)
# 
# 
# #定义路径下训练集的文件夹及文件类型，注意：文件夹名称需要和文件类别对应
# #如C35-Law文件夹存放Law相关的txt文件
# folderlen<-NULL
# folderdirec<-NULL
# folderdirec<-dir("./",full.names = TRUE)
# types<-dir("./")
# 
# #获取文件夹个数,得到一重循环的次数
# folderlen<-length(folderdirec)
# 
# 
# num<-0
# filedirec<-NULL
# filelen<-NULL
# txtcontents<-NULL
# #print(txtcontents)
# mytype<-NULL
# #print(mytype)
# test<-NULL
# 
# #预定义预分配内存
# length(filelen)<-length(filedirec)
# length(mytype)<-10000
# length(txtcontents)<-10000
# #循环读取测试集中各类别的txt文本文件
# for (k in 1:folderlen) {
#   
#   filedirec<-dir(folderdirec[k],full.names = TRUE)
#   #获取文件夹下文件个数，得到二重循环的次数
#   filelen[k]<-length(filedirec)
#   
#   for (j in 1:filelen[k]) {
#     
#     txts<-iconv(readLines(filedirec[j],n=-1,skipNul = TRUE),"gb2312","utf-8")
#     ald<-NULL
#     len<-length(txts)
#     #将单行文字拼接为一篇文章
#     for (i in 1:len) {
#       ald<-paste(txts[len+1-i],ald)
#     }
#     
#     num<- num+1
#     #print(num)
#     txtcontents[num]<-ald
#     #print(txtcontents)
#     #mytype[num]<-c(rep(types[k],filelen[k]))
#     mytype[num]<-c(types[k])
#     
#     rm(ald)
#     rm(txts)
#     gc()
#     
#   }
#   
# }
# num<-0
# #获得测试集，并整合成矩阵
# test<-list(type=mytype,txt=txtcontents)
# 
# rm(mytype)
# rm(txtcontents)
# gc()
# 

test$type<-as.character(test$type)
test$txt<-as.character(test$txt)
#length(test)
table(test$type)

#添加停词,可构建自己的停词库

#去除文本中的特殊字符
testtemp<- gsub("[0-9 < > ~]"," ",test$txt)
#testtemp还未分词，是整篇的文章
#testtemp[1]
segwords1<- segmentCN(testtemp)
#取第一篇和第二篇文本查看效果
#segwords1[1:2]
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
#apply(x,function,..参数..)
segwords2 <- lapply(segwords1,removeStopWords,stopwords)
#segwords2[1:2]

#library(tm)
#创建corpus语料库对象
corpustest<- Corpus(VectorSource(segwords2))
#创建文档-条目矩阵
dtm<- DocumentTermMatrix(corpustest,control = list(wordLengths=c(2,Inf)))
#矩阵转换
#dtm_matrix横轴为分隔词，纵轴为出现的频率
dtm_matrix<-as.matrix(dtm)
#dtm_matrix[1,]
dim(dtm_matrix)

#构建测试样本
#setwd(traininputdirc)








#构建训练样本和测试样本
data.train<-dtm_matrix[c(1:48,51:98,101:165,176:215,221:242),]
data.test<-dtm_matrix[c(46:50,96:100,166:180,216:220),]
#为训练样本指定类别
row.names(data.train)<- test$type[c(1:48,51:98,101:165,176:215,221:242)]
#测试样本的类别为空
row.names(data.test)<- NULL
#指定要预测的类别
testclass<-as.factor(row.names(data.train))
#加载class程序包
library(class)
#用knn模型对文档进行分类
predict<-knn(data.train,data.test,testclass,k=5)

shiji<-test$type[c(46:50,96:100,166:180,216:220)]
predict
shiji

#table(predict,shiji)
#分类准确率
precision <-sum(diag(table(predict,shiji)))/sum(table(predict,shiji))
table(shiji)
table(predict)

mylist<-list(trueresult=shiji,predictresult=predict,precision=precision)

# write.csv(mylist,file = "/home/yimr/R/data/output/outputtest1.csv",na="", fileEncoding = "utf-8",col.names = FALSE)
# result<-read.csv(file = "/home/yimr/R/data/output/outputtest1.csv")
#outputdirc<-c("/home/yimr/R/data/output/")
outputdirc<-gsub(" ","",paste(outputdirc,"outputtest1.csv"))
write.csv(mylist,file = outputdirc,na=" ", fileEncoding = "utf-8",col.names = FALSE)
#result<-read.csv(file = outputdirc)

rm(list=ls())
gc()
















# (function(x, y){ z <- x^2 + y^2; x+y+z })(0:7, 1)
# 
# testcom<-function(x, y){ 
#   z <- x^2 + y^2; 
#   x+y+z 
#   mytestlist<-list(y,z)
#   return(mytestlist)
#   }
# mytxtlists<- testcom(0:7, 2)

