#!/usr/bin/env python3
# -*- coding=utf-8 -*-

from mq_manager import MQProducer, MQConsumer
import threading
import os
import time


def task_1():
    print('task_1', os.getpid())
    mq_p = MQProducer('mq_queue')
    while True:
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        mq_p.publish(t)


def task_2():
    print('task_2', os.getpid())

    def callback(body):
        print(body)

    mq_c = MQConsumer('mq_queue', callback=callback)
    mq_c.start_consuming()


def main():
    print('\n======task_start======')
    t1 = threading.Thread(target=task_1, name='task_1')
    t2 = threading.Thread(target=task_2, name='task_2')
    t1.start()
    t2.start()
    print('======task_end======\n')


if __name__ == '__main__':
    main()
