# 作者: 王道 龙哥
# 2025年12月29日15时00分18秒
# xxx@qq.com

import calc
import random

print(calc.__name__)
print(__name__)
print(calc.pi)
# print(calc.m)  #不可访问
# calc.use()

# 模块的其他属性
print(random.__file__)
print(calc.__file__)

print('-'*50)

from calc2 import User
# print(sum1(1,2,3))
# user=User('张三',20)
# user.print_info()
# import calc2
# user=calc2.User('张三',20)
# user.print_info()