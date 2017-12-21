# -*- coding: utf-8 -*-
"""
Created on Tue Oct 17 10:28:30 2017

@author: 赵慧
"""

import pandas as pd
import os
import numpy as np
from numpy import nan as NA
import datetime
from sklearn.cross_validation import train_test_split
from sklearn import metrics
from sklearn.preprocessing import Imputer
from sklearn import grid_search
from sklearn.externals import joblib

import sys

print(sys.argv)

# a = sys.argv[2:]
os.getcwd()


def DataProcessing(InputDataFilePath, NewinputDataFilePath):
    testdata = pd.read_csv(InputDataFilePath, encoding="utf-8")  # ,na_values='NaN',na_filter="NA"
    print('origin data.columns:',testdata.columns)
    print('********Total Data counts**********:',len(testdata))

    data = testdata[['user_id',  'brand_id', 'innet_date',
                       'cust_sex', 'constelllation_desc',
                      'cert_age_0', 'credit_class_0',
                      'is_lost_2', 'is_lost_1' , 'is_lost_0' ,'is_this_break_2', 'is_this_break_1','is_this_break_0',
                       'month_fee_2', 'month_fee_1', 'month_fee_0',
                       'month_flux_2', 'month_flux_1', 'month_flux_0',
                     'user_3wu_flag_2', 'user_3wu_flag_1', 'user_3wu_flag_0',
                     'roaming_days_0', 'call_times_0', 'originate_times_0',  'destination_phone_numbers_0',
                     'no_calling_days_0', 'using_days_0', 'yue_2', 'yue_1', 'yue_0', 'recv_fee_2', 'recv_fee_1',
                     'recv_fee_0']].copy()

    data['cust_sex'] = data['cust_sex'].replace('(null)', str(3))
    data['constelllation_desc'] = data['constelllation_desc'].replace('(null)', str(13))
    data['brand_id'] = data['brand_id'].replace("(null)", str(200))
    innetdate = data['innet_date'].values
    data["innet_days"] = [i.days for i in
                          (datetime.datetime(int(sys.argv[2]), int(sys.argv[3]), 28) - pd.to_datetime(innetdate, format='%Y%m%d'))]
    #print(',@@@@@@@@@@@@@@@@@@@@@',data["innet_days"].head())
    #data['channel_id'] = data['channel_id'].replace("(null)", str(999))
    lost = []
    for i in range(len(data)):
        if data['is_this_break_2'][i] + data['is_this_break_1'][i] + data['is_this_break_0'][i]  == 0:

            lost.append(0)
        elif data['is_this_break_2'][i] + data['is_this_break_1'][i]==0  and  data['is_this_break_0'][i] == 1:
            lost.append(1)
        else:
            lost.append(-2)

    data["lost"] = lost
    print('total leave num', len(data[data["lost"] == 1]))
    data = data[data["lost"] == 0]
    print('total stay num',len(data))


    ####data = data[data['month_fee_2'] + data['month_fee_1'] + data['month_fee_0'] != -3]
    del data['innet_date']
    # data.to_csv(OutputDataFilePath)

    ##data_leave = data[data["lost"] == 1]
    ##data_stay = data[data["lost"] == 0].sample(n=len(data_leave), axis=0)
    ##out = data_leave.append(data_stay)
    data3 = data[data["innet_days"] > 90]
    data1 = data3[data3["innet_days"] <= 365]
    data2 = data[data["innet_days"] > 365]
    if sys.argv[1]=='1':
        print('data1 num-0',len(data1))
        data1.to_csv(sys.argv[1] + NewinputDataFilePath)
    elif  sys.argv[1]=='2':
        print('data2 num-0', len(data2))
        data2.to_csv(sys.argv[1] + NewinputDataFilePath)
    elif sys.argv[1] == '3':
        print('data3 num-0', len(data3))
        data3.to_csv(sys.argv[1] + NewinputDataFilePath)

