# 作者: 王道 龙哥
# 2025年12月27日10时56分53秒
# xxx@qq.com
class Flyable:
    def fly(self):
        print("会飞")


# 父类2
class Swimmable:
    def swim(self):
        print("会游泳")


# 子类继承多个父类
class Duck(Flyable, Swimmable):
    pass


# 使用子类
duck = Duck()
duck.fly()  # 继承Flyable → 会飞
duck.swim()  # 继承Swimmable → 会游泳
