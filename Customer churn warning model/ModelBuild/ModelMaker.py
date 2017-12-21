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


def ModelMaker(NewinputDataFilePath):
    from sklearn.linear_model import LogisticRegression
    from sklearn.ensemble import RandomForestClassifier
    from sklearn import tree
    #xx = ReadData(InputDataPath)

    X_train = xx[0]
    X_test = xx[1]
    y_train = xx[2]
    y_test = xx[3]

    # print "============"
    # print y_test

    names = ["LogisticRegression", "Decision Tree", "Random Forest"]
    models = [LogisticRegression(penalty='l2'), tree.DecisionTreeClassifier(),
              RandomForestClassifier(random_state=500)]
   
    tt = pd.DataFrame({"y_test": y_test})
    for model, name  in zip(models, names):

        X_train = Imputer().fit_transform(X_train)
        X_test = Imputer().fit_transform(X_test)
        # print "1========",len(y_train)
        # y_train=y_train.dropna(axis=0,how='all')
        # print "2========", len(y_train)
        # model.fit(X_train, y_train)
 
        model.fit(X_train, y_train)
        ###print(name, gm.best_params_)

    
        filename = sys.argv[1]+name+'.model'
        joblib.dump(model, filename)
        # print(gm)
        # gm.fit(X_train, y_train)


        ###此处读入新的要预测的xtest
        y_prob1 = model.predict_proba(X_test)[:,1]

        #y_prob0 = model.predict_proba(X_test)[:, 0]
        y_pred = model.predict(X_test)
        # print(y_pred)
        y_test = [int(str(i)[0:1]) for i in y_test]

        classify_report = metrics.classification_report(y_test, y_pred)

        confusion_matrix = metrics.confusion_matrix(y_test, y_pred)
        print('confusion_matrix for ' + name + '\n', confusion_matrix)
        print('classify_report for ' + name + '\n', classify_report)

        tt['y_pred_' + name] = y_pred
        #print(tt.head())
        tt['y_prob_'+ name] = y_prob1
        #print(tt.head(100))

    ###df_importance = pd.DataFrame()
    ###for index in gm.feature_importances_.argsort()[::-1][:5]:
        ###df_importance['Tree' + index] = X_test[index]
    ###print('------------------',df_importance.head())
    return tt
    # pd.DataFrame(y_test,y_pred)


