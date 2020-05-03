from cache.DoubleLinkedList import DoubleLinkedList, Node


class LFUNode(Node):

    def __init__(self, key, value):
        """
        LFU节点 增加频率属性
        :param key:
        :param value:
        """
        self.freq = 0
        super(LFUNode, self).__init__(key, value)


class LFUCache(object):

    def __init__(self, capacity=0xffffffff):
        """
        LFU缓存置换算法 最不经常使用
        :param capacity:
        """
        self.capacity = capacity
        self.size = 0
        self.map = {}
        self.freq_map = {}

    def __update_freq(self, node):
        """
        更新节点频率
        :param node:
        :return:
        """
        freq = node.freq

        # 当前节点所在频率存在 在当前频率链表中移除当前节点
        if freq in self.freq_map:
            node = self.freq_map[freq].remove(node)
            # 当前频率链表为空时删除该频率链表
            if self.freq_map[freq].size == 0:
                del self.freq_map[freq]

        # 将节点按照新频率写入频率链表
        freq += 1
        node.freq = freq
        if freq not in self.freq_map:
            self.freq_map[freq] = DoubleLinkedList()
        self.freq_map[freq].append(node)

        return node

    def get(self, key):
        """
        获取元素
        :return:
        """
        # 节点不存在
        if key not in self.map:
            return None

        old_node = self.map.get(key)
        new_node = self.__update_freq(old_node)
        self.map[key] = new_node
        return new_node.value

    def put(self, key, value):
        """
        设置元素
        :param key:
        :param value:
        :return:
        """
        # 节点已存在 更新频率
        if key in self.map:
            old_node = self.map.get(key)
            old_node.value = value
            new_node = self.__update_freq(old_node)
            self.map[key] = new_node
        else:
            # 节点容量达到上限 移除最小频率链表头部的节点
            if self.size >= self.capacity:
                min_freq = min(self.freq_map)
                node = self.freq_map[min_freq].pop()
                del self.map[node.key]
                self.size -= 1

            new_node = LFUNode(key, value)
            new_node = self.__update_freq(new_node)
            self.map[key] = new_node
            self.size += 1

        return new_node

    def print(self):
        """
        打印当前链表
        :return:
        """
        for freq, link in self.freq_map.items():
            print("frequencies： %d" % freq)
            link.print()
        # print(self.freq_map[1].size)


if __name__ == '__main__':
    lfu_cache = LFUCache(4)
    lfu_cache.put(1, 1)
    lfu_cache.print()
    lfu_cache.put(2, 2)
    lfu_cache.print()
    print(lfu_cache.get(1))
    lfu_cache.print()
    lfu_cache.put(3, 3)
    lfu_cache.print()
    lfu_cache.put(4, 4)
    lfu_cache.print()
    lfu_cache.put(5, 5)
    lfu_cache.print()
    print(lfu_cache.get(2))
    lfu_cache.put(4, 400)
    lfu_cache.print()
