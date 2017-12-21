#coding:utf-8
import os
import sys
import codecs
import datetime
import pandas as pd
from sklearn.cross_validation import train_test_split
from sklearn import metrics
from sklearn.preprocessing import Imputer
import numpy as np
from numpy import nan as NA
import math
from sklearn.externals import joblib

os.getcwd()
reload(sys)
sys.setdefaultencoding( "utf-8" )

def MysqlToFile(mysqltable,outfile):
    print "dump mysql table ...."
    cmdline = 'mysqldump -uroot -P31360 -h10.162.160.114 -pqazXSW qinghai '+mysqltable+' > ./'+outfile
    print cmdline
    if (str(os.system(cmdline)).endswith('0')):
        print "table dumped."
        return 0
    else:
        return -1

def InsertFile2Standard(infilepath,outfilepath,issave,strHeader):
    print "Insert File Transfering to Standard CSV file"
    if not os.path.exists(infilepath):
        print "file doesnt exist. The path is :", infilepath
        sys.exit(-3)
    #if issave == 0:
    #    return

    fp = open(infilepath, 'r')
    filelines = fp.readlines()
    fp.close()

    rows = []
    dict = {"摩羯座": 1, "白羊座": 2, "双鱼座": 3, "狮子座": 4, "双子座": 5, "天秤座": 6,
            "巨蟹座": 7, "天蝎座": 8, "金牛座": 9, "射手座": 10, "水瓶座": 11, "处女座": 12}
    for ilines in filelines[4:-2]:
        if not ilines.startswith("INSERT"):
            continue
        content = ilines.split("VALUES ")[1]
        lines = []
        lines = content.split("),(")

        lines[0] = str(lines[0]).replace("(", "")
        lines[-1] = str(lines[-1]).replace(")", "").replace(";", "")
        for i in lines:
            row = i.replace("'", "").replace("NULL", "-1")
            row = row.replace("?", "")
            for xing in dict.keys():
                if xing in row:
                    row = row.replace(xing, str(dict[xing]))
            row = row + '\n'
            rows.append(row)

    output = open(outfilepath, 'w')
    # output.write("user_id,DEVICE_NUMBER,BRAND_ID,INNET_DATE,CHANNEL_ID,AREA_ID,CUST_SEX,CONSTELLATION_DESC,CUST_BIRTHDAY,CREDIT_CLASS,roaming_days,call_times,originate_times,destination_phone_numbers,no_phone_days,using_days,lost_6,lost_7,lost_8,break_6,break_7,break_8,fee_6,fee_7,fee_8,flux_6,flux_7,flux_8,3wu_6,3wu_7,3wu_8\n")
    output.write(strHeader+'\n')
    output.writelines(rows)
    output.close()

def getHeader(Headerpath):
    #header="user_id,DEVICE_NUMBER,BRAND_ID,INNET_DATE,CHANNEL_ID,AREA_ID,CUST_SEX,CONSTELLATION_DESC,CUST_BIRTHDAY,CREDIT_CLASS,roaming_days,call_times,originate_times,destination_phone_numbers,no_phone_days,using_days,lost_6,lost_7,lost_8,break_6,break_7,break_8,fee_6,fee_7,fee_8,flux_6,flux_7,flux_8,3wu_6,3wu_7,3wu_8,lost_9,break_9,fee_9,flux_9,3wu_9
    #\n
    if not os.path.exists(Headerpath):
        print "Header doesnt exist. The path is :", Headerpath
        sys.exit()

    fp = open(Headerpath, 'r')
    header = fp.readline()
    fp.close()
    if(len(header)>0):
        header = header.replace("\r","")
        header = header.replace("\n","")
        return header
    else:
        print("Header File doesnt contain header")
        sys.exit()
def Header2frmHead(strHeader):
    #print "deal Header to Frame header tuple"
    #print strHeader
    headers = strHeader.split(',')
   
    #for he in headers:
    #    strh=strh +he+","

    return headers

