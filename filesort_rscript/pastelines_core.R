getwd()
setwd("/home/yimr/R/data/test/C35-Law")
#windows环境下目录用\\
setwd("D:\\chinaunicom\\R\\data\\test\\C36-Medical")
setwd("/home/yimr/R/data/train/C38-Politics")

setwd("/home/yimr/R/data/test")

getwd()
setwd("/home/yimr/R/data/test/C35-Law")
getwd()
files<-dir("./")
types<-c("law","medical","military","sports")
#file1<-dir(files[1])
a<-data.frame()
a<-NULL
txtcontents<-as.character(0)
for (j in 1:length(files)) {
  
  txts<-iconv(readLines(files[j],n=-1,skipNul = TRUE),"gb2312","utf-8")
  ald<-NULL
  len<-length(txts)
  for (i in 1:len) {
    ald<-paste(txts[len+1-i],ald)
  }
  
  txtcontents[j+length(files)]<-ald
  b<-data.frame(txt=ald)
  a<-rbind(a,b)
}

type<-c(rep(types[1],length(files)))
#type<-c(rep("Medical",length(files)))

alldata<-cbind(type,a)
length(alldata$type)
test<-alldata


#test<-character(0)
#test[1:52]<-alldata

setwd("/home/yimr/R/data/test/C36-Medical")
getwd()
files<-dir("./")
#types<-c("law","medical","military","sports")
#file1<-dir(files[1])
a<-data.frame()
a<-NULL

for (j in 1:length(files)) {
  
  txts<-iconv(readLines(files[j],n=-1,skipNul = TRUE),"gb2312","utf-8")
  ald<-NULL
  len<-length(txts)
  for (i in 1:len) {
    ald<-paste(txts[len+1-i],ald)
  }
  
  b<-data.frame(txt=ald)
  a<-rbind(a,b)
}

type<-c(rep(types[2],length(files)))
#type<-c(rep("Medical",length(files)))


alldata<-cbind(type,a)
length(alldata$type)
test$type[53:105]<-alldata$type

#test<-character(0)


#test[1:52]<-alldata
#test[53:105]<-alldata

test<-alldata

test[]


type<-c(rep(types[1],length(files)))


setwd("/home/yimr/R/data/train/C38-Politics")
files<-dir("./")
#types<-c("law","medical","military","sports")
#file1<-dir(files[1])
a<-data.frame()
a<-NULL
txtcontents<-as.character(0)
for (j in 1:length(files)) {
  
  txts<-iconv(readLines(files[j],n=-1,skipNul = TRUE),"gb2312","utf-8")
  ald<-NULL
  len<-length(txts)
  for (i in 1:len) {
    ald<-paste(txts[len+1-i],ald)
  }
  
  txtcontents[j+length(files)]<-ald
  b<-data.frame(txt=ald)
  a<-rbind(a,b)
}

#type<-c(rep(types[1],length(files)))
type<-c(rep("Politics",length(files)))

alldata<-cbind(type,a)
write.csv(alldata,file = "/home/yimr/R/data/train/C38-Politics.csv")

data<-read.csv("D:\\chinaunicom\\R\\data\\test\\sourcedata.csv",encoding = "UTF-8")
data<-read.csv("/home/hadoop/answer/C15-Energy.csv")


length(data$type)