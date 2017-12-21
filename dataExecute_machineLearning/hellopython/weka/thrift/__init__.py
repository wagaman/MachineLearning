# coding: utf-8
__author__ = 'Administrator'

import classify_service as cs

if __name__ == '__main__':
    filePath = "D:\workspaceHuayu\helloWeb\jeesite-master\src\main\webapp\userfiles\\1\\files\\test\\2017\\03\isPoor_logic.txt";
    dict = cs.getRandomForest(filePath, filePath)