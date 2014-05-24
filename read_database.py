#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import MySQLdb

def main(title):
    try:
        conn=MySQLdb.connect(host='localhost',user='root',passwd='123456',port=3306,charset="utf8")
        cur=conn.cursor()
        conn.select_db('monitor')
        cmd = 'select * from search_result_table where key_words = "%s";' % title
        cur.execute(cmd)
        result = cur.fetchall()
        if len(result) == 0:
            print '未找到影片信息'
        else:
            for i in result:
                print i[1], i[2]
                print i[3]
                print 
        print 'total: %s' % len(result)
        conn.commit()
        cur.close()
        conn.close()
    except Exception, e:
        print e
        

if __name__ == '__main__':
    if len(sys.argv) < 2:
        title = raw_input("请输入要查找的影片：")
    else:
        title = sys.argv[1]
    main(title)