def load_model(NewinputDataFilePath):
    xxx = pd.read_csv(sys.argv[1]+NewinputDataFilePath)
    print('load_model origin data：',xxx.columns)
    print('data_file_name',sys.argv[1] + NewinputDataFilePath)
    '''
    user_id,month_id,device_number,brand_id,innet_date,channel_id,
    area_id,cust_sex,constelllation_desc,cust_birthday,cert_age_0,credit_class_0,
    roaming_days_0,call_times_0,originate_times_0,destination_phone_numbers_0,
    no_calling_days_0,using_days_0,is_lost_0,is_this_break_0,month_fee_0,month_flux_0,
    user_3wu_flag_0,yue_0,recv_fee_0,cert_age_1,credit_class_1,roaming_days_1,call_times_1,
    originate_times_1,destination_phone_numbers_1,no_calling_days_1,using_days_1,is_lost_1,
    is_this_break_1,month_fee_1,month_flux_1,user_3wu_flag_1,yue_1,recv_fee_1,cert_age_2,
    credit_class_2,roaming_days_2,call_times_2,originate_times_2,destination_phone_numbers_2,
    no_calling_days_2,using_days_2,
    is_lost_2,is_this_break_2,month_fee_2,month_flux_2,user_3wu_flag_2,yue_2,recv_fee_2
    
    原模型用的
    'brand_id', 'cust_sex', 'constelllation_desc',
                      'cert_age', 'credit_class',
                      'lost_5', 'lost_6', 'lost_7', 
                       'break_5', 'break_6','break_7',
                       'fee_5', 'fee_6', 'fee_7',
                      'flux_5', 'flux_6', 'flux_7', 
                       '3wu_5','3wu_6', '3wu_7',  
                       'roaming_days_7', 'call_times_7',
                      'originate_times_7', 'destination_phone_numbers_7', 'no_phone_days_7',
                      'using_days_7', 'yue_5', 'yue_6', 'yue_7', 'recv_fee_5',
                      'recv_fee_6', 'recv_fee_7','innet_days'
    
    '''
    ###xxx = xxx[xxx['is_lost_2'] + xxx['is_lost_1'] + xxx['is_lost_0'] == 0]
    X = xxx[['brand_id','cust_sex', 'constelllation_desc','cert_age_0', 'credit_class_0',
             'is_lost_2','is_lost_1','is_this_break_2','is_this_break_1',
             'month_fee_2','month_fee_1','month_fee_0',
             'month_flux_2','month_flux_1','month_flux_0',
             'user_3wu_flag_2','user_3wu_flag_1','user_3wu_flag_0',
             'roaming_days_0','call_times_0','originate_times_0','destination_phone_numbers_0',
             'no_calling_days_0','using_days_0','yue_2','yue_1','yue_0','recv_fee_2','recv_fee_1','recv_fee_0',
             'innet_days']].copy()
    colnames = X.columns
    print('load model filds count',len(colnames))
    print('*******people_stay_count*********:',sys.argv[1] ,len(X))
    Result = pd.DataFrame({'user_id':xxx['user_id']})
    ###print('typeResult',type(Result),Result.head())
    modelname = [sys.argv[1]+"LogisticRegression.model", sys.argv[1]+"Decision Tree.model", sys.argv[1]+"Random Forest.model"]

    for loadmodel in modelname:
        gm_back = joblib.load(loadmodel)
        XX = Imputer().fit_transform(X)
        Result['pred_'+loadmodel] = gm_back.predict(XX)
        Result['probs_'+loadmodel] = gm_back.predict_proba(XX)[:,1]

        if loadmodel == sys.argv[1]+"Random Forest.model":
            count=0
            for index in gm_back.feature_importances_.argsort()[::-1][:5]:
                nam = colnames[index]
                count += 1
                Result[nam+'-'+str(count)] = X.ix[:, index]
                Result['Score'] = Result.ix[:, [2, 4, 6]].mean(1, skipna=True) * 100
                Result['Result_class'] = [np.argmax(np.bincount(Result.ix[i, [1, 3, 5]].astype(np.int64))) for i in Result.index]
        else:
            continue
    for i in Result.columns:
        if i.endswith('.model'):
            del Result[i]

    Result=Result.sort_values(by=['Score'],ascending=False)
    Result.to_csv(sys.argv[1]+"user_predict.csv")
    print('well done')



#InputDataPath = 'qinghai_9_11.csv'
InputDataPath = 'AllUserData201712.csv'
NewinputDataFilePath = 'Data_new.csv'
ddd = DataProcessing(InputDataPath,NewinputDataFilePath)
load_model(NewinputDataFilePath)

