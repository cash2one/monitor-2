#!/usr/bin/env python
# -*- coding: utf-8 -*-

import daemon

from optparse import OptionParser
from judge_run_cycle import JudgeCycle
from baidu_urlparse import BaiduParser
from log import loginf, logwarn, dbg, trace_err, options, args

def main(title, mode, cycle, userid, taskid):
    loginf("title = %s" % title.decode("utf-8").encode("utf-8"))
    baiduparser = BaiduParser(title, mode, userid, taskid)
    baiduparser.start()
    baiduparser.join()
    if cycle:
        judgecycle = JudgeCycle(title, mode, cycle)
        judgecycle.start()
        judgecycle.join()

if __name__ == '__main__':
    loginf("options: %s" % options)

    if options.daemon:
        daemon.daemonize(noClose=False)

    loginf("监控系统启动...")
    title = options.program
    mode = options.mode
    cycle = options.cycle
    userid = options.userid
    taskid = options.taskid
    if not title:
        title = args[0]
    main(title, mode, cycle, userid, taskid)
