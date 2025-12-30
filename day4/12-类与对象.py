# 作者: 王道 龙哥
# 2025年12月26日16时13分04秒
# xxx@qq.com

class Car:
    def __init__(self, name):
        self.name = name

    def run(self):
        print(f'{self.name}车跑起来')
        self.sound()

    def sound(self):
        print(f'发出跑车声音')


wen_jie = Car('问界')
xiao_mi = Car('小米')

print(wen_jie.name)
print(xiao_mi.name)
wen_jie.run()
xiao_mi.run()
wen_jie.name='问界1'
print(wen_jie.name)
# wen_jie.color='红色'
# print(wen_jie.color)

