# coding: utf-8
import codecs
import threading
import _thread
from sklearn.cross_validation import cross_val_score
from sklearn.externals import joblib
import time
import sys

__author__ = 'Administrator'

from sklearn.ensemble import AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier
import numpy as np

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

    print('****************完成训练数据加载，开始训练******************')

    ct = CountdownTask()
    ct.start()
    bdt_discrete = AdaBoostClassifier(
        DecisionTreeClassifier(max_depth=2),
        n_estimators=600,
        learning_rate=1.5,
        algorithm="SAMME")

    bdt_discrete.fit(dataMat[0:row_num, 0:col_num - 2], dataMat[0:row_num, col_num-1])
    print()
    time.sleep(7)
    ct.terminate()

    print('****************完成模型训练******************')
    print('****************开始交叉验证******************')

    ct = CountdownTask()
    ct.start()
    scores = cross_val_score(bdt_discrete, dataMat[0:row_num, 0:col_num - 2], dataMat[0:row_num, col_num-1], cv=5, scoring='accuracy')
    print()
    ct.terminate()

    #joblib.dump(bdt_discrete, 'lr.model', compress=1)

    print(scores)


