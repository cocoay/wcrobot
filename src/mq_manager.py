#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import pika
from constant import mq_username, mq_password, mq_host


class MQBase(object):

    def __init__(self,
                 connection,
                 queue,
                 exchange=None,
                 routing_key=None,
                 durable=False):
        if not exchange:
            exchange = queue + "_exchange"

        if not routing_key:
            routing_key = ""

        # 创建频道
        channel = connection.channel()
        # 创建交换器 type = direct, 是否持久化
        channel.exchange_declare(exchange, durable=durable)
        # 创建队列，是否持久化
        channel.queue_declare(queue=queue, durable=durable)

        self.connection = connection
        self.queue = queue
        self.exchange = exchange
        self.routing_key = routing_key
        self.durable = durable
        self.channel = channel

    @staticmethod
    def setup_conn():
        credentials = pika.PlainCredentials(mq_username, mq_password)
        params = pika.ConnectionParameters(mq_host, credentials=credentials)
        connection = pika.BlockingConnection(params)
        return connection


class MQProducer(MQBase):
    def __init__(self, queue):
        connection = MQBase.setup_conn()
        super().__init__(connection, queue)
        # 消息是否持久化
        properties = pika.BasicProperties()
        if self.durable:
            properties.delivery_mode = 2
        self.properties = properties

    def publish(self, body):
        self.channel.basic_publish(self.exchange, self.routing_key, body,
                                   self.properties)


class MQConsumer(MQBase):
    def __init__(self, queue, callback=None):
        connection = MQBase.setup_conn()
        super().__init__(connection, queue)
        # prefetch_count=1, 完成任务之后，才会再次接收到任务
        self.channel.basic_qos(prefetch_count=1)
        # 交换器绑定队列
        self.channel.queue_bind(queue, self.exchange, self.routing_key)
        is_func = (callback and callable(callback))
        self.callback = None if not is_func else callback
        # self.start_consuming()

    def consumer_callback(self, channel, method, properties, body):
        callback = self.callback
        if callback:
            callback(body)
        channel.basic_ack(delivery_tag=method.delivery_tag)

    def start_consuming(self):
        self.channel.basic_consume(self.consumer_callback, self.queue)
        self.channel.start_consuming()


def main():
    def callback(body):
        print(body)

    queue_name = "test_queue"
    producer = MQProducer(queue_name)
    producer.publish("测试MQaa")
    consumer = MQConsumer(queue_name, callback=callback)
    consumer.start_consuming()


if __name__ == '__main__':
    main()
