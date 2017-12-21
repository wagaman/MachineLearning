#以下简单事例，用于更改工作路径，会报错显示无法更改工作路径
#原因是R不支持创建级联目录
getwd()
setwd("/home/yimr/R/data/train/")
getwd()
dir.create("/home/yirm/R/data/test/",recursive = TRUE)
setwd("/home/yirm/R/data/test/")
getwd()
setwd("../test")
#knn测试，用knn进行分类时，dim维度必须一致，否则报错dim不一致
#解决方法：只能将分词、去停用词等操作后的训练集、测试集进行汇总，然后进行矩阵转换
library(class)
train <- rbind(iris3[1:25,,1], iris3[1:25,,2], iris3[1:25,,3])
test <- rbind(iris3[26:50,,1], iris3[26:50,,2], iris3[26:50,,3])
cl <- factor(c(rep("s",25), rep("c",25), rep("v",25)))
knn(train, test, cl, k = 3, prob=TRUE)