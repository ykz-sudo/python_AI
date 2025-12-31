# 作者: 王道 龙哥
# 2025年12月31日11时19分26秒
# xxx@qq.com
class TreeNode:
    def __init__(self, value):
        self.value = value
        self.left = None  # 左孩子
        self.right = None


class Tree:
    def __init__(self):
        self.root = None  # 树根
        self.queue = []  # 辅助队列

    def insert(self, node: TreeNode):
        # 放入队列
        self.queue.append(node)
        if self.root is None:  # 如果树为空
            self.root = node  # 新结点作为树根
        else:
            if self.queue[0].left is None:  # 判断父亲的左孩子是否为空
                self.queue[0].left = node
            else:
                self.queue[0].right = node  # 放到右孩子
                self.queue.pop(0)  # 出队

    def pre_order(self, current_node: TreeNode):
        """
        前序遍历，即深度优先遍历
        :param current_node:
        :return:
        """
        if current_node:
            print(current_node.value, end=' ')
            self.pre_order(current_node.left)
            self.pre_order(current_node.right)

    def mid_order(self, current_node: TreeNode):
        if current_node:
            self.mid_order(current_node.left)
            print(current_node.value, end=' ')
            self.mid_order(current_node.right)

    def last_order(self, current_node: TreeNode):
        if current_node:
            self.last_order(current_node.left)
            self.last_order(current_node.right)
            print(current_node.value, end=' ')

    def level_order(self):
        """
        层序遍历，即广度优先遍历
        :return:
        """
        queue = [self.root]
        while queue:
            queue_head: TreeNode = queue.pop(0)
            print(queue_head.value, end=' ')  # 打印
            if queue_head.left:  # 如果左孩子不为空，左孩子入队
                queue.append(queue_head.left)
            if queue_head.right:  # 如果右孩子不为空，右孩子入队
                queue.append(queue_head.right)


if __name__ == '__main__':
    tree = Tree()
    for i in range(1, 11):
        new_node = TreeNode(i)  # 实例化一个新结点对象
        tree.insert(new_node)
    # 前序遍历
    tree.pre_order(tree.root)
    print()
    # 中序遍历
    tree.mid_order(tree.root)
    print()
    # 后序遍历
    tree.last_order(tree.root)
    print()
    # 层序遍历
    tree.level_order()

