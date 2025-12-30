list1 = [1, 2, 3, 4, 5]


def change_list():
    list1[0] = 985


change_list()
print(list1)


# 位置参数与keyword参数
def print_info(name, age=18, gender=True):
    print(f'姓名{name}, 年龄{age}, 性别{gender}')


print_info(20, '小明', True)
print_info(age=20, name='小明', gender=True)  # keyword参数手法
print_info('MAX', gender=False)


# Traceback (most recent call last):
#   File "D:\python_code2026\day4\exercise.py", line 19, in <module>
#     print_info('MAX', 20, gender1=False)
# TypeError: print_info() got an unexpected keyword argument 'gender1'


def demo2(*args, **kwargs):
    print(args)
    print(kwargs)


def demo(*args, **kwargs):
    print(f'demo的args为{args}')
    print(f'demo的kwargs为{kwargs}')
    demo2(*args, **kwargs)


demo(1, 2, 3, height=666, age=120, name='车力巨人')

my_tuple = ([1, 2, 9], [985, 211])
a, b = my_tuple
print(a, b)


# 对函数的多个返回值拆包
def sum_substract(a, b):
    return a + b, a - b


a, b = sum_substract(10, 20)
print(a, b)

dict1 = {'name': '孙笑川', 'age': 91, 'gender': '男'}

# 对字典拆包的时候，获取到的是key值
key1, key2, key3 = dict1
print(f"key1:{key1},key2:{key2},key3:{key3}")


# 4.
class dog():
    def __init__(self, color, name):
        self.name = name
        self.color = color

    def __str__(self):
        return f'颜色是{self.color}, 名字是{self.name}'

    def __del__(self):
        print('小黄升天了')

    def walf(self):
        print('汪汪叫')

    def behavior(self):
        print('摇尾巴')


dog1 = dog('Yellow', '小黄')
dog1.walf()
dog1.behavior()
print(dog1)



