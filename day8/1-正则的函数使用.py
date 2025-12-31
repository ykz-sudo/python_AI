# 作者: 王道 龙哥
# 2025年12月31日09时45分23秒
# xxx@qq.com
import re

text = "我的手机号：13812345678，备用号：13987654321"
pattern = r"1[34578]\d{9}"  # 不限制位置，只匹配手机号格式
ret = re.search(pattern, text)
if ret:
    print(f'第一个手机号{ret.group()}')
    print(f'手机号位置{ret.span()}')

print('-' * 50)
result_list = re.findall(pattern, text)
if result_list:
    print(result_list)

print('-' * 50)
text = "这个内容是垃圾，不要传播垃圾信息"
pattern = r"垃圾"
new_text = re.sub(pattern, '-', text, count=1)  # count控制替换次数
print(new_text)

text = "13812345678"
print('-' * 50)
# ()： 表示分组匹配，将内部字符视为一个整体，后续可以提取
pattern = r"(\d{3})(\d{4})(\d{4})"  # 分3个分组（前3/中4/后4位）
new_text = re.sub(pattern, r'\1 \2 \3', text)
print(new_text)

print('-' * 50)
text = "apple banana,orange;grape"
pattern = r"[ ,;]"  # 匹配空格、逗号、分号中的任意一个
result_list = re.split(pattern, text)
print(result_list)

print('时间替换练习', '-' * 50)
text = '2025-12-30 06:55:23'


def add(ret):
    """
    按search通过pattern把匹配到的ret，传入给add
    :param ret:
    :return:
    """
    str_hour = ret.group()
    hour = 8 + int(str_hour)  # 加8个小时
    return ' ' + str(hour)


pattern = r'\s\d{2}'
new_text = re.sub(pattern, add, text)  # add只能是函数名，它是回调函数
print(new_text)

print('-'*50)
pattern = r'(\d{4}-\d{2}-\d{2})\s(\d{2}):(\d{2}):(\d{2})'
ret = re.match(pattern, text)
if ret:
    print(ret.group())
    print(ret.group(1))
    print(ret.group(2))
    print(ret.group(3))
    print(ret.group(4))
