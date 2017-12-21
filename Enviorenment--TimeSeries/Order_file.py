import os
import re

print(os.getcwd())
os.chdir('C:\\Users\lenovo\Desktop\envio_origin')


# 获得训练用的wav文件路径列表
def get_wav_files(wav_path):
    wav_files = []
    for (dirpath, dirnames, filenames) in os.walk(wav_path):
        for filename in filenames:
            if filename.endswith('.csv') or filename.endswith('.CSV'):
                filename_path = filename

                #filename_path = os.sep.join([dirpath, filename])
                if os.stat(filename_path).st_size < 240000:  # 剔除掉一些小文件
                    continue
                wav_files.append(filename_path)
    return wav_files

# 获取括号中内容
def get_bracket(ing):
    patt = re.compile(r"\((.*?)\)", re.I|re.X)
    return patt.findall(ing)[0]


if __name__ == '__main__':

    # 训练样本路径
    #C:\Users\lenovo\Desktop\envio_origin
    path = 'C:\\Users\lenovo\Desktop\envio_origin'
    files = get_wav_files(path)
    sort_files = sorted(files, key=lambda item: get_bracket(item), reverse=False)
    print(sort_files)