import pandas as pd
import numpy as np
import matplotlib.pylab as plt
from matplotlib.pylab import rcParams

rcParams['figure.figsize'] = 15, 6
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.seasonal import seasonal_decompose
from sklearn.metrics import mean_squared_error
from statsmodels.tsa.stattools import acf, pacf
from statsmodels.tsa.arima_model import ARIMA


def TimeSeriesModle():
    import pandas as pd
    EndDate = '2017-8-9'
    SaveOriginDataPath = "D:/Programma/Environmentaltest"
    DirPath = SaveOriginDataPath + '/' + 'combined_enviorenment' + '/' + EndDate

    Total_com_data_Glory = pd.read_csv(DirPath + '/' + 'Total_com_data_glory.csv', sep=",")
    print('==============读取数据成功！=====================')
    # Total_com_data_glory.csv
    # Total_com_data_Glory就是最终要使用的数据了，已经保存，后面直接读取这个文件
    # pm2.5
    InputFilePath = str(input("please enter a num:  "))
    grouped_pm = Total_com_data_Glory['pm2.5'].groupby(
        [Total_com_data_Glory['area'], Total_com_data_Glory["Timestamp"]])
    # print(grouped_pm)
    mean_pm = grouped_pm.mean()
    print('===============PM2.5在每个房间的浓度变化=========', mean_pm)

    InputFilePath = str(input("please enter a num:  "))
    print('===============PM2.5在每个房间的浓度可视化对比=========')
    # 把各个房间画折线图看出哪个房间高低,array(['A6009', 'A6016', 'A6017', 'A6027', 'B6005', 'B6008', 'B6017'], dtype=object)
    import datetime

    def datelist(start, end):
        start_date = datetime.datetime(*start)
        end_date = datetime.datetime(*end)

        result = []
        curr_date = start_date
        while curr_date != end_date:
            result.append("%04d%02d%02d%02d" % (curr_date.year, curr_date.month, curr_date.day, curr_date.hour))
            curr_date += datetime.timedelta(hours=1)
        result.append("%04d%02d%02d%02d" % (curr_date.year, curr_date.month, curr_date.day, curr_date.hour))
        return result

    # 用于生成x轴的标签
    #EndDate
    import re
    #timestamp_new_for_pic = datelist((2017, re.findall(r'-(.*?)-',EndDate), 31, 0), (2017, 8, 9, 23))
    timestamp_new_for_pic = datelist((2017,7,31,0),(2017,8,9,23))
    timestamp_new_for_pic1 = pd.to_datetime(timestamp_new_for_pic, format='%Y%m%d%H')  # 将读取的日期转为datatime格式
    people_room = pd.read_csv(SaveOriginDataPath + '/' + 'people_room.csv', sep=',', encoding='utf-8')
    room_device = pd.read_csv(SaveOriginDataPath + '/' + 'room_data.csv', sep=',', encoding='utf-8')

    #people_room = pd.read_csv("people_room.csv", sep=',', encoding='utf-8')
    #room_device = pd.read_csv("room_data.csv", sep=',', encoding='utf-8')
    #print(len(timestamp_new_for_pic1 ),len(mean_pm['A6009']))
    y_pm_A6009 = mean_pm['A6009']
    #print(y_pm_A6009)
    y_pm_A6016 = mean_pm['A6016']
    y_pm_A6017 = mean_pm['A6017']
    y_pm_A6027 = mean_pm['A6027']
    y_pm_B6005 = mean_pm['B6005']
    y_pm_B6008 = mean_pm['B6008']
    y_pm_B6017 = mean_pm['B6017']

    ##这个图加一个图标表示那条线是哪一个

    import matplotlib.pyplot as plt
    plt.figure(figsize=(20, 10))
    plt.plot(timestamp_new_for_pic1, y_pm_A6009, label="A6009")
    plt.plot(timestamp_new_for_pic1, y_pm_A6016, label="A6016")
    plt.plot(timestamp_new_for_pic1, y_pm_A6017, label="A6017")
    plt.plot(timestamp_new_for_pic1, y_pm_A6027, label="A6027")
    plt.plot(timestamp_new_for_pic1, y_pm_B6005, label="B6005")
    plt.plot(timestamp_new_for_pic1, y_pm_B6008, label="B6008")
    plt.plot(timestamp_new_for_pic1, y_pm_B6017, label="B6017")
    plt.title("compare PM2.5 in every room")
    plt.legend(loc="best")
    plt.show()

    InputFilePath = str(input("please enter a num:  "))
    print('===============PM2.5在每个房间的浓度可视化=========')

    rooms = ['A6009', 'A6016', 'A6017', 'A6027', 'B6005', 'B6008', 'B6017']
    for room in rooms:
        plt.figure(figsize=(20, 10))
        # da = data_new[data_new['DeviceSN']!=fild]
        y_pm_room = mean_pm[room]
        # da = data_new[data_new['DeviceSN']==device]
        # dat = da[['Timestamp','pm2.5']]
        plt.plot(timestamp_new_for_pic1, y_pm_room, label=room)
        plt.legend(loc=2, shadow=True, fontsize=25)
        plt.show()

    plt.figure(figsize=(20, 10))
    plt.plot(timestamp_new_for_pic1, y_pm_A6009, label="A6009", linewidth=3)

    alpha = 0.2
    #p = plt.axvspan(timestamp_new_for_pic1[24 * 2], timestamp_new_for_pic1[24 * 4], facecolor='g', alpha=alpha)
    #p = plt.axvspan(timestamp_new_for_pic1[24 * 4], timestamp_new_for_pic1[24 * 9], facecolor='r', alpha=alpha)
    #p = plt.axvspan(timestamp_new_for_pic1[24 * 9], timestamp_new_for_pic1[24 * 11], facecolor='g', alpha=alpha)
    #p = plt.axvspan(timestamp_new_for_pic1[24 * 11], timestamp_new_for_pic1[24 * 16], facecolor='r', alpha=alpha)
    #p = plt.axvspan(timestamp_new_for_pic1[24 * 16], timestamp_new_for_pic1[24 * 18], facecolor='g', alpha=alpha)
    #p = plt.axvspan(timestamp_new_for_pic1[24 * 18], timestamp_new_for_pic1[24 * 23], facecolor='r', alpha=alpha)
    #p = plt.axvspan(timestamp_new_for_pic1[24 * 23], timestamp_new_for_pic1[24 * 25], facecolor='g', alpha=alpha)
    #p = plt.axvspan(timestamp_new_for_pic1[24 * 25], timestamp_new_for_pic1[24 * 30], facecolor='r', alpha=alpha)
    #p = plt.axvspan(timestamp_new_for_pic1[24 * 30], timestamp_new_for_pic1[24 * 32], facecolor='g', alpha=alpha)
    #p = plt.axvspan(timestamp_new_for_pic1[24 * 32], timestamp_new_for_pic1[24 * 37], facecolor='r', alpha=alpha)
    #p = plt.axvspan(timestamp_new_for_pic1[24 * 37], timestamp_new_for_pic1[24 * 39], facecolor='g', alpha=alpha)
    #p = plt.axvspan(timestamp_new_for_pic1[24 * 39], timestamp_new_for_pic1[24 * 44], facecolor='r', alpha=alpha)
    #p = plt.axvspan(timestamp_new_for_pic1[24 * 44], timestamp_new_for_pic1[24 * 46], facecolor='g', alpha=alpha)
    #p = plt.axvspan(timestamp_new_for_pic1[24 * 46], timestamp_new_for_pic1[24 * 51], facecolor='r', alpha=alpha)
    #p = plt.axvspan(timestamp_new_for_pic1[24 * 51], timestamp_new_for_pic1[24 * 53], facecolor='g', alpha=alpha)
    #p = plt.axvspan(timestamp_new_for_pic1[24 * 53], timestamp_new_for_pic1[24 * 58], facecolor='r', alpha=alpha)
    #p = plt.axvspan(timestamp_new_for_pic1[24 * 58], timestamp_new_for_pic1[24 * 59], facecolor='g', alpha=alpha)
    #p = plt.axvspan(timestamp_new_for_pic1[0], timestamp_new_for_pic1[24 * 2], facecolor='r', alpha=alpha)
    #plt.legend(loc=2, shadow=True, fontsize=40)
    #plt.show()

    InputFilePath = str(input("please enter a num:  "))
    print('===============PM2.5在每个房间的基本统计信息可视化=========')
    rooms = ['A6009', 'A6016', 'A6017', 'A6027', 'B6005', 'B6008', 'B6017']
    room_pm_mean = []
    room_pm_max = []
    room_pm_min = []
    room_pm_var = []
    room_pm_med = []
    import numpy as np
    for room in rooms:
        # plt.figure(figsize=(20,10))
        # da = data_new[data_new['DeviceSN']!=fild]
        room_pm_mean.append(np.mean(mean_pm[room]))
        room_pm_max.append(np.max(mean_pm[room]))
        room_pm_min.append(np.min(mean_pm[room]))
        room_pm_var.append(np.var(mean_pm[room]))
        room_pm_med.append(np.median(mean_pm[room]))

    df = pd.DataFrame({'group_labels': ['A6009', 'A6016', 'A6017', 'A6027', 'B6005', 'B6008', 'B6017'],
                       'room_pm_mean': room_pm_mean,
                       'room_pm_min': room_pm_min,
                       'room_pm_max': room_pm_max,
                       'room_pm_var': room_pm_var,
                       'room_pm_med': room_pm_med})

    df = df.sort("room_pm_mean")
    df

    print('===============PM2.5在每个房间的均值可视化=========')
    # mean：
    from matplotlib import pyplot as plt
    from numpy import sin, exp, absolute, pi, arange
    from numpy.random import normal

    # df
    t = arange(0.0, 7.0)
    s = df["room_pm_mean"]
    fig = plt.figure(figsize=(12, 6))
    hax = fig.add_subplot(111)

    group_labels = df["group_labels"]
    hax.plot(s, t, 'b^')
    hax.hlines(t, [0], s, lw=2)
    hax.set_xlabel('mean pm2.5 in room')
    hax.set_ylabel('Room')
    hax.set_title('Average pm2.5 in every room')
    plt.yticks(t, group_labels, rotation=0)
    plt.show()

    InputFilePath = str(input("please enter a num:  "))
    print('===============PM2.5在每个房间的最大浓度可视化=========')
    # max：
    from matplotlib import pyplot as plt
    from numpy import sin, exp, absolute, pi, arange
    from numpy.random import normal

    # df
    t = arange(0.0, 7.0)
    s = df["room_pm_max"]

    fig = plt.figure(figsize=(12, 6))
    hax = fig.add_subplot(111)

    group_labels = df["group_labels"]

    # hax.plot(s + nse, t, 'b^')
    hax.plot(s, t, 'b^')
    hax.hlines(t, [0], s, lw=2)
    hax.set_xlabel('max pm2.5 in room')
    hax.set_ylabel('Room')
    hax.set_title('Max pm2.5 in every room')
    plt.yticks(t, group_labels, rotation=0)
    plt.show()

    InputFilePath = str(input("please enter a num:  "))
    print('===============PM2.5在每个房间的变动情况可视化=========')
    # var：
    from matplotlib import pyplot as plt
    from numpy import sin, exp, absolute, pi, arange
    from numpy.random import normal

    # df
    t = arange(0.0, 7.0)

    # t =['a', 'b','c','d','e','f','g']
    s = df["room_pm_var"]
    # nse = normal(0.0, 0.3, t.shape) * s


    fig = plt.figure(figsize=(12, 6))
    hax = fig.add_subplot(111)

    group_labels = df["group_labels"]

    # hax.plot(s + nse, t, 'b^')
    hax.plot(s, t, 'b^')
    hax.hlines(t, [0], s, lw=2)
    hax.set_xlabel('var pm2.5 in room')
    hax.set_ylabel('Room')
    hax.set_title('Var pm2.5 in every room')
    plt.yticks(t, group_labels, rotation=0)
    plt.show()

    InputFilePath = str(input("please enter a num:  "))
    print('===============甲醛在每个房间的基本统计信息=========')
    #people_room = pd.read_csv("people_room.csv", sep=',', encoding='utf-8')
    #room_device = pd.read_csv("room_data.csv", sep=',', encoding='utf-8')
    # ch2o
    # Total_com_data_glory
    grouped_ch2o = Total_com_data_Glory['ch2o'].groupby(
        [Total_com_data_Glory['DeviceSN'], Total_com_data_Glory["Timestamp"]])
    # print(grouped_ch2o)
    mean_chh2o = grouped_ch2o.mean()

    InputFilePath = str(input("please enter a num:  "))
    print('===============下面对pm2.5进行时间序列建模=========')
    print('===============选取房间为 A6009=========')
    # 以某一个房间为基础做时间序列
    # 时间序列建模
    import pandas as pd
    import numpy as np
    import matplotlib.pylab as plt
    from matplotlib.pylab import rcParams

    rcParams['figure.figsize'] = 15, 6
    from statsmodels.tsa.stattools import adfuller
    from statsmodels.tsa.seasonal import seasonal_decompose
    from sklearn.metrics import mean_squared_error
    from statsmodels.tsa.stattools import acf, pacf
    from statsmodels.tsa.arima_model import ARIMA

    def test_stationarity(timeseries):
        # 决定起伏统计
        rolmean = pd.rolling_mean(timeseries, window=64)  # 平均数
        rolstd = pd.rolling_std(timeseries, window=64)  # 偏离原始值多少
        # 画出起伏统计
        orig = timeseries.plot(color='blue', label='Original')
        mean = rolmean.plot(color='red', label='Rolling Mean')
        std = rolstd.plot(color='black', label='Rolling Std')
        plt.legend(loc='best')
        plt.title('Rolling Mean & Standard Deviation')
        plt.show(block=False)
        # 进行df测试
        print('Result of Dickry-Fuller test')
        dftest = adfuller(timeseries, autolag='AIC')
        dfoutput = pd.Series(dftest[0:4],
                             index=['Test Statistic', 'p-value', '#Lags Used', 'Number of observations Used'])
        for key, value in dftest[4].items():
            dfoutput['Critical value(%s)' % key] = value
        print(dfoutput)

    InputFilePath = str(input("please enter a num:  "))
    print('===============选取房间为 A6009=========')
    print('===============A6009 pm 2.5可视化=========')
    # timestamp_new_for_pic1
    data = pd.DataFrame({'pm2.5': mean_pm["A6009"]}, index=timestamp_new_for_pic1)

    ts = data['pm2.5']

    ts.plot()
    plt.show()

    test_stationarity(ts)
    plt.show()

    ##estimating##
    ts_log = np.log(ts)
    ts_log.plot()
    plt.show()

    moving_avg = pd.rolling_mean(ts_log, 64)
    moving_avg.plot()
    moving_avg.plot(color='red')
    plt.show()

    ts_log_moving_avg_diff = ts_log - moving_avg
    print(ts_log_moving_avg_diff.head(1352))
    ts_log_moving_avg_diff.dropna(inplace=True)
    test_stationarity(ts_log_moving_avg_diff)
    plt.show()

    ##diffrencing##
    ts_log_diff = ts_log - ts_log.shift()
    plt.plot(ts_log_diff)
    plt.show()

    ts_log_diff.dropna(inplace=True)
    test_stationarity(ts_log_diff)
    plt.show()

    Input = input("please enter a num: ")
    print("===========时间序列建模预测==========")

    ##预测##
    Input = input("please enter a num: ")
    print("===========时间序列建模:ACF PACF ==========")
    # 确定参数
    lag_acf = acf(ts_log_diff, nlags=20)
    lag_pacf = pacf(ts_log_diff, nlags=20, method='ols')
    # q的获取:ACF图中曲线第一次穿过上置信区间.这里q取2
    plt.subplot(121)
    plt.plot(lag_acf)
    plt.axhline(y=0, linestyle='--', color='gray')
    plt.axhline(y=-1.96 / np.sqrt(len(ts_log_diff)), linestyle='--', color='gray')  # lowwer置信区间
    plt.axhline(y=1.96 / np.sqrt(len(ts_log_diff)), linestyle='--', color='gray')  # upper置信区间
    plt.title('Autocorrelation Function')
    # p的获取:PACF图中曲线第一次穿过上置信区间.这里p取2
    plt.subplot(122)
    plt.plot(lag_pacf)
    plt.axhline(y=0, linestyle='--', color='gray')
    plt.axhline(y=-1.96 / np.sqrt(len(ts_log_diff)), linestyle='--', color='lightgreen')
    plt.axhline(y=1.96 / np.sqrt(len(ts_log_diff)), linestyle='--', color='gray')
    plt.title('Partial Autocorrelation Function')
    plt.tight_layout()
    plt.show()
    import zipfile
    import os
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    from datetime import datetime
    import math

    Input = input("please enter a num: ")
    print("===========时间序列建模:AR==========")

    # AR model
    model = ARIMA(ts_log, order=(2, 1, 0))
    result_AR = model.fit(disp=-1)
    plt.plot(ts_log_diff)
    plt.plot(result_AR.fittedvalues, color='blue')
    plt.title('RSS:%.4f' % sum(result_AR.fittedvalues - ts_log_diff) ** 2)
    plt.show()

    Input = input("please enter a num: ")
    print("===========时间序列建模:MA==========")

    # MA model
    model = ARIMA(ts_log, order=(0, 1, 2))
    result_MA = model.fit(disp=-1)
    plt.plot(ts_log_diff)
    plt.plot(result_MA.fittedvalues, color='blue')
    plt.title('RSS:%.4f' % sum(result_MA.fittedvalues - ts_log_diff) ** 2)
    plt.show()

    import itertools

    # Define the p, d and q parameters to take any value between 0 and 2
    p = d = q = range(0, 3)

    # Generate all different combinations of p, q and q triplets
    pdq = list(itertools.product(p, d, q))
    print('p,d,q', pdq, '\n')

    for param in pdq:
        print(param)

    Input = input("please enter a num: ")
    print("===========时间序列建模:ARIMA==========")
    # ARIMA 将两个结合起来  效果更好
    # warnings.filterwarnings("ignore") # specify to ignore warning messages

    for param in pdq:
        try:
            model = ARIMA(ts_log, order=param)
            # model=ARIMA(ts_log,order=(2,1,2))
            result_ARIMA = model.fit(disp=-1)
            print('ARIMA{}- AIC:{} - BIC:{} - HQIC:{}'.format(param, result_ARIMA.aic, result_ARIMA.bic,
                                                              result_ARIMA.hqic))
        except:
            continue

    Input = input("please enter a num: ")
    print("===========最后时间序列参数建模:ARIMA==========")
    # model=ARIMA(ts_log,order=(2,1,2))
    model = ARIMA(ts_log, order=(2, 1, 0))
    result_ARIMA = model.fit(disp=-1)
    plt.plot(ts_log_diff)
    plt.plot(result_ARIMA.fittedvalues, color='blue')
    plt.title('RSS:%.4f' % sum(result_ARIMA.fittedvalues - ts_log_diff) ** 2)
    plt.show()

    Input = input("please enter a num: ")
    print("===========最后时间序列参数建模:ARIMA==========")

    # print(result_ARIMA.summary().tables[1])
    print(result_ARIMA.summary())
    # plot residual errors
    residuals = pd.DataFrame(result_ARIMA.resid)
    residuals.plot(kind='kde')
    plt.show()
    print(residuals.describe())
    # print(results.summary().tables[1])



    #4
    import zipfile
    import os
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    from datetime import datetime
    import math

    import statsmodels.api as sm
    print(sm.stats.durbin_watson(result_ARIMA.resid.values))
    # 2附近即不存在一阶自相关


    from statsmodels.graphics.api import qqplot
    resid1 = result_ARIMA.resid  # 残差
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111)
    fig = qqplot(resid1, line='q', ax=ax, fit=True)
    plt.show()

    # Ljung-Box test是对randomness的检验,或者说是对时间序列是否存在滞后相关的一种统计检验
    resid1  # = arma_mod20.resid#残差
    r, q, p = sm.tsa.acf(resid1.values.squeeze(), qstat=True)
    data = np.c_[range(1, 41), r[1:], q, p]
    table = pd.DataFrame(data, columns=['lag', "AC", "Q", "Prob(>Q)"])
    print(table.set_index('lag'))
    # 如果取显著性水平为0.05，那么相关系数与零没有显著差异，即为白噪声序列,此处为白噪声序列



    # result_ARIMA.plot_diagnostics(figsize=(15, 12))
    ##log的
    result_ARIMA.plot_predict()
    # residuals.plot_diagnostics(figsize=(15, 12))
    plt.show()

    predictions_ARIMA_diff = pd.Series(result_ARIMA.fittedvalues, copy=True)
    # print predictions_ARIMA_diff.head()#发现数据是没有第一行的,因为有1的延迟
    predictions_ARIMA_diff_cumsum = predictions_ARIMA_diff.cumsum()
    # print predictions_ARIMA_diff_cumsum.head()


    predictions_ARIMA_log = pd.Series(ts_log.ix[0], index=ts_log.index)
    predictions_ARIMA_log = predictions_ARIMA_log.add(predictions_ARIMA_diff_cumsum, fill_value=0)
    # print predictions_ARIMA_log.head()




    predictions_ARIMA = np.exp(predictions_ARIMA_log)
    plt.plot(ts)
    plt.plot(predictions_ARIMA, color='red')
    plt.title('RMSE: %.4f' % np.sqrt(sum((predictions_ARIMA - ts) ** 2) / len(ts)))
    plt.show()

    predictions_ARIMA = np.exp(predictions_ARIMA_log)
    # plt.plot(ts)
    plt.plot(predictions_ARIMA, color='red')
    plt.title('RMSE: %.4f' % np.sqrt(sum((predictions_ARIMA - ts) ** 2) / len(ts)))
    plt.show()

    predictions_ARIMA = np.exp(predictions_ARIMA_log)
    plt.plot(ts)
    # plt.plot(predictions_ARIMA,color='red')
    plt.title('RMSE: %.4f' % np.sqrt(sum((predictions_ARIMA - ts) ** 2) / len(ts)))
    plt.show()

    size = int(len(ts_log) - 15)
    train, test = ts_log[0:size], ts_log[size:len(ts_log)]
    history = [x for x in train]
    predictions = list()

    #5
    import zipfile
    import os
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    from datetime import datetime
    import math

    print('Printing Predicted vs Expected Values...')
    print('\n')
    for t in range(len(test)):
        model = ARIMA(history, order=(2, 1, 0))
        model_fit = model.fit(disp=0)
        output = model_fit.forecast()
        yhat = output[0]
        predictions.append(float(yhat))
        obs = test[t]
        history.append(obs)
        print('predicted=%f, expected=%f' % (np.exp(yhat), np.exp(obs)))

    error = mean_squared_error(test, predictions)

    print('\n')
    print('Printing Mean Squared Error of Predictions...')
    print('Test MSE: %.6f' % error)

    predictions_series = pd.Series(predictions, index=test.index)

    test
    ####下面可以拿掉###########
    # 一部分放大
    fig, ax = plt.subplots()
    ax.set(title='ch2o prediction', xlabel='Date', ylabel='ch2o')
    ##ax.plot(ts[-100:], 'o', label='observed')
    ax.plot(ts[-100:], label='observed')
    ax.plot(np.exp(predictions_series), 'red', label=' forecast')
    legend = ax.legend(loc='upper left')
    legend.get_frame().set_facecolor('w')
    plt.show()

    
    predict_sunspots = result_ARIMA.predict('2017-09-18 00:00:00', '2017-09-19 00:00:00 ', dynamic=True)
    # 2017-08-06 23:58:19   -3.952845
    # 2017-08-06 23:59:22   -3.952845
    print(predict_sunspots)
    fig, ax = plt.subplots(figsize=(12, 8))
    # ax = t.ix['2001':].plot(ax=ax)
    # predict_sunspots.plot(ax=ax)
    predict_sunspots.plot()
    plt.show()


TimeSeriesModle()