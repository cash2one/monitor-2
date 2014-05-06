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
            print url
            print '被封了'
        req.close()
    except Exception, e:
        if "timed out" in str(e):
            print 'time out '
            try:
                req = urllib2.urlopen(url, timeout=20)
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

if __name__ == '__main__':
    con = get_html("http://www.baidu.com")
    print con



