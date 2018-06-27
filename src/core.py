#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import os
import itchat
from itchat.content import TEXT, PICTURE, CARD
from constant import pkl_path, qr_path, pic_dir, cmd_user_name
from log import gen_logger
from tools import msg_repeated, clear_db_task
from user_manager import UserManager


logger = gen_logger("logger.py")
# UserManager对象
user_m = UserManager()


def log_card(msg):
    '''打印名片'''
    nickname = msg.get('RecommendInfo', {}).get('NickName', "NULL")
    logger.info(nickname)


@itchat.msg_register(
    [TEXT, PICTURE, CARD], isFriendChat=True, isGroupChat=True)
def msg_reply(msg):
    '''接收消息'''
    msg_type = msg.type
    if msg_type == CARD:
        # 名片消息
        log_card(msg)
    else:
        # 文字消息、图片消息
        # 处理控制命令
        is_control = handle_cmd(msg, msg_type)
        if is_control:
            return
        # 处理消息
        handle_msg(msg)


def handle_cmd(msg, msg_type):
    '''处理控制命令'''
    if msg_type != TEXT:
        return False

    # 消息接收人 filehelper
    from_user = msg.get('ToUserName')
    is_control = (isinstance(from_user, str) and from_user == cmd_user_name)
    if not is_control:
        return False

    # 执行命令
    print(msg.text)
    return True


def handle_msg(msg):
    '''处理消息'''
    # 是否存在消息接收人
    users = user_m.contain_receiver(msg)
    if not isinstance(users, tuple):
        return

    # 是否已发送过
    repeated = msg_repeated(msg)
    if repeated:
        return

    # 转发
    relay_msg(msg, users)


def relay_msg(msg, users):
    '''转发消息
    - users: (s_user, r_wc_users)
    '''

    s_user, v = users
    # 消息发送人真实姓名
    s_user_name = s_user.get('name')
    if not s_user_name:
        # 备注名字
        s_user_name = s_user.get('remarkName')
    if not s_user_name:
        # 群名
        s_user_name = s_user.get('roomName')
    if not s_user_name:
        s_user_name = '未知发送人'

    msg_type = msg.type
    # 文本消息内容
    content = None
    file_path = None
    if msg_type == TEXT:
        content = msg.text + "\n【消息来自】 " + s_user_name
    else:
        content = "【图片消息来自】" + s_user_name
        file_path = "@img@" + os.path.join(pic_dir, msg.fileName)

    ok_list = []
    for user in v:
        # 接收人id
        user_name = user.get('userName')

        if msg_type == TEXT:
            r = itchat.send(content, user_name)
            is_ok = bool(r)
            ok_list.append(is_ok)
        else:
            itchat.send(content, user_name)
            r = itchat.send(file_path, user_name)
            is_ok = bool(r)
            ok_list.append(is_ok)
    # 是否全部发送成功
    is_ok = list(set(ok_list))[0]
    if is_ok:
        # 插入数据库
        insert_md5 = msg.get('insert_md5')
        insert_md5()


def login_callback():
    '''登录成功回调'''
    print("登录成功")

    # 加载user
    user_m.load_user()
    print("user_config: ", user_m.conf)
    print("users: ", user_m.items)


def login_wechat():
    '''微信登录'''
    itchat.auto_login(
        True, pkl_path, picDir=qr_path, loginCallback=login_callback)
    itchat.run()


def main():
    # 定时任务
    clear_db_task()

    login_wechat()


if __name__ == '__main__':
    main()
