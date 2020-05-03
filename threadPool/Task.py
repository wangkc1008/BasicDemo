# -*- coding=utf-8 -*-
import uuid
import threading


class Task(object):

    def __init__(self, func, *args, **kwargs):
        """
        基本任务对象初始化
        :param func:
        :param args:
        :param kwargs:
        """
        self.id = uuid.uuid4()
        self.callable = func
        self.args = args
        self.kwargs = kwargs

    def __str__(self):
        return 'Task id: %s' % str(self.id)


class AsyncTask(Task):

    def __init__(self, func, *args, **kwargs):
        """
        异步任务对象初始化
        :param callable:
        """
        super(AsyncTask, self).__init__(func, *args, **kwargs)
        self.result = None
        self.condition = threading.Condition()

    def set_result(self, result):
        """
        设置返回结果
        :param result:
        :return:
        """
        self.condition.acquire()
        self.result = result
        self.condition.notify()
        self.condition.release()

    def get_result(self):
        """
        获取返回结果 结果不存在时会阻塞当前线程
        :return:
        """
        self.condition.acquire()
        if not self.result:
            self.condition.wait()
        result = self.result
        self.condition.release()
        return result