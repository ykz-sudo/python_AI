# 作者: 王道 龙哥
# 2025年12月26日14时15分43秒
# xxx@qq.com

my_tuple = ((1, 2), (3, 5))

a, b = my_tuple
print(a, b)


# 对函数的多个返回值拆包
def sum_substract(a, b):
    return a + b, a - b


a, b = sum_substract(10, 20)
print(a, b)

dict1 = {'name': '李云龙', 'age': 20, 'gender': '男'}

# 对字典拆包的时候，获取到的是key值
key1, key2, key3 = dict1
print(f"key1:{key1},key2:{key2},key3:{key3}")
