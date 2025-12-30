# 作者: 王道 龙哥
# 2025年12月27日10时35分32秒
# xxx@qq.com
class Student:
    def __init__(self, name, gender):
        self.name = name
        self.gender = gender
        self.__age = 20  # 赋予年龄默认值20
        self.__score = 80  # 赋予成绩默认值80

    def __str__(self):
        return f"name:{self.name}, gender:{self.gender}, age:{self.__age}, score:{self.__score}"

    # 定义获取年龄的方法
    def get_age(self):
        return self.__age

    # 定义修改年龄的方法
    def set_age(self, age):
        if 30 >= age >= 10:
            self.__age = age

    # 定义获取成绩的方法
    def get_score(self):
        return self.__score

    # 定义设置成绩的方法
    def set_score(self, score):
        if 0 <= score <= 100:
            self.__score = score
        else:
            print('设置失败，请重新设置')