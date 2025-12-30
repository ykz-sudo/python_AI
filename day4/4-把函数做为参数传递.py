# 作者: 王道 龙哥
# 2025年12月26日10时46分33秒
# xxx@qq.com
# 定义加法函数
def get_sum(a, b):
    return a + b


# 定义减法函数
def get_substract(a, b):
    return a - b


# 定义计算函数
def calculate(a, b, fn):
    """
    自定义函数, 模拟计算器, 传入什么 函数, 就做什么操作.
    :param a:
    :param b:
    :param fn:
    :return:
    """
    return fn(a,b)

print(calculate(10,20,get_sum))
print(calculate(30,10,get_substract))