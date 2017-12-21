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

wc3<-wordcount(input = '/user/yimr/Rhadoop/test/securecrt.txt','/user/yimr/Rhadoop/output/output3')
result3<-from.dfs(wc3)
write.csv(result3,file = "/home/yimr/R/data/output/result3.csv")
hdfs.put('/home/yimr/R/data/output/result3.csv','/user/yimr/Rhadoop/result/result3')

# clear the local csv files
file.remove("/home/yimr/R/data/output/result2.csv")
rm(list=ls())
gc()

# secucrt command line
# hdfs dfs -text /user/yimr/Rhadoop/output/output2/part-00008

# make.output.format("csv",mode = "text")

