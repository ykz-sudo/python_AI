# 作者: 王道 龙哥
# 2025年12月27日11时06分08秒
# xxx@qq.com
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age


class Student(Person):
    def __init__(self, name, age, school):
        super().__init__(name, age)
        self.school = school

    def __str__(self):
        # 调用父类的属性，添加子类信息
        return f"{self.name}, {self.age}岁, 在{self.school}上学"

if __name__ == '__main__':
    s = Student("张三", 15, "阳光中学")
    print(s)