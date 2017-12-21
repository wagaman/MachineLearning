#coding=utf-8
'''
Created on 2017年5月10日

@author: cyf

@description: 将数据导入到oracle数据库
'''
import logging
import re
import os
import cx_Oracle as orcl
import sys
import time
import xlrd
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

def xlsxToDict(path, sheetName):
    "将数据库表的参数读入到字典中.eg:{1：[name,code, dataType]}"
    #读取xlsx文件
    data = xlrd.open_workbook(path)
    table = data.sheet_by_name(sheetName)
    rows = table.nrows
    
    ret = {}
    for i in xrange(rows):
        if i < 3:
            continue
        rowData = table.row_values(i)
        name = rowData[1]
        code = rowData[2]
        dataType = rowData[3]
        num = i - 3
        
        if num not in ret:
            ret[num] = [name, code, dataType]
        
    logging.info("数据处理成功:%s!", ret)
    
    return ret



def createTable(listName, dataDict):
    "创建数据库，对应的表格.{1：[name,code, dataType]}"
    fieldsList = []
    commentsList = []
    for k, v in dataDict.items():
        field = "%s %s NULL" %(v[1], v[2])
        comment = "COMMENT ON COLUMN %s.%s IS \'%s\';" %(listName, v[1], v[0])
        fieldsList.append(field)
        commentsList.append(comment)
    
    fields = ",".join(fieldsList)
    comments = "".join(commentsList)
    
    #创建库表的语句
    commandToFile = 'CREATE TABLE %s (%s);\n%s' %(listName, fields, comments)
    command = 'CREATE TABLE %s (%s)' %(listName, fields)
    logging.info("建表语句:%s", command)
    
    #写入文件
    sqlFilePath = '../sql'
    if not os.path.exists(sqlFilePath):
        os.mkdir(sqlFilePath)
    sqlFile = "%s/%s.sql" %(sqlFilePath, listName)
    with open(sqlFile, 'w') as f:
        f.write(commandToFile)
    logging.info("%s,写入成功", sqlFile)

    try:
        db = orcl.connect('C##dandanxu/D6yUfzJ0@10.1.131.65/rac12c')
        cursor = db.cursor()   
        cursor.execute(command)
    except orcl.DatabaseError, e:
        logging.info(str(e))
        return 
    finally:
        db.commit()
        db.close()
    logging.info("数据表创建成功:%s", listName)
    


def createFileControl(path, listName, dataDict):
    "创建sqllrd控制文件{1：[name,code, dataType]}"
    start = "load data\ncharacterset utf8\nappend\ninto table %s\nFIELDS TERMINATED BY X\'01\'\nTRAILING NULLCOLS\n" %listName
    fieldsList = []
    
    #如果目录不存在，创建目录
    if not os.path.exists(path):
        os.mkdir(path)
    
    for k, v in dataDict.items():
        code = v[1]
        dataType = v[2]
        if dataType == 'DATE':
            code = '%s DATE \"YYYY-MM-DD HH24:MI:SS\"' %code
        elif int(re.findall(r'\(\d+\)', dataType)[0][1:-1]) > 255:
            code = '%s char(%d) ' %(code, int(re.findall(r'\d+', dataType)[1]))
        fieldsList.append(code)
    
    #获取columns。eg：(id, name, ...)
    stringField = ",".join(fieldsList)
    field = "(%s)" %stringField
    
    #写入文件
    controlFile = "%s/%s.ctl" %(path, listName)
    with open(controlFile, 'w') as f:
        f.write(start)
        f.write(field)
    
    logging.info("控制文件创建成功: %s", controlFile)

  


if __name__ == "__main__":
    if len(sys.argv) < 2:
        logging.info("input error")
        sys.exit()
    tableName = sys.argv[1]
    controlPath = '../ctl'
    fileXlsx = 'ODS.xlsx'
    data= xlsxToDict(fileXlsx, tableName)
    createFileControl(controlPath, tableName, data)
    createTable(tableName, data)
