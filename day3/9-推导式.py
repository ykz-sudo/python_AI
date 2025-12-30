# 作者: 王道 龙哥
# 2025年12月25日16时59分27秒
# xxx@qq.com

# 生成式
num_list = [i ** 2 for i in range(10) if i % 2 == 0]
print(num_list)

# 下面的看情况掌握
# 有else的时候，要写前面
num_list = [i if i % 2 == 0 else i ** 2 for i in range(10)]
print(num_list)
# 嵌套
num_list = [[j for j in range(i)] for i in range(1, 5)]
print(num_list)
# 二维变一维，前面是外层循环，后面是内存循环
num_list_2 = [i for inner_list in num_list for i in inner_list]
print(num_list_2)

print('-' * 50)
# 字典生成式
fruits = ['apple', 'banana', 'orange']

dict1 = {}
for key, value in enumerate(fruits):
    dict1[key] = value
print(dict1)

print({value: key for key, value in enumerate(fruits)})

student_scores = {'Alice': 95, 'Bob': 88, 'Charlie': 92, 'David': 70}
score2 = {k: v for k, v in student_scores.items() if v >= 90}
print(score2)
numbers = [1, 2, 2, 3, 4, 4]
print(set(i ** 2 for i in numbers))
