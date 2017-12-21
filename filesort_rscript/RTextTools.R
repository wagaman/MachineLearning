# http://www.tuicool.com/articles/immQ3uF
library("tm")

reuters =VCorpus(VectorSource(doc_CN))

reuters <- tm_map(reuters, stripWhitespace)

data_stw<- unlist (read.table("E:\\text mining\\stopword \\中文停用词.txt",stringsAsFactors=F))

#head(data_stw,n=10)

reuters=tm_map(reuters,removeWords,data_stw)

# 删除停用词

############################

####生成tfidf特征##################

control=list(removePunctuation=T,minDocFreq=5,wordLengths = c(1, Inf),weighting = weightTfIdf)

doc.tdm=TermDocumentMatrix(reuters,control)

length(doc.tdm$dimnames$Terms)

tdm_removed=removeSparseTerms(doc.tdm, 0.97)

length(tdm_removed$dimnames$Terms)

mat = as.matrix(tdm_removed)####转换成文档矩阵

classifier = naiveBayes(mat[1:x,], as.factor(data$标题[1:x]) )##贝叶斯分类器，训练

predicted = predict(classifier, mat[z:y,]);#预测

A=table(data$标题[z:y], predicted)#预测交叉矩阵

predicted

b1=length(which(predicted==data$标题[z:y]))/length(predicted)#计算召回率

library(RTextTools)

container = create_container(mat[1:y,], as.factor(data$标题[1:y]) ,
                             
                             trainSize=1:x, testSize=1:y,virgin=TRUE)

models = train_models(container, algorithms=c("BAGGING" , "MAXENT" , "NNET" , "RF" , "SVM" , "TREE" ))

results = classify_models(container, models)

#How about the accuracy?

# recall accuracy

森林=recall_accuracy(as.numeric(as.factor(data$标题[z:y])), results[,"FORESTS_LABEL"])

最大熵=recall_accuracy(as.numeric(as.factor(data$标题[z:y])), results[,"MAXENTROPY_LABEL"])

决策树=recall_accuracy(as.numeric(as.factor(data$标题[z:y])), results[,"TREE_LABEL"])

袋袋=recall_accuracy(as.numeric(as.factor(data$标题[z:y])), results[,"BAGGING_LABEL"])

向量机=recall_accuracy(as.numeric(as.factor(data$标题[z:y])), results[,"SVM_LABEL"])

神经网络=recall_accuracy(as.numeric(as.factor(data$标题[z:y])), results[,"NNETWORK_LABEL"])

a=c()

c=c()

e=c()

a=cbind( 随机森林=as.vector(results[,"FORESTS_LABEL"]), 决策树=as.vector(results[,"TREE_LABEL"]) , 支持向量机=as.vector(results[,"SVM_LABEL"]),
        
        贝叶斯=as.vector(predicted), 最大熵=as.vector(results[,"MAXENTROPY_LABEL"]),袋袋=as.vector(results[,"BAGGING_LABEL"]),
        
        神经网络=as.vector( results[,"NNETWORK_LABEL"]))

for(i in 1:length(results[,"FORESTS_LABEL"][z:y]))
  
{ 
  
  b=table(a[i,])
  
  c[i]<-names(which(b==max(table(a[i,]))))
  
}

模型预测=cbind(a,组合模型=c)

A=table(data$标题[z:y],c)

b=length(which(c==data$标题[z:y]))/length(c)

组合模型=b

e=c(贝叶斯=b1,森林=森林,最大熵=最大熵,决策树=决策树,袋袋=袋袋,向量机=向量机,神经网络=神经网络,组合投票=组合模型)

e
##结果该满意了吧！！！
