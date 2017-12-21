# import the envirenment vars
Sys.setenv(HADOOP_CMD="/opt/cloudera/parcels/CDH-5.3.3-1.cdh5.3.3.p0.5/bin/hadoop")
Sys.setenv(HADOOP_STREAMING="/opt/cloudera/parcels/CDH-5.3.3-1.cdh5.3.3.p0.5/lib/hadoop-0.20-mapreduce/contrib/streaming/hadoop-streaming-2.5.0-mr1-cdh5.3.3.jar")
Sys.setenv(JAVA_LIBRARY_PATH="/opt/cloudera/parcels/CDH/lib/hadoop/lib/native")
Sys.setenv(HADOOP_HOME="/opt/cloudera/parcels/CDH-5.3.3-1.cdh5.3.3.p0.5")

# clear the memory
rm(list=ls())
gc()

# Rwordseg based on the rJava
library("rJava")
options(warn = -1)
# options(max.print=1000000)
options(max.print = Inf) 
options(java.parameters = "-Xmx5120m")
.jinit(parameters="-Xmx5120m")



#加载rmr2包
library(rmr2)
library(rhdfs)

hdfs.init()
hdfs.ls("./")
#import the target hdfs file
hdfs.ls("/user/yimr/Rhadoop/test")
# target hdfs file directory
#"/user/yimr/Rhadoop/test/securecrt.txt"
hdfs.cat("/user/yimr/Rhadoop/test/securecrt.txt")

wordcount = 
  function(
    input, 
    output, 
    pattern = " "){
    ## @knitr wordcount-map
    wc.map = 
      function(., lines) {
        keyval(
          unlist(
            strsplit(
              x = lines,
              split = pattern)),
          1)}
    ## @knitr wordcount-reduce
    wc.reduce =
      function(word, counts ) {
        keyval(word, sum(counts))}
    
    
    ## @knitr wordcount-mapreduce
    mapreduce(
      input = input,
      output = output,
      input.format = "text",
      output.format = "native",
      map = wc.map,
      reduce = wc.reduce,
      combine = TRUE)}
## @knitr end

wc2<-wordcount(input = '/user/yimr/Rhadoop/test/securecrt.txt','/user/yimr/Rhadoop/output/output2')
result2<-from.dfs(wc2)
write.csv(result2,file = "/home/yimr/R/data/output/result2.csv")
hdfs.put('/home/yimr/R/data/output/result2.csv','/user/yimr/Rhadoop/result/result2')







hdfs.ls("/tmp/")
# /tmp/file55f02bc1e83d 

#还是现实 luanma
hdfs.cp('/tmp/file55f02bc1e83d','/user/yimr/Rhadoop/output')
hdfs.cat('/user/yimr/Rhadoop/output/file55f02bc1e83d/part-00014')

result1<-from.dfs('/user/yimr/Rhadoop/output/file55f02bc1e83d')
write.csv(result1,file = "/home/yimr/R/data/output/result1.csv")
hdfs.put('/home/yimr/R/data/output/result1.csv','/user/yimr/Rhadoop/result/result1')







# wc1<-wordcount(input = '/user/yimr/Rhadoop/test/securecrt.txt','/user/yimr/Rhadoop/output/output1')
# 
# # from.dfs("/tmp/file55f04e17297c")
# from.dfs('/user/yimr/Rhadoop/output/output1')
# 
# to.dfs('/user/yimr/Rhadoop/result/result1')
# 
# 
# 
# 
# 
# 
# 
# hdfs.cat("/tmp/file55f04e17297c")
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# mapreduce(
#   input = "/user/yimr/Rhadoop/test/securecrt.txt",
#   input.format = "text",
#   output = "/user/yimr/Rhadoop/output/output1.csv",
#   map = function()
#   {
#     
#   },
#   reduce = function()
#   {
#     
#     
#   }
#   
#   
#   
# )
# 
# hdfs.ls("/user/yimr/Rhadoop/output")

