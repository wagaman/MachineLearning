# combine的简单总版本（跑通）
# D:\Programma\Environmental
import os
import re

def mkdir(path):
    # 引入模块
    import os

    # 去除首位空格
    path = path.strip()
    # 去除尾部 \ 符号
    path = path.rstrip("\\")

    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    isExists = os.path.exists(path)
    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        # 创建目录操作函数
        os.makedirs(path)

        print(path + ' 创建成功')
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        print(path + ' 目录已存在')
        return False


# 定义要创建的目录
#'C://Users/lenovo/Desktop/chromedriver.exe'
#mkpath = 'C:\\Users\\lenovo\\Desktop\\tttttttt\\'
#mkpath = "d:\\qttc\\web\\"
# 调用函数
#mkdir(mkpath)
#mkpath1 = 'C:\\Users\\lenovo\\Desktop\\tttttttt\\dddd'
#mkdir(mkpath1)





# 获取括号中内容
def get_bracket(ing):
    patt = re.compile(r"\((.*?)\)", re.I|re.X)
    return patt.findall(ing)


def CombineData(InputDataPath,OutDataPath,EndDate):
    #csvs = []
    #for file in os.listdir("D:/Programma/Environmental"):
    #for file in os.listdir(InputDataPath):
    #   if file.endswith(").csv"):
    #        csvs.append(file)
    #print(csvs)


    #SaveOriginDataPath = "D:/Programma/Environmentaltest"
    #DirPath = SaveOriginDataPath + '/' + 'combined_enviorenment' + '/' + EndDate
    #os.chdir(DirPath)

    files = os.listdir(InputDataPath)
    # print(files)
    sort_files = sorted(files, key=lambda item: get_bracket(item), reverse=False)
    print(sort_files)

    csvs = sort_files
    print(csvs)
    length = len(EndDate)
    for csv in csvs:
        if csv[4:4+length] == EndDate:
            aa = csvs.index(csv)

    print(aa)
    csvs = csvs[(aa-8):(aa+2)]
    from itertools import islice
    #fout = open("D:/Programma/Environmental/combined_enviorenment.csv", "a")
    #fout = open(InputDataPath + '/' + 'combined_enviorenment' + 'EndDate.csv', "a")
    #SaveOriginDataPath.replace('/', '\\') + '\\'
    #EndDate = '2017-10-10'
    SaveOriginDataPath = "D:/Programma/Environmentaltest"
    DirPath = SaveOriginDataPath + '/' + 'combined_enviorenment' + '/' + EndDate
    mkdir(DirPath.replace('/', '\\'))

    os.chdir(DirPath)
    #print(os.getcwd())
    #OutDataPath = 'com_env' + EndDate + '.csv'
    fout = open(OutDataPath, "a")
    #OutDataPath = mkdir(InputDataPath.replace('/','\\'))
    #fout = open(OutDataPath+ '/' +'combined_enviorenment'+str(EndDate)+'.csv', "a")
    # 第一个文件保存头部column name信息:
    #for line in open("D:/Programma/Environmental/" + csvs[0]):
    print(os.getcwd())
    for line in open(InputDataPath +'/'+ csvs[0]):
        fout.write(line)

    # 后面的部分可以跳过 headers:
    for file in csvs[1:]:
        #f = open("D:/Programma/Environmental/" + file)
        f = open(InputDataPath + '/'+file)
        for line in islice(f, 6, None):
            fout.write(line)
        f.close()  # 关闭文件
    fout.close()




EndDate = '2017-8-9'
SaveOriginDataPath = "D:/Programma/Environmentaltest"
InputDataPath = SaveOriginDataPath
OutDataPath = 'com_env'+EndDate+'.csv'
#OutDataPath = SaveOriginDataPath+'/'+'combined_enviorenment'+'/'+EndDate
#DirPath = SaveOriginDataPath+'/'+'combined_enviorenment'+'/'+EndDate
#mkdir(DirPath.replace('/','\\'))

#print(OutDataPath)

#os.chdir(OutDataPath)
print(os.getcwd())
#OutDataPath = 'com_env'+EndDate+'.csv'
#fout = open('com_env'+EndDate+'.csv', "a")
CombineData(InputDataPath,OutDataPath,EndDate)


