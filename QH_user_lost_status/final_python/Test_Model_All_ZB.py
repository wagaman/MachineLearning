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
    #if is_save=='1':
    #    print "================"
    #else:
    #    print is_save
    #sys.exit()
    testdata = pd.read_csv(InputDataFilePath, encoding="utf-8")  # ,na_values='NaN',na_filter="NA"
    #print "======================"
    #print frmHeader
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
        if data['break_6'][i] + data['break_7'][i] + data['break_8'][i] + data['break_5'][i] == 0:
            lost.append(0)
        elif data['break_6'][i] + data['break_7'][i] + data['break_5'][i] == 0 and data['break_8'][i] == 1:
            lost.append(1)
        else:
            lost.append(-2)
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
        data = data[data['fee_6'] + data['fee_7'] + data['fee_8'] +data['flux_6'] + data['flux_7'] + data['flux_8'] <= -3]


    print "user balanced"
    data_leave = data[data["lost"]==1]
    data_stay = data[data["lost"] == 0]#.sample(n = math.ceil(len(data_leave)*1.1),axis=0)
    print "leave users :",len(data_leave)
    print "innet users :", len(data_stay)

    out1 = data_leave.append(data_stay)
   
    if is_save =='1':
        print "saving balanced file....."
        out1.to_csv(OutputDataFilePath)
        print "balanceFile saved."
    if is_save == '3':
        return out1


def ReadData(InputDataPath,fromFile,infrm):
    if fromFile == '0' or fromFile == '3':
        data = infrm
    else:
        data = pd.read_csv(InputDataPath, encoding="utf-8")
    X = data[['brand_id',
              'cust_sex', 'constellation_desc', 'credit_class',
              'roaming_days_7', 'call_times_7', 'originate_times_7',
              'destination_phone_numbers_7', 'no_phone_days_7',
              'using_days_7', 'fee_6', 'fee_7', 'fee_5',
              'flux_6', 'flux_7', 'flux_5', '3wu_6', '3wu_7', '3wu_5', 'INNET_DAYS',
              'cert_age','recv_fee_5','recv_fee_6','recv_fee_7','yue_6','yue_7','yue_5']]
    y = data['lost']
    return X,y


def ModelMaker(InputDataPath,fromFile,infrm):
    from sklearn.linear_model import LogisticRegression
    from sklearn.ensemble import RandomForestClassifier
    from sklearn import tree
    print "Model Training Begin"
    X_train, X_test, y_train, y_test = ReadData(InputDataPath,fromFile,infrm)

    names = ["LogisticRegression", "Decision Tree", "Random Forest"]
    models = [LogisticRegression(penalty='l2', C=10.0, tol=0.0001), tree.DecisionTreeClassifier(max_depth=5),
              RandomForestClassifier(n_estimators=10, max_depth=None, max_features=4, oob_score=False,
                                     random_state=531)]
    tt = pd.DataFrame({"y_test": y_test})
    for model, name in zip(models, names):
        X_train = Imputer().fit_transform(X_train)
        X_test = Imputer().fit_transform(X_test)

        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        #y_pred_odds = model.predict_proba(X_test)
        joblib.dump(model, "./models/"+name+"_"+sys.argv[3]+".m")
        print "model ==>"+ name +" saved to dir whose path is ./models/"

        print y_pred
        y_test = [int(str(i)[0:1]) for i in y_test]

        classify_report = metrics.classification_report(y_test, y_pred)
        tt['y_pred' + name] = y_pred
    return tt, y_test

def model_reuse(Xfrm,y,models,filtertype):
    #os.chdir('/home/apple/ML/code/')
   
    frm = pd.DataFrame(columns=['LR','Tree','RF'])
    #frm['user_id'] = x
    #y = [int(str(i)[0:1]) for i in y]
    frm['lost'] = y
    x = Imputer().fit_transform(Xfrm)
    y = Imputer().fit_transform(y)
    for mod in models:
        mod = './models/'+mod+"_"+filtertype+".m"
        clf = joblib.load(mod)
        if 'LogisticRegression' in str(mod):
            #frm['LR'] = clf.predict_proba(x)
            frm['LR'] = clf.predict(x)
        if 'Tree' in str(mod):
            #frm['Tree'] = clf.predict_proba(x)
            frm['Tree'] = clf.predict(x)
        if 'Random' in str(mod):
            #frm['RF'] = clf.predict_proba(x)
            frm['RF'] = clf.predict(x)
    #frm['MeanValue'] = frm.mean(0)
    #frm = frm.loc[:,['user_id','MeanValue']]

    Median = frm.median(1)
    list = np.array([ int(str(i)[0:1]) for i in Median])
    
    frm['MedianValue'] = list
    frm = frm.loc[:,['MedianValue','lost']]
    #frm.to_excel("user_predict.xls")
    return frm


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
sqldumfile = "Tmysqldumpfile_"+timetmp.strftime('%Y%m')+".txt"
AllUserData = "AllUserData"+timetmp.strftime('%Y%m')+".csv"
BalancedData = "TBalancedData"+timetmp.strftime('%Y%m%d')+"_"+sys.argv[4]+".csv"
strHeader = getHeader("./conf/Header.conf")
if(skipmysqlTrans == '0'):
    MysqlToFile(sys.argv[2],sqldumfile)
    #MysqlToFile(mysqltable,outfile)
    #InsertFile2Standard(infilepath, outfilepath, issave, strHeader)
    InsertFile2Standard(sqldumfile,AllUserData,1,strHeader)

#sys.exit()

datafrm = GetModelData(AllUserData, BalancedData, sys.argv[3], Header2frmHead(strHeader), sys.argv[4])
#GetModelData(InputDataFilePath, OutputDataFilePath, is_save, frmHeader, rm_op, sample)

#ModelMaker(InputDataPath,fromFile,infrm)

##tt= ModelMaker(BalancedData,sys.argv[3],datafrm)
#if sys.argv[3] == '0':
#    datafrm = pd.read_csv(BalancedData, encoding="utf-8")
x,y=ReadData(BalancedData,sys.argv[3],datafrm)
models=["LogisticRegression", "Decision Tree", "Random Forest"]
outFrm = model_reuse(x,y,models,sys.argv[4])
#y_pred = [np.median(tt.ix[i, [1, 2, 3]]) for i in tt.index]
#Total = pd.DataFrame({"y_test": yTest, 'y_pred': y_pred})
classify_report = metrics.classification_report(outFrm['lost'], outFrm['MedianValue'])
confusion_matrix = metrics.confusion_matrix(outFrm['lost'], outFrm['MedianValue'])
print 'classify_report for ' + "Ensemble" + '\n', confusion_matrix
print 'classify_report for ' + "Ensemble" + '\n', classify_report
