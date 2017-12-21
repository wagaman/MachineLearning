# coding: utf-8
from __future__ import division
from weka.taohuadao_poor.demo3 import data_execute

__author__ = 'Administrator'

# 文件格式 1,2,3,4,5,7,7,8
#
#


from sklearn.ensemble import RandomForestRegressor
import numpy as np




if __name__ == '__main__':
    filePath = "D:\workspaceHuayu\helloWeb\jeesite-master\src\main\webapp\\userfiles\\1\\files\\test\\2017\\03\isPoor_logic.txt";
    dataMat = data_execute.loadDataSet(filePath)
    row_num = len(dataMat)
    col_num = len(dataMat[0])
    dataMat = np.array(dataMat)

    # print(dataMat[0:row_num, 0])

    regr_rf = RandomForestRegressor(max_depth=3, random_state=2)
    regr_rf.fit(dataMat[0:row_num, 1:col_num], dataMat[0:row_num, 0])

    print(regr_rf.feature_importances_)
    print(regr_rf.predict(dataMat[0:row_num, 1:col_num]))

    testMat = data_execute.loadDataSet(filePath)
    testMat = np.array(testMat)
    testPros = regr_rf.predict(testMat[0:row_num, 1:col_num])
    testClass = [round(x) for x in testPros]
    right = 0
    for i in range(0, row_num):
        trueClass = testMat[i, 0]
        preClass = testClass[i]
        if(trueClass == preClass):
            right += 1
    print( right / len(testMat))