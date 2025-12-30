# 作者: 王道 龙哥
# 2025年12月26日10时54分52秒
# xxx@qq.com

def return_num():
    return 1, 2, 3


result = return_num()
print(result)

print('-' * 50)


# 位置参数与keyword参数
def print_info(name, age, gender):
    print(f'姓名{name}, 年龄{age}, 性别{gender}')


print_info(20, '小明', True)

print_info(age=20, name='小明', gender=True)  # keyword参数手法

print('-' * 50)


# 缺省参数,必须放在最后

def print_info2(name, age, gender=True):
    print(f'姓名{name}, 年龄{age}, 性别{gender}')
    print(f'姓名{name}, 年龄{age}, 性别{gender}')


print_info2('小明', 20)
print_info2('小明', 20, False)

