import re
import random
import time
import sys


def use_search():
    text = '我的移动手机号为18364321516，我的电信手机号为15383927664'
    pattern = re.compile(r'1[345789]\d{9}')
    result = pattern.search(text)
    if result:
        print(f'{text} 匹配成功 {result.group()}')


def use_findall():
    text = '我的移动手机号为18364321516，我的电信手机号为15383927664'
    pattern = re.compile(r'1[345789]\d{9}')
    result = pattern.findall(text)
    if result:
        print(f'{text} 匹配成功 {result}')


def use_sub():
    text = '中门大狙架的一坨屎'
    pattern = r'一坨屎'
    new_text = re.sub(pattern, '***', text)
    print(new_text)


def use_split():
    text = 'iphone, huawei; vivo, oppo'
    pattern = r'[, ;]+'
    nex_text = re.split(pattern, text)
    print(nex_text)


class TreeNode:
    def __init__(self, data, left=None, right=None):
        self.data = data
        self.left = left
        self.right = right


class Tree:
    def __init__(self, root=None):
        self.root = root
        self.queue = []

    def add_data(self, data):
        current_node = TreeNode(data)

        if len(self.queue) == 0:
            self.root = current_node
            self.queue.append(current_node)
        else:
            if self.queue[0].left is None:
                self.queue[0].left = current_node
                self.queue.append(current_node)
            else:
                self.queue[0].right = current_node
                self.queue.append(current_node)
                del self.queue[0]

    def insert(self, node: TreeNode):
        self.queue.append(node)
        if self.root is None:
            self.root = node
        else:
            if self.queue[0].left is None:
                self.queue[0].left = node
            else:
                self.queue[0].right = node
                self.queue.pop(0)

    def pre_order(self, node: TreeNode):
        if node is None:
            return
        print(node.data, end=' ')
        self.pre_order(node.left)
        self.pre_order(node.right)

    def in_order(self, node: TreeNode):
        if node is None:
            return
        self.in_order(node.left)
        print(node.data, end=' ')
        self.in_order(node.right)

    def post_order(self, node: TreeNode):
        if node is None:
            return
        self.post_order(node.left)
        self.post_order(node.right)
        print(node.data, end=' ')

    @staticmethod
    def level_order(node: TreeNode):
        queue = [node]
        while queue:
            current_node = queue.pop(0)
            print(current_node.data, end=' ')
            if current_node.left is not None:
                queue.append(current_node.left)
            if current_node.right is not None:
                queue.append(current_node.right)


class Sort:
    def __init__(self, length):
        self.length = length
        self.array = [None] * self.length
        self.__random_num()

    def __random_num(self):
        for i in range(self.length):
            self.array[i] = random.randint(0, 99)

    def partition(self, left, right):
        array = self.array
        k = left
        random_pos = random.randint(left, right - 1)
        array[random_pos], array[right] = array[right], array[random_pos]
        for i in range(left, right):
            if array[i] < array[right]:
                array[i], array[k] = array[k], array[i]
                k += 1
        array[right], array[k] = array[k], array[right]
        return k

    def quick_sort(self, left, right):
        if left < right:
            pivot = self.partition(left, right)
            self.quick_sort(left, pivot - 1)
            self.quick_sort(pivot + 1, right)

    def max_heap(self, pos, length):
        array = self.array
        father = pos
        son = father * 2 + 1

        while son < length:
            if son + 1 < length and array[son] < array[son + 1]:
                son = son + 1
            if array[father] < array[son]:
                array[father], array[son] = array[son], array[father]
                father = son
                son = father * 2 + 1
            else:
                break

    def heap(self):
        array = self.array
        for father in range(self.length // 2 - 1, -1, -1):
            self.max_heap(father, self.length)
        for length in range(self.length - 1, 0, -1):
            array[0], array[length] = array[length], array[0]
            self.max_heap(0, length)


if __name__ == '__main__':
    use_search()
    print('-' * 50)
    use_findall()
    print('-' * 50)
    use_sub()
    print('-' * 50)
    use_split()
    print('-' * 50)

    tree = Tree()
    # for i in range(10):
    #     tree.insert(TreeNode(i))

    for i in range(10):
        tree.add_data(i)

    tree.pre_order(tree.root)
    print()
    tree.in_order(tree.root)
    print()
    tree.post_order(tree.root)
    print()
    tree.level_order(tree.root)
    print()

    my_sort = Sort(10)
    print(my_sort.array)
    # my_sort.quick_sort(0, len(my_sort.array) - 1)
    # print(my_sort.array)
    my_sort.heap()
    print(my_sort.array)

    dict1 = {'name': 'zs', 'age': 20, 'gender': 'male', 'height': 180}
    print(sorted(dict1))
