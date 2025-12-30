# 作者: 王道 龙哥
# 2025年12月25日16时37分11秒
# xxx@qq.com

def container_compare():
    list_a = [1, 2, 3]
    list_b = [3, 1]
    print(list_a > list_b)
    print('hello' > 'how')
    print({1, 2} < {1, 3, 4})  # 是否是子集的效果


def container_function():
    str1 = "acbd"
    list1 = ['a', 'b', 'c', 'd']
    tup1 = ('a', 'b', 'c', 'd')
    dict1 = {'a': 1, 'b': 2, 'c': 3, 'd': 4}
    set1 = {'a', 'b', 'c', 'd'}
    print(sorted(dict1, reverse=True))
    print(sorted(set1, reverse=True))
    print('-' * 50)
    print(list(reversed(str1)))  # 返回的都是可迭代对象，打印的是对象的内存地址值
    print(list(reversed(list1)))
    print(list(reversed(tup1)))
    print(list(reversed(dict1)))  # 用的很少
    print('-' * 50)
    for pos, value in enumerate(list1):  # 把每个元素的位置取出来
        print(pos, value)
    print('-' * 50)
    for pos, value in enumerate(dict1):  # 没啥用
        print(pos, value)


# container_compare()
container_function()
