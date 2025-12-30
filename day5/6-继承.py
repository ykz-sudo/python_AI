# 作者: 王道 龙哥
# 2025年12月27日10时49分55秒
# xxx@qq.com
class Father:
    def __init__(self):
        self.gender = 'man'

    def walk(self):
        print('爱好散步行走')

class Son(Father):
    pass

if __name__ == '__main__':
    xiaoming=Son()
    print(xiaoming.gender)
    xiaoming.walk()