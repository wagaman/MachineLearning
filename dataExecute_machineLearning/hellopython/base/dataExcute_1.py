__author__ = 'Administrator'

import gzip

from os import listdir
from os.path import isfile, join
import pandas as pd

#mypath = '/home/yimr/sss/data'
mypath = 'D:\\tmp'
onlyfiles = [join(mypath, f) for f in listdir(mypath) if isfile(join(mypath, f))]

for file in onlyfiles:
    with gzip.open(file, 'rt') as f:
        text = f.readlines()
        print(text)

