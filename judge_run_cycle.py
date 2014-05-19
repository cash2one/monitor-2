#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import threading

from log import loginf, logerr

class JudgeCycle(threading.Thread):
    def __init__(self, title, mode, cycle):
        super(JudgeCycle, self).__init__()
        self.title = title
        self.mode = mode
        self.cycle = cycle

    def run(self):
        loginf("正在设置运行周期")
        try:
            fd = open('/var/spool/cron/crontabs/root')
            con = fd.read()
            fd.close()
            if self.title not in con:
                if ":" not in str(self.cycle):
                    src = "*/%s * * * * python run.py -p %s -m %s -d" % (self.cycle, self.title, self.mode)
                    cmd = """echo '%s' >> /var/spool/cron/crontabs/root""" % src
                    os.system(cmd)
                    loginf("设置周期命令：%s" % cmd)
            else:
                loginf("%s的周期已经设置，请打开/var/spool/cron/crontabs/root修改" % self.title)
        except exception, e:
                logerr("周期设置失败：%s" % str(e))

if __name__ == '__main__':
    judgecycle = JudgeCycle('百变大咖秀', 'tv', 30)
    judgecycle.start()
    judgecycle.join()
