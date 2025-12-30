# 作者: 王道 龙哥
# 2025年12月25日14时36分27秒
# xxx@qq.com
t1 = (1, 2, 3)

print(t1[0])
t1 = ('李云龙', '楚云飞', '谢宝庆', '蟹部落')

for i in t1:
    print(i, end=' ')
print()

tup = ('aa', 'bb', 'cc', 'dd', 'ee', 'bb', 'cc')

# 2. 查找某个元素 index()
print(tup.index('bb'))
print(tup.count('bb'))

tuple1 = (1, 2)
a, b = tuple1
print(a, b)

a, b = b, a
print(f'交换后a {a} b {b}')

new_tuple = (1,)
print(type(new_tuple))
for i in new_tuple:
    print(i)
