#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2
import datetime
from log import loginf, logerr, dbg, trace_err

def get_html(url):
    con = ""
    try:
        req = urllib2.urlopen(url, timeout=3)
        con = req.read().decode('utf-8', 'ignore')
        if len(con) < 4000 and u"请输入以下验证码" in con:
            loginf("百度被封了, url: %s" % url.encode("utf-8"))
        req.close()
    except Exception, e:
        if "timed out" in str(e):
            try:
                req = urllib2.urlopen(url, timeout=10)
                con = req.read().decode('utf-8', 'ignore')
                req.close()
                return con
            except:
                logerr("%s" % e)
                logerr("url = %s" % url)
                return ""
                
        logerr("%s" % e)
        logerr("url = %s" % url)
    return con

def is_monitor_result(title, html, mode, search_content):
    judge = lambda x: x in title and x in html
    flag = False
    if mode == 'tv':
        if judge(u'直播') and ((u'预告') not in title) and (search_content in title):
            flag = True
    elif mode == 'movie':
        if "游戏" not in search_content:
            if (judge(u'下载') or judge(u'在线观看') or judge(u'在线点播'))\
                                and ((u'游戏介绍') not in html)\
                                and ((u'游戏下载') not in html)\
                                and ((u'游戏') not in title)\
                                and ((u'预告') not in title)\
                                and ((u'软件') not in title):
                flag = True
        else:
            if (judge(u'下载') or judge(u'在线观看') or judge(u'在线点播'))\
                                and ((u'游戏下载') not in html)\
                                and ((u'预告') not in title)\
                                and ((u'软件') not in title):
             
                flag = True
    return flag

if __name__ == '__main__':
    con = get_html("http://www.baidu.com")
    print con



