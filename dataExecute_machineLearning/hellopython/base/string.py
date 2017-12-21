__author__ = 'Administrator'

info = 'abca'
# 从下标1开始，查找在字符串里第一个出现的子串：返回结果3

print(info == 'abca')

print( info.find('a', 1) )


print(info.find('3333'))

line = '#微信号：x45655 月发文 240 篇'
print(line[line.find('月发文 ') + 4:-2])
print(line[line.find('月发文 ') + 4:line.find('篇')])