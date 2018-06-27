#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import os

# os.getcwd()为工作路径，不推荐使用

# 当前文件所在目录
c_dir = os.path.dirname(__file__)

# 项目目录
proj_dir = os.path.dirname(c_dir)

# res文件夹
res_dir = os.path.join(proj_dir, "res")

# itchat图片消息下载文件夹
pic_dir = os.path.join(res_dir, "pic")

# itchat log路径
pkl_path = os.path.join(res_dir, "itchat.pkl")

# QR路径
qr_path = os.path.join(res_dir, "QR.png")

# log路径
log_path = os.path.join(res_dir, "record.log")

# user_config路径
config_path = os.path.join(res_dir, "user_config.yml")

# db路径
db_path = os.path.join(res_dir, "proj.db")

# cmd用户的名字
cmd_user_name = "filehelper"

# 定时任务执行时间(时, 分)
task_time = (3, 0)

# 日志文件最大值
maxBytes = 10 * 1024 * 1024

# 是否使用消息队列
use_mq = True

# mq用户
mq_username = "admin"
mq_password = "admin"

# mq_host地址
mq_host = "192.168.1.109"

# mq队列名字
mq_queue = "mq_queue"
