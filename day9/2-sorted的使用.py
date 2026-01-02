# 作者: 王道 龙哥
# 2026年01月02日09时54分03秒
# xxx@qq.com

def use_sorted1():
    """
    排序返回了一个新列表
    :return:
    """
    nums = [3, 1, 4, 2]
    sorted_nums = sorted(nums)
    print(sorted_nums)
    print(nums)
    # 排序字符串（按字符ASCII码）
    s = "python"
    print(sorted(s))  # ['h', 'n', 'o', 'p', 't', 'y']


def my_len(element):
    return len(element)


def sorted_str():
    words = ["apple", "banana", "cat", "dog"]
    # key=len：按字符串长度排序
    sorted_words = sorted(words, key=len)
    print(sorted_words)


def func1(x):
    return x['age']


def sorted_dict_key():
    """
    排序列表嵌套字典，排序规则是按照字典的键
    :return:
    """
    students = [
        {"name": "Alice", "age": 18},
        {"name": "Bob", "age": 16},
        {"name": "Charlie", "age": 20}
    ]
    # lambda表达式就是匿名函数，冒号前面是入参，冒号后面的是返回值
    print(sorted(students, key=lambda x: x['age']))


def sorted_reverse():
    nums = [3, 1, 4, 2]
    sorted_nums = sorted(nums, reverse=True)
    print(sorted_nums)


def sorted_two_column():
    """
    排序两列
    :return:
    """
    tup = [(3, 5), (1, 2), (2, 4), (3, 1), (1, 3)]
    print(sorted(tup, key=lambda x: (x[0], -x[1])))
    students = [
        {"name": "Alice", "age": 18},
        {"name": "Bob", "age": 18},
        {"name": "Charlie", "age": 20}
    ]
    print(sorted(students, key=lambda x: (x['age'], len(x['name']))))


def sorted_dict():
    """
    字典排序
    :return:
    """
    dict1 = {"xiaoming": 65, "lele": 83, "xiaowang": 91}
    for kv in dict1.items():
        print(kv)
    print('-'*50)
    print(sorted(dict1.items(),key=lambda x:x[1]))


if __name__ == '__main__':
    # use_sorted1()
    # sorted_str()
    # sorted_dict_key()
    # sorted_reverse()
    # sorted_two_column()
    sorted_dict()
