#!/usr/bin/env python
# -*- coding: utf-8 -*-

import threading
import urllib, urllib2
from lxml import etree
import re
import os
import datetime

from libs import get_html

class BaiduParser(threading.Thread):
    def __init__(self, search_content=""):
        super(BaiduParser, self).__init__()
        self.content = search_content
        self.result_dct = {}

    def baidu_search(self, page=0):
        p = {
                'word': self.content,
                'tn': 'baidu',
                'pn': (page-1)*10,
            }
        res = urllib2.urlopen("http://www.baidu.com/baidu?" + urllib.urlencode(p), timeout=20)
        html = res.read().decode('utf-8', 'ignore')
        return html

    def get_url_and_title(self, all_buf_list):
        for buf in all_buf_list:
            title = ""
            url = ""
            res = etree.HTML(buf)
            hrefs = res.xpath(u"//a")
            if hrefs:
                url = hrefs[0].attrib.get('href', ' ')
            tmp = res.xpath("//h3[@class='t']")
            if tmp:
                title = tmp[0].xpath(u"string()")
                print title, url
            else:
                tmp = res.xpath("//h3[@class='t c-gap-bottom-small']")
                if tmp:
                    title = tmp[0].xpath(u"string()")
                    print title, url
            if title and url.startswith("http"):
                search_time = datetime.datetime.now()
                html = get_html(url)
                print html

    def baidu_urlparse(self, content=""):
        html = content.replace("\n", "")
        all_buf = re.findall('(<div class="result.*? id=".*?)(?=</div>)', html)
        if len(all_buf) == 10:
            pass
        else:
            all_buf.extend(re.findall('(<table class="result.*? id=".*?)(?=</table>)', html))
        if len(all_buf) != 10: 
            pass
        if len(html) < 4000:
            print '被封了'
            print '结束时间：', datetime.datetime.now()
            import sys
            sys.exit()
        self.get_url_and_title(all_buf)
    
    def run(self):
        print '开始时间：', datetime.datetime.now()
        for i in range(1,77,1):
            html = self.baidu_search(i)
            self.baidu_urlparse(html)

if __name__ == '__main__':
    baiduparser = BaiduParser("百变大咖秀")
    baiduparser.start()
    baiduparser.join()
    pass
        

