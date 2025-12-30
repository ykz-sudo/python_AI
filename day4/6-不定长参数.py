# 作者: 王道 龙哥
# 2025年12月26日11时09分25秒
# xxx@qq.com
# 需求：求任意个整数的和
def sum_total(*args):
    """
    args是吃掉所有的位置参数的，类型是元组
    :param args:
    :return:
    """
    total = 0
    for i in args:
        total += i
    print(total)


sum_total(1, 2, 3, 4)
sum_total(1, 2, 3)
sum_total(1, 2)


def print_user_info(**kwargs):
    """
    kwargs吃掉所有的keyword的参数
    :param kwargs:
    :return:
    """
    print("接收的关键字参数（字典）：", kwargs)
    print(f"姓名：{kwargs.get('name')}，年龄：{kwargs.get('age')}，性别：{kwargs.get('gender')}")


# 调用函数，传递多个关键字参数
print_user_info(name="Alice", age=20, gender="女")
print_user_info(name="Bob", age=22, gender="男", hobby="篮球")  # 可传递额外参数

print('-' * 50)


def demo2(*args, **kwargs):
    print(f'demo2的args {args}')
    print(f'demo2的kwargs {kwargs}')


def demo(num, *args, **kwargs):
    print(num)
    print(f'demo1的args {args}')
    print(f'demo1的kwargs {kwargs}')
    demo2(*args, **kwargs) #拆包只能放到实参位置


demo(1, 2, 3, name='Alice', age=20, gender="女")
