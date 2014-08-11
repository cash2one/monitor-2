#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import threading

from log import loginf, logerr

CRON_FILE = '/var/spool/cron/crontabs/root'
SRC_PATH = '/home/monitor/'

class JudgeCycle(threading.Thread):
    def __init__(self, title, mode, cycle, userid, taskid):
        super(JudgeCycle, self).__init__()
        self.title = title
        self.mode = mode
        self.cycle = cycle
        self.userid = userid
        self.taskid = taskid

    def run(self):
        loginf("正在设置运行周期")
        src_file = os.path.join(SRC_PATH, "run.py")
        loginf("源文件目录：%s" % src_file)
        try:
            fd = open(CRON_FILE, 'a+')
            con = fd.read()
            fd.close()
            #if self.title in con:
                #cmd = "sed -i /%s/d %s" % (self.title, CRON_FILE)
                #os.system(cmd)
                #loginf("正在删除原始周期：%s" % cmd)
            if ":" not in str(self.cycle):
                src = "0 */%s * * * python %s -p %s -m %s -U %s -T %s -d" % (self.cycle, src_file, self.title, self.mode, self.userid, self.taskid)
                cmd = """echo '%s' >> %s""" % (src, CRON_FILE)
                os.system(cmd)
                loginf("设置周期命令：%s" % cmd)
            else:
                tmp = self.cycle.split(":")
                week = tmp[0].split("-")[0]
                hour = tmp[0].split("-")[1]
                minute = tmp[1]
                src = "%s %s * * %s python %s -p %s -m %s -U %s -T %s -d" % (minute, hour, week, src_file, self.title, self.mode, self.userid, self.taskid)
                cmd = """echo '%s' >> %s""" % (src, CRON_FILE)
                os.system(cmd)
                loginf("设置周期命令：%s" % cmd)
            os.system("crontab %s" % CRON_FILE)
        except Exception, e:
                logerr("周期设置失败：%s" % str(e))

if __name__ == '__main__':
    judgecycle = JudgeCycle('百变大咖秀', 'tv', 30)
    judgecycle.start()
    judgecycle.join()
