getwd()
setwd("./answer/C15-Energy")
#windows环境下目录用\\
setwd("D:\\chinaunicom\\R\\data\\test\\C36-Medical")
setwd("D:\\chinaunicom\\R\\data\\test\\C39-Sports")

setwd("/home/yimr/R/data/answer")
getwd()
files<-dir("./")
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


type<-c(rep("Medical",length(files)))
alldata<-cbind(type,a)

write.csv(alldata,file = "D:\\chinaunicom\\R\\data\\test\\C36-Medical.csv")
data<-read.csv("D:\\chinaunicom\\R\\data\\test\\sourcedata.csv",encoding = "UTF-8")
data<-read.csv("/home/hadoop/answer/C15-Energy.csv")


length(data$type)