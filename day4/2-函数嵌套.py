# 作者: 王道 龙哥
# 2025年12月26日09时59分46秒
# xxx@qq.com


def testA():
    print('---- testA start----')
    # 嵌套调用函数B
    testB()
    print('---- testA end----')


def testB():
    print('---- testB start----')
    print('这里是testB函数执行的代码...(省略)...')
    print('---- testB end----')


# 调用函数
testA()
