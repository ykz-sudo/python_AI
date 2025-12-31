# 作者: 王道 龙哥
# 2025年12月31日14时48分12秒
# xxx@qq.com
import random
import time
import sys

sys.setrecursionlimit(1000000)


class Sort:
    def __init__(self, length):
        # self.arr = [3, 87, 2, 93, 78, 56, 61, 38, 12, 40]
        self.arr = []
        self.length = length
        self.__random_num()

    def __random_num(self):
        """

        :return:
        """
        for i in range(self.length):
            self.arr.append(random.randint(0, 99))

    def partition(self, left, right):
        arr = self.arr
        k = left
        # 随机一个位置，把这个位置和分割点交换
        random_pos = random.randint(left, right - 1)
        arr[right], arr[random_pos] = arr[random_pos], arr[right]
        for i in range(left, right):
            if arr[i] < arr[right]:
                arr[i], arr[k] = arr[k], arr[i]
                k += 1
        arr[right], arr[k] = arr[k], arr[right]
        return k

    def arr_quick(self, left, right):
        if left < right:
            pivot = self.partition(left, right)
            self.arr_quick(left, pivot - 1)
            self.arr_quick(pivot + 1, right)

    def ajust_max_heap(self, ajust_pos, length):
        """
        调整某棵子树为大根堆
        :param ajust_pos: 被调整的位置
        :param length: 列表长度
        :return:
        """
        arr = self.arr
        dad = ajust_pos
        son = 2 * dad + 1
        while son < length:
            if son + 1 < length and arr[son] < arr[son + 1]:  # 判断左孩子如果小于右孩子，就对son+1
                son += 1
            if arr[son] > arr[dad]:  # 大于父亲就交换，交换后，从新把孩子作为父亲，进行下面子树的调整
                arr[son], arr[dad] = arr[dad], arr[son]
                dad = son
                son = 2 * dad + 1
            else:
                break

    def arr_heap(self):
        arr = self.arr
        # 从最后一个父亲，调整到根部,变为大根堆
        for dad in range(self.length // 2 - 1, -1, -1):
            self.ajust_max_heap(dad, self.length)
        for length in range(self.length - 1, 0, -1):
            arr[0], arr[length] = arr[length], arr[0]  # 交换顶部元素和最后一个元素
            self.ajust_max_heap(0, length)  # 把剩余元素继续调整为大根堆

    @staticmethod
    def sort_use_time(func, *args):
        """
        func就是回调函数
        :param func:
        :return:
        """
        start = time.time()
        func(*args)
        end = time.time()
        print(f'排序使用了{end - start}')


if __name__ == '__main__':
    my_sort = Sort(10)
    print(my_sort.arr)  # 排序前打印
    # my_sort.arr_quick(0, my_sort.length - 1)
    # Sort.sort_use_time(my_sort.arr_heap)
    Sort.sort_use_time(my_sort.arr_quick, 0, my_sort.length - 1)
    print(my_sort.arr)  # 排序后打印
