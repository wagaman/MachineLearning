import codecs
import numpy as np
from sklearn.cross_validation import cross_val_score
from sklearn.ensemble import AdaBoostClassifier
from sklearn.feature_selection import SelectKBest, chi2
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
            try:
                for i in curLine:
                    if "" is i:
                        aa.append(0)
                    else:
                        aa.append(float(i))
                dataMat.append(aa)
            except:
                print(line)
                pass
        lineNum += 1

    return dataMat


if __name__ == '__main__':
    filePath = "D:\workspaceHuayu\helloPython\hellopython\weka\chinaunicom_test2\\relate.txt"
    dataMat = loadDataSet(filePath)
    row_num = len(dataMat)
    col_num = len(dataMat[0])
    dataMat = np.array(dataMat)
    X = dataMat[1:row_num, 0:col_num - 1]
    y = dataMat[1:row_num, col_num - 1]
    X_chi2 = SelectKBest(chi2, k=5).fit_transform(X, y)

    print(X_chi2)


