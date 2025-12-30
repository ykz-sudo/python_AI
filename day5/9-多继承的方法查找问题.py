# 作者: 王道 龙哥
# 2025年12月27日11时02分44秒
# xxx@qq.com
class A:  # 祖父类
    def say(self):
        print("A的say方法")


class B(A):  # 父类1，继承A
    def say(self):
        print("B的say方法")


class C(A):  # 父类2，继承A
    def say(self):
        print("C的say方法")


class D(B, C):  # 子类，继承B和C
    pass  # 未重写say方法


# 问题：D的对象调用say()，会执行B还是C的方法？
d = D()
print(D.__mro__)
d.say()  # 输出：B的say方法（为什么？）
