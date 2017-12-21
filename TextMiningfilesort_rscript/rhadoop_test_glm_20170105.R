
###test1——glm论文测试，理解glm的概念和应用
install.packages("faraway") 
library(faraway) 
#载入数据集

data(pima,package="faraway") 
#pima 数据集如下
#提取出数据集的 
# test 变量

b<-factor(pima$test) 
#test 变量值的分布范围为 
# 0-1 分布

#构建模型，汇总信息存入变量 
m 
m<-glm(b~diastolic+bmi,family=binomial,data=pima)    #q 其中变量 
# diastolic 表示
# 舒张血压，变量 b
# mi 表示身体重量指数。

#汇总模型信息
>summary(m) 
#结果如下：

# 由上图可知，d
# iastolic 的值为 
# 0.805，
# bmi 的值为 
# 1.95e-14，接近为 
# 0，所以只有变
# 量 b
# mi 是显著的，对我们的模型有重要的影响，简化模型如下：

m.reduce<-glm(b~bmi,family=binomial,data=pima) 
# 简化后的模型依然可以用 s
# ummary 查看汇总信息：

summary(m.reduce) 
# 然后，用这个模型来计算一个中等体重指数（例如 B
# MI 的值为 
# 35）的人糖尿病检
# 查为阳性的概率。 
newdata<-data.frame(bmi=35) 
# #调用 
# predict 函数

predict(m.reduce,type="response",newdata=newdata) 
# 返回结果如下：




###test2——glm测试用例
utils::data(anorexia, package = "MASS")

anorex.1 <- glm(Postwt ~ Prewt + Treat + offset(Prewt),
                family = gaussian, data = anorexia)
summary(anorex.1)

anorexia
#     Treat Prewt Postwt
# 1   Cont  80.7   80.2
# 2   Cont  89.4   80.1
# 3   Cont  91.8   86.4
# 4   Cont  74.0   86.3

anorex.1
