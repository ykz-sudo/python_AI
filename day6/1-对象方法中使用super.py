# 作者: 王道 龙哥
# 2025年12月29日09时18分12秒
# xxx@qq.com
class Animal:
    def __init__(self, name):
        self.name = name

    def make_sound(self):
        print("动物发出声音")

    def hungry(self):
        print('动物饿了')

class Cat(Animal):
    # 重写父类方法
    def make_sound(self):
        super().hungry()
        print(f"{self.name}在喵喵叫")  # 覆盖父类实现


cat = Cat("咪咪")
cat.make_sound()  # 输出：咪咪在喵喵叫（使用子类重写的方法）