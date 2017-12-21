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


def load_model(NewinputDataFilePath):
    xxx = pd.read_csv(sys.argv[1]+NewinputDataFilePath)

    X = xxx[['brand_id', 'cust_sex', 'constellation_desc',
                      'cert_age', 'credit_class',
                      'lost_5', 'lost_6',  'break_5', 'break_6',
                       'fee_5', 'fee_6', 'fee_7',
                      'flux_5', 'flux_6', 'flux_7',  '3wu_5',
                      '3wu_6', '3wu_7',  'roaming_days_7', 'call_times_7',
                      'originate_times_7', 'destination_phone_numbers_7', 'no_phone_days_7',
                      'using_days_7', 'yue_5', 'yue_6', 'yue_7', 'recv_fee_5',
                      'recv_fee_6', 'recv_fee_7','innet_days'
                       ]].copy()
    colnames = X.columns
    Result = pd.DataFrame({'user_id':xxx['user_id']})
    ###print('typeResult',type(Result),Result.head())

    modelname = [sys.argv[1]+"LogisticRegression.model", sys.argv[1]+"Decision Tree.model", sys.argv[1]+"Random Forest.model"]
    #Result['user_id'] =xxx['user_id'].copy()
    #print('typeResult',type(Result))
    for loadmodel in modelname:
        gm_back = joblib.load(loadmodel)
        print("************load model ***********",loadmodel)
        #print("&&&&&&&&&",X.head())
        #XX = Imputer().fit_transform(X)
        #print('%%%%%%', XX[1])
        #XX=X.dropna(inplace=True)
        #array = X.values
        #XX = array[:,:]
        #print(X.head())
        XX = Imputer().fit_transform(X)
        #XX = XX.copy()
        #print('type(XX)',type(XX))
        Result['pred_'+loadmodel] = gm_back.predict(XX)
        Result['probs_'+loadmodel] = gm_back.predict_proba(XX)[:,1]

        #import bigfloat
        #bigfloat.exp(5000, bigfloat.precision(100))

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
    #print('----------------',Result.head())
    Result=Result.sort_values(by=['Score'],ascending=False)
    Result.to_csv(sys.argv[1]+"user_predict.csv")


'''

df_importance = pandas.DataFrame()
colnames = aaa.columns

for index in loaded_model.feature_importances_.argsort()[::-1][:5]:
    print(index)
    #print(aaa.columns)
    #print('********',aaa.ix[:,index].head())
    nam = colnames[index]
    df_importance[nam] = aaa.ix[:,index]

'''
# InputDataFilePath = 'inputdata.csv'
# OutputDataFilePath ='Data_new.csv'
# DataProcessing(InputDataFilePath,OutputDataFilePath)

# binputdata09_user.csv
InputDataPath = 'AllUserData201712.csv'
NewinputDataFilePath = 'Data_new.csv'
ddd = DataProcessing(InputDataPath,NewinputDataFilePath)
xx = ReadData(NewinputDataFilePath)
tt = ModelMaker(NewinputDataFilePath)
tt['Score'] = tt.ix[:,[2,4,6]].mean(1,skipna=True)*100
print(tt.head())

y_pred = [np.argmax(np.bincount(tt.ix[i, [1, 3, 5]].astype(np.int64))) for i in tt.index]

#y_prob = [np.mean(tt.ix[i, [1, 2, 3]]) for i in tt.index]
#tt['score'] = y_prob

#prob = y_prob
#pred =  y_pred
#df_importance
#result_df  = pd.DataFrame({'userid':,'prob':prob,'pred':pred})

Total_pre = pd.DataFrame({"y_test": xx[3], 'y_pred': y_pred})
classify_report = metrics.classification_report(Total_pre['y_test'], Total_pre['y_pred'])
confusion_matrix = metrics.confusion_matrix(Total_pre['y_test'], Total_pre['y_pred'])
print('confusion_matrix for ' + "Ensemble" + '\n', confusion_matrix)
print('classify_report for ' + "Ensemble" + '\n', classify_report)

load_model(NewinputDataFilePath)

