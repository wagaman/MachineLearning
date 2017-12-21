#! /usr/bin/env Rscript
# #duplication重复的
# x <- c(3:5, 11:8, 8 + 0:5)
# (ux <- unique(x))
# (u2 <- unique(x, fromLast = TRUE)) # different order
# stopifnot(identical(sort(ux), sort(u2)))
# 
# length(unique(sample(100, 100, replace = TRUE)))
# ## approximately 100(1 - 1/e) = 63.21
# 
# unique(iris)
# 
# demotxt<-c("/home/yimr/R/data/ex_data/分类_分词@12大类5485文本1127万_搜狗.20151022/搜狗词库_20151022/人文科学/01154545466678.txt")
# demotxt<-c("/home/yimr/R/data/ex_data/分类_分词@12大类5485文本1127万_搜狗.20151022/搜狗词库_20151022/人文科学/2011入学.txt")
# demotxt<-c(".//C39-Sports/C39-Sports0001.txt")
# readLines(demotxt,n=-1,skipNul = TRUE)
# #源文件编码格式为utf-8，应用iconv时反而出现乱码
# #iconv(readLines(demotxt,n=-1,skipNul = TRUE),"gb2312","utf-8")
# 
# currentencode<-getCharset()
# names<-readLines(demotxt,n=-1,skipNul = TRUE)
# names<-iconv(readLines(demotxt,n=-1,skipNul = TRUE),from = "gb2312", to="utf-8")
# unique(names)





####
###
##
#start

# getwd()
# setwd("/home/yimr/R/data/ex_data/分类_分词@12大类5485文本1127万_搜狗.20151022/搜狗词库_20151022/")
# filenames<-dir("./")

# for (j in 1:filelen[k]) {
#   
#   txts<-iconv(readLines(filedirec[j],n=-1,skipNul = TRUE),"gb2312","utf-8")
#   ald<-NULL
#   len<-length(txts)
#   for (i in 1:len) {
#     ald<-paste(txts[len+1-i],ald)
#   }
#   
#   num<- num+1
#   txtcontents[num]<-ald
#   type[num]<-c(rep(types[k],filelen[k]))
#   
# }

#the length result=905
# filenames<-dir("./人文科学")
# filenames
# length(filenames)
#the length result=904
#检索包含txt字样的文件名称及路径，去除子文件夹PaxHeader
getwd()
setwd("/home/yimr/R/data/ex_data/分类_分词@12大类5485文本1127万_搜狗.20151022/搜狗词库_20151022/")
filenames<-dir("./")

#for (k in 4:length(filenames)) {
  
  #filternames<-dir(filenames[k],pattern = "txt",full.names = TRUE)
  filternames<-dir("./运动休闲",pattern = "txt",full.names = TRUE)
  #filternames
  length(filternames)
  mydic<-data.frame()
  mydic<-NULL
  txt<-NULL
  #filternames[1:5]
  #汇总每类别词典
  
  for (i in 1:length(filternames)) {
    txt<-readLines(filternames[i],n=-1,skipNul = TRUE)
    #确保每篇词典都没有重复的词组
    txt<-unique(txt)
    b<-data.frame(txt)
    #汇总词组
    mydic<-rbind(mydic,b)
  }
  
  #去重，经过测试，文章“2011年入学.txt”中有重复名字，通过unique可去重
  mydic<-unique(mydic)
  output<-c("/home/yimr/R/data/ex_data/分类_分词@12大类5485文本1127万_搜狗.20151022/搜狗词库_20151022/mydics/")
  #paste(output,"艺术.txt")
  output<-gsub(" ","",paste(output,"运动休闲.txt"))
  #output<-gsub(" ","",paste(output, filenames,".txt"))
  write.table(mydic,file = output,quote =FALSE,row.names = FALSE,col.names = FALSE, fileEncoding = "utf-8")
  
  
#}





# length(mydic$txt)
# mydic$txt[51988]
# length(mydic)
# 
# 
# 
# 
# 
# 
# txt1<-readLines(filternames[1],n=-1,skipNul = TRUE)
# txt1
# mytxt1<-txt1




