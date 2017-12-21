
library("xlsx")
#读取原始数据
test<-read.xlsx("sourcedata.xlsx",sheetIndex = 1,encoding = "UTF-8")
#test[1:2]

test$type<-as.character(test$type)
test$txt<-as.character(test$txt)
length(test)

table(test$type)

#读取中文文献
x<-readLines("C3-Art0002.txt")
x
y<-iconv(x,"gb2312","utf-8")












#加载自定义词典
#添加相关词典
installDict("/home/hadoop/Rpackages/Dict/Sports.scel",dictname = "Sports")
installDict("/home/hadoop/Rpackages/Dict/Medical.scel",dictname = "Medical")
installDict("/home/hadoop/Rpackages/Dict/Law.scel",dictname = "Law")
installDict("/home/hadoop/Rpackages/Dict/Military.scel",dictname = "Military")

readLines("/home/hadoop/data/C11-Space1279.txt",encoding = "utf-8")#出现中文乱码，同文件夹下的csv也是乱码

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

#词云统计
words <- lapply(segwords2,strsplit," ")  
wordsNum <- table(unlist(words))  
wordsNum <- sort(wordsNum) #排序  
wordsData <- data.frame(words =names(wordsNum), freq = wordsNum)  
library(wordcloud) #加载画词云的包  
weibo.top150 <- tail(wordsData,150) #取前150个词  
colors=brewer.pal(8,"Dark2")  
wordcloud(weibo.top150$words,weibo.top150$freq,scale=c(8,0.5),colors=colors,random.order=F)

#词云统计单篇文章关键词
words <- lapply(segwords2[1],strsplit," ")  
wordsNum <- table(unlist(words))  
wordsNum <- sort(wordsNum) #排序  
wordsData <- data.frame(words =names(wordsNum), freq = wordsNum)  
library(wordcloud) #加载画词云的包  
weibo.top150 <- tail(wordsData,15) #取前150个词  
colors=brewer.pal(8,"Dark2")  
wordcloud(weibo.top150$words,weibo.top150$freq,scale=c(8,0.5),colors=colors,random.order=F)


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
library(class)
#用knn模型对文档进行分类
predict<-knn(data.train,data.test,testclass)

shiji<-test$type[c(66:82,221:240,281:300)]
table(predict,shiji)
#分类准确率
sum(diag(table(predict,shiji)))/sum(table(predict,shiji))
table(shiji)
table(predict)