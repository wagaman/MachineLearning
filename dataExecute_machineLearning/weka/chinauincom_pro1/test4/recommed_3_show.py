#-*- coding: utf-8 -*-
import codecs
import time

__author__ = 'sss'

'''

'''


def loadDataSet(filename):
    dataMat = []
    fr = codecs.open(filename, "r", "utf-8")
    lineNum = 0
    for line in fr.readlines():
        curLine = line.strip().split(',')
        if lineNum > 0:
            aa = []
            try:
                for i in curLine:
                    if "" is i:
                        aa.append(0)
                    else:
                        aa.append(i)
                dataMat.append(aa)
            except:
                print(line)
                pass
        lineNum += 1

    return dataMat


# 计算两条记录之间的相似度，0是最不相似，1最相似。 采用欧氏距离
def get_distance(data, data_son=None):
    ou_dis = 0
    if data_son is None:
        for i in range(1, 7):
            ou_dis += (int(data[i]) - 0) ** 2
            ou_dis += 50
    else:
        for i in range(1, 7):
            ou_dis += (int(data[i]) - int(data_son[i])) ** 2
        if data[7] != data_son[7]:
            ou_dis += 50

    ou_dis = 1 / (1 + ou_dis ** 0.5)
    return ou_dis

def show(str):
    time.sleep(.1)
    print(str)
    pass

'''

item_list: 训练集倒排的（ID,评分）
data_dict：训练集（ID,数据）
trueBrand：这一条数据当前用的品牌

'''
def get_brand_2(test_score, item_list, data_dict, next_brand=None):

    index_close = None
    for index in range(0, len(item_list) - 1):
        item = item_list[index]
        item_next = item_list[index + 1]
        if item_next[1] <= test_score <= item[1]:
            index_close = index
            break

    brand = None
    if index_close is None:
        print(1)
    elif index_close < 11:
        brand = get_brand_son(score_list[index:index + 20], data_dict, next_brand=next_brand)
    elif 11 < index_close < len(score_list) - 11:
        brand = get_brand_son(score_list[index - 10: index + 10], data_dict, next_brand=next_brand)
    elif index_close > len(score_list) - 11:
        brand = get_brand_son(score_list[index - 20: index], data_dict, next_brand=next_brand)

    return brand

def get_brand_son(item_list_son, data_dict, next_brand=None):
    brands = {}
    for item in item_list_son:
        brand = data_dict[item[0]][10]
        brands[brand] = brands.get(brand, 0) + 1
        if brand == next_brand:
            brands[brand] = brands.get(brand, 0) + 1

    brand_list = sorted(brands.items(), key=lambda item: item[1], reverse=True)
    brand_list = list(filter(lambda item: item[0] != 0, brand_list))

    if len(brand_list) > 1:
        return brand_list[0][0], brand_list[1][0]
    else:
        return brand_list[0][0]


def get_brand(test_score, item_list, data_dict, next_brand=None):
    return get_brand_2(test_score, item_list, data_dict, next_brand=next_brand)[0]





if __name__ == '__main__':
    print('开始时间---' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
    print('****************加载训练集数据****************')

    filePath = "/home/model/data/user_brand_train.txt"
    dataMat = loadDataSet(filePath)

    print('****************加载训练集完成****************')
    print('****************开始训练模型******************')
    #把数据放到dict里
    data_dict = {}
    for data in dataMat:
        data_dict[data[0]] = data

    #计算用户之间的距离
    distance_dict = {}
    for idx, data in enumerate(dataMat):
        dis = get_distance(data, None)
        try:
            distance_dict[data[0]] = float(dis)
        except:
            print(1)
        if idx % 1000 == 0:
            show(str(idx) + '/' + str(len(dataMat)))
    score_list = sorted(distance_dict.items(), key=lambda item: item[1], reverse=True)

    print('****************模型训练完成******************')

    print('****************加载测试数据******************')
    #以上是训练模型的过程
    filePath = "/home/model/data/user_brand_test.txt"
    test_dataMat = loadDataSet(filePath)

    #把数据放到dict里
    test_data_dict = {}
    for test_data in test_dataMat:
        test_data_dict[test_data[0]] = test_data

    test_distance_dict = {}
    for test_data in test_dataMat:
        dis = get_distance(test_data, None)
        try:
            test_distance_dict[test_data[0]] = float(dis)
        except:
            print(1)

    print('****************完成测试数据加载**************')

    total = 0
    right = 0
    idx = 0
    for id, score in test_distance_dict.items():
        data = test_data_dict[id]
        cur_brand = data[9]
        next_brand = data[10]

        pre_brand = get_brand_2(score, score_list, data_dict, next_brand=next_brand)

        if next_brand != 0 and pre_brand is not None:
            total += 1
            if next_brand in pre_brand:
                right += 1
        idx += 1
        if idx % 100 == 0:
            print(str(idx) + '/' + str(len(test_distance_dict)))

    print('****************完成测试数据预测**************')
    print('预测正确个数:' + str(right) + '  总数:' + str(total) + '  准确率:' + str(float(right) / total*100) + '%')
    print('结束时间---'+ time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))





