# 作者: 王道 龙哥
# 2025年12月25日09时54分13秒
# xxx@qq.com
# s = '123456"7'
# s1 = "abc'd"
# s2 = '12\"\''
# s5 = """
# 我是安卓人
# 	你是苹果人
# 		他是鸿蒙人
# 			我们都是地球人
# 			'"
# """


def str_slice():
    """
    字符串切片
    :return:
    """
    name = "cskaoyan2025"
    # 字符串前5个字符
    print(name[0:5])
    # 隔一个取一个
    print(name[::2])
    # 截取从第5个到结尾
    print(name[5:])

    # 从-4开始拿
    print(name[-4:])
    # 从-4拿到-2位置
    print(name[-4:-2])

    # 步长为负,逆序
    print(name[::-1])
    # 当步长为负时，开始要比结束大
    print(name[-1:-5:-1])


def use_str_method():
    s = 'hello world'
    print(s[0])
    # 没找到返回-1
    print(s.find('wo'))
    s1 = 'dbjakbdj123bkabdjka12bjkabdjk123bjadbja123bfegbrk123;jfpej12'
    print(s1.replace('123', '456', 1))
    print(s1)  # s1是没变的
    print(s1.count('123'))  # 统计子串出现的次数
    s2 = 'hello,world,how are you'
    str_list = s2.split(',')  # 默认进行空格分割
    print(str_list)
    str_list = ['hello', 'world', 'how']
    new_str = ' '.join(str_list)  # 拼接元素
    print(new_str)
    str_list = 'hello\nworld\nhowareyou'
    print(str_list.splitlines())


# str_slice()
use_str_method()
