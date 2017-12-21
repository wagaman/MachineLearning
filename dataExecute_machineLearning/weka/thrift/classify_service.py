# coding: utf-8


__author__ = 'Administrator'

# Author: Noel Dawe <noel.dawe@gmail.com>
#
# License: BSD 3 clause


from sklearn.ensemble import RandomForestRegressor
from weka.thrift import data_execute
import numpy as np
import uuid



if __name__ == '__main__':
    filePath = "D:\workspaceHuayu\helloWeb\jeesite-master\src\main\webapp\userfiles\\1\\files\\test\\2017\\03\isPoor_logic.txt";
    dataMat = data_execute.loadDataSet(filePath)
    row_num = len(dataMat)
    col_num = len(dataMat[0])
    dataMat = np.array(dataMat)

    # print(dataMat[0:row_num, 0])

    regr_rf = RandomForestRegressor(max_depth=3, random_state=2)
    regr_rf.fit(dataMat[0:row_num, 1:col_num], dataMat[0:row_num, 0])

    print(regr_rf.feature_importances_)
    print(regr_rf.predict(dataMat[0:row_num, 1:col_num]))


def getRandomForest(trainPath, testPath):
    dict = {}
    dataMat = data_execute.loadDataSet(trainPath)
    row_num = len(dataMat)
    col_num = len(dataMat[0])
    dataMat = np.array(dataMat)

    regr_rf = RandomForestRegressor(max_depth=3, random_state=2)
    regr_rf.fit(dataMat[0:row_num, 1:col_num], dataMat[0:row_num, 0])

    dict['cols'] = regr_rf.feature_importances_
    dict['model'] = regr_rf
    dict['id'] = uuid.uuid1()

    testMat = data_execute.loadDataSet(testPath)
    testMat = np.array(testMat)
    print(x for x in testMat)
    testPros = regr_rf.predict(testMat[0:row_num,  1:col_num])
    testClass = [round(x) for x in testPros]
    err = 0
    for x,y in testMat[0:row_num, 0],testClass:
        if(x != y):
            err += 1
    dict['right'] = err / len(testMat)
    return dict


