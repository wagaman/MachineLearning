import sys

from urllib.parse import quote

url = quote('苹果 iPhone 5S')
print('\n不带附加参数：\n%s' % url)
url = quote('红米，1s'.encode('utf8'))
print('\n不带附加参数：\n%s' % url)