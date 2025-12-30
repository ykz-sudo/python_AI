# 作者: 王道 龙哥
# 2025年12月29日09时28分09秒
# xxx@qq.com
class Animal:
    def make_sound(self):
        # 父类方法：定义接口
        pass


# 2. 子类（继承+重写）
class Dog(Animal):
    def make_sound(self):  # 重写父类方法
        print("汪汪叫")


class Cat(Animal):
    def make_sound(self):  # 重写父类方法
        print("喵喵叫")


class Duck(Animal):
    # def make_sound(self):  # 重写父类方法
    #     print("嘎嘎叫")
    pass


def animal_sound(animal: Animal):  # 参数声明为父类类型
    animal.make_sound()


# 测试多态
dog = Dog()
cat = Cat()
duck = Duck()

animal_sound(dog)  # 输出：汪汪叫
animal_sound(cat)  # 输出：喵喵叫
animal_sound(duck)  # 输出：嘎嘎叫
# del Animal
