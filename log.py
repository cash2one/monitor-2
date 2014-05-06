#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  log
#
#  Author: Zhang Xu <xu.zhang@chinacache.com>

import os
import sys
import logging
import traceback
from simplejson import dumps

from optparse import OptionParser

opt = OptionParser()
opt.add_option('-d', dest='daemon', action='store_true', default=False,
                help=u'以 Daemon 模式后台运行')
opt.add_option('-p', dest='program',
                help=u'节目名称')

options, args = opt.parse_args()
title = options.program
if not title:
    title = args[0]

DEBUG = True
LOG_PATH = '/tmp/log'  # 日志目录，使用时可根据需要修改

__all__ = ['loginf', 'logwarn', 'logerr', 'logfatal',
           'dbg', 'trace_err', 'jsonformat']


def log_handle(log_type):
    '''
    获取logging handle

    @params log_type: 日志类型，字符串类型，可选项：'info', 'error'。
    '''
    logpath = LOG_PATH
    if not os.path.isdir(logpath):
        os.system('rm -rf %s' % logpath)
        os.makedirs(logpath, 0775)
    log_name, path, level, template = {
        'info': (
            'INF', logpath + '/%s-out' % title, logging.DEBUG,
            '%(asctime)s %(levelname)7s %(module)s.%(funcName)s : %(message)s'
        ),
        'error': (
            'ERR', logpath + '/err', logging.WARNING,
            '%(asctime)s %(levelname)8s by %(module)s.%(funcName)s in line %(lineno)d [%(threadName)s] -> %(message)s'
        )
    }[log_type]

    _log = logging.getLogger(log_name)
    hdlr = logging.FileHandler(path)
    formatter = logging.Formatter(template)
    hdlr.setFormatter(formatter)
    _log.addHandler(hdlr)
    _log.setLevel(level)
    return _log


inf_hdlr = log_handle('info')
err_hdlr = log_handle('error')

debug = inf_hdlr.debug
loginf = inf_hdlr.info
logwarn = err_hdlr.warning  # 警告
logerr = err_hdlr.error     # 错误
logfatal = err_hdlr.fatal   # 致命错误


def trace_code(start_layer=1, max_layers=10):
    module = lambda filename: os.path.splitext(os.path.basename(filename))[0]
    try:
        s = ''
        for i in xrange(start_layer, max_layers + start_layer):
            fcode = sys._getframe(i).f_code
            if fcode.co_name == 'run':
                if sys._getframe(i + 1).f_code.co_name == '__bootstrap_inner':
                    mod = module(fcode.co_filename)
                    s = mod + '.' + fcode.co_name + '.' + s
                    raise
            elif fcode.co_name == '<module>':
                mod = module(fcode.co_filename)
                s = mod + '.' + s
                raise
            else:
                s = fcode.co_name + '.' + s
    finally:
        if s and s[-1] == '.':
            s = s[:-1]
        return s


def dbg(*args, **kwargs):
    '''
    打印调试数据

    用法：
        a, b, c = 1, 'a string', {'q': [111, 222, 333], 'w': 'poiuy', 'e': 123}
        dbg(b)
        dbg(a, b, c)
        dbg(a, b=b, arg3=jsonformat(c))
    '''
    if DEBUG:
        s = trace_code(2, 1)

        if len(args) == 1 and not kwargs:
            s += ' : ' + str(args[0])
        else:
            for arg in args:
                s += ('\n >>> ' + str(arg))
            for k, v in kwargs.iteritems():
                s += ('\n >>> ' + str(k) + ': ' + str(v))
            s += '\n'
        debug(s)

        # 手动控制，单步执行
        if kwargs.get('block') and raw_input('press e to exit, else continue -> ').lower() == 'e':
            exit()


def trace_err(ext_msg=None):
    '''
    将捕获到的异常信息输出到错误日志(*最好每个 except 后面都加上此函数*)

    直接放到 expect 下即可，E.G.：
        try:
            raise
        except Exception, e:
            output_err()

    @params ext_msg: 补充的异常信息
    '''
    msg = '' if ext_msg is None else ext_msg
    msg += '\n------------------- Local Args -------------------\n'
    for k, v in sys._getframe(1).f_locals.iteritems():
        msg += (' >>> ' + str(k) + ': ' + str(v) + '\n')
    msg += '--------------------- Error ----------------------\n'
    exc_info = traceback.format_exception(*sys.exc_info())  # 取出格式化的异常信息
    msg += ''.join(exc_info)
    msg += '---------------------- End -----------------------\n'
    logfatal(msg)


def jsonformat(data):
    '''返回json格式化的数据'''
    return dumps(data, indent=4)


if __name__ == '__main__':
    # test
    debug('debug')
    loginf('loginf')
    logwarn('logwarn')
    logerr('logerr')
    logfatal('logfatal')

    a, b, c = 1, 'a string', {'q': [111, 222, 333], 'w': 'poiuy', 'e': 12345}
    dbg(b)
    dbg(a, b, c)
    dbg(a, b=b, arg3=jsonformat(c))

    def err(a):
        b = {}
        print b
        try:
            raise
        except:
            trace_err('asdf')

    err(12)

    def foo():
        print trace_code(max_layers=2)

    def fpp():
        foo()

    def fll():
        fpp()
    fll()
    import threading

    class A(threading.Thread):

        def __init__(self):
            threading.Thread.__init__(self)

        def run(self):
            fll()
    t = A()
    t.start()
