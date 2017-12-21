# coding: utf-8
from weka.taohuadao_poor.demo3 import data_execute

__author__ = 'Administrator'

# Author: Noel Dawe <noel.dawe@gmail.com>
#
# License: BSD 3 clause

from sklearn.ensemble import AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier
#引入其他包下的需要从根目录，如引用demo2下的data_execute from weka.demo2 import data_execute
import numpy as np

if __name__ == '__main__':
    filePath = "D:\maintainwork\data\扶贫数据\精准资助\\train\结果数据\宽表\\train.txt";
    dataMat = data_execute.loadDataSet(filePath)
    row_num = len(dataMat)
    col_num = len(dataMat[0])
    dataMat = np.array(dataMat)

    # print(dataMat[0:row_num, 0])

    bdt_discrete = AdaBoostClassifier(
        DecisionTreeClassifier(max_depth=3),
        n_estimators=600,
        learning_rate=1.5,
        algorithm="SAMME")

    bdt_discrete.fit(dataMat[0:row_num, 2:col_num], dataMat[0:row_num, 1])

    #print(bdt_discrete.feature_importances_)
    #print(bdt_discrete.predict(dataMat[0:10, 2:col_num]))

    testFile_path = "D:\maintainwork\data\扶贫数据\精准资助\\train\结果数据\宽表\\test.txt";
    testMat = data_execute.loadDataSet(testFile_path)
    testMat = np.array(testMat)
    row_num_test = len(testMat)
    testPros = bdt_discrete.predict(testMat[0:row_num_test, 2:col_num])
    testTrue = testMat[0:row_num_test, 1]

    err = 0
    for i in range(0, row_num_test):
        if testPros[i] != testTrue[i]:
            err += 1

    print(err / row_num_test)


