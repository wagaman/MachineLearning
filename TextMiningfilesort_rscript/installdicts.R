# library(Rwordseg)
# installDict("/home/yimr/R/packages/Dict/工程与应用科学.txt",dictname = "engineer")
# installDict("/home/yimr/R/packages/Dict/农林渔畜.txt",dictname = "agriculter")
# installDict("/home/yimr/R/packages/Dict/全国.txt",dictname = "country")
# installDict("/home/yimr/R/packages/Dict/人文科学.txt",dictname = "culture")
# 
# installDict("/home/yimr/R/packages/Dict/社会科学.txt",dictname = "scientist")
# installDict("/home/yimr/R/packages/Dict/生活.txt",dictname = "life")
# installDict("/home/yimr/R/packages/Dict/艺术.txt",dictname = "art")
# installDict("/home/yimr/R/packages/Dict/娱乐.txt",dictname = "entertainment")
# installDict("/home/yimr/R/packages/Dict/运动休闲.txt",dictname = "leisuretime")
# 
# installDict("/home/yimr/R/packages/Dict/自然科学.txt",dictname = "nature")

# memory.size()
# ls()
# rm(ls())
# gc()
# system(memory.limit())
rm(list=ls())
gc()
library(rJava)
library(methods)
library(Rwordseg)
setwd("/home/yimr/R/data/ex_data/分类_分词@12大类5485文本1127万_搜狗.20151022/搜狗词库_20151022/娱乐")
dicnames<-dir("./",pattern = "txt",full.names = TRUE)
#dicnamestest<-dicnames
for (i in 1:length(dicnames)) {
  
  installDict(dicnames[i],dictname = "")
}




