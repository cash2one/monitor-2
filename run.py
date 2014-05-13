#!/usr/bin/env python
# -*- coding: utf-8 -*-

from optparse import OptionParser

from baidu_urlparse import BaiduParser
from log import loginf, logwarn, dbg, trace_err, options, args

import daemon

def main(title, mode):
    loginf("title = %s" % title.decode("utf-8").encode("utf-8"))
    baiduparser = BaiduParser(title, mode)
    baiduparser.start()
    baiduparser.join()

if __name__ == '__main__':
    loginf("options: %s" % options)

    if options.daemon:
        daemon.daemonize(noClose=False)

    loginf("监控系统启动...")
    title = options.program
    mode = options.mode
    if not title:
        title = args[0]
    main(title, mode)
