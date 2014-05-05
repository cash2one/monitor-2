#!/usr/bin/env python
# -*- coding: utf-8 -*-

import MySQLdb

def save2mysql(value_list):
    conn = MySQLdb.connect(host='localhost', user='root', passwd='123456', port=3306, charset='utf8')
    cur = conn.cursor()

    try:
        cur.execute("use monitor")
    except:
        cur.execute("create database if not exists monitor")
    conn.select_db("monitor")
    res = cur.execute("SELECT table_name FROM information_schema.TABLES WHERE table_name='search_result_table'")
    if not res:
        cur.execute("create table search_result_table(\
                        baidu_search_websize varchar(255) charset utf8,\
                        search_time datetime,\
                        title_words varchar(255) charset utf8,\
                        result_url varchar(255) charset utf8,\
                        download_url varchar(255)) charset utf8")

    cur.executemany("insert into search_result_table values(%s, %s, %s, %s, %s)", value_list)
    conn.commit()

    cur.close()
    conn.close()

def __test():
    import datetime
    t = datetime.datetime.now()
    values = []
    for i in range(10):
        values.append(("www.baidu.com", t, "百变大咖秀", "www.baidu.com", "www.baidu.com"))

    save2mysql(values)

if __name__ == '__main__':
    __test()


