# -*- coding=utf-8 -*-
import time
import threading
import random


class ThreadSafeException(Exception):
    pass


class ThreadSafeQueue(object):

    def __init__(self, max_size=0):
        self.queue = []
        self.max_size = max_size  # max_size为0表示无限大
        self.lock = threading.Lock()  # 互斥量
        self.condition = threading.Condition()  # 条件变量

    def size(self):
        """
        获取当前队列的大小
        :return: 队列长度
        """
        # 加锁
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

        # 加锁
        self.lock.acquire()
        self.queue.append(item)
        self.lock.release()
        self.condition.acquire()
        # 通知等待读取的线程
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
        :param block: 是否阻塞线程
        :param timeout: 等待时间
        :return:
        """
        if self.size() == 0:
            if block:
                self.condition.acquire()
                self.condition.wait(timeout)
                self.condition.release()
            else:
                return None

        # 加锁
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

        # 加锁
        self.lock.acquire()
        item = self.queue[index]
        self.lock.release()

        return item


def thread_queue_test_1():
    thread_queue = ThreadSafeQueue(10)

    def producer():
        while True:
            thread_queue.put(random.randint(0, 10))
            time.sleep(2)

    def consumer():
        while True:
            print('current time before pop is %d' % time.time())
            item = thread_queue.pop(block=True, timeout=3)
            # item = thread_queue.get(2)
            if item is not None:
                print('get value from queue is %s' % item)
            else:
                print(item)
            print('current time after pop is %d' % time.time())

    t1 = threading.Thread(target=producer)
    t2 = threading.Thread(target=consumer)
    t1.start()
    t2.start()
    t1.join()
    t2.join()


def thread_queue_test_2():
    thread_queue = ThreadSafeQueue(10)

    def producer():
        while True:
            thread_queue.put(random.randint(0, 10))
            time.sleep(2)

    def consumer(name):
        while True:
            item = thread_queue.pop(block=True, timeout=1)
            # item = thread_queue.get(2)
            if item is not None:
                print('%s get value from queue is %s' % (name, item))
            else:
                print('%s get value from queue is None' % name)

    t1 = threading.Thread(target=producer)
    t2 = threading.Thread(target=consumer, args=('thread1',))
    t3 = threading.Thread(target=consumer, args=('thread2',))
    t1.start()
    t2.start()
    t3.start()
    t1.join()
    t2.join()
    t3.join()


if __name__ == '__main__':
    # thread_queue_test_1()
    thread_queue_test_2()