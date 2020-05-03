# -*- coding=utf8 -*-
import time
from threadPool.Task import Task, AsyncTask
from threadPool.Pool import ThreadPool


class SimpleTask(Task):

    def __init__(self, func, *args, **kwargs):
        super(SimpleTask, self).__init__(func, *args, **kwargs)

#
class SimpleAsyncTask(AsyncTask):

    def __init__(self, func, *args, **kwargs):
        super(SimpleAsyncTask, self).__init__(func, *args, **kwargs)


def counter(name):
    sum = 0
    for i in range(100):
        sum += i
    # print(name, sum)
    time.sleep(5)
    return sum


def task_test_1():

    start_time = time.time()

    thread_pool = ThreadPool()
    print('thread pool not start')
    thread_pool.start()
    print('thread pool already start')
    for s in range(10):
        task = SimpleTask(func=counter, name=('thread' + str(s)))
        thread_pool.put(task)

    end_time = time.time()
    print('total time is %d' % (end_time - start_time))


def task_test_2():

    start_time = time.time()

    thread_pool = ThreadPool()
    print('thread pool not start')
    thread_pool.start()
    print('thread pool already start')
    task = SimpleTask(func=counter, name=('thread'))
    thread_pool.put(task)

    end_time = time.time()
    print('total time is %d' % (end_time - start_time))


def async_test_1():

    def async_counter(name):
        sum = 0
        for i in range(100):
            sum += i
        print(name, sum)
        return sum

    start_time = time.time()

    thread_pool = ThreadPool()
    print('thread pool not start')
    thread_pool.start()
    print('thread pool already start')
    for s in range(10):
        task = SimpleAsyncTask(func=async_counter, name=('task' + str(s)))
        thread_pool.put(task)
        print('result from thread %d is %s' % (task.id, task.get_result()))

    end_time = time.time()
    print('total time is %d' % (end_time - start_time))


# 等待结果
def async_test_2():

    def async_counter():
        sum = 0
        for i in range(100):
            sum += i
        time.sleep(5)
        return sum

    start_time = time.time()

    thread_pool = ThreadPool()
    print('thread pool not start')
    thread_pool.start()
    print('thread pool already start')
    task = SimpleAsyncTask(func=async_counter)
    thread_pool.put(task)
    print('result from thread %d is %s' % (task.id, task.get_result()))

    end_time = time.time()
    print('total time is %d' % (end_time - start_time))


# 未进行等待
def async_test_3():

    def async_counter():
        sum = 0
        for i in range(100):
            sum += i
        return sum

    start_time = time.time()

    thread_pool = ThreadPool()
    print('thread pool not start')
    thread_pool.start()
    print('thread pool already start')
    task = SimpleAsyncTask(func=async_counter)
    thread_pool.put(task)
    time.sleep(5)
    print('result from thread %d is %s' % (task.id, task.get_result()))

    end_time = time.time()
    print('total time is %d' % (end_time - start_time))


if __name__ == '__main__':
    # task_test_1()
    # async_test_1()
    # async_test_2()
    async_test_3()