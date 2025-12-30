# 作者: 王道 龙哥
# 2025年12月30日15时50分59秒
# xxx@qq.com
import re

original_data = 'wangdao@cskaoyan.com'
ret=re.match('wangdao',original_data)
if ret:
    print(ret.group())


#匹配手机号
print('手机号匹配练习','-'*50)
pattern=r'1[34578]\d{9}' #手机号正则表达式
text1 = "13812345678"  # 合法手机号
text2 = "12345678901"  # 非法手机号（开头不符）

ret=re.match(pattern,text1)
if ret:
    print(ret.group())
else:
    print('非法手机号')

ret=re.match(pattern,text2)
if ret:
    print(ret.group())
else:
    print('非法手机号')

print('单个字母匹配练习','-'*50)
pattern = r"[a-zA-Z]\d[a-zA-Z]"
texts = ["a1b", "B2C", "x3y", "1ab"]
for text in texts:
    ret=re.match(pattern,text)
    if ret:
        print(ret.group())
    else:
        print(f'{text}未匹配')

print('多个字母匹配练习','-'*50)
pattern = r"\d+"  # 1次或多次数字
texts = ["20", "34bc", "abc", "123"]
for text in texts:
    ret=re.match(pattern,text)
    if ret:
        print(ret.group())
    else:
        print(f'{text}未匹配')

print('多个字母匹配练习','-'*50)
pattern = r"\d*"  # 1次或多次数字
texts = ["20", "34bc", "abc", "123"]
for text in texts:
    ret=re.match(pattern,text)
    if ret:
        print(ret.group())
    else:
        print(f'{text}未匹配')
print('-'*50)
pattern = r"[a-zA-Z]{3,6}"
texts = ["abc", "abcd12", "ab", "abcdefmn"]
for text in texts:
    ret=re.match(pattern,text)
    if ret:
        print(ret.group())
    else:
        print(f'{text}未匹配')

print('邮箱匹配练习','-'*50)
pattern=r'^\w{4,20}@163\.com$'
emails = ["user@163.com", "user@.com", "abc@123", "user@163.com.abc"]
for text in emails:
    ret=re.match(pattern,text)
    if ret:
        print(ret.group())
    else:
        print(f'{text}未匹配')

print('邮箱匹配练习2','-'*50)
pattern=r'^\w{4,20}@(163|qq)\.com$'
emails = ["user@163.com", "user@.com", "abcd123@qq.com", "user@163.com.abc"]
for text in emails:
    ret=re.match(pattern,text)
    if ret:
        print(ret.group())
    else:
        print(f'{text}未匹配')

print('引用分组使用-----')
pattern=r'<(\w+)>.*</\1>'
texts=["<div>你好</div>", "<div>今天天气</h1>"]
for text in texts:
    ret=re.match(pattern,text)
    if ret:
        print(ret.group())
    else:
        print(f'{text}未匹配')