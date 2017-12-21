import codecs

__author__ = 'sss'

'''
理论：
    http://www.cnblogs.com/luchen927/archive/2012/02/01/2325360.html
输入的数据：
    数据id，用户id, 付费标签类型，信用等级，流量（通过length(num)等级处理），基站，品牌，时间戳

    计算每条数据的相似度，根据用户id获取该条数据下一次购买什么品牌的手机


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


def get_brand_2(item_list, data_dict, cur_brand=None):
    brands = {}
    for item in item_list:
        brand = data_dict[item[0]][10]
        brands[brand] = brands.get(brand, 0) + 1
        if brand == cur_brand:
            brands[brand] = brands.get(brand, 0) + 1

    brand_list = sorted(brands.items(), key=lambda item: item[1], reverse=True)
    brand_list = list(filter(lambda item: item[0] != 0, brand_list))

    if len(brand_list) > 1:
        return brand_list[0][0], brand_list[1][0]
    else:
        return brand_list[0][0]


def get_brand(item_list, data_dict, cur_brand=None):
    return get_brand_2(item_list, data_dict, cur_brand=None)[0]


if __name__ == '__main__':
    filePath = "D:\workspaceHuayu\helloPython\hellopython\weka\chinaunicom_test4\\user_brand.txt"
    dataMat = loadDataSet(filePath)

    #把数据放到dict里
    data_dict = {}
    for data in dataMat:
        data_dict[data[0]] = data

    #计算用户之间的距离
    distance_dict = {}
    for data in dataMat:
        dis = get_distance(data, None)
        try:
            distance_dict[data[0]] = float(dis)
        except:
            print(1)

    #根据距离最近的一些用户，下一个选择的品牌，推荐类似的品牌
    score_list = sorted(distance_dict.items(), key=lambda item: item[1], reverse=True)
    total = 0
    right = 0
    for index, item in enumerate(score_list):

        data = data_dict[item[0]]
        cur_brand = data[9]
        next_brand = data[10]

        if index < 11:
            brand = get_brand(score_list[index:index + 20], data_dict, next_brand=next_brand)
        elif 11 < index < len(score_list) - 11:
            brand = get_brand(score_list[index - 10: index + 10], data_dict, next_brand=next_brand)
        elif index > len(score_list) - 11:
            brand = get_brand(score_list[index - 20: index], data_dict, next_brand=next_brand)

        if next_brand != 0:
            total += 1
            if next_brand in brand:
                right += 1

    print(right, total, float(right / total))



