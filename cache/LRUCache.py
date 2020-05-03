from cache.DoubleLinkedList import DoubleLinkedList, Node

class LRUCache(object):

    def __init__(self, capacity=0xffffffff):
        """
        LRU缓存置换算法 最近最少使用
        :param capacity:
        """
        self.capacity = capacity
        self.size = 0
        self.map = {}
        self.list = DoubleLinkedList(capacity)

    def get(self, key):
        """
        获取元素
            获取元素不存在 返回None
            获取元素已存在 将节点从当前位置删除并添加至链表头部
        :param key:
        :return:
        """
        # 元素不存在
        if key not in self.map:
            return None

        node = self.map.get(key)
        self.list.remove(node)
        self.list.append_front(node)

        return node.value

    def put(self, key, value):
        """
        添加元素
            被添加的元素已存在 更新元素值并已到链表头部
            被添加的元素不存在
                链表容量达到上限 删除尾部元素
                链表容量未达上限 添加至链表头部
        :param key:
        :param value:
        :return:
        """
        if key in self.map:
            node = self.map.get(key)
            node.value = value
            self.list.remove(node)
            self.list.append_front(node)
        else:
            if self.size >= self.capacity:
                old_node = self.list.remove()
                del self.map[old_node.key]
                self.size -= 1

            node = Node(key, value)
            self.map[key] = node
            self.list.append_front(node)
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
    lru_cache = LRUCache(3)
    lru_cache.put(1, 1)
    lru_cache.print()
    lru_cache.put(2, 2)
    lru_cache.print()
    print(lru_cache.get(1))
    lru_cache.print()
    lru_cache.put(3, 3)
    lru_cache.print()
    lru_cache.put(1, 100)
    lru_cache.print()
    lru_cache.put(4, 4)
    lru_cache.print()
    print(lru_cache.get(1))
    lru_cache.print()