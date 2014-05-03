#!/usr/bin/env python
# -*- coding: utf-8 -*-

import threading
import urllib, urllib2
from lxml import etree
import re
import os
import datetime

from libs import get_html
from save_to_database import save2mysql

change_charset = lambda x: x.encode("utf-8").decode("utf-8")

class BaiduParser(threading.Thread):
    def __init__(self, search_content=""):
        super(BaiduParser, self).__init__()
        self.content = search_content
        self.result_list = []

    def baidu_search(self, page=0):
        p = {
                'word': self.content,
                'tn': 'baidu',
                'pn': (page-1)*10,
            }
        url = "http://www.baidu.com/baidu?" + urllib.urlencode(p)
        res = urllib2.urlopen(url, timeout=20)
        html = res.read().decode('utf-8', 'ignore')
        return url, html

    def get_url_and_title(self, baidu_url, all_buf_list):
        for buf in all_buf_list:
            title = ""
            url = ""
            res = etree.HTML(buf)
            hrefs = res.xpath(u"//a")
            if hrefs:
                url = hrefs[0].attrib.get('href', None)
                if not url:
                    url = hrefs[-1].attrib.get('href', None)
            tmp = res.xpath("//h3[@class='t']")
            if tmp:
                title = tmp[0].xpath(u"string()")
#print title.encode("utf-8"), url.encode("utf-8")
            else:
                tmp = res.xpath("//h3[@class='t c-gap-bottom-small']")
                if tmp:
                    title = tmp[0].xpath(u"string()")
#print title.encode("utf-8"), url.encode("utf-8")
            if title and url.startswith("http"):
                search_time = datetime.datetime.now()
                html = get_html(url)
                if html:
                    values = (change_charset(baidu_url), search_time, change_charset(title), change_charset(url), change_charset(""))
                    self.result_list.append(values)
#print html.encode("utf-8")

    def baidu_urlparse(self, baidu_url, content=""):
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
        self.get_url_and_title(baidu_url, all_buf)
    
    def run(self):
        print '开始时间：', datetime.datetime.now()
        for i in range(1,2,1):
            baidu_url, html = self.baidu_search(i)
            self.baidu_urlparse(baidu_url, html)
        print self.result_list
        save2mysql(self.result_list)

if __name__ == '__main__':
    baiduparser = BaiduParser("百变大咖秀")
    baiduparser.start()
    baiduparser.join()
    pass
        

