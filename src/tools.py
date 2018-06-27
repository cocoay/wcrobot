#!/usr/bin/env python3
# -*- coding=utf-8 -*-

from hashlib import md5
import os
import json
import itchat
from itchat.content import TEXT, PICTURE
from itchat.components.messages import get_download_fn
from apscheduler.schedulers.background import BackgroundScheduler
from db_manager import DBManager
from constant import pic_dir, task_time

# 判断文件夹是否存在，不存在就创建
if not os.path.exists(pic_dir):
    os.makedirs(pic_dir)


def get_md5(v, is_file=False):
    '''获取md5'''
    if not is_file:
        return md5(v.encode('utf-8')).hexdigest()
    try:
        with open(v, 'rb') as f:
            r = f.read()
            return md5(r).hexdigest()
    except Exception as e:
        print("获取md5错误", e)


def get_dbm(dbm=DBManager()):
    '''数据库对象

    - 可选参数默认值的设置在Python中只会被执行一次，当做懒加载
    '''
    return dbm


def msg_repeated(msg):
    '''消息是否重复'''
    msg_type = msg.get('Type')
    md5 = None
    if msg_type == TEXT:
        # 文本类型
        md5 = get_md5(msg.get('Text'))
        r = get_dbm().query_item_md5(md5)
        if r:
            return True
    elif msg_type == PICTURE:
        # 图片类型
        # 储存路径
        file_path = os.path.join(pic_dir, msg.get('FileName'))
        # 下载图片
        download = msg.get('download')
        download(file_path)
        md5 = get_md5(file_path, True)
        r = get_dbm().query_item_md5(md5)
        if r:
            return True
    # 保存insert_md5()到消息体中，等消息发送成功后调用插入数据库
    if md5:
        insert_md5 = get_insert_md5(msg_type, md5)
        msg['insert_md5'] = insert_md5
        return False


# 也可以使用functools.partial
def get_insert_md5(tpy, md5):
    '''插入数据库'''

    def insert_md5():
        return get_dbm().insert_item(TEXT, md5)

    return insert_md5


def msg2json(msg):
    '''消息转json字符串'''
    items = {}
    items['FromUserName'] = msg.get('FromUserName')
    items['ToUserName'] = msg.get('ToUserName')
    items['ActualUserName'] = msg.get('ActualUserName')
    items['NewMsgId'] = msg.get('NewMsgId')
    items['Type'] = msg.get('Type')
    text = msg.get('Text')
    if isinstance(text, str):
        items['Text'] = text
    else:
        items['Text'] = None
        items['FileName'] = msg.get('FileName')
    s = json.dumps(items)
    return s


def json2msg(b):
    '''json字符串转消息'''
    j = b.decode()
    msg = json.loads(j)
    core = itchat.originInstance
    download_fn = get_download_fn(
        core, '%s/webwxgetmsgimg' % core.loginInfo.get('url'), msg['NewMsgId'])
    msg['download'] = download_fn
    return msg


def clear_db_task():
    '''定时任务清空数据库'''

    def work():
        get_dbm().clear_tabel()

    hour, minute = task_time
    # 每天task_time时执行任务
    sched = BackgroundScheduler()
    sched.add_job(work, 'cron', hour=hour, minute=minute)
    sched.start()


def main():
    clear_db_task()


if __name__ == '__main__':
    main()
