# 作者: 王道 龙哥
# 2025年12月26日14时23分30秒
# xxx@qq.com

def func():
    a = 10
    print(id(a))


func()
b = 10
print(id(b))
print('-' * 100)


def change(num):
    """
    无法在函数内通过num1改变外面的值
    :param num1:
    :return:
    """
    num = 20
    print(f'change函数内num {num}')


num = 10
change(num)
print(f'函数外的num{num}')


# 可变数据类型,如何使用

def list_change(num_list1):
    num_list1.insert(0,10)


num_list = [1, 2, 3]
print(f'调用函数前{num_list},id(num_list)={id(num_list)}')
list_change(num_list)
print(f'调用函数后{num_list},id(num_list)={id(num_list)}')
