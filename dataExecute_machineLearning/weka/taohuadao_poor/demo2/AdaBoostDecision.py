# coding: utf-8
from weka.taohuadao_poor.demo3 import data_execute

__author__ = 'Administrator'

# Author: Noel Dawe <noel.dawe@gmail.com>
#
# License: BSD 3 clause

from sklearn.ensemble import AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier
import numpy as np

if __name__ == '__main__':
    filePath = "D:\workspaceHuayu\helloWeb\jeesite-master\src\main\webapp\\userfiles\\1\\files\\test\\2017\\03\isPoor_logic.txt";
    dataMat = data_execute.loadDataSet(filePath)
    row_num = len(dataMat)
    col_num = len(dataMat[0])
    dataMat = np.array(dataMat)

    # print(dataMat[0:row_num, 0])

    bdt_discrete = AdaBoostClassifier(
        DecisionTreeClassifier(max_depth=2),
        n_estimators=600,
        learning_rate=1.5,
        algorithm="SAMME")

    bdt_discrete.fit(dataMat[0:row_num, 1:col_num], dataMat[0:row_num, 0])

    print(bdt_discrete.feature_importances_)
    print(bdt_discrete.predict(dataMat[0:row_num, 1:col_num]))

    testMat = data_execute.loadDataSet(filePath)
    testMat = np.array(testMat)
    testPros = bdt_discrete.predict(testMat[0:row_num, 1:col_num])
    testClass = [round(x) for x in testPros]
    right = 0
    for i in range(0, row_num):
        trueClass = testMat[i, 0]
        preClass = testClass[i]
        if(trueClass == preClass):
            right += 1
    print( right / len(testMat))

