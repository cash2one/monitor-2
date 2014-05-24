#!/usr/bin/env python
# -*- coding: utf-8 -*-

import MySQLdb
from log import loginf

def save2mysql(value_list, title):
    save_flag = True
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
                        key_words varchar(255) charset utf8,\
                        show_url varchar(255) charset utf8)")

    cmd = 'select * from search_result_table where key_words = "%s";' % title
    cur.execute(cmd)
    result = cur.fetchall()
    all_title_words = [i[2] for i in result]
    if value_list[2] not in all_title_words:
        cur.execute("insert into search_result_table values(%s, %s, %s, %s, %s, %s)", value_list)
        conn.commit()
    else:
        save_flag = False

    cur.close()
    conn.close()
    return save_flag

def __test():
    import datetime
    t = datetime.datetime.now()
    values = ["www.baidu.com", t, "百变大咖秀", "www.baidu.com", "www.baidu.com", "aa"]

    save2mysql(values, '行尸走肉')

if __name__ == '__main__':
    __test()


