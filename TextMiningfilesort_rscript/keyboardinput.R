mydata<-data.frame(age=numeric(0),gender=character(0),weight=numeric(0))
mydata<-edit(mydata)



# use xedit on the function mean and assign the changes
mean <- edit(mean, editor = "xedit")

# use vi on mean and write the result to file mean.out
vi(mean, file = "mean.out")

## End(Not run)



argv <- commandArgs(TRUE)
x <- as.numeric(argv[1])
y <- as.numeric(argv[2])
sourcedirc<-as.character(argv)
cat("x =", x, "\n")
cat("y =", y, "\n")
cat("x + y = ", x + y, "\n")
cat("x - y = ", x - y, "\n")
cat("x * y = ", x * y, "\n")
cat("x / y = ", x / y, "\n")

#end
###
##
#




argv <- commandArgs(TRUE)
inputdirc<-as.character(argv[1])
outputdirc<-as.character(argv[2])

getwd()
setwd("/home/yimr/R/data/test/")
folderdirec<-dir("./",full.names = TRUE)
types<-dir("./")
#获取文件夹个数,得到一重循环的次数
folderlen<-length(folderdirec)
folderdirec
typeof(folderdirec)


filedirec<-NULL
filedirec<-dir(folderdirec[1],full.names = TRUE)
#获取文件夹下文件个数，得到二重循环的次数
filelen<-length(filedirec)
filedirec
typeof(filedirec)

txts<-iconv(readLines(filedirec,n=-1,skipNul = TRUE),"gb2312","utf-8")
txts

num<-NULL

for (k in 1:folderlen) {
  
  filedirec<-NULL
  filelen<-NULL
  filedirec<-dir(folderdirec[k],full.names = TRUE)
  #获取文件夹下文件个数，得到二重循环的次数
  filelen[k]<-length(filedirec[k])
  
  for (j in 1:filelen[k]) {
    
    txts<-iconv(readLines(filedirec[j],n=-1,skipNul = TRUE),"gb2312","utf-8")
    ald<-NULL
    len<-length(txts)
    for (i in 1:len) {
      ald<-paste(txts[len+1-i],ald)
    }
    
    num<- j+num
    txtcontents[num]<-ald
    type[num]<-c(rep(types[k],filelen[k]))
    
  }
  
}









#在dir函数中设置full.names=true,即可得到全路径，可替代gsub和paste得到的路径
dirctory<-NULL
#dirctory[1]<-paste("./",folderdirec[1],"/",filedirec[1])
#dirctory[1]<-gsub(" ","",dirctory)
#dirctory[1]<-gsub(" ","",paste("./",folderdirec[1],"/",filedirec[1]))
dirctory
txts<-iconv(readLines(dirctory,n=-1,skipNul = TRUE),"gb2312","utf-8")
txts







for (variable in vector) {
  
  
  
}


