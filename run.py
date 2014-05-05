#!/usr/bin/env python
# -*- coding: utf-8 -*-

from optparse import OptionParser

from baidu_urlparse import BaiduParser
from log import loginf, logwarn, dbg, trace_err

import daemon

def main(args):
    title = args[0]
    baiduparser = BaiduParser(title)
    baiduparser.start()
    baiduparser.join()
    print title

if __name__ == '__main__':
    opt = OptionParser()
    opt.add_option('-d', dest='daemon', action='store_true', default=False,
                    help=u'以 Daemon 模式后台运行')
    opt.add_option('-p', dest='program',
                    help=u'节目名称')
    opt.add_option('-m', dest='mode', 
                    help=u'运行模式("直播模式：live, 点播模式：movie")')

    options, args = opt.parse_args()
    print options

    if options.daemon:
        daemon.daemonize(noClose=False)

    loginf("监控系统启动...")
    main(args)
