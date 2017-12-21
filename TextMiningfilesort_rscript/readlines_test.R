argv <- commandArgs(TRUE)
inputdirc<-as.character(argv[1])
#testinputdirc<-as.character(argv[2])
outputdirc<-as.character(argv[2])
setwd("/home/yimr/R/data/train/")
filedirec<-".//C39-Sports/C39-Sports0657.txt"
txts<-iconv(readLines(filedirec,n=-1,skipNul = TRUE),"gb2312","utf-8")
txts