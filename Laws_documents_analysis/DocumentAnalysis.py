#coding:utf-8

from win32com import client as wc
import os
import fnmatch
import datetime
import pandas as pd
import logging
import traceback
import sys
import shutil


#function: load Case Number that has been recorded
#parameter: filepath(case number file,basename is doneTXTlist.txt,can be arranged)
def LoadDoneFileList(filepath):
    if os.path.exists(filepath):
        fp = open(filepath,'r')
        filelist = fp.readlines()
        filelist = [str.replace("\n","") for str in filelist]
        fp.close()
        return filelist
    else:
        logging.error(filepath+":didnt exist")
        print(filepath+":didnt exist")
        return []


#function:transform Word file to TXT file
def Translate(path,desdir):
    '''''
    将一个目录下所有doc和docx文件转成txt
    该目录下创建一个新目录newdir
    新目录下fileNames.txt创建一个文本存入所有的word文件名
    本版本具有一定的容错性，即允许对同一文件夹多次操作而不发生冲突
    '''
    # 该目录下所有文件的名字
    files = os.listdir(path)
    # 该目下创建一个新目录newdir，用来放转化后的txt文本
    #dirname = datetime.datetime.now().strftime('%Y%m%d')
    #New_dir = os.path.abspath(os.path.join(path,dirname ))
    New_dir = path
    doneWordList  = []

        # 创建一个文本存入所有的word文件名

    try:
        for filename in files:
                # 如果不是word文件：继续
            if not fnmatch.fnmatch(filename, '*.doc') and not fnmatch.fnmatch(filename, '*.docx'):
                continue;
                # 如果是word临时文件：继续
            if fnmatch.fnmatch(filename, '~$*'):
                continue;

            docpath = os.path.abspath(os.path.join(path, filename))

            # 得到一个新的文件名,把原文件名的后缀改成txt
            new_txt_name = ''
            if fnmatch.fnmatch(filename, '*.doc'):
                new_txt_name = filename[:-4] + '.txt'
            else:
                new_txt_name = filename[:-5] + '.txt'

            word_to_txt = os.path.join(path, new_txt_name)

            if os.path.exists(word_to_txt):
                wordapp = wc.Dispatch('Word.Application')
                continue

            #print(word_to_txt)
            wordapp = wc.Dispatch('Word.Application')
            doc = wordapp.Documents.Open(docpath)
            # 为了让python可以在后续操作中r方式读取txt和不产生乱码，参数为4

            doc.SaveAs(word_to_txt, 4)
            doc.Close()


            doneWordList.append(docpath)

    finally:
        wordapp.Quit()

    #move doc file to another directory, name is donedoc,can be arranged
    for docf in doneWordList:
        shutil.move(docf,os.path.abspath(os.path.join(desdir,os.path.basename(docf))))


    return len(doneWordList)


