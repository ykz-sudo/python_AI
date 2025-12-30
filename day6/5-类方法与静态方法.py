# 作者: 王道 龙哥
# 2025年12月29日09时48分31秒
# xxx@qq.com
class Tool:
    __count = 0

    def __init__(self, name):
        self.name = name
        Tool.__count += 1  # 每次创建对象，类属性+1

    @classmethod
    def show_total(cls):
        """
        当一个方法被classmethod装饰，那么方法的入参就是类名，也就是cls就是Tool
        :return:
        """
        print(f'当前的工具总数 {cls.__count}')

    @staticmethod
    def tool_help():
        print('静态方法不会传入类名，对象')


t1 = Tool('斧子')
t2 = Tool('螺丝刀')
Tool.show_total()
Tool.tool_help()


class MathHelper:
    # 静态方法：纯功能逻辑（判断是否为偶数）
    @staticmethod
    def is_even(num):
        return num % 2 == 0

    # 静态方法：纯功能逻辑（计算平均值）
    @staticmethod
    def average(a, b):
        return (a + b) / 2


# 调用静态方法（推荐用类名）
print(MathHelper.is_even(4))  # 输出：True
print(MathHelper.average(3, 5))  # 输出：4.0