def GetModelData(InputDataFilePath, OutputDataFilePath,is_save,frmHeader,rm_op):
    
    print "Begin Generating Balanced File......"
    if is_save == '0':
        return  pd.read_csv(OutputDataFilePath, encoding="utf-8")
    
    testdata = pd.read_csv(InputDataFilePath, encoding="utf-8")  # ,na_values='NaN',na_filter="NA"
    
    data = testdata[frmHeader].copy()
    print "frame got"
    data["cust_sex"] = data["cust_sex"].replace('(null)', str(3))
    data["constellation_desc"] = data["constellation_desc"].replace('(null)', str(13))
    data["brand_id"] = data["brand_id"].replace("(null)", str(200))
    data["INNET_DAYS"] = [i.days for i in
                          (datetime.datetime(2017, 7, 31) - pd.to_datetime(data["innet_date"], format='%Y%m%d'))]
    data["channel_id"] = data["channel_id"].replace("(null)", str(999))
    lost = []
    
    for i in range(len(data)):
        if data['break_8'][i] + data['break_9'][i] + data['break_10'][i] > 1:
            lost.append(-2)
        else:
            lost.append(0)
    print "column null dealt"
    
    data["lost"] = lost
    data = data[data["lost"] > -2]
    del data['innet_date']
	
	
    if rm_op== '1':
        #data = data[data['fee_6']+data['fee_7']+data['fee_8']!=-3 ]
        data = data[data['INNET_DAYS']<=356]
    if rm_op == '2':
        data = data[data['INNET_DAYS'] >356 ]
    if rm_op == '3':
        data = data[data['fee_8'] + data['fee_9'] + data['fee_10'] +data['flux_8'] + data['flux_9'] + data['flux_10'] <= -3]
    
    print "user balanced"
    #data_leave = data[data["lost"]==1]
    #data_stay = data[data["lost"] == 0]#.sample(n = math.ceil(len(data_leave)*1.1),axis=0)
    #print "leave users :",len(data_leave)
    print "users :", len(data)

    #out1 = data_leave.append(data_stay)
   
    if is_save =='1':
        print "saving balanced file....."
        data.to_csv(OutputDataFilePath)
        print "balanceFile saved."
    if is_save == '3':
        return data


def ReadData(InputDataPath,fromFile,infrm):
    
    if fromFile == '0' or fromFile == '3':
        data = infrm
    else:
	print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'+fromFile
        data = pd.read_csv(InputDataPath, encoding="utf-8")
    X = data[['user_id','brand_id',
              'cust_sex', 'constellation_desc', 'credit_class',
              'roaming_days_10', 'call_times_10', 'originate_times_10',
              'destination_phone_numbers_10', 'no_phone_days_10',
              'using_days_10', 'fee_8', 'fee_9', 'fee_10',
              'flux_8', 'flux_9', 'flux_10', '3wu_8', '3wu_9', '3wu_10', 'INNET_DAYS',
              'cert_age','recv_fee_8','recv_fee_09','recv_fee_10','yue_8','yue_09','yue_10']]
    #y i= data['lost']
    return X
 

def model_reuse(Xfrm,models,filtertype):
    #os.chdir('/home/apple/ML/code/')
   
    frm = pd.DataFrame(columns=['LR','Tree','RF'])
    outfrm = pd.DataFrame(columns=['user_id','innet_days','Score'])
        
    x = Xfrm[['brand_id',
              'cust_sex', 'constellation_desc', 'credit_class',
              'roaming_days_10', 'call_times_10', 'originate_times_10',
              'destination_phone_numbers_10', 'no_phone_days_10',
              'using_days_10', 'fee_8', 'fee_9', 'fee_10',
              'flux_8', 'flux_9', 'flux_10', '3wu_8', '3wu_9', '3wu_10', 'INNET_DAYS',
              'cert_age','recv_fee_8','recv_fee_09','recv_fee_10','yue_8','yue_09','yue_10']]
    x = Imputer().fit_transform(x)
    cpath = "./coef_"+filtertype+".txt"
    if not os.path.exists(cpath):
	os.mknod(cpath)
    coefFile = open("./coef_"+filtertype+".txt",'w')
    cols = Xfrm.columns.values
    kk = 0
    for i in cols:
	if kk ==0:
            kk = kk+1
	    continue
        coefFile.write(i+",")
    for mod in models:
        mod = './models/'+mod+"_"+filtertype+".m"
        print mod
        clf = joblib.load(mod)
        if 'LogisticRegression' in str(mod):
            frm['LR'] = clf.predict_proba(x)[:,1]
            coefFile.writelines("\n===>1.LR\n")
            coefFile.writelines(str(clf.coef_))
        if 'Tree' in str(mod):
            frm['Tree'] = clf.predict_proba(x)[:,1]
	    coefFile.writelines("\n===>2.Decision Tree\n")
            coefFile.writelines(str(clf.feature_importances_))
	    #frm['Tree_INT'] = clf.predict(x)
        if 'Random' in str(mod):
	    coefFile.writelines("\n===>3.Random Forest\n")
            coefFile.writelines(str(clf.feature_importances_))
            frm['RF'] = clf.predict_proba(x)[:,1]
   
    Xfrm['Score'] = frm.loc[:,['LR','Tree','RF']].mean(1,skipna=True)*100
    Xfrm = Xfrm.loc[:,['user_id','INNET_DAYS','Score']]
    coefFile.close()
    '''
    ttttt =  pd.DataFrame(columns=['Score'])
    print "Transformed Before:~~~~~~~~~~~~~~~~~~~~~~~~"
   
    LLR=[]
    ttttt['LR'] = frm['LR']
    print ttttt['LR']
    ttttt['Tree'] = frm['Tree']
    ttttt['RF'] = frm['RF']
    ttttt = ttttt.fillna(-1)
    LLR = [i for i in ttttt['LR'] if i == -1]
    print "\n--------LR:\n"+str(len(LLR))
    LTree = []
    LTree = [i for i in ttttt['Tree'] if i == -1]
    print "\n--------Tree:\n"+str(len(LTree))
   
    LRF = []
    LRF = [i for i in ttttt['RF'] if i == -1]
    print "\n--------RF:\n"+str(len(LRF))
    print "Transformed Done:~~~~~~~~~~~~~~~~~~~~~~~~"
    '''	
    timetmp =datetime.datetime.now()	
    Xfrm = Xfrm.round(2)
    Xfrm.to_csv("user_predict_"+timetmp.strftime('%Y%m%d')+"_"+filtertype+".csv")
    print Xfrm
    outfrm1 = Xfrm[Xfrm['Score']>50]
    outfrm1.to_csv("user_leave_"+timetmp.strftime('%Y%m%d')+"_"+filtertype+".csv")
    return outfrm


