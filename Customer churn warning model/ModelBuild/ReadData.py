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


def ReadData(NewinputDataFilePath):
    data = pd.read_csv(sys.argv[1]+NewinputDataFilePath, encoding="utf-8")

    X = data[['brand_id', 'cust_sex', 'constellation_desc',
                      'cert_age', 'credit_class',
                      'lost_5', 'lost_6',  'break_5', 'break_6',
                       'fee_5', 'fee_6', 'fee_7',
                      'flux_5', 'flux_6', 'flux_7',  '3wu_5',
                      '3wu_6', '3wu_7',  'roaming_days_7', 'call_times_7',
                      'originate_times_7', 'destination_phone_numbers_7', 'no_phone_days_7',
                      'using_days_7', 'yue_5', 'yue_6', 'yue_7', 'recv_fee_5',
                      'recv_fee_6', 'recv_fee_7','innet_days'
                       ]]
    y = data['lost']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.4)
    return X_train, X_test, y_train, y_test


