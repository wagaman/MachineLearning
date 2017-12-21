__author__ = 'Administrator'

#*args 收集位置参数
def do(*args):
    print(args)
do(1, 2, 3)


#**kwargs 收集关键字参数
def do(**kwargs):
    print(kwargs)
do(a=1, b=2, c='la')
# {'c': 'la', 'a': 1, 'b': 2}

# 一个装饰器
def document_it(func):
    def new_function(*args, **kwargs):
        print("Runing function: ", func.__name__)
        print("Positional arguments: ", args)
        print("Keyword arguments: ", kwargs)
        result = func(*args, **kwargs)
        print("Result: " ,result)
        return result
    return new_function

# 人工赋值
def add_ints(a, b):
    return a + b


cooler_add_ints = document_it(add_ints) #人工对装饰器赋值
cooler_add_ints(3, 5)