# 作者: 王道 龙哥
# 2025年12月31日10时58分58秒
# xxx@qq.com
import re
text = "<div>内容1</div><div>内容2</div>"

# 1. 贪婪匹配（.*尽可能多匹配，从第一个<div>到最后一个</div>）
greedy_pattern = r"<div>.*</div>"
print("贪婪匹配：", re.findall(greedy_pattern, text))


# 2. 非贪婪匹配（.*尽可能多匹配，从第一个<div>到最后一个</div>）
non_greedy_pattern = r"<div>(.*?)</div>"
print("非贪婪匹配：", re.findall(non_greedy_pattern, text))

print('r的作用')
text='c:\\dir'
print(text)

print(re.match(r'c:\\',text).group())