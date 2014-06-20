#!/usr/bin/env python
# -*- coding: utf-8 -*-

import MySQLdb

def save2mysql(value_list, title):
    save_flag = True
    conn = MySQLdb.connect(host='localhost', user='root', passwd='123', port=3306, charset='utf8')
    cur = conn.cursor()

    try:
        cur.execute("use cmsdb")
    except:
        cur.execute("create database if not exists cmsdb")
    conn.select_db("cmsdb")

    cmd = 'select * from search_result_table where key_words = "%s";' % title
    cur.execute(cmd)
    result = cur.fetchall()
    all_title_words = [i[3] for i in result]
    if value_list[2] not in all_title_words:
        cur.execute("insert into search_result_table values(null, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", value_list)
        conn.commit()
    else:
        save_flag = False

    cur.close()
    conn.close()
    return save_flag

def __test():
    import datetime
    t = datetime.datetime.now()
    values = ["www.baidu.com", t, "百变大咖秀", "www.baidu.com", "www.baidu.com", "aa", None, 0, None, 13, 1]

    save2mysql(values, '行尸走肉')

if __name__ == '__main__':
    __test()


