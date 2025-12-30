# 作者: 王道 龙哥
# 2025年12月30日14时59分25秒
# xxx@qq.com
import copy


def use_assign():
    """
    赋值，一个列表改变另外一个列表会同步改变
    :return:
    """
    a = [1, 2, 3]
    b = a
    a[0] = 10
    print(b)


def use_copy():
    """
    浅copy
    :return:
    """
    a = [1, 2, 3]
    b = copy.copy(a)  # 等价于a.copy()
    a[0] = 10
    print(f'a的值 {a}')
    print(f'b的值 {b}')


def use_deepcopy():
    """
    深copy
    :return:
    """
    a = [1, 2]
    b = [3, 4]
    c = [a, b]
    # d=copy.copy(c)
    d = copy.deepcopy(c)
    a[0] = 10
    print(f'c的值 {c}')
    print(f'd的值 {d}')


if __name__ == '__main__':
    # use_copy()
    use_deepcopy()