def CutFile(txtdirpath,LawNoList,csvdir,donetxtdir,listfName):
    filelist = os.listdir(txtdirpath)

    # print filelist[0].encode('utf-8')
    structuredFile = pd.DataFrame(columns=[  # （2014）民申字第523号
                                           'CYear',
                                           'Province',
                                           'type',  # 民事裁定书-0，民事判决书-1
                                           'sue',  # 被告（被申请人）-0，原告(申请人)-1
                                           #'result',  # 败诉-0，胜诉-1
                                           'courtime',  # 法庭判决时间，最后事件为准
                                           'money',  # 赔偿金额，若无为0
                                           #'reason',
                                           'FileName',
                                           'FullLawNo',
                                           'Plaintiff',
                                           'Defendant'])  # 事件描述，可为“空”
    datedic = {'一': 1, '二': 2, '三': 3, '四': 4, '五': 5, '六': 6, '七': 7, '八': 8, '九': 9, '〇': 0, '十': 1,'０':0}
    pdList =[]

    repeatFilelist = []
    NewLawList = []

    for file in filelist:
        #logging.info("file:",file)
        print("===========",file)
        lawNO = '空'
        Cyear =0
        Provice =''
        type = 0
        sue = -1
        #result = 0
        money = 0
        #reason = "空"
        courtime = ""
        Plantiff = ""
        Defendant = ""

        logging.info('Dealing file :%s'%file)

        fullfilepath = os.path.abspath(os.path.join(txtdirpath,file))
        if not os.path.isfile(fullfilepath):
            continue
        fileinstnc = open(fullfilepath, 'r')
        lineindex = 1
        try:
            lines = fileinstnc.readlines()
            line_s = []
            for i in lines:
                #######i = str(i).decode('utf-8')

                i = i.strip()
                i = i.replace(" ", "")
                #######i = i.encode('utf-8')

                if len(i) == 0:
                    continue
                lineindex = lineindex + 1
                line_s.append(i)

            tmp = str(line_s[1]).strip().replace(" ", "")

            if "民事裁定书" in tmp:
                type = 0
            elif tmp == '民事判决书' in tmp:
                type = 1
            else:
                print('ERROR:this row is supposed to be the type row ,but it isnt.')
                logging.error(file+" this row is supposed to be the type row ,but it isnt.")
                return

            if str(line_s[2]).endswith('号'):
                # print line_s[2]
                # （2016）鲁0113民初1223号
                if "民初" not in line_s[2] and "商初" not in line_s[2]:
                    print(file," is not first charge")
                    logging.warning(file," is not first charge,take it as repeat file")
                    repeatFilelist.append(file)
                    continue
                lawNO = line_s[2]
                if lawNO in LawNoList :
                    repeatFilelist.append(file)
                    continue
                NewLawList.append(lawNO)
                lawNO.replace("(","（")
                lawNO.replace(")","）")

                Cyear = lawNO.split("（")[1].split("）")[0]

                Provice = str(lawNO.split("）")[1])[0]

            else:
                print('ERROR:this row is supposed to be the LawNO row ,but it isnt.')
                logging.error(file+':this row is supposed to be the LawNO row ,but it isnt.')

                logging.error(file+': case number dealt problem')
                return


            #  record  all the  defendants.splited by ","
            DefendantAccur = False
            PlantiffAccur = False
            escape = False
            for strl in line_s[3:-1]:
                #原告和被告：切分准确，待确认
                if ("原告" in strl or "被告"  in strl ) and "受理费" not in strl: #or "中国联合网络" in strl  :
                    if not str(strl).startswith("原告") and not str(strl).startswith("被告")  : continue # remove invalid multiple lines
                    #if "原告" in strl and "被告" in strl and "受理费" not in strl:
                    if  "原告" in strl:
                        if DefendantAccur and PlantiffAccur:
                            escape = True
							#如果原告被告都已经出现，再次出现原告，说明已经到了事实说明及以下部分
                        if not DefendantAccur:
                            if "中国联合网络" in strl:
                                sue = 1
                            strltuple = strl.split("原告")
                            tmpline = strltuple[1]
                            if(str(strltuple[1]).startswith("：")):
                                tmpline = strltuple[1][1:]
                            tmpinx = 0
                            counttmp = 0
                            try:
                                firinx = str(tmpline).index('，')
                            except ValueError as ve:
                                counttmp  = 1
                                pass
                            try:
                                secinx = str(tmpline).index('。')
                            except ValueError as ve:
                                if(counttmp  == 0) : counttmp = 2
                                else: counttmp = 3
                                pass
                            if counttmp == 0:
                                if   firinx < secinx  and firinx >-1 :
                                    tmpinx = firinx
                                elif secinx > -1:
                                    tmpinx = secinx
                            elif counttmp == 1:
                                tmpinx = secinx
                            elif counttmp == 2 :
                                tmpinx = firinx
                            else:
                                logging.error(file+" cant pick the plantiff and defendant")

                            Plantiff = tmpline[0:tmpinx]
                            #print(file+":plantiff"+Plantiff)
                            PlantiffAccur = True
                    elif  "被告" in strl:
                        if not escape:
                            if "中国联合网络" in strl:
                                sue = 0
                            strltuple = strl.split("被告")
                            tmpline = strltuple[1]
                            if (str(strltuple[1]).startswith("：")):
                                tmpline = strltuple[1][1:]

                            tmpinx = 0
                            counttmp = 0
                            try:
                                firinx = str(tmpline).index('，')
                            except ValueError as ve:
                                counttmp  = 1
                                pass
                            try:
                                secinx = str(tmpline).index('。')
                            except ValueError as ve:
                                if(counttmp  == 0) : counttmp = 2
                                else: counttmp = 3
                                pass
                            if counttmp == 0:
                                if   firinx < secinx  and firinx >-1 :
                                    tmpinx = firinx
                                elif secinx > -1:
                                    tmpinx = secinx
                            elif counttmp == 1:
                                tmpinx = secinx
                            elif counttmp == 2 :
                                tmpinx = firinx
                            else:
                                logging.error(file+" cant pick the plantiff and defendant")
                            if len(Defendant) > 0:
                                Defendant = Defendant + "," + tmpline[0:tmpinx]
                            else : Defendant = tmpline[0:tmpinx]
                            DefendantAccur = True
                            ##print(file + ":Defendant" + Defendant)
                if "受理费"  in strl and "元" in strl:
                    strafter = str(strl).split("元")[0].split("受理费")
                    if(len(strafter)<=0):
                        continue
                    numQ=strafter[1].split("人民币")
                    if len(numQ) > 1:
                        if is_number(numQ[1]): # is digit
                            money = numQ[1]

                    elif len(numQ) == 1:
                        if is_number(numQ[0]): # is digit
                            money = numQ[0]
                    else:
                        print("cant find case expense in file: ",file)
                        logging.warning(file+': case expense keyword found,but digit not found')
                    continue
                if "年" in strl and "月" in strl and "日" in strl and len(strl) >=9 and len(strl) <13 :
                    year = str(strl).split("年")[0]
                    month = str(strl).split("年")[1].split("月")[0]
                    day = str(strl).split("年")[1].split("月")[1].split("日")[0]

                    year = TimeTransfer(year, datedic)
                    month = TimeTransfer(month, datedic)
                    day = TimeTransfer(day, datedic)

                    courtime = str(year) + "-" + str(month) + "-" + str(day)
                else:
                    continue


            structuredFile = structuredFile.append( {'CYear':Cyear,
                                                     'Province':Provice,
                                                     'type':type,  # 民事裁定书-0，民事判决书-1
                                                     'sue':sue,  # 被告（被申请人）-0，原告(申请人)-1
                                                     #'result':'not dealt',  # 败诉-0，胜诉-1
                                                     'courtime':courtime,  # 法庭判决时间，最后事件为准
                                                     'money':money,  # 赔偿金额，若无为0
                                                     #'reason':'not dealt'
                                                     'FileName':file,
                                                     'FullLawNo':lawNO,
                                                     'Plaintiff':Plantiff,
                                                     'Defendant':Defendant },ignore_index= True)
        except Exception as e :
            traceback.print_exc()
            print(e)
            logging.error(file+" " +e.__str__())
            pass
        finally:
            fileinstnc.close()


    csvfile = os.path.abspath(os.path.join(csvdir,str(datetime.datetime.now().strftime('%Y%m%d%H%M'))+'.csv'))
    if os.path.exists(csvfile):
        os.remove(csvfile)

    structuredFile.to_csv(csvfile)
    print(str(len(structuredFile))+" files have been transformed to csv files")

    try:
        if not os.path.exists(listfName):
            donefl = open(listfName,'w+')
            donefl.write('')
            donefl.close()

        donefl = open(listfName,'a')
        i = 0
        #
        print("==============================================")
        print("all files in directory:"+str(len(filelist)))
        print("repeat file count :" + str(len(repeatFilelist)))
        print("New Filelist:" + str(len(NewLawList)))

        for file1 in filelist:
            if file1 not in repeatFilelist:
                shutil.move(os.path.abspath(os.path.join(txtdirpath,file1)),os.path.abspath(os.path.join(donetxtdir,file1)))
                donefl.write(NewLawList[i]+"\n")
                i=i+1
            else:
                os.remove(os.path.abspath(os.path.join(txtdirpath,file1)))

        donefl.close()
    except Exception as e:
        logging.error(str(e))
        traceback.print_exc()
        pass

