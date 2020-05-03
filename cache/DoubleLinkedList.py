class Node:

    def __init__(self, key, value):
        """
        初始化方法
        :param key:
        :param value:
        """
        self.key = key
        self.value = value
        self.prev = None
        self.next = None

    def __str__(self):
        val = '{%s: %s}' % (self.key, self.value)
        return val

    def __repr__(self):
        val = '{%s: %s}' % (self.key, self.value)
        return val


class DoubleLinkedList:

    def __init__(self, capacity=0xffffffff):
        """
        双向链表
        :param capacity: 链表容量 初始化为int的最大值
        :return:
        """
        self.capacity = capacity
        self.size = 0
        self.head = None
        self.tail = None

    def __add_head(self, node):
        """
        向链表头部添加节点
            头部节点不存在 新添加节点为头部和尾部节点
            头部节点已存在 新添加的节点为新的头部节点
        :param node: 要添加的节点
        :return: 已添加的节点
        """
        # 头部节点为空
        if not self.head:
            self.head = node
            self.tail = node
            self.head.next = None
            self.tail.prev = None
        # 头部节点不为空
        else:
            node.next = self.head
            self.head.prev = node
            self.head = node
            self.head.prev = None
        self.size += 1

        return node

    def __add_tail(self, node):
        """
        向链表尾部添加节点
            尾部节点不存在 新添加的节点为头部和尾部节点
            尾部节点已存在 新添加的节点为新的尾部节点
        :param node: 添加的节点
        :return: 已添加的节点
        """
        # 尾部节点为空
        if not self.tail:
            self.tail = node
            self.head = node
            self.head.next = None
            self.tail.prev = None
        # 尾部节点不为空
        else:
            node.prev = self.tail
            self.tail.next = node
            self.tail = node
            self.tail.next = None
        self.size += 1

        return node

    def __remove_head(self):
        """
        删除头部节点
            头部节点不存在 返回None
            头部节点已存在 判断链表节点数量 删除头部节点
        :return: 头部节点
        """
        # 头部节点不存在
        if not self.head:
            return None

        # 链表至少存在两个节点
        head = self.head
        if head.next:
            head.next.prev = None
            self.head = head.next
        # 只存在头部节点
        else:
            self.head = self.tail = None
        self.size -= 1

        return head

    def __remove_tail(self):
        """
        删除尾部节点
            尾部节点不存在 返回None
            尾部节点已存在 判断链表节点数量 删除尾部节点
        :return: 尾部节点
        """
        # 尾部节点不存在
        if not self.tail:
            return None

        # 链表至少存在两个节点
        tail = self.tail
        if tail.prev:
            tail.prev.next = None
            self.tail = tail.prev
        # 只存在尾部节点
        else:
            self.head = self.tail = None
        self.size -= 1

        return tail

    def __remove(self, node):
        """
        删除任意节点
            被删除的节点不存在 默认删除尾部节点
            删除头部节点
            删除尾部节点
            删除其他节点
        :param node: 被删除的节点
        :return: 被删除的节点
        """
        # 被删除的节点不存在
        if not node:
            node = self.tail

        # 删除的是头部节点
        if node == self.head:
            self.__remove_head()
        # 删除的是尾部节点
        elif node == self.tail:
            self.__remove_tail()
        # 删除的既不是头部也不是尾部节点
        else:
            node.next.prev = node.prev
            node.prev.next = node.next
            self.size -= 1

        return node

    def pop(self):
        """
        弹出头部节点
        :return: 头部节点
        """
        return self.__remove_head()

    def append(self, node):
        """
        添加尾部节点
        :param node: 待追加的节点
        :return: 尾部节点
        """
        return self.__add_tail(node)

    def append_front(self, node):
        """
        添加头部节点
        :param node: 待添加的节点
        :return: 已添加的节点
        """
        return self.__add_head(node)

    def remove(self, node=None):
        """
        删除任意节点
        :param node: 待删除的节点
        :return: 已删除的节点
        """
        return self.__remove(node)

    def print(self):
        """
        打印当前链表
        :return:
        """
        node = self.head
        line = ''
        while node:
            line += '%s' % node
            node = node.next
            if node:
                line += '=>'
        print(line)


if __name__ == '__main__':
    double_linked_list = DoubleLinkedList(10)
    nodes = []
    # 构建十个节点的双向列表
    for i in range(10):
        node_item = Node(i, i)
        nodes.append(node_item)

    double_linked_list.append(nodes[0])
    double_linked_list.print()
    double_linked_list.append(nodes[1])
    double_linked_list.print()
    double_linked_list.pop()
    double_linked_list.print()
    double_linked_list.append_front(nodes[2])
    double_linked_list.print()
    double_linked_list.append(nodes[3])
    double_linked_list.print()
    double_linked_list.remove(nodes[3])
    double_linked_list.print()
    double_linked_list.remove()
    double_linked_list.print()
