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


