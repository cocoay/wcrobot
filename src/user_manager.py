#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import yaml
from copy import deepcopy
from itchat import search_friends, search_chatrooms
from constant import config_path


class UserManager(object):
    def __init__(self):
        self.conf = None
        self.items = {}
        self.open_conf()

    def open_conf(self):
        '''读取'''
        try:
            with open(config_path, 'r') as f:
                r = yaml.load(f)
                self.conf = r
        except Exception as e:
            raise e

    def find_users(self, users):
        '''通过itchat查找用户、群组，返回数组'''
        if not isinstance(users, list):
            return

        wc_users = []
        for user in users:
            if not isinstance(user, dict):
                continue
            items = None
            # 是否为群组
            is_chat_room = user.get('isChatRoom')
            if is_chat_room:
                # 群组
                room_name = user.get('roomName')
                if not room_name:
                    continue
                items = search_chatrooms(name=room_name)
            else:
                # 普通用户
                remark_name = user.get('remarkName')
                if not remark_name:
                    continue
                items = search_friends(name=remark_name)

            # 是否找到群组、用户
            if not isinstance(items, list):
                continue
            for item in items:
                # user_name
                user_name = item.get('UserName')
                if not user_name:
                    continue
                # 深拷贝
                d_user = deepcopy(user)
                d_user['userName'] = user_name
                wc_users.append(d_user)

        return wc_users

    def load_user(self):
        '''加载user，微信登录后调用

        - {s_user_name, (s_user, r_wc_users)}
        '''

        if not isinstance(self.conf, list):
            return
        for d in self.conf:
            if not isinstance(d, dict):
                continue

            sender_list = d.get('sender')
            receiver_list = d.get('receiver')
            s_wc_users = self.find_users(sender_list)
            r_wc_users = self.find_users(receiver_list)

            # 是否有效
            v_s = (isinstance(s_wc_users, list) and len(s_wc_users) > 0)
            r_s = (isinstance(r_wc_users, list) and len(r_wc_users) > 0)
            if not v_s or not r_s:
                continue
            for s_user in s_wc_users:
                s_user_name = s_user['userName']
                v = (s_user, r_wc_users)
                self.items[s_user_name] = v

    def reload_data(self):
        '''重新读取'''
        self.conf = None
        self.items = {}
        self.open_conf()
        self.load_user()

    def insert(self, v):
        '''插入'''
        pass

    def delete(self, v):
        '''删除'''
        pass

    def contain_receiver(self, msg):
        '''根据msg中的消费发送人，查看items中是否包含消息接收人, 返回(s_user, r_wc_users)'''

        # 消息来源人id
        from_user = msg.get('FromUserName')
        # 群组消息的真实消息来源人id
        actual_from_user = msg.get('ActualUserName')
        if not from_user and not actual_from_user:
            return

        # tuple
        v = self.items.get(from_user)
        if not isinstance(v, tuple):
            v = self.items.get(actual_from_user)
        if not isinstance(v, tuple):
            return
        return v


def main():
    um = UserManager()
    print("user_config: ", um.conf)
    um.insert("aaa")


if __name__ == '__main__':
    main()
