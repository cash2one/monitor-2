#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib, urllib2
from lxml import etree

def baidu_search(content="", page=0):
    p = {
            'wd': content,
            'pn': page,
            'ie': 'utf-8'
        }
    res = urllib2.urlopen("http://www.baidu.com/s?" + urllib.urlencode(p))
    html = res.read()
    return html

def baidu_urlparse(content=""):
    pass


