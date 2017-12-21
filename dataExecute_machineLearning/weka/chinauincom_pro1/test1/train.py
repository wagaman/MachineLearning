import codecs
import numpy as np
from sklearn.cross_validation import cross_val_score
from sklearn.ensemble import AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.externals import joblib

__author__ = 'sss'



def loadDataSet(filename):
    dataMat=[]
    fr = codecs.open(filename, "r", "utf-8")
    lineNum = 0
    for line in fr.readlines():
        curLine = line.strip().split(',')
        if lineNum > 0:
            aa = []
            for i in curLine:
                if "" is i:
                    aa.append(0)
                else:
                    aa.append(float(i))
            dataMat.append(aa)
        lineNum += 1

    return dataMat


if __name__ == '__main__':
    filePath = "D:\workspaceHuayu\helloPython\hellopython\weka\chinaunicom_test1\\result.txt"
    dataMat = loadDataSet(filePath)
    row_num = len(dataMat)
    col_num = len(dataMat[0])
    dataMat = np.array(dataMat)

    # print(dataMat[0:row_num, 0])

    bdt_discrete = AdaBoostClassifier(
        DecisionTreeClassifier(max_depth=3),
        n_estimators=600,
        learning_rate=0.01,
        algorithm="SAMME")

    bdt_discrete.fit(dataMat[1:row_num, 1:col_num - 2], dataMat[1:row_num, col_num - 1])

    scores = cross_val_score(bdt_discrete, dataMat[1:row_num, 1:col_num - 2], dataMat[1:row_num, col_num - 1], cv=10, scoring='accuracy')

    joblib.dump(bdt_discrete, 'lr.model', compress=1)

    print(scores)