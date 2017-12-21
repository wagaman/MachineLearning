
## classic wordcount 
## input can be any text file
## inspect output with from.dfs(output) -- this will produce an R list watch out with big datasets
Sys.setenv(HADOOP_CMD="/opt/cloudera/parcels/CDH-5.3.3-1.cdh5.3.3.p0.5/bin/hadoop")
Sys.setenv(HADOOP_STREAMING="/opt/cloudera/parcels/CDH-5.3.3-1.cdh5.3.3.p0.5/lib/hadoop-0.20-mapreduce/contrib/streaming/hadoop-streaming-2.5.0-mr1-cdh5.3.3.jar")
Sys.setenv(JAVA_LIBRARY_PATH="/opt/cloudera/parcels/CDH/lib/hadoop/lib/native")
Sys.setenv(HADOOP_HOME="/opt/cloudera/parcels/CDH-5.3.3-1.cdh5.3.3.p0.5")
setwd("/opt/cloudera/parcels/CDH-5.3.3-1.cdh5.3.3.p0.5")
library('rmr2')
library('rhdfs')
hdfs.init()

## @knitr wordcount-signature
wordcount = 
  function(
    input, 
    output = NULL, 
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
      map = wc.map,
      reduce = wc.reduce,
      combine = TRUE)}
## @knitr end



text = capture.output(license())
out = list()
for(be in c("local", "hadoop")) {
  rmr.options(backend = be)
  out[[be]] = from.dfs(wordcount(to.dfs(keyval(NULL, text)), pattern = " +"))}
#当没有input.format="text"时，上述字符统计等价于下列三行
lines_text<-to.dfs(text)
wc2<-wordcount(lines_text)
from.dfs('/tmp/file24bc7a655ae1')

#当有input.format="text"时，才能运行成功，否则输出的文件中key，value均为null；
# wordcount('/user/yimr/Rhadoop/test/securecrt.txt')
# from.dfs('/tmp/file24bc237ad7e8')

wc1<-wordcount('/user/yimr/Rhadoop/test/securecrt.txt')
#wc1<-wordcount("/user/yimr/Rhadoop/test/securecrt.txt")
from.dfs(wc1)

stopifnot(rmr2:::kv.cmp(out$hadoop, out$local))

# hdfs.ls("/user/yimr/Rhadoop/test/")
# permission owner      group     size          modtime                                     file
# 1  drwxr-xr-x  yimr supergroup        0 2016-12-01 09:22          /user/yimr/Rhadoop/test/C35-Law
# 2  -rw-r--r--  yimr supergroup   186749 2016-12-01 09:24      /user/yimr/Rhadoop/test/C35-Law.csv
# 3  drwxr-xr-x  yimr supergroup        0 2016-12-01 09:24      /user/yimr/Rhadoop/test/C36-Medical
# 4  -rw-r--r--  yimr supergroup    90424 2016-12-01 09:24  /user/yimr/Rhadoop/test/C36-Medical.csv
# 5  drwxr-xr-x  yimr supergroup        0 2016-12-01 09:24     /user/yimr/Rhadoop/test/C37-Military
# 6  -rw-r--r--  yimr supergroup   137355 2016-12-01 09:24 /user/yimr/Rhadoop/test/C37-Military.csv
# 7  drwxr-xr-x  yimr supergroup        0 2016-12-01 09:24       /user/yimr/Rhadoop/test/C39-Sports
# 8  -rw-r--r--  yimr supergroup 15983299 2016-12-01 09:24   /user/yimr/Rhadoop/test/C39-Sports.csv
# 9  -rw-r--r--  yimr supergroup    14984 2016-12-01 09:24    /user/yimr/Rhadoop/test/securecrt.txt
# 10 -rw-r--r--  yimr supergroup   573310 2016-12-01 09:24        /user/yimr/Rhadoop/test/table.csv
# 
ebook<-"/user/yimr/Rhadoop/test/C39-Sports/C39-Sports2506.txt"
ebook<-"/user/yimr/Rhadoop/test/C35-Law.csv"
wc2<-wordcount(ebook)
#wc1<-wordcount("/user/yimr/Rhadoop/test/securecrt.txt")
from.dfs(wc2)










