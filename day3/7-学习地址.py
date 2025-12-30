# 作者: 王道 龙哥
# 2025年12月25日16时10分02秒
# xxx@qq.com


a = [1, 2, 3]
b = a.copy()
print(id(a))
print(id(b))
a[0] = 10
print(b)
