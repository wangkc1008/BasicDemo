from cache.DoubleLinkedList import DoubleLinkedList, Node


class FIFOCache(object):

    def __init__(self, capacity=0xffffffff):
        """
        FIFO缓存置换算法
        :param capacity:
        """
        self.capacity = capacity
        self.map = {}
        self.size = 0
        self.list = DoubleLinkedList(capacity)

    def get(self, key):
        """
        获取元素
            不存在 返回None
            已存在 则返回缓存值
        :param key:
        :return:
        """
        # 当前缓存中不存在
        if key not in self.map:
            return None

        # 当前缓存中存在
        node = self.map.get(key)

        return node.value

    def put(self, key, value):
        """
        添加元素
            已存在 更新值并添加至链表尾部
            不存在 判断缓存容量大小后添加
        :param key:
        :param value:
        :return: 已添加的节点
        """
        # 当前缓存中已存在
        if key in self.map:
            node = self.map.get(key)
            self.list.remove(node)
            node.value = value
            self.list.append(node)
        else:
            # 缓存容量达到上限 删除头结点
            if self.size >= self.capacity:
                old_node = self.list.pop()
                del self.map[old_node.key]
                self.size -= 1

            node = Node(key, value)
            self.map[key] = node
            self.list.append(node)
            self.size += 1

        return node

    def print(self):
        """
        打印当前链表
        :return:
        """
        self.list.print()
        # print(self.map)


if __name__ == '__main__':
    fifo_cache = FIFOCache(2)
    fifo_cache.put(1, 1)
    fifo_cache.print()
    fifo_cache.put(2, 2)
    fifo_cache.print()
    print(fifo_cache.get(2))
    fifo_cache.put(3, 3)
    fifo_cache.print()
    print(fifo_cache.get(1))
    fifo_cache.put(2, 4)
    fifo_cache.print()