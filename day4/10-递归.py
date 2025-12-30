# 作者: 王道 龙哥
# 2025年12月26日15时24分14秒
# xxx@qq.com
import sys

sys.setrecursionlimit(1000000)


def total(n):
    if n == 1:
        return 1
    return n + total(n - 1)


print(total(100000))


def step(n):
    if n == 1 or n == 2:
        return n
    return step(n - 1) + step(n - 2)


print([step(n) for n in range(1, 10)])
