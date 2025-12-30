class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age


class Hero(Person):
    def __init__(self, level, rank, name, age):
        super().__init__(name, age)
        self.__level = level
        self.__rank = rank

    def __str__(self):
        return f'姓名：{self.name} 级别：{self.__level} 排名：{self.__rank}'

    def __del__(self):
        print(f'{self.name}倒下了')

    def set_level(self, level):
        if level in ['S', 'A', 'B', 'C']:
            self.__level = level

    def set_rank(self, rank):
        if rank > 0:
            self.__rank = rank

    def __secret(self):
        print(f'{self.name} 是怪人')

    def fight(self):
        self.__secret()


if __name__ == '__main__':
    hero1 = Hero('S', '1', '爆破', '23')
    print(hero1)
    hero1.fight()
    hero2 = Hero('A', '2', '战栗的龙卷', '18')
    print(hero2)
    hero2.set_level('S')
    print(hero2)
