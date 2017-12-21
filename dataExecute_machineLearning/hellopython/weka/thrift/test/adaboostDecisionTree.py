# coding: utf-8
from weka.thrift import data_execute


__author__ = 'Administrator'

# Author: Noel Dawe <noel.dawe@gmail.com>
#
# License: BSD 3 clause

from sklearn.ensemble import AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier
import numpy as np

if __name__ == '__main__':
    filePath = "D:\workspaceHuayu\helloWeb\jeesite-master\src\main\webapp\userfiles\\1\\files\\test\\2017\\03\isPoor_logic.txt";
    dataMat = data_execute.loadDataSet(filePath)
    row_num = len(dataMat)
    col_num = len(dataMat[0])
    dataMat = np.array(dataMat)

    #print(dataMat[0:row_num, 0])

    bdt_discrete = AdaBoostClassifier(
        DecisionTreeClassifier(max_depth=2),
        n_estimators=600,
        learning_rate=1.5,
        algorithm="SAMME")


    bdt_discrete.fit(dataMat[0:row_num, 1:col_num], dataMat[0:row_num, 0])
    print(bdt_discrete.feature_importances_)
    print(bdt_discrete.predict(dataMat[0:row_num, 1:col_num]))
    print(bdt_discrete.predict_proba(dataMat[0:row_num, 1:col_num]))
