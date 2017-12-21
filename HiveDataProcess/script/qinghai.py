#!/usr/bin/env python
# coding=utf-8
#######################################################################
#	> File Name: qinghai.py
#	> Author: cyf
#	> Mail: XXX@qq.com
#	> Created Time: 2017年09月28日 星期四 10时07分19秒
#######################################################################
import logging
import os
import sys
import time
import xlrd
#import MySQLdb as mdb
import pandas as pd
from pandas import Series, DataFrame
import sqlalchemy
import re

reload(sys)
sys.setdefaultencoding('utf-8') 
cur_path=os.path.abspath(os.path.dirname(os.path.abspath(sys.argv[0])))

#时间格式
timeFormat = '%Y%m%d%H'
curTime = time.strftime(timeFormat, time.localtime())

#设置log路径
logPath = "%s/../log" %(cur_path)
if not os.path.exists(logPath):
    os.mkdir(logPath)
logFile = '%s/%s_py.log' %(logPath, curTime)

logging.basicConfig(level=logging.DEBUG,
                format='[%(levelname)s] %(asctime)s %(filename)s [line:%(lineno)d] [%(message)s]',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename=logFile,
                filemode='a+')
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(filename)s: %(lineno)d %(levelname)-4s  %(message)s')
console.setFormatter(formatter)
#logging.getLogger('').addHandler(console)

def xlsxToDict(path, sheetName):
    "将数据库表的参数读入到字典中.eg:{1：[name,code, dataType]}"
    #读取xlsx文件
    table_pattern='^([a-zA-Z_23]+)+(_\d+)+'
    info = re.search(table_pattern, sheetName)
    sheet_name=info.group(1)
    
    data = xlrd.open_workbook(path)
    table = data.sheet_by_name(sheet_name)
    rows = table.nrows
    ret = {}
    columns = []
    for i in xrange(rows):
        if i < 4:
            continue
        rowData = table.row_values(i)
        name = rowData[1]
        #hive=>4,mysql=>2
        dataType = rowData[4]
        des = rowData[0]
        num = i - 3
        columns.append(name)
        if num not in ret:
            ret[num] = [name, dataType, des]
        
    logging.info("数据字典创建成功!")
    #print '|'.join(columns)
    return ret



def createTable(listName, dataDict, sep='\\001'):
    "创建数据库，对应的表格.{1：[name, dataType, des]}"
    fieldsList = []
    commentsList = []
    for k, v in dataDict.items():
        #field = "%s %s NULL comment \'%s\'" %(v[0], v[1], v[2])
        field = "%s %s" %(v[0], v[1])
        fieldsList.append(field)
        
    
    fields = ",".join(fieldsList)
    #创建库表的语句
    commandToFile = 'CREATE TABLE IF NOT EXISTS %s (%s) row format delimited fields terminated by \'%s\' stored as textfile;' %(listName, fields, sep)
    #print fields 

    command = 'CREATE TABLE IF NOT EXISTS %s (%s) row format delimited fields terminated by \'%s\' stored as textfile;' %(listName, fields, sep)
    logging.info("建表语句:%s", command)
    
    #写入文件
    sqlFilePath = '%s/../sql' %(cur_path)
    if not os.path.exists(sqlFilePath):
        os.mkdir(sqlFilePath)
    sqlFile = "%s/%s.sql" %(sqlFilePath, listName)
    with open(sqlFile, 'w') as f:
        f.write(commandToFile)
    logging.info("%s,写入成功", sqlFile)
if __name__=='__main__':
    if len(sys.argv) < 2:
        print "input error"
        sys.exit(-1)
    '''
    table_name = ['DWA_V_M_CUS_RNS_010',
                  'DWA_V_D_CUS_NM_CHARGE_010', 
                  'DWA_V_M_CUS_NM_CHARGE_010', 
                  'DWA_V_M_CUS_NM_SING_FLUX_010', 
                  'DWD_D_USE_CB_FLUX_CBSSGPRS', 
                  'DWD_D_USE_CB_SMS_CBSS', 
                  'DWD_D_USE_CB_VOICE_CBSS',
                  'DWA_V_M_CUS_CB_USER_3WU_010', 
                  'DWA_V_M_CUS_CB_IMEI_FLUX_010', 
                  'DWA_V_M_CUS_2G_IMEI_FLUX_010', 
                  'DWA_V_M_CUS_CB_USER_INFO_010', 
                  'DWA_V_M_CUS_3G_IMEI_FLUX_010',
                  'DWA_V_M_CUS_3G_USER_3WU_010',
                  'DWA_V_M_CUS_3G_RNS_WIDE']
    '''
    name=sys.argv[1]

    table_path = "%s/../table/table_1025.xlsx" %(cur_path)
    ret = xlsxToDict(table_path, name)
    #ret = xlsxToDict("./23G.xlsx", name)
    if len(sys.argv) == 3:
        sep = sys.argv[2]
        createTable(name, ret, sep)
    else:
        createTable(name, ret)
