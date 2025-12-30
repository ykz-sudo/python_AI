# 作者: 王道 龙哥
# 2025年12月26日16时45分23秒
# xxx@qq.com

class StudentInfo:
    def __init__(self, name, age, height=180, weight=150):
        self.name = name
        self.age = age
        self.height = height
        self.weight = weight

    def study(self):
        print("学生要学习...")

    def __str__(self):
        """
        打印对象的结果，是str返回值
        :return:
        """
        return f'名字 {self.name} 年龄 {self.age}'

    def __del__(self):
        print(f'{self.name} 要被销毁了')


s1 = StudentInfo('张飞', 30, weight=140)
print(s1.name)
print(s1.age)
print(s1.height)
print(s1.weight)

print(s1)

print(id(s1))
s1.age = 50
print(id(s1))

del s1
print('进程结束')

class Dog:
    def __init__(self, name, color):
        self.name = name
        self.color = color
    def bark(self):
        print('汪汪叫')

    def shake(self):
        print('摇尾巴')