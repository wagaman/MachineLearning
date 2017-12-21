__author__ = 'Administrator'

print([ i for i in range(5)])

a = ["a", "b", "c", "d"]

# iterate with index
for i, el in enumerate(a):
    print(i, el)

testPros = [1, 2.4, 3.5, 4]
print(testPros[0])

#列表推导式

testClass = [round(x) for x in testPros]
print(testClass)

rows = range(1, 4)
cols = range(1, 3)
x = [(i, j) for i in rows for j in cols]
print(x)


#zip() 并行迭代
a = [1,2,3]
b = ['one','two','three']

list(zip(a,b))
# [(1, 'one'), (2, 'two'), (3, 'three')]


#字典推导式   查询每个字母出现的次数。
strs = 'Hello World'
s = {k: strs.count(k) for k in set(strs) }
print(s)