def TimeTransfer(timestr,datedic):
    dd = []
    inx = 0
    lastten = False
    midten = False
    if (timestr[-1] == '十'):
        lastten = True
    if (len(timestr) == 3 and timestr[-2] == '十'):
        midten = True

    # print '======================================'
    if len(timestr) > 1:
        while inx < len(timestr):
            if midten and inx == 1:
                inx = inx + 1
                continue
            dd.append(timestr[inx:(inx + 1)])
            inx = inx + 1
        if lastten:
            dd[-1] = '〇'
    elif len(timestr) == 1:
        if '十' in timestr:
            return '%s%s' % (datedic[timestr], '0')
        else:
            return datedic[timestr]

    out = ""

    for ii in dd:
        out = '%s%s' % (out, datedic[ii])
    # print '======================================'

    return out

def TimeTransferLinux(timestr,datedic):
    dd = []
    inx = 0
    #print '======================================'
    if len(timestr) > 3:
        while inx < len(timestr) / 3:
            dd.append(timestr[inx * 3:(inx + 1) * 3])
            inx = inx + 1
    elif len(timestr) == 3:
        if '十' in timestr:
            return '%s%s'%(datedic[timestr],'0')
        else:
            return datedic[timestr]

    out = ""

    for ii in dd:
        out = '%s%s' % (out, datedic[ii])
    #print '======================================'

    return out


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False


if __name__ == '__main__':
    print
    ''''' 
        将一个目录下所有doc和docx文件转成txt 
        该目下创建一个新目录newdir 
        新目录下fileNames.txt创建一个文本存入所有的word文件名 
        本程序具有一定的容错性 
    '''
    #print('Enter your Director\'s path:')
    #print("路径用\或\\表示均可")

    basePath ="E:\\work\\2017\\法律部\\simulation"
    donedocdir = "donedoc"
    dontxtdir = "donetxt"
    originalfiledir = "todofile"
    desdir = "csv"
    logdir = "log"

    logFileName = "log.txt"
    donefilelist = "doneTXTlist.txt"

    logFullPath = os.path.abspath(os.path.join(os.path.join(basePath,logdir),logFileName))
    if not os.path.exists(logFullPath):
        loftmp = open(logFullPath,'w+')
        loftmp.write('')
        loftmp.close()

    logging.basicConfig(filename=logFullPath,level=logging.INFO)
    logging.info(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')+ " Start===============")

    ''' word to txt '''
    FullOriDocdir =  os.path.abspath(os.path.join(basePath,originalfiledir))
    if not os.path.exists(FullOriDocdir) or not os.path.isdir(FullOriDocdir):
        print("original file dir doesnt exit,please check,dir name is "+FullOriDocdir )
        logging.error("original file dir doesnt exit,please check,dir name is "+FullOriDocdir)
        sys.exit()

    print("Transforming Word to Text Files.........")

    FullmoveDocdir = os.path.abspath(os.path.join(basePath,donedocdir))
    movedfile = Translate(FullOriDocdir,FullmoveDocdir)
    print(str(movedfile)+ " Word files have been transformed to TXT files. ")

    FullLogDir = os.path.abspath(os.path.join(basePath,logdir))
    LawNoList = LoadDoneFileList(os.path.abspath(os.path.join(FullLogDir,donefilelist)))

    print("Cutting  Text Files.........")
    FullDesdir = os.path.abspath(os.path.join(basePath,desdir))
    Fulldonetxtdir = os.path.abspath(os.path.join(basePath,dontxtdir))
    CutFile(FullOriDocdir,LawNoList,FullDesdir,Fulldonetxtdir,os.path.abspath(os.path.join(FullLogDir,donefilelist)))

    #logging.info(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + " Start===============")
    print("Programm done")
