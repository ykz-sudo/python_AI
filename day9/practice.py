import random


def use_sorted():
    """
    sorted()函数
    :return:
    """
    tup = [(3, 5), (1, 2), (2, 4), (3, 1), (1, 3)]
    sored_tup = sorted(tup, key=lambda x: (x[0], -x[1]))
    print(sored_tup)


class Sort:
    def __init__(self, length):
        self.length = length
        self.array = []
        self.__random_num()

    def __random_num(self):
        for i in range(self.length):
            self.array.append(str(random.randint(0, 120)))

    def max_heap(self, pos, length, key):
        array = self.array
        father = pos
        son = father * 2 + 1

        while son < length:
            if son + 1 < length and key(array[son]) < key(array[son + 1]):
                son = son + 1
            if key(array[father]) < key(array[son]):
                array[father], array[son] = array[son], array[father]
                father = son
                son = father * 2 + 1
            else:
                break

    def heap(self):
        array = self.array
        for father in range(self.length // 2 - 1, -1, -1):
            self.max_heap(father, self.length, len)
        for length in range(self.length - 1, 0, -1):
            array[0], array[length] = array[length], array[0]
            self.max_heap(0, length, len)


if __name__ == '__main__':
    use_sorted()

    my_sort = Sort(10)
    print(my_sort.array)

    my_sort.heap()
    print(my_sort.array)
