rm(list=ls())
gc()

Sys.setenv(HADOOP_CMD="/opt/cloudera/parcels/CDH-5.3.3-1.cdh5.3.3.p0.5/bin/hadoop")
Sys.setenv(HADOOP_STREAMING="/opt/cloudera/parcels/CDH-5.3.3-1.cdh5.3.3.p0.5/lib/hadoop-0.20-mapreduce/contrib/streaming/hadoop-streaming-2.5.0-mr1-cdh5.3.3.jar")
Sys.setenv(JAVA_LIBRARY_PATH="/opt/cloudera/parcels/CDH/lib/hadoop/lib/native")
Sys.setenv(HADOOP_HOME="/opt/cloudera/parcels/CDH-5.3.3-1.cdh5.3.3.p0.5")

library(tmcn)
library(rmr2)
library(rhdfs)
hdfs.init()


rmr.options(backend = 'hadoop')


# Word count --------------------------------------------------------------

hdfs.ls("/user/yimr/Rhadoop/test/")
hdfs.ls("/user/yimr/Rhadoop/test/C35-Law")
#/home/yimr/R/data/train/C39-Sports/C39-Sports0145.txt
#/user/yimr/Rhadoop/test/C35-Law/C35-Law002.txt
# ebookLocation <- "/home/ndscbigdata/wofile.txt"
ebookLocation <- "/user/yimr/Rhadoop/test/C35-Law/C35-Law002.txt"
# ebookLocation<-"/user/yimr/Rhadoop/test/small.csv"
# ebookLocation<-"/user/yimr/Rhadoop/test/C39-Sports.csv"
# ebookLocation<-"/home/yimr/R/data/train/C39-Sports/C39-Sports0145.txt"
#text = capture.output(license())
#lines_text<-to.dfs(text)

m <- mapreduce(input = ebookLocation,
               input.format  =  "text",
               
               map = function(k, v){
                 #以空格和标点符号分割字符串
                 words <- unlist(strsplit(v, split = "[[:space:][:punct:]]"))
                 words <- tolower(words)
                 words <- gsub("[0-9]", "", words)
                 words <- words[words != ""]
                 wordcount <- table(words)
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




# Retrieve results and prepare to plot ------------------------------------




x <- from.dfs(m)
x
dat <- data.frame(
  word  = keys(x),
  count = values(x)
)
dat <- dat[order(dat$count, decreasing=TRUE), ]
head(dat, 50)
with(head(dat, 25), plot(count, names = word))
