###===============RUN============================
'''
1.=>MysqlToFile(mysqltable,outfile)
  dump file from mysql to a insertfile
  PARAMETERS:
    mysqltable: one table name
    outfile: store file name.prefix has been set ==>/home/opdn1_hlwyy/
2.=>InsertFile2Standard(infilepath,outfilepath,issave,strHeader)
  transform Insert File got from previous step.
  PARAMETERS:
    infilepath: outfile from Step 1.
    outfilepath: to store a file .
    issave : 0 -- dont save , 1 -- save
    strHeader: dataframe header, format is 'col1,col2,......,coln',
               this parameter got from function "getHeader"
  =>getHeader(Headerpath)
     get one line from a file
  PARAMETERS:
     Headerpath: header file full path or relative path
3.=>GetModelData(InputDataFilePath, OutputDataFilePath,is_save,frmHeader,rm_op,sample)
  get data to put into Model,repalce null,remove users
  Parameters:
    InputDataFilePath:file path from the out file created in Step 2.
    OutputDataFilePath: if save, the save file name.
    is_save : save:1, means the outdata saved
              not save:0 means the outdata is not going to save
    frmHeader: data frame Header.
    rm_op :1=>remove fee and flux abnormal 
           2=>remove less than 100 days
           3=>remove above two
           0=>not remove all
    sample Ã¯Â¼Å¡ how many users to get from whole stay users.
  =>Header2frmHead(strHeader):
    generate parameter "frmHeader" in function "GetModelData"

4.=>ReadData(InputDataPath,fromFile,infrm)
  Read file data or frame data to model,split train and test set.
  
  


sys.argv:order 
  1.skip mysqldump procesure
    0==>dont skip
    1==>skip
  2. mysql table name
  3. is_save: wether to save the balanced data collection
     0 ==> dont save
     1 ==> save
  4. remove option 
     rm_op :1=>remove fee and flux abnormal 
            2=>remove less than 100 days
            3=>remove above two
            0=>not remove all
     
     
  
'''
skipmysqlTrans = sys.argv[1]
timetmp =datetime.datetime.now()
sqldumfile = "Tmysqldumpfile_"+timetmp.strftime('%Y%m%d')+".txt"
AllUserData = "TP_AllUserData"+timetmp.strftime('%Y%m')+".csv"
BalancedData = "TP_BalancedData"+timetmp.strftime('%Y%m%d')+"_"+sys.argv[4]+".csv"
strHeader = getHeader("./conf/11Header.conf")
if(skipmysqlTrans == '0'):
    MysqlToFile(sys.argv[2],sqldumfile)
    #MysqlToFile(mysqltable,outfile)
    #InsertFile2Standard(infilepath, outfilepath, issave, strHeader)
    InsertFile2Standard(sqldumfile,AllUserData,1,strHeader)


datafrm = GetModelData(AllUserData, BalancedData, sys.argv[3], Header2frmHead(strHeader), sys.argv[4])
#GetModelData(InputDataFilePath, OutputDataFilePath, is_save, frmHeader, rm_op)

x=ReadData(BalancedData,sys.argv[3],datafrm)
models=["LogisticRegression", "Decision Tree", "Random Forest"]
outFrm = model_reuse(x,models,sys.argv[4])
print "========================  Result Saved as CSV File ============================="
print "========================  Programme Done! ============================="

#classify_report = metrics.classification_report(outFrm['lost'], outFrm['MedianValue'])
#confusion_matrix = metrics.confusion_matrix(outFrm['lost'], outFrm['MedianValue'])
#print 'classify_report for ' + "Ensemble" + '\n', confusion_matrix
#print 'classify_report for ' + "Ensemble" + '\n', classify_report
