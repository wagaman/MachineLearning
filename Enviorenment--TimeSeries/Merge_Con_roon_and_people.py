import pandas as pd
import numpy as np
import os
import math
from datetime import datetime
print(os.getcwd())

def JoinRoom():
    EndDate = '2017-8-9'
    # 读取数据
    SaveOriginDataPath = "D:/Programma/Environmentaltest"
    DirPath = SaveOriginDataPath + '/' + 'combined_enviorenment' + '/' + EndDate
    #os.chdir(DirPath)
    comdata = pd.read_csv(DirPath+'/'+ 'com_env'+EndDate+'.csv', sep=',', na_values='(null)',
                          na_filter="NA", skiprows=5, encoding='utf-8')

    # 去掉ID列的汇总数据，并且将时间戳放到前面几列方便查看
    print(comdata.head())
    data_origin = comdata[
        ['DeviceSN', 'Timestamp', 'tem', 'hum', 'noise', 'pm2.5', 'ch2o', 'VOC', 'pm1', 'pm10', 'co2',
         'AQI']]
    print(data_origin.head())

    #data_origin = data[['DeviceSN', 'Timestamp', 'tem', 'hum', 'noise', 'pm2.5',
     #                   'ch2o', 'VOC', 'pm1', 'pm10', 'co2',  'AQI']]
    #print(data_origin.head())


    # 提取年月日以及小时，用于按照小时合并数据（因分钟收集数据没有规律）
    tt = pd.to_datetime(data_origin["Timestamp"], format='%Y-%m-%d %H:%M:%S')  # 将读取的日期转为datatime格式
    Year = [i.year for i in tt]
    Month = [i.month for i in tt]
    Day = [i.day for i in tt]
    Hour = [i.hour for i in tt]  # 遍历时间变量

    xy = zip(Year, Month, Day, Hour)
    List_xy = list(xy)

    # 正确
    Timestamp_new = []
    for i in range(0, len(List_xy)):
        time = List_xy[i]
        if math.isnan(time[0]):
            List_xy[i] = List_xy[i - 1]
            time = List_xy[i]
        stamp = datetime(int(time[0]), int(time[1]), int(time[2]), int(time[3]))
        Timestamp_new.append(stamp.strftime('%Y-%m-%d %H'))

    print(len(data_origin["Timestamp"]) == len(Timestamp_new))

    data_origin["Timestamp"] = Timestamp_new

    #data_origin.to_csv("data_origin.csv")


    # 读取刚刚保存过的数据
    #data_origin = pd.read_csv("data_origin.csv", sep=',', encoding='utf-8')

    data_origin_end = data_origin[['DeviceSN', 'Timestamp', 'tem', 'hum',
                                   'noise', 'pm2.5', 'ch2o']]
    print(data_origin_end.head())
    del (comdata)
    del (data_origin)
    del (tt)
    del (List_xy)
    del (Hour)
    del (Day)
    del (Month)
    del (Year)
    #D:\Programma\Environmentaltest
    people_room = pd.read_csv(SaveOriginDataPath+'/'+'people_room.csv', sep=',', encoding='utf-8')
    room_device = pd.read_csv(SaveOriginDataPath+'/'+'room_data.csv', sep=',', encoding='utf-8')
    room_device_end = room_device[["Device_SN ", "area"]]

    tt = room_device_end.merge(people_room, left_on='area', right_on='room_num', how='right')  # 右连接
    print(tt.head())
    Needed_to_rule = tt[:31]

    Total_com_data_temp = data_origin_end.merge(Needed_to_rule, left_on='DeviceSN', right_on='Device_SN ',
                                                how='inner')  # 内连接，取交集

    Total_com_data = Total_com_data_temp[['DeviceSN', 'area', 'Timestamp', 'tem', 'hum', 'noise', 'pm2.5', 'ch2o']]

    # 找出所有有设备的房间，再找出有办公区域的房间，这个和people关联
    np.unique(Total_com_data["area"])
    import os
    os.getcwd()
    Total_com_data.to_csv(DirPath+'/'+'Total_com_data_glory.csv')

#JoinRoom()