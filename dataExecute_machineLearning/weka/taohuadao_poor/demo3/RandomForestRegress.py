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
    filePath = "D:\maintainwork\data\扶贫数据\精准资助\\train\结果数据\宽表\\train.txt"
    dataMat = data_execute.loadDataSet(filePath)
    row_num = len(dataMat)
    col_num = len(dataMat[0])
    dataMat = np.array(dataMat)

    # print(dataMat[0:row_num, 0])

    regr_rf = RandomForestRegressor(max_depth=3, random_state=2)
    regr_rf.fit(dataMat[0:row_num, 2:col_num], dataMat[0:row_num, 1])

    #print(regr_rf.feature_importances_)
    #print(regr_rf.predict(dataMat[0:row_num, 1:col_num]))

    testFile_path = "D:\maintainwork\data\扶贫数据\精准资助\\train\结果数据\宽表\\test.txt"
    testMat = data_execute.loadDataSet(testFile_path)
    testMat = np.array(testMat)
    row_num_test = len(testMat)

    testPros = regr_rf.predict(testMat[0:row_num_test, 2:col_num])
    testTrue = testMat[0:row_num_test, 1]

    err = 0
    for i in range(0, row_num_test):
        if testPros[i] < 500:
            testPros[i] = 0
        elif 500 <= testPros[i] < 1000:
            testPros[i] = 500
        elif 1000 <= testPros[i] < 1500:
            testPros[i] = 1000
        elif 1500 <= testPros[i] < 3500:
            testPros[i] = 1500

        if testPros[i] != testTrue[i]:
            err += 1

    print(err / row_num_test)
