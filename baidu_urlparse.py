#!/usr/bin/env python
# -*- coding: utf-8 -*-

import threading
import urllib, urllib2
from lxml import etree
import re
import os
import datetime

from log import loginf, logwarn, dbg, trace_err
from libs import get_html
from save_to_database import save2mysql

change_charset = lambda x: x.encode("utf-8").decode("utf-8")

class BaiduParser(threading.Thread):
    def __init__(self, search_content=""):
        super(BaiduParser, self).__init__()
        self.content = search_content
        self.result_list = []

    def baidu_search(self, page=0):
        try:
            p = {
                    'word': self.content,
                    'tn': 'baidu',
                    'pn': (page-1)*10,
                }
            url = "http://www.baidu.com/baidu?" + urllib.urlencode(p)
            loginf("正在抓取百度网页: %s" % url.encode("utf-8"))
            res = urllib2.urlopen(url, timeout=20)
            html = res.read().decode('utf-8', 'ignore')
            return url, html
        except Exception, e:
            logerr('出错啦')
            return '', ''

    def get_url_and_title(self, baidu_url, all_buf_list):
        for buf in all_buf_list:
            title = ""
            url = ""
            res = etree.HTML(buf)
            tmp = res.xpath("//h3[@class='t']")
            if tmp:
                title = tmp[0].xpath(u"string()")
            else:
                tmp = res.xpath("//h3[@class='t c-gap-bottom-small']")
                if tmp:
                    title = tmp[0].xpath(u"string()")
            if tmp:
                tmp = etree.HTML(etree.tostring(tmp[0]))
                hrefs = tmp[0].xpath(u"//a")
                if hrefs:
                    url = hrefs[0].attrib.get('href', "")
            if title and url.startswith("http"):
                search_time = datetime.datetime.now()
                loginf("标题: %s" % title.encode("utf-8"))
                loginf("正在抓取监控页: %s\n" % url.encode("utf-8"))
                html = get_html(url)
                if html:
                    values = (change_charset(baidu_url), search_time, change_charset(title), change_charset(url), change_charset(""))
                    self.result_list.append(values)
            else:
                # 遗露无标题的情况, 可write文件查看
                print buf
                print title, url
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
        if len(html) < 4000 and u"请输入以下验证码" in html:
            loginf('百度搜索被封了')
            loginf('结束时间：%s' % datetime.datetime.now())
            import sys
            sys.exit()
        self.get_url_and_title(baidu_url, all_buf)

    def run(self):
        import time
        _t = time.time()
        loginf('开始时间：%s' % datetime.datetime.now())
        for i in range(1,77,1):
            baidu_url, html = self.baidu_search(i)
            self.baidu_urlparse(baidu_url, html)
#print self.result_list
        loginf("正在存入数据库")
        loginf("存入数据库的内容: %s" % self.result_list)
        save2mysql(self.result_list)
        loginf('结束时间：%s' % datetime.datetime.now())
        loginf("本轮耗时: %s" % (time.time() - _t))
        print len(self.result_list)

if __name__ == '__main__':
    baiduparser = BaiduParser("百变大咖秀")
    baiduparser.start()
    baiduparser.join()
    pass


