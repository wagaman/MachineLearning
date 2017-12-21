import codecs
import random

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
    for datas in dataMat:
        newPrice = datas[1] * 9.88 * 10**-8 - datas[2] * 5.6*10 **-8 + 980

        print(round(newPrice, -2) + random.randint(-10, 10)*20)