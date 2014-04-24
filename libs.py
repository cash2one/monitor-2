#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib, urllib2
from lxml import etree
import re
import os
import datetime

def baidu_search(content="", page=0):
    p = {
            'word': content,
            'tn': 'baidu',
            'pn': (page-1)*10,
        }
    res = urllib2.urlopen("http://www.baidu.com/baidu?submit=%B0%D9%B6%C8%D2%BB%CF%C2" + urllib.urlencode(p))
    html = res.read()
    return html

def baidu_urlparse(content=""):
    pass

if __name__ == '__main__':
    print '开始时间：', datetime.datetime.now()
    for i in range(1,7000,1):
    	html = baidu_search('百变大咖秀', i)
        html = html.replace("\n", "")
        all_buf = re.findall('(<div class="result.*? id=".*?)(?=</div>)', html)
        if len(all_buf) == 10:
            pass
        else:
            all_buf.extend(re.findall('(<table class="result.*? id=".*?)(?=</table>)', html))
        if len(all_buf) != 10:
            print (i-1)*10
    	fd = open("html/%d.html" % i, 'w')
    	fd.write(html)
    	fd.close()
        if len(html) < 4000:
            print '****************'
            print i
            print '被封了'
    	    print '结束时间：', datetime.datetime.now()
            break
        

