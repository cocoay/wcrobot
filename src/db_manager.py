#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import sqlite3
from constant import db_path
from time import time


class SQLBase(object):
    def __init__(self, db=db_path):
        self.db = db
        self.connected = False
        self.conn = None
        self.cur = None
        self.connect()

    def __del__(self):
        self.close()

    def connect(self):
        '''连接数据库'''
        try:
            # check_same_thread多线程操作
            self.conn = sqlite3.connect(self.db, check_same_thread=False)
            self.cur = self.conn.cursor()
            self.connected = True
        except Exception as e:
            self.connected = False
            print("数据库链接错误")
            raise e

    def close(self):
        '''关闭连接'''
        if not self.connected:
            return
        try:
            self.cur.close()
            self.conn.close()
            self.connected = False
        except Exception as e:
            print("数据库关闭错误", e)

    def check(self):
        '''检查连接，未连接再次连接'''
        if self.connected:
            return
        self.connect()

    def execute(self, sql, cur_close=True):
        '''执行sql语句

        - sql: sql语句
        - cur_close: 执行完语句后是否关闭cur
        '''
        self.check()
        try:
            cur = self.conn.cursor()
            cur.execute(sql)
            # 关闭
            if cur_close:
                cur.close()
            return cur
        except Exception as e:
            print("数据库操作错误", e)

    def commit(self):
        '''提交'''
        try:
            self.conn.commit()
        except Exception as e:
            print("数据库提交错误")
            raise e


class DBManager(SQLBase):
    # 表名
    table_name = "msg_hash"
    # 创建表(if not exists 不存在则创建)
    sql_creat_table = """create table if not exists '%s' (
    id integer primary key autoincrement,
    type varchar(10),
    md5 varchar(32),
    time varchar(10))"""
    # 插入数据
    sql_insert = """insert into '%s' (type, md5, time)
    values ('%s', '%s', '%s')"""
    # 删除数据
    sql_delete = """delete from '%s'
    where %s"""
    # 删除全部数据
    sql_delete_all = "delete from '%s'"
    # 查找数据
    sql_select = """select * from '%s'
    where %s"""

    def __init__(self):
        super().__init__()
        self.creat_tabel()

    def creat_tabel(self):
        '''创建table'''
        sql = self.sql_creat_table % self.table_name
        cur = self.execute(sql)
        if cur:
            self.commit()

    def insert_item(self, typ, md5):
        '''插入数据

        - typ: 类型
        - md5: md5
        '''
        # 时间戳
        t = str(int(time()))
        sql = self.sql_insert % (self.table_name, typ, md5, t)
        cur = self.execute(sql)
        if cur:
            self.commit()
        return True if cur else False

    def clear_tabel(self):
        '''清空table中的数据'''
        sql = self.sql_delete_all % self.table_name
        cur = self.execute(sql)
        if cur:
            self.commit()
        return True if cur else False

    def delete_item(self, condition):
        '''删除数据

        - condition: 条件
        '''
        sql = self.sql_delete % (self.table_name, condition)
        cur = self.execute(sql)
        if cur:
            self.commit()
        return True if cur else False

    def select_item(self, condition):
        '''查询数据

        - condition: 条件
        '''
        sql = self.sql_select % (self.table_name, condition)
        cur = self.execute(sql, False)
        r = None
        if cur:
            r = cur.fetchone()
            cur.close()
        return r

    def query_item_md5(self, md5):
        '''查询数据

        - md5: md5条件值
        '''
        if not md5:
            return
        condition = "md5='%s'" % md5
        return self.select_item(condition)


def main():
    md5 = "922ec9531b1f94add983a8ce2ebdc97b"
    db = DBManager()
    ok = db.insert_item('test', md5)
    print("插入", ok)
    r = db.query_item_md5(md5)
    print("查询", r)
    condition = "md5='%s'" % md5
    ok = db.delete_item(condition)
    print("删除", ok)
    ok = db.clear_tabel()
    print("清空数据", ok)


if __name__ == '__main__':
    main()
