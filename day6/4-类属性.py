# 作者: 王道 龙哥
# 2025年12月29日09时40分45秒
# xxx@qq.com
class Student:
    # 类属性：定义在__init__外，所有学生共享
    count = 0

    def __init__(self, name):
        self.name = name  # 对象属性
        Student.count+=1


# 所有对象共享类属性
stu1 = Student("张三")
stu2 = Student("李四")
stu3 = Student('王五')
print(Student.count)
