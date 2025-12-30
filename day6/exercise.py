# class Tool:
#     __count = 0
#
#     def __init__(self, name):
#         self.name = name
#         Tool.__count += 1
#
#     @classmethod
#     def show_total(cls):
#         """
#
#         :return:
#         """
#
#         print(f'当前的工具总数{cls.__count}')
#
#     @staticmethod
#     def tool_help():
#         print('静态方法不传入类名、对象')
#
#
# t1 = Tool('斧子')
# t2 = Tool('螺丝刀')
# Tool.show_total()
#
# Tool.tool_help()
#
#
# class MusicPlayer:
#     _instance = None
#
#     def __init__(self, name):
#         self.music_name = name
#
#     def __new__(cls, *args, **kwargs):
#         if (cls._instance is None):
#             cls.instance = super().__new__(cls)
#         return cls._instance
#
#
# if __name__ == "__main__":
#     pass
#
# import time
#
#
# def timing_decorator(func):
#     def wrapper(*args, **kwargs):
#         start_time = time.time()
#         result = func(*args, **kwargs)
#         end_time = time.time()
#         print(f"函数 {func.__name__} 执行时间：{end_time - start_time} 秒")
#         return result
#
#     return wrapper
#
#
# @timing_decorator
# def time_consuming_function():
#     # 模拟耗时操作
#     time.sleep(2)
#     print("函数执行完成")
#
#
# time_consuming_function()


class Person:
    total_person = 0

    def __init__(self, name, age):
        self.name = name
        self.age = age
        Person.total_person += 1


class Hero(Person):
    _instance = None

    def __init__(self, level, rank, name, age):
        super().__init__(name, age)
        self.__level = level
        self.__rank = rank

    def __str__(self):
        return f'姓名：{self.name} 级别：{self.__level} 排名：{self.__rank}'

    def __del__(self):
        print(f'{self.name}倒下了')

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @classmethod
    def get_number(cls):
        return cls.total_person

    @staticmethod
    def average_power(a, b):
        return (a + b) / 2

    def set_level(self, level):
        if level in ['S', 'A', 'B', 'C']:
            self.__level = level

    def set_rank(self, rank):
        if rank > 0:
            self.__rank = rank

    def __secret(self):
        print(f'{self.name} 是怪人')

    def fight(self):
        self.__secret()


def symmetric_number():
    num = int(input('请输入一个整数：'))
    i = 0
    list1 = []
    list2 = []
    while num:
        list1.append(num % 10)
        num //= 10
    for i in reversed(list1):
        list2.append(i)
    print(list1)
    print(list2)
    assert list1 == list2, "不是对称数"
    print("是对称数")


if __name__ == '__main__':
    hero1 = Hero('S', '1', '爆破', '23')
    print(hero1)
    hero2 = Hero('S', '2', '战栗的龙卷', '18')
    print(hero2)
    print(f'英雄协会人员数量:{Hero.get_number()}')
    print(Hero.average_power(30, 50))
    print(hero1 is hero2)
    try:
        symmetric_number()
    except ValueError:
        print('请输入整数！')
    except Exception as e:
        print(e)
