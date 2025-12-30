# 作者: 王道 龙哥
# 2025年12月29日16时56分51秒
# xxx@qq.com
import os
# print(os.getcwd())


file1=open('dir/file1.txt','r',encoding='utf8')
# file1=open('D:\\BaiduSyncdisk\\python_code\\python_code2026\\day6\\dir\\file1.txt','r',encoding='utf8')
txt=file1.read()
print(txt)
file1.close()