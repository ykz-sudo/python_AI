# 一切皆对象
import keyword

age = 18
name = 'ykz'
height = 190.3
print(name)
print(type(name))
print(type(age))
print(type(height))
print('-' * 50)
is_male = True
print(type(is_male))
k = complex(2, 3)
print(k.real, k.imag)
print(type(k))
print('-' * 50)

num1 = 100
num2 = 200
num3 = num1 + num2
print(num3)
print(f'is_male+num1={is_male + num1}')

my_list = [1, 2, 3]
print(my_list)
print(type(my_list))

my_tuple = ('abc', '123', 3)
print(my_tuple)

my_dict = {"a": 1, 'b': 2, 'c': 3}
print(my_dict)

my_set = {'a', 'b', 'c'}
print(my_set)


def use_print():
    print(bin(num1))
    print(oct(num1))
    print(hex(num1))


# 17bit精度
f = 1.2

print(keyword.kwlist)


# 4.
def odd_sum():
    sum = 0
    for i in range(1, 100, 2):
        sum += i
    print(sum)


odd_sum()


# 5.
def print_multiply():
    """
    打印九九乘法表
    :return:
    """
    for i in range(1, 10):
        for j in range(1, i + 1):
            print(f'{j}*{i}={i * j}', end=' ')
        print('')


print_multiply()


# 6.
def count_1():
    sum = 0
    x = input('请输入整数：')
    x = int(x)
    for i in range(64):
        sum += x >> i & 1
    print(sum)


count_1()
