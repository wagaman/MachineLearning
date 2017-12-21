#coding:utf-8
import os
import sys
import codecs
import datetime
import pandas as pd
#from sklearn.cross_validation import train_test_split
from sklearn import metrics
from sklearn.preprocessing import Imputer
import numpy as np
from numpy import nan as NA
import math
from sklearn.externals import joblib

from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.wrappers.scikit_learn import KerasClassifier
from keras.utils import np_utils
from sklearn.model_selection import train_test_split, KFold, cross_val_score
from sklearn.preprocessing import LabelEncoder

os.getcwd()
reload(sys)
sys.setdefaultencoding( "utf-8" )

def getAllHeader(Headerpath):
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
    headers = strHeader.split(',')
    return headers

def getTargetHeader(Headerpath):
    if not os.path.exists(Headerpath):
        print "Header doesnt exist. The path is :", Headerpath
        sys.exit()

    fp = open(Headerpath, 'r')
    header = fp.readlines()[1]
    fp.close()
    if(len(header)>0):
        header = header.replace("\r","")
        header = header.replace("\n","")
        return Header2frmHead(header)
    else:
        print("Header File doesnt contain header")
        sys.exit()


def FilterData(InputDataFilePath, OutputDataFilePath, is_save, AllHeader,targetHeader):
    from sklearn.preprocessing import LabelEncoder

    print "Begin reading data from input file: "+ InputDataFilePath
    testdata = pd.read_csv(InputDataFilePath, encoding="utf-8")  # ,na_values='NaN',na_filter="NA"

    dataa = testdata[AllHeader].copy()
    data = dataa[targetHeader] # choose some certain columns

    print "Target data frame has been got"

    channel_mapping = {label: idx for idx, label in enumerate(np.unique(data['channel_id']))}
    data['channel_id'] = data['channel_id'].map(channel_mapping)

    data["constellation_desc"] = data["constellation_desc"].replace('(null)', str(13))
    data["innet_month"] = [math.floor(i.days/30) for i in
                          (datetime.datetime(2017, 8, 31) - pd.to_datetime(data["innet_date"], format='%Y%m%d'))]

    lost = []
    for i in range(len(data)):
        if data['break_5'][i] + data['break_6'][i] + data['break_7'][i] + data['break_8'][i] == 0:
            lost.append(0)
        else:
            lost.append(-2)

    paytime_cat = []
    data['avepaytimes'] = data['avepaytimes'].astype('float64')
    for i in range(len(data)):
        # print data['avepaytimes'][i]
        if data['avepaytimes'][i] > 0 and data['avepaytimes'][i] < 2:
            paytime_cat.append('0-2')
        elif data['avepaytimes'][i] >= 2 and data['avepaytimes'][i] < 4:
            paytime_cat.append('2-4')
        elif data['avepaytimes'][i] >= 4 and data['avepaytimes'][i] < 6:
            paytime_cat.append('4-6')
        elif data['avepaytimes'][i] >= 6:
            paytime_cat.append('6-')
    data['paytime_cat'] = paytime_cat

    data = data.fillna(-1);

    data["lost"] = lost
    del data['innet_date']
    data = data.drop(['lost_5','lost_6','lost_7','lost_8','break_5','break_6','break_7','break_8'],axis=1)
    data = data[data["lost"] > -2]

    print "++++Column null dealt"
    print "++++The Model data collection contains "+str(len(data))+" users"
    if is_save=='1':
        data.to_csv(OutputDataFilePath)

    return data
    #dict = ["摩羯座", "白羊座", "双鱼座", "狮子座", "双子座", "天秤座",
            #"巨蟹座", "天蝎座", "金牛座", "射手座", "水瓶座", "处女座"]
    #le = LabelEncoder()
    #le.fit(dict)
    #data["constellation_desc"] = data["constellation_desc"].fillna({0:13})
    #print data["constellation_desc"].head()
    #data["constellation_desc"] = le.transform(data["constellation_desc"])
    #print data.head()
def baseline_model():
    model = Sequential()
    model.add(Dense(output_dim=80, input_dim=37, activation='relu'))
    model.add(Dropout(0.2))
    model.add(Dense(output_dim=4, input_dim=80, activation='softmax'))
    # Compile model
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model

def MakingKerasModel_Class(dataframe):
    #dataframe = pd.read_csv("./ModelData.csv")
    X=dataframe.iloc[:,1:38]
    Y=dataframe.iloc[:,-2]

    encoder = LabelEncoder()
    encoded_Y = encoder.fit_transform(Y)
    # convert integers to dummy variables (one hot encoding)
    dummy_y = np_utils.to_categorical(encoded_Y)
    print "=================================\n"
    print dummy_y

    estimator = KerasClassifier(build_fn=baseline_model,  batch_size=256)
    # splitting data into training set and test set. If random_state is set to an integer, the split datasets are fixed.
    X_train, X_test, Y_train, Y_test = train_test_split(X, dummy_y, test_size=0.3, random_state=0)
    #print (X_train)
    result = estimator.fit(np.array(X_train), Y_train,nb_epoch=100)

    # make predictions
    pred = estimator.predict(np.array(X_test))

    # inverse numeric variables to initial categorical labels
    init_lables = encoder.inverse_transform(pred)

    # k-fold cross-validate
    seed = 42
    np.random.seed(seed)
    kfold = KFold(n_splits=10, shuffle=True, random_state=seed)
    results = cross_val_score(estimator, np.array(X), np.array(dummy_y), cv=kfold)
    return result,results


headerpath='./conf/Header.conf'
OutputDataFilePath = './ModelData.csv'
AllHeadr = Header2frmHead(getAllHeader(headerpath))
#print AllHeadr

TarHeader = getTargetHeader(headerpath)
#print TarHeader

#FilterData(InputDataFilePath, OutputDataFilePath, is_save, AllHeader,targetHeader):
datafrm=FilterData("./AllUserData201712.csv",OutputDataFilePath,'1',AllHeadr,TarHeader)
result,results = MakingKerasModel_Class(datafrm)

print "\n"
print results

print result.history

import matplotlib.pyplot as plt

plt.figure
plt.plot(result.epoch,result.history['acc'],label="acc")
#plt.plot(result.epoch,result.history['val_acc'],label="val_acc")
plt.scatter(result.epoch,result.history['acc'],marker='*')
#plt.scatter(result.epoch,result.history['val_acc'])
plt.legend(loc='under right')
plt.show()

plt.figure
plt.plot(result.epoch,result.history['loss'],label="loss")
#plt.plot(result.epoch,result.history['val_loss'],label="val_loss")
plt.scatter(result.epoch,result.history['loss'],marker='*')
#plt.scatter(result.epoch,result.history['val_loss'],marker='*')
plt.legend(loc='upper right')
plt.show()

print "========================Programme Done!"

