# -*- coding: utf-8 -*-
"""
Created on Tue Oct 17 10:28:30 2017

@author: ут╩ш
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
    #print(testdata.columns)
    '''
    ['user_id', 'device_number', 'brand_id', 'innet_date', 'channel_id',
       'area_id', 'cust_sex', 'constellation_desc', 'cust_birthday',
       'cert_age', 'credit_class', 'roaming_days_8', 'call_times_8',
       'originate_times_8', 'destination_phone_numbers_8', 'no_phone_days_8',
       'using_days_8', 'roaming_days_9', 'call_times_9', 'originate_times_9',
       'destination_phone_numbers_9', 'no_phone_days_9', 'using_days_9',
       'lost_5', 'lost_6', 'lost_7', 'lost_8', 'lost_9', 'break_5', 'break_6',
       'break_7', 'break_8', 'break_9', 'fee_5', 'fee_6', 'fee_7', 'fee_8',
       'fee_9', 'flux_5', 'flux_6', 'flux_7', 'flux_8', 'flux_9', '3wu_5',
       '3wu_6', '3wu_7', '3wu_8', '3wu_9', 'roaming_days_7', 'call_times_7',
       'originate_times_7', 'destination_phone_numbers_7', 'no_phone_days_7',
       'using_days_7', 'yue_5', 'yue_6', 'yue_7', 'yue_8', 'recv_fee_5',
       'recv_fee_6', 'recv_fee_7', 'recv_fee_8', 'recv_fee_9', 'yue_9',
       'roaming_days_10', 'call_times_10', 'originate_times_10',
       'destination_phone_numbers_10', 'no_phone_days_10', 'using_days_10',
       'lost_10', 'break_10', 'fee_10', 'flux_10', '3wu_10', 'yue_10',
       'recv_fee_10']
    '''
    data = testdata[['user_id',  'brand_id', 'innet_date',
                       'cust_sex', 'constellation_desc',
                      'cert_age', 'credit_class',
                      'lost_5', 'lost_6',  'break_5', 'break_6',
                       'break_9', 'fee_5', 'fee_6', 'fee_7',
                       'flux_5', 'flux_6', 'flux_7',   '3wu_5',
                      '3wu_6', '3wu_7',  'roaming_days_7', 'call_times_7',
                      'originate_times_7', 'destination_phone_numbers_7', 'no_phone_days_7',
                      'using_days_7', 'yue_5', 'yue_6', 'yue_7',  'recv_fee_5',
                      'recv_fee_6', 'recv_fee_7']].copy()

    data['cust_sex'] = data['cust_sex'].replace('(null)', str(3))
    data['constellation_desc'] = data['constellation_desc'].replace('(null)', str(13))
    data['brand_id'] = data['brand_id'].replace("(null)", str(200))
    innetdate = data['innet_date'].values
    data["innet_days"] = [i.days for i in
                          (datetime.datetime(int(sys.argv[2]), int(sys.argv[3]), 28) - pd.to_datetime(innetdate, format='%Y%m%d'))]
    #print(',@@@@@@@@@@@@@@@@@@@@@',data["innet_days"].head())
    #data['channel_id'] = data['channel_id'].replace("(null)", str(999))
    lost = []
    for i in range(len(data)):
        if data['break_5'][i] + data['break_6'][i] + data['break_9'][i] == 0:
            lost.append(0)
        elif data['break_5'][i] + data['break_6'][i] == 0 and data['break_9'][i] == 1:
            lost.append(1)
        else:
            lost.append(-2)

    data["lost"] = lost
    data = data[data["lost"] > -2]
    data = data[data['fee_5'] + data['fee_6'] + data['fee_7'] != -3]
    del data['innet_date']
    # data.to_csv(OutputDataFilePath)

    data_leave = data[data["lost"] == 1]
    data_stay = data[data["lost"] == 0].sample(n=len(data_leave), axis=0)
    out = data_leave.append(data_stay)
    out = out[out["innet_days"] > 90]
    data1 = out[out["innet_days"] <= 356]
    data2 = out[out["innet_days"] > 356]
    if sys.argv[1]=='1':
        data1.to_csv(sys.argv[1] + NewinputDataFilePath)
    elif  sys.argv[1]=='2':
        data2.to_csv(sys.argv[1] + NewinputDataFilePath)
    elif sys.argv[1] == '3':
        out.to_csv(sys.argv[1] + NewinputDataFilePath)
    #"innet_days"

    #print('&&&&&&&&@@@@@@@@@@',out.columns)

