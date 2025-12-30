# 作者: 王道 龙哥
# 2025年12月29日15时36分31秒
# xxx@qq.com
__all__ = ['zero', 'sum1']

# 变量
zero = 0


# 函数
def sum1(*args):
    result = 0
    for i in args:
        result += i
    return result


# 类
class User:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def print_info(self):
        print(f"{self.name}同学的年龄是:{self.age}")
