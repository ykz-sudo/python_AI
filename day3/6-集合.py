# 作者: 王道 龙哥
# 2025年12月25日15时59分16秒
# xxx@qq.com
myset1 = set("wangdao")  # 通过字符串创建集合
list2 = [10, 20, 30, 40, 10, 20]
myset2 = set(list2)  # 通过列表创建集合
tuple3 = (10, 20, 30, 40, 10, 20)
myset3 = set(tuple3)

print(myset1)
print(myset2)
print(myset3)

print(41 in myset2)  # 判断某个元素有没有在集合中

myset1.add(40)
print(myset1)
myset1.discard(40)
print(myset1)

print('-' * 50)
set1 = {1, 2, 3, 4}
set2 = {3, 4, 5, 6}

# 并集
union_set = set1 | set2
print(union_set)  # 输出: {1, 2, 3, 4, 5, 6}

# 差集
diff_set = set1 - set2
print(diff_set)  # 输出: {1, 2}

# 交集
inter_set = set1 & set2
print(inter_set)
