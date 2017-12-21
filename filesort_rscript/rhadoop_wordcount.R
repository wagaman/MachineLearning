Sys.setenv(HADOOP_CMD="/opt/cloudera/parcels/CDH-5.3.3-1.cdh5.3.3.p0.5/bin/hadoop")
Sys.setenv(HADOOP_STREAMING="/opt/cloudera/parcels/CDH-5.3.3-1.cdh5.3.3.p0.5/lib/hadoop-0.20-mapreduce/contrib/streaming/hadoop-streaming-2.5.0-mr1-cdh5.3.3.jar")
Sys.setenv(JAVA_LIBRARY_PATH="/opt/cloudera/parcels/CDH/lib/hadoop/lib/native")




library('rhdfs')
library('rmr2')

hdfs.init()
lines <- c('this is just a joke,','and that is just another joke,','we all like them very much,','because they are so funny.')

lines_dfs <- to.dfs(lines)
wordcount <- function (input, output=NULL, split='[[:punct:][:space:]]+'){
  mapreduce(input=input, output=output, 
            map=function(., v){
              v2=unlist(strsplit(x=v, split=split))
              v3=v2[v2!=' ']
              lapply(v3, function(w){keyval(w, 1)})
            },
            reduce=function(k, vv){
              keyval(k, sum(vv))
            })
}
wc1 <- wordcount(input=lines_dfs)
from.dfs(wc1)


#测试成功事例
lines <- c('this is just a joke,','and that is just another joke,','we all like them very much,','because they are so funny.')
lines_dfs <- to.dfs(lines)

wordcount <- function (input, output=NULL, split='[[:punct:][:space:]]+'){
  mapreduce(input=input, output=output, 
            map=function(k, v){
              v2=unlist(strsplit(x=v, split=split))
              v3=v2[v2!=' ']
              lapply(v3, function(w){keyval(w, 1)})
            })
}

wc1 <- wordcount(input=lines_dfs)
from.dfs(wc1)




