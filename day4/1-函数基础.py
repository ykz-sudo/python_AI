# 作者: 王道 龙哥
# 2025年12月26日09时46分02秒
# xxx@qq.com
def calculate_area(r,m):
    area = 3.14 * r ** 2
    return area


# 2. 调用函数
area1 = calculate_area(2)  # 计算半径为2的圆的面积
area2 = calculate_area(5.5)  # 计算半径为2的圆的面积
area3 = calculate_area(8)  # 计算半径为2的圆的面积

# 打印数据
print(f"半径为2的圆的面积:{area1}")
print(f"半径为5的圆的面积:{area2}")
print(f"半径为8的圆的面积:{area3}")

# 定义字典
dict1 = {"zs": 88, "ls": 100, "ww": 85, 'zl': 62}


def score_level(score):
    """
    把分数转换为A，B，C，D
    :param score: 分数
    :return: 返回级别
    """
    if score > 90:
        return 'A'
    elif score > 80:
        return 'B'
    elif score > 70:
        return 'C'
    else:
        return 'D'


dict2 = {k: score_level(v) for k, v in dict1.items()}
print(dict2)
