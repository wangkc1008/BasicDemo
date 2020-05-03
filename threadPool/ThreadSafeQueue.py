# -*- coding=utf-8 -*-
import time
import threading
import numpy as np


class ThreadSafeException(object):
    pass


class ThreadSafeQueue(object):

    def __init__(self, max_size=0):
        self.queue = []
        self.max_size = max_size
        self.lock = threading.Lock()  # 互斥量
        self.condition = threading.Condition()  # 条件变量

    def size(self):
        """
        获取当前队列的大小
        :return: 队列长度
        """
        self.lock.acquire()
        size = len(self.queue)
        self.lock.release()
        return size

    def put(self, item):
        """
        将单个元素放入队列
        :param item:
        :return:
        """
        # 队列已满 max_size为0表示无限大
        if self.max_size != 0 and self.size() >= self.max_size:
            return ThreadSafeException()

        self.lock.acquire()
        self.queue.append(item)
        self.lock.release()
        self.condition.acquire()
        self.condition.notify()
        self.condition.release()

        return item

    def batch_put(self, item_list):
        """
        批量添加元素
        :param item_list:
        :return:
        """
        if not isinstance(item_list, list):
            item_list = list(item_list)

        res = [self.put(item) for item in item_list]

        return res

    def pop(self, block=False, timeout=0):
        """
        从队列头部取出元素
        :param block:
        :param timeout:
        :return:
        """
        if self.size() == 0:
            if block:
                self.condition.acquire()
                self.condition.wait(timeout)
                self.condition.release()
            else:
                return None

        self.lock.acquire()
        item = None
        if len(self.queue):
            item = self.queue.pop()
        self.lock.release()

        return item

    def get(self, index):
        """
        获取指定位置的元素
        :param index:
        :return:
        """
        if self.size() == 0 or index >= self.size():
            return None

        self.lock.acquire()
        item = self.queue[index]
        self.lock.release()

        return item


if __name__ == '__main__':
    thread_queue = ThreadSafeQueue(10)

    def producer():
        while True:
            thread_queue.batch_put(np.arange(1, 10))
            time.sleep(10)

    def consumer():
        while True:
            # item = thread_queue.pop(block=True, timeout=2)
            item = thread_queue.get(2)
            if item is not None:
                print('get value from queue is %s' % item)
            else:
                print(item)

            time.sleep(2)

    t1 = threading.Thread(target=producer)
    t2 = threading.Thread(target=consumer)
    t1.start()
    t2.start()
    t1.join()
    t2.join()
