# 作者: 王道 龙哥
# 2025年12月25日17时19分20秒
# xxx@qq.com

def homework4():
    print(sum([i for i in range(1, 100) if i % 2 == 1]))


def homework5():
    for i in range(1, 10):
        for j in range(1, i + 1):
            print(f'{j}*{i}={j * i:2d}', end=' ')
        print()


def homework6():
    while True:
        num = int(input('请输入一个整数:'))
        count = 0  # 统计有多少位为1
        flag = 1
        i = 1
        while i <= 64:
            if num & flag:
                count += 1
            flag <<= 1
            i += 1
        print(count)


# homework4()
# homework5()
homework6()
