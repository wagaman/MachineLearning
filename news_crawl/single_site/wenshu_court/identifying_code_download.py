# -*- coding: utf-8 -*-
"""
Created on Thu Aug 10 16:00:26 2017

@author: TF Liu
"""

url = 'http://wenshu.court.gov.cn/waf_captcha/'       
from urllib.request import urlretrieve
import imghdr
import time
for i in range(3000):
    time.sleep(2)
    filename = 'C:\\Users\sss\Desktop\验证码\\'+str(i)+'.jpg'
    urlretrieve(url, filename)
#    imghdr.what(str(i)+'.jpg')