# 作者: 王道 龙哥
# 2025年12月25日10时56分31秒
# xxx@qq.com
import random


def list_slice():
    list1 = ['red', 'green', 'blue', 'yellow', 'white', 'black']
    print(list1[0])  # red
    print(list1[1])  # green
    print(list1[2])  # blue

    print(list1[-1])  # black
    print(list1[-2])  # white
    print(list1[-3])  # yellow

    # print(list1[10])

    print(list('hello'))
    print(len(list1))

    for color in list1:
        print(color, end=' ')


def list_append() -> None:
    name_list = ['Tom', 'Lily', 'Rose']
    print(name_list)
    name_list.append('zhangsan')
    print(name_list)
    name_list.insert(1, 'longge')
    print(name_list)
    city_list = ["北京", "上海", "广州", "深圳"]
    name_list.extend(city_list)
    print(name_list)
    name_list[4:4] = [1, 2, 3]  # 把一个列表快速插入到某个位置
    print(name_list)


def list_index():
    """
    列表查询
    :return:
    """
    my_list = ['小李', '小明', '嘉豪', '小张', '嘉豪', '老王', '老李', '楚云飞', '嘉豪']
    print(my_list.index('嘉豪'))
    print(f"my_list.count('嘉豪') 结果是{my_list.count('嘉豪')}")
    print('小李' in my_list)
    print('小李' not in my_list)


def list_del():
    """
    列表删除
    :return:
    """
    hero_list = ['吴用', '宋江', '鲁智深', '林冲', '花荣', '晁盖', '宋江']
    # del hero_list[0]
    del hero_list[1:3]  # 左闭右开
    # hero_list.pop(1)
    # hero_list.remove('宋江')  # 只能删除第一个
    print(hero_list)
    # hero_list.clear()
    # print(hero_list)


# 循环删除问题
def list_while_del():
    """
    循环删除
    :return:
    """
    num_list = [1, 2, 3, 4, 3, 5]
    i = 0
    list_length = len(num_list)
    while i < list_length:
        if num_list[i] == 3:
            num_list.pop(i)
            list_length -= 1  # 删除元素时列表变短，由于后面元素会往前移动，所以无需对i加1
        else:
            i += 1
    print(num_list)


def list_modify():
    """
    列表修改
    :return:
    """
    my_list = [0] * 10
    print(my_list)
    my_list[0] = 20
    print(my_list)
    my_list = [1, 9, 3, 4, 8, 5]
    my_list.reverse()
    print(my_list)
    my_list.sort(reverse=True)  # 默认升序，reverse=True降序
    print(my_list)


def classroom():
    """
    有3个教室[[],[],[]]，8名讲师['A','B','C','D','E','F','G','H']，将8名讲师随机分配到3个教室中
    ord
    chr
    :return:
    """
    classroom = [[] for i in range(3)]
    print(classroom)
    lecturer = [chr(ord('A') + i) for i in range(8)]
    print(lecturer)
    for teacher in lecturer:
        classroom[random.randint(0, 2)].append(teacher)
    print(classroom)


# list_append()
# list_index()
# list_del()
# list_while_del()
# list_modify()
classroom()
