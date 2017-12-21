# -*- coding: utf-8 -*-
import codecs
import threading
import numpy as np
from sklearn import svm
from sklearn.grid_search import GridSearchCV
import sys
import time

'''
SVM模型有两个非常重要的参数C与gamma。其中 C是惩罚系数，即对误差的宽容度。c越高，说明越不能容忍出现误差,容易过拟合。C越小，容易欠拟合。C过大或过小，泛化能力变差

gamma是选择RBF函数作为kernel后，该函数自带的一个参数。隐含地决定了数据映射到新的特征空间后的分布，gamma越大，支持向量越少，gamma值越小，支持向量越多。支持向量的个数影响训练与预测的速度。

这里面大家需要注意的就是gamma的物理意义，大家提到很多的RBF的幅宽，它会影响每个支持向量对应的高斯的作用范围，从而影响泛化性能。我的理解：如果gamma设的太大，方差会很小，方差很小的高斯分布长得又高又瘦， 会造成只会作用于支持向量样本附近，对于未知样本分类效果很差，存在训练准确率可以很高，(如果让方差无穷小，则理论上，高斯核的SVM可以拟合任何非线性数据，但容易过拟合)而测试准确率不高的可能，就是通常说的过训练；而如果设的过小，则会造成平滑效应太大，无法在训练集上得到特别高的准确率，也会影响测试集的准确率。
'''

def loadDataSet(filename):
    dataMat=[]
    fr = codecs.open(filename, "r", "utf-8")
    lineNum = 0
    for line in fr.readlines():
        curLine = line.strip().split(',')
        if (lineNum > 0):
            aa = [i for i in curLine]
            dataMat.append(aa)
        lineNum += 1

    return dataMat

class CountdownTask(threading.Thread):
    def __init__(self):
        super(CountdownTask, self).__init__()
        self._running = True

    def terminate(self):
        self._running = False

    def run(self):
        while self._running:
            sys.stdout.write('.')
            sys.stdout.flush()
            time.sleep(1)

if __name__ == '__main__':

    print('****************开始******************')
    filePath = "D:\workspaceHuayu\helloPython\hellopython\weka\chinauincom_pro1\\test5\\user_brand_train.txt"
    dataMat = loadDataSet(filePath)
    row_num = len(dataMat)
    col_num = len(dataMat[0])
    dataMat = np.array(dataMat)

    X_train = dataMat[0:row_num, 0:col_num - 2]
    y_train = dataMat[0:row_num, col_num - 1]

    #'linear', 'rbf', 'poly'
    clf = svm.SVC(kernel='rbf', gamma=10)
    #sample_weight=None 不平衡问题
    print('****************完成训练数据加载，开始训练******************')

    ct = CountdownTask()
    ct.start()
    clf.fit(X_train, y_train, sample_weight=None)
    ct.terminate()
    print()

    print('****************完成模型训练******************')
    print('****************加载测试数据 验证准确率******************')
    ct = CountdownTask()
    ct.start()
    #使用clf scores
    test_filePath = "D:\workspaceHuayu\helloPython\hellopython\weka\chinauincom_pro1\\test5\\user_brand_test.txt"
    test_dataMat = loadDataSet(test_filePath)
    test_dataMat = np.array(test_dataMat)

    X_test = test_dataMat[0:row_num, 0:col_num - 2]
    y_test = test_dataMat[0:row_num, col_num - 1]
    score = clf.score(X_test, y_test)
    ct.terminate()
    print()
    print(score)

    '''
    #使用交叉验证  会出问题
    scores = cross_validation.cross_val_score(clf, X_train, y_train, cv=5)
    print(scores)
    '''

    '''
    #自动调参  也会出问题
    grid = GridSearchCV(svm.SVC(kernel='rbf'), param_grid={"C":[0.1, 1, 10], "gamma": [1, 0.1, 0.01]}, cv=4)
    grid.fit(X_train, y_train)
    print("The best parameters are %s with a score of %0.2f" % (grid.best_params_, grid.best_score_))
    '''


