#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2
import datetime

def get_html(url):
    con = ""
    try:
        req = urllib2.urlopen(url, timeout=10)
        con = req.read().decode('utf-8', 'ignore')
        if len(con) < 4000:
            print '被封了'
        req.close()
    except:
        pass
    return con

if __name__ == '__main__':
    con = get_html("http://www.baidu.com")
    print con



