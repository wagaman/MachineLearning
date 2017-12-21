# coding: utf-8
__author__ = 'Administrator'
from sklearn import datasets

import codecs



def loadDataSet(filename):
    dataMat=[]
    fr = codecs.open(filename, "r", "utf-8")
    lineNum = 0
    for line in fr.readlines():
        curLine = line.strip().split(',')
        if (lineNum > 0):
            aa = [float(i) for i in curLine]
            dataMat.append(aa)
        lineNum += 1

    return dataMat

if __name__ == '__main__':
    filePath = "D:\workspaceHuayu\helloWeb\jeesite-master\src\main\webapp\userfiles\\1\\files\\test\\2017\\03\isPoor_logic.txt";
    dataMat = loadDataSet(filePath)

    print(dataMat[1])

