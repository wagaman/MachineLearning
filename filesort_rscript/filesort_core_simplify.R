#获取源文件路径并读取
getwd()
setwd("/home/yimr/R/data/test/C35-Law")
getwd()
files<-dir("./")
files
types<-c("law","medical","military","sports")
#file1<-dir(files[1])
#a<-data.frame()
#a<-NULL
txtcontents<-as.character(0)
len_law<-length(files)
#len_law<-52
for (j in 1:length(files)) {
  
  txts<-iconv(readLines(files[j],n=-1,skipNul = TRUE),"gb2312","utf-8")
  ald<-NULL
  len<-length(txts)
  for (i in 1:len) {
    ald<-paste(txts[len+1-i],ald)
  }
  
  txtcontents[j]<-ald
  #b<-data.frame(txt=ald)
  #a<-rbind(a,b)
}

type<-c(rep(types[1],length(files)))


setwd("/home/yimr/R/data/test/C36-Medical")
getwd()
files<-dir("./")
files
#types<-c("law","medical","military","sports")
#file1<-dir(files[1])
#a<-data.frame()
#a<-NULL
#txtcontents<-as.character(0)
len_medical<-length(files)
for (j in 1:length(files)) {
  
  txts<-iconv(readLines(files[j],n=-1,skipNul = TRUE),"gb2312","utf-8")
  ald<-NULL
  len<-length(txts)
  for (i in 1:len) {
    ald<-paste(txts[len+1-i],ald)
  }
  
  txtcontents[j+len_law]<-ald
  type[j+len_law]<-c(rep(types[2],length(files)))
  #b<-data.frame(txt=ald)
  #a<-rbind(a,b)
}

#type[len_law+1]<-c(rep(types[1],length(files)))

setwd("/home/yimr/R/data/test/C37-Military")
getwd()
files<-dir("./")
files
#types<-c("law","medical","military","sports")
#file1<-dir(files[1])
#a<-data.frame()
#a<-NULL
#txtcontents<-as.character(0)
len_military<-length(files)
for (j in 1:length(files)) {
  
  txts<-iconv(readLines(files[j],n=-1,skipNul = TRUE),"gb2312","utf-8")
  ald<-NULL
  len<-length(txts)
  for (i in 1:len) {
    ald<-paste(txts[len+1-i],ald)
  }
  
  txtcontents[j+len_law+len_medical]<-ald
  type[len_law+len_medical+j]<-c(rep(types[3],length(files)))
  #b<-data.frame(txt=ald)
  #a<-rbind(a,b)
}

setwd("/home/yimr/R/data/test/C39-Sports")
getwd()
files<-dir("./")
files
#types<-c("law","medical","military","sports")
#file1<-dir(files[1])
#a<-data.frame()
#a<-NULL
#txtcontents<-as.character(0)
len_sports<-length(files)
for (j in 1:length(files)) {
  
  txts<-iconv(readLines(files[j],n=-1,skipNul = TRUE),"gb2312","utf-8")
  ald<-NULL
  len<-length(txts)
  for (i in 1:len) {
    ald<-paste(txts[len+1-i],ald)
  }
  
  txtcontents[j+len_law+len_medical+len_military]<-ald
  type[j+len_law+len_medical+len_military]<-c(rep(types[4],length(files)))
  #b<-data.frame(txt=ald)
  #a<-rbind(a,b)
}

test<-list(type=type,txt=txtcontents)
test$type<-as.character(test$type)
test$txt<-as.character(test$txt)
#length(test)
table(test$type)
#加载库文件
install.packages("~/R/packages/tmcn_0.1-4.tar.gz", repos = NULL, type = "source")
install.packages("~/R/packages/Rwordseg_0.2-1.tar.gz", repos = NULL, type = "source")
install.packages("tm")
#添加停词,可构建自己的停词库
library(tmcn)
#如stopwords<- unlist(read.table("D:\\R\\RWorkspace\\StopWords.txt",stringsAsFactors=F))  
stopwords<-stopwordsCN()
length(stopwords)

#加载Rwordseg程序包
library(Rwordseg)
#加载自定义词典
#添加相关词典
installDict("/home/yimr/R/packages/Dict/Sports.scel",dictname = "Sports")
installDict("/home/yimr/R/packages/Dict/Medical.scel",dictname = "Medical")
installDict("/home/yimr/R/packages/Dict/Law.scel",dictname = "Law")
installDict("/home/yimr/R/packages/Dict/Military.scel",dictname = "Military")
installDict("/home/yimr/R/packages/Dict/mywords.txt",dictname = "Mywords")
#去除文本中的特殊字符
testtemp<- gsub("[0-9 < > ~]"," ",test$txt)
#testtemp
segwords1<- segmentCN(testtemp)
#取第一篇和第二篇文本查看效果
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
#dtm_matrix[1,]
dim(dtm_matrix)

#构建训练样本和测试样本
data.train<-dtm_matrix[c(1:48,51:98,101:165,176:215,221:241),]
data.test<-dtm_matrix[c(46:50,96:100,166:180,216:220),]
#为训练样本指定类别
row.names(data.train)<- test$type[c(1:48,51:98,101:165,176:215,221:241)]
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
sum(diag(table(predict,shiji)))/sum(table(predict,shiji))
table(shiji)
table(predict)
#结束end
###
##
#

#批量注释，选中代码，然后ctrl+shift+c
# getwd()
# setwd("/home/yimr/R/data/test/")
# folderdirec<-dir("./",full.names = TRUE)
# #获取文件夹个数,得到一重循环的次数
# folderlen<-length(folderdirec)
# folderdirec
# typeof(folderdirec)
# 
# 
# filedirec<-NULL
# filedirec<-dir(folderdirec[1],full.names = TRUE)
# #获取文件夹下文件个数，得到二重循环的次数
# filelen<-length(filedirec)
# filedirec
# typeof(filedirec)
# 
# #在dir函数中设置full.names=true,即可得到全路径，可替代gsub和paste得到的路径
# dirctory<-NULL
# #dirctory[1]<-paste("./",folderdirec[1],"/",filedirec[1])
# #dirctory[1]<-gsub(" ","",dirctory)
# dirctory[1]<-gsub(" ","",paste("./",folderdirec[1],"/",filedirec[1]))
# dirctory
# txts<-iconv(readLines(dirctory,n=-1,skipNul = TRUE),"gb2312","utf-8")
# txts













