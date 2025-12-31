# 作者: 王道 龙哥
# 2025年12月31日10时50分52秒
# xxx@qq.com
import re
pattern = re.compile(r"1[34578]\d{9}")

# 多次使用预编译的Pattern对象
texts = ["文本1：13812345678", "文本2：13987654321", "文本3：abc123"]
for text in texts:
    ret=pattern.search(text)
    if ret:
        print(ret.group())
    else:
        print(f'{text}没找手机号')

print('使用flags----------------------')
pattern = r"hello"
text = "Hello HELLO hello"

# 不忽略大小写：只匹配小写hello
print(re.findall(pattern, text))
print(re.findall(pattern, text,re.I))

print('-'*50)
pattern = r"hello.world"
text = "hello\nworld"
print(re.findall(pattern, text,re.S))