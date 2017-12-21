import codecs

__author__ = 'sss'


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

def get_changeDict(dataMat):

    #拿到用户的更换手机信息
    total_changes = []
    for data in dataMat:
        phones = data[1].split('|')
        changes = {}
        for phone in phones:
            changes[phone.split('_')[1]] = phone.split('_')[0]
        sorted_keys = sorted(changes)

        new_changes = []
        for sk in sorted_keys:
            new_changes.append(changes.get(sk))

        for i in range(0, len(new_changes) - 1):
            total_changes.append(new_changes[i] + ',' + new_changes[i + 1])

    #统计更换手机的信息
    change_dicts = {}
    for item in total_changes:
        pre = item.split(',')[0]
        ne = item.split(',')[1]
        subdict = change_dicts.get(pre, {})

        subdict[ne] = subdict.get(ne, 0) + 1
        change_dicts[pre] = subdict

    return change_dicts

def get_recommend_brand(input_brand, change_dicts):
    dict = change_dicts.get(input_brand, change_dicts.get('小品牌'))
    dict_list = sorted(dict.items(), key=lambda item: item[1], reverse=True)
    total = 0
    for data in dict_list:
        total += data[1]

    turn = input_brand + ' 品牌手机。更换的手机品牌前三占比：' + '\n'
    for i in range(0, 10):
        turn += dict_list[i][0] + ':' + str(round(dict_list[i][1]/total, 2)) + '\n'

    for i in range(0, 10):
        print('\'' + dict_list[i][0] + '\',', end='')
    print()
    for i in range(0, 10):
        print('' + str(round(dict_list[i][1]/total*100, 2)) + ',', end='')

    return turn


if __name__ == '__main__':
    filePath = "D:\workspaceHuayu\helloPython\hellopython\weka\chinaunicom_test3\\recommend.txt"
    dataMat = loadDataSet(filePath)
    change_dicts = get_changeDict(dataMat)
    print(get_recommend_brand('小品牌', change_dicts))
    #print(get_recommend_brand('三星', change_dicts))
    #print(get_recommend_brand('诺基亚', change_dicts))
    #print(get_recommend_brand('中兴', change_dicts))
    #print(get_recommend_brand('宇龙计算机通信科技（深圳）有限公司-酷派', change_dicts))

    #print(get_recommend_brand('北京天语', change_dicts))
    #print(get_recommend_brand('四川长虹', change_dicts))
    #print(get_recommend_brand('小米', change_dicts))
    #print(get_recommend_brand('联想', change_dicts))
    print(get_recommend_brand('苹果', change_dicts))

    print(1)

