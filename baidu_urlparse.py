#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import threading
import urllib, urllib2
from lxml import etree
import re
import os
import datetime

from log import loginf, logerr, dbg, trace_err
from libs import get_html, is_monitor_result
from save_to_database import save2mysql

change_charset = lambda x: x.encode("utf-8").decode("utf-8")

class BaiduParser(threading.Thread):
    def __init__(self, search_content="", mode="tv", userid=0, taskid=0):
        super(BaiduParser, self).__init__()
        self.content = search_content
        self.mode = mode
        self.userid = userid
        self.taskid = taskid
        self.total = 0
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
            logerr(str(e))
            return '', ''

    def get_url_and_title(self, baidu_url, all_buf_list):
        for buf in all_buf_list:
            title = ""
            url = ""
            res = etree.HTML(etree.tostring(buf))

            show_url = ""
            tmp = res.xpath("//div[@class='g']")
            if not tmp:
            	tmp = res.xpath("//div[@class='g']")
            if not tmp:
                tmp = res.xpath("//span[@class='c-showurl']")
            if not tmp:
                tmp = res.xpath("//span[@class='g']")
            if tmp:
                show_url = tmp[0].xpath(u"string()")

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
            if url.startswith("//"):
                url = "http:" + url
            if title and url.startswith("http"):
                search_time = datetime.datetime.now()
                loginf("标题: %s" % title.encode("utf-8"))
                loginf("url : %s" % url.encode("utf-8"))
                loginf("showurl : %s" % show_url.encode("utf-8"))
                html = get_html(url)
                if html:
                    flag = is_monitor_result(title, html, self.mode, self.content)
                    if flag:
                        loginf("监控到（%s: %s ）包含下载或播放等内容" % (title.encode("utf-8"), url.encode("utf-8")))
                        k_words = u"百度快照"
                        if k_words in show_url:
                            #show_url = show_url.split(k_words)[0]
                            show_url = show_url[0: -8]
                        values = [change_charset(baidu_url), search_time, change_charset(title), change_charset(url),\
                                 self.content, change_charset(show_url), None,0,None, self.taskid, self.userid]
                        self.result_list = values 
                        self.total += 1
                        loginf("正在存入数据库")
                        save_flag = save2mysql(self.result_list, self.content)
                        if save_flag == True:
                            loginf("数据保存成功\n\n")
                        else:
                            loginf("数据库已经包含该链接: %s\n\n", self.result_list[2].encode("utf-8"))
                    else:
                        pass
            else:
                # 遗露无标题的情况, 可write文件查看
                loginf("标题解析为空, url: %s" % url.encode("utf-8"))

    def baidu_urlparse(self, baidu_url, content="", page=0):
        html = content.replace("\n", "")
        res = etree.HTML(html)
        all_buf = []
        for i in range(10*page-9, 10*page+1):
            tmp = res.xpath("//div[@id='%s']" % i)
            if tmp:
                all_buf.append(tmp[0])
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
            if baidu_url and html:
                self.baidu_urlparse(baidu_url, html, i)
            else:
                loginf("百度搜索抓取为空") 
        loginf("监控到的个数：%s" % self.total)
        loginf('结束时间：%s' % datetime.datetime.now())
        loginf("本轮耗时: %.2f s" % (time.time() - _t))

if __name__ == '__main__':
    baiduparser = BaiduParser("百变大咖秀")
    baiduparser.start()
    baiduparser.join()
    pass


