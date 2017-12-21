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
    dataMat=[]
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

#计算两条记录之间的相似度，0是最不相似，1最相似。 采用欧氏距离
def get_distance(data, data_son):
    ou_dis = 0
    for i in range(1, 7):
        ou_dis += int(data[i])**2 - int(data_son[i])**2
    if data[7] != data_son[7]:
        ou_dis += 100

    ou_dis = 1 / (1 + ou_dis**0.5)
    return ou_dis

if __name__ == '__main__':
    filePath = "D:\workspaceHuayu\helloPython\hellopython\weka\chinaunicom_test4\\user_brand_train.txt"
    dataMat = loadDataSet(filePath)

    #计算用户之间的距离。 10000用户，计算10000*10000次，运行太慢了
    distance_dict = {}
    for data in dataMat:
        user_dict = {}
        for data_son in dataMat:
            dis = get_distance(data, data_son)
            user_dict[data_son[0]] = dis
        distance_dict[data[0]] = user_dict

    #根据距离最近的一些用户，下一个选择的品牌，推荐类似的品牌
    for key, value in distance_dict.items():
        score_list = sorted(value.items(), key=lambda item: item[1], reverse=True)
        score_list[0:20]

