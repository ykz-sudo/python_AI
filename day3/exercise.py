import random


def guess_num():
    computer_num = random.randint(1, 100)
    i = 0
    while i < 5:
        user_num = int(input('请输入'))
        i += 1
        if user_num < computer_num:
            print('too small')
        elif user_num > computer_num:
            print('too big')
        else:
            print('you win')
            break
    else:  # 没有从break出来，就会进else
        print('you lose')
    print(f'computer_num = {computer_num}')


def list_add():
    name_list = ['Tom', 'Lily', 'Rose']
    print(name_list)
    name_list.append('ykz')
    print(name_list)
    name_list.insert(2, 'MAX')
    print(name_list)
    city_list = ["北京", "上海", "广州", "深圳"]
    name_list.extend(city_list)
    print(name_list)
    name_list[2:2] = [1, 2, 3]
    print(name_list)


def list_del():
    hero_list = ['吴用', '宋江', '鲁智深', '林冲', '花荣', '晁盖', '宋江', '于孔泽']
    print(hero_list)
    del hero_list[0]
    print(hero_list)
    del hero_list[1:3]
    print(hero_list)
    hero_list.remove('宋江')
    print(hero_list)
    hero_list.clear()
    print(hero_list)


def list_while_del():
    num_list = [1, 2, 3, 3, 3, 5, 3]
    i = 0
    length = len(num_list)
    while i < length:
        if num_list[i] == 3:
            num_list.pop(i)
            length -= 1
        else:
            i += 1
    print(num_list)


def list_modify():
    my_list = [0] * 10
    print(my_list)
    my_list[2] = 985
    print(my_list)
    my_list = [985, 211, 666]
    my_list.reverse()
    print(my_list)
    my_list.sort(reverse=True)
    print(my_list)


def list_index():
    my_list = ['小李', '小明', '嘉豪', '小张', '嘉豪', '老王', '老李', '楚云飞', '嘉豪']
    print(my_list.index('嘉豪'))
    print(f"my_list.count('嘉豪')结果是{my_list.index('嘉豪')}")
    print('小李' in my_list)
    print('小李' not in my_list)


def str_slice():
    num_str = '0123456789'
    print(num_str[2:6])
    print(num_str[2:])
    print(num_str[:6])
    print(num_str[::])
    print(num_str[::2])
    print(num_str[2:-1])
    print(num_str[-2:10])
    print(num_str[::-1])


def container_function():
    seasons = ['Spring', 'Summer', 'Fall', 'Winter']
    enum_list = enumerate(seasons)
    seasons_dict = {}
    for pos, value in enum_list:
        seasons_dict[pos] = value
    print(seasons_dict)


# 2.

def seq_same():
    """
    求两个有序数字列表的公共元素
    :return:
    """
    list1 = [1, 3, 4, 5, 9, 10]
    list2 = [4, 5, 6, 7, 9]
    list3 = []
    for i in range(len(list1)):
        if (list1[i] in list2):
            list3.append(list1[i])
    print(list3)


def find_x():
    """
    3、给定一个n个整型元素的列表a，其中有一个元素出现次数超过n / 2，求这个元素
    :return:
    """
    a = []
    for i in range(10):
        a.append(random.randint(1, 3))
    print(a)

    for i in range(len(a)):
        if a.count(a[i]) > len(a) / 2:
            if i == a.index(a[i]):
                print(a[i])


def merge():
    """
    5、将元组 (1,2,3) 和集合 {4,5,6} 合并成一个列表
    :return:
    """
    tuple1 = (1, 2, 3)
    set1 = {4, 5, 6}
    list1 = list(tuple1) + list(set1)
    print(list1)


def change_num(n):
    n += 5  # n是栈帧中的引⽤，指向堆中新对象15


my_num = 10  # 堆中对象10，my_num引⽤在模块命名空间
change_num(my_num)
print(my_num)  # 输出？


def clear_list(lst):
    lst.clear()  # 改堆中列表的内容（清空），没改lst的引⽤


my_list = [1, 2, 3]  # 堆中列表，my_list引⽤在模块命名空间
clear_list(my_list)
print(my_list)
