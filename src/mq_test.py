#!/usr/bin/env python3
# -*- coding=utf-8 -*-

from mq_manager import MQProducer, MQConsumer
import multiprocessing
import os
import time


def task_1():
    print('task_1', os.getpid())
    mq_p = MQProducer('mq_queue')
    while True:
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        mq_p.publish(t)
        time.sleep(10)


def task_2():
    print('task_2', os.getpid())

    def callback(body):
        print(body)

    mq_c = MQConsumer('mq_queue', callback=callback)
    mq_c.start_consuming()


def main():
    print('\n======task_start======')
    # 停止调试，子进程会变成僵尸进程，需要手动处理
    pool = multiprocessing.Pool(2)
    pool.apply_async(task_1)
    pool.apply_async(task_2)
    pool.close()
    pool.join()
    print('======task_end======\n')


if __name__ == '__main__':
    main()
