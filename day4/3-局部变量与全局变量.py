# 作者: 王道 龙哥
# 2025年12月26日10时29分01秒
# xxx@qq.com

b = 100  # 全局变量


def testA():
    a = 100
    print(a)
    print(f'testA中的b {b}')


testA()


# print(a)

def func2():
    print(f'func2函数, b: {b}')  # 访问全局变量b，并打印变量b存储的数据


def func3():
    global b  # 在函数内要修改全局变量的值，需要使用global
    print(f'修改b之前 func3函数, b: {b}')
    b = 300
    print(f'func3函数, b: {b}')  # 访问全局变量b，并打印变量b存储的数据


# 调用函数
func2()  # 100
func3()  # 100
print(b)
