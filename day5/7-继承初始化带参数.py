# 作者: 王道 龙哥
# 2025年12月27日10时54分12秒
# xxx@qq.com
class Animal:
    def __init__(self, name):
        self.name = name

    def eat(self):
        print(f"{self.name}在吃东西")


# 子类（派生类），通过`()`指定父类
class Dog(Animal):
    # 新增子类独有的方法
    def bark(self):
        print(f"{self.name}在汪汪叫")

    def eat(self):
        print(f'{self.name} 吃东西特别好看')


# 使用子类
dog = Dog("旺财")
dog.bark()
dog.eat()