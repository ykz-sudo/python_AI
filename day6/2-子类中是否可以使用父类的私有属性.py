# 作者: 王道 龙哥
# 2025年12月29日09时21分00秒
# xxx@qq.com
class Animal:
    def __init__(self, name):
        self.name = name
        self.__age = 20

    def make_sound(self):
        print("动物发出声音")

    def hungry(self):
        print('动物饿了')


class Cat(Animal):
    # 重写父类方法
    def make_sound(self):
        print(f"{self.name}在喵喵叫")  # 覆盖父类实现
        # print(f'年龄是{self.__age}')  #子类中不可以使用父类中的私有属性


cat = Cat("咪咪")
cat.make_sound()  # 输出：咪咪在喵喵叫（使用子类重写的方法）
