# 作者: 王道 龙哥
# 2025年12月25日14时57分48秒
# xxx@qq.com

def dict_add_modify_del():
    student = {'name': 'bob', 'age': 20, 'height': 98.5}
    print(student)

    # 添加
    student['score'] = 66
    print(student)
    student['score'] = 88
    print(student)

    print(student.setdefault('python', 98))  # 不存在才增加,存在是没有做变化的
    print(student)
    print('-' * 50)
    # 删除
    # del student['score']
    print(student.popitem())
    print(student)
    print(student.pop('name'))
    print(student)

    print('-' * 50)
    # 清空
    student.clear()
    print(student)


def dict_get():
    s = {'name': 'zs', "age": 20, "height": 180, "score": 10}

    ## 1. 直接通过key查找
    print(s['name'])
    # print(s['name1'])
    print(s.get('age'))
    print('-' * 50)
    for key in s.keys():
        print(key)
    print('-' * 50)
    for value in s.values():
        print(value)
    print('-' * 50)
    for k, v in s.items():  # 最多的使用就是遍历
        print(k, v)

    new_items = s.items()
    print(new_items)
    s['name'] = 'zhangsan'
    print(new_items)


def dict_work():
    data = [
        {'name': '小明', 'fruit': ['苹果', '草莓', '香蕉'], 'total_price': 89},
        {'name': '小刚', 'fruit': ['葡萄', '橘子', '樱桃'], 'total_price': 87}
    ]
    data1 = {'小明': (['苹果', '草莓', '香蕉'], 89), '小刚': (['葡萄', '橘子', '樱桃'], 87)}
    print('小明' in data1)
    print(max(data1))


# dict_add_modify_del()
# dict_get()
dict_work()
