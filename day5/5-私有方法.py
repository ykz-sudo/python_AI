# 作者: 王道 龙哥
# 2025年12月27日10时39分26秒
# xxx@qq.com
class Girl:
    def __init__(self, age):
        self.__age = age


    def __secret(self):
        """
        只能在类内部被调用
        :return:
        """
        print(self.__age)

    def boy_friend(self):
        self.__secret()


if __name__ == '__main__':
    xiaoli = Girl(20)
    xiaoli.boy_friend()

