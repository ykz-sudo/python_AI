# 作者: 王道 龙哥
# 2025年12月29日14时27分46秒
# xxx@qq.com
def calculate_average(numbers):
    assert len(numbers) > 0, 'numbers 列表不能为空'
    return sum(numbers) / len(numbers)


# 正常情况：列表非空
print(calculate_average([1, 2, 3]))  # 输出：2.0

try:
    # 异常情况：列表为空，触发断言异常
    calculate_average([])  # 抛出AssertionError: 列表不能为空，无法计算平均值
except Exception as e:
    print(e)
