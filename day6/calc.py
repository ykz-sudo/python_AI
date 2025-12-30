# 作者: 王道 龙哥
# 2025年12月29日14时42分34秒
# xxx@qq.com
# calc.py（一个简单的模块）
pi = 3.14159  # 模块变量


def add(a, b):  # 模块函数
    return a + b


# def use():
#     """
#     不可以在函数内使用__main__下面的全局变量
#     :return:
#     """
#     print(m, n)


class Calculator:  # 模块类
    def multiply(self, a, b):
        return a * b


if __name__ == '__main__':
    # 写的是本模块的测试代码
    m, n = 1, 2
    print(add(1, 2))
    # use()
