#coding=utf-8
'''
Created on 2017年5月11日

@author: cyf

@description: 
'''
import logging
import time
import os
import xlrd
import sys
reload(sys)
sys.setdefaultencoding('utf-8') 
#时间格式
timeFormat = '%Y%m%d%H'
curTime = time.strftime(timeFormat, time.localtime())

#设置log路径
logPath = "../log/py"
if not os.path.exists(logPath):
    os.mkdir(logPath)
logFile = '%s/%s.log' %(logPath, curTime)

logging.basicConfig(level=logging.DEBUG,
                format='[%(levelname)s] %(asctime)s %(filename)s[line:%(lineno)d] [%(message)s]',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename=logFile,
                filemode='a+')
'''
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(name)-8s: %(levelname)-8s %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)
'''

def convertDict(path, sheetName):
    "{'sd':{tablename:[name, code, num, size]...,}, 'hb':{tablename:[name, code, num, size]...,}"
    data = xlrd.open_workbook(path)
    table = data.sheet_by_name(sheetName)
    rows = table.nrows
    hb = 'hb'
    sd = 'hb'
    ret = {}
    
    if sd not in ret:
        ret[sd] = {}
    if hb not in ret:
        ret[hb] = {}
    
    for i in xrange(rows):
        if i < 3:
            continue
        rowData = table.row_values(i)
        
        
        sdTable = rowData[1]
        sdName = rowData[2]
        sdCode = rowData[3]
        sdNum = rowData[4]
        sdSize = "%sM" %rowData[5]
        
        hbTable = rowData[7]
        hbName = rowData[8]
        hbCode = rowData[9]
        hbNum = rowData[10]
        hbSize = "%sM" %rowData[11]
        
        if sdTable not in ret[sd]:
            ret[sd][sdTable] = [sdName, sdCode, sdNum, sdSize]
        
        if hbTable not in ret[hb]:
            ret[hb][hbTable] = [hbName, hbCode, hbNum, hbSize]
    #logging.info("字典生成成功%s", ret)
        
    return ret

def getCode(dataDict, province, table):
    "返回对应省份表的code"
    return dataDict[province][table][1]

if __name__ == "__main__":
    if len(sys.argv) < 3:
        logging.info("input error")
        sys.exit()
        
    table = sys.argv[2]
    province = sys.argv[1]
    fileXlsx = 'ODS12.xlsx' 
    dataDict = convertDict(fileXlsx,'Sheet1')
    code = getCode(dataDict, province, table)
    logging.info("%s省%s的接口号：%s", province, table, code)
    print code
