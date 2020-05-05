# -*- coding=utf-8 -*-
from threadPool.Task import Task, AsyncTask
from threadPool.ThreadSafeQueue import ThreadSafeQueue
import threading
import psutil


class ThreadProcess(threading.Thread):

    def __init__(self, task_queue, *args, **kwargs):
        """
        线程处理方法初始化
        :param task_queue:
        :param args:
        :param kwargs:
        """
        super(ThreadProcess, self).__init__(*args, **kwargs)
        self.dismiss_flag = threading.Event()  # 任务停止的标记
        self.task_queue = task_queue
        self.args = args
        self.kwargs = kwargs

    def run(self):
        """
        线程运行方法
        :return:
        """
        while True:
            # 线程停止标志设定则停止执行
            if self.dismiss_flag.is_set():
                break
            # task对象是否是Task的实例
            task = self.task_queue.pop()
            if not isinstance(task, Task):
                continue

            print('task id:%d' % task.id)
            # print(type(task))
            result = task.callable(*task.args, **task.kwargs)
            # 如果是异步任务 设置返回结果
            if isinstance(task, AsyncTask):
                print('set result:%d' % task.id)
                task.set_result(result)

    def __dismiss(self):
        self.dismiss_flag.set()

    def stop(self):
        """
        线程停止方法
        :return:
        """
        self.__dismiss()


class ThreadPool:

    def __init__(self, size=0):
        if not size:
            size = psutil.cpu_count() * 2
        print('size is %d' % size)
        self.size = size
        # 任务队列 存放待处理的任务
        self.task_queue = ThreadSafeQueue()
        # 线程池
        self.pool = ThreadSafeQueue(size)

        for i in range(self.size):
            print('put thread:%d' % i)
            self.pool.put(ThreadProcess(self.task_queue))

    def start(self):
        """
        开启线程池
        :return:
        """
        for i in range(self.pool.size()):
            print('start thread:%d' % i)
            thread = self.pool.get(i)
            thread.start()

    def join(self):
        """
        停止线程池
        :return:
        """
        for i in range(self.pool.size()):
            print('join thread:%d' % i)
            thread = self.pool.get(i)
            thread.stop()
        # 线程池未完全停止
        if not self.pool:
            thread = self.pool.pop()
            thread.join()

    def put(self, task):
        """
        将任务放入线程池
        :param task:
        :return:
        """
        if not isinstance(task, Task):
            raise TaskTypeException()
        res = self.task_queue.put(task)
        print('put task %d' % task.id)

        return res

    def batch_put(self, task_list):
        """
        向线程池中批量添加任务
        :param task_list:
        :return:
        """
        if not isinstance(task_list, list):
            task_list = list(task_list)

        return [self.put(task) for task in task_list]

    def size(self):
        """
        获取线程池的大小
        :return:
        """

        return self.pool.size()


class TaskTypeException(Exception):
    pass