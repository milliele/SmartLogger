# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version Jun 17 2015)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################
import os
import time
import threading
import inspect
import ctypes


def endWith(*endstring):
    ends = endstring

    def run(s):
        f = map(s.endswith, ends)
        if True in f:
            return s

    return run

def Change():
    linespace = os.linesep
    localpath = './'
    print u'扫描日志文件夹:%s...'%os.path.abspath(localpath)+linespace
    if os.path.exists(localpath):
        list_file = os.listdir(localpath)
        a = endWith('.log')
        log_file = filter(a, list_file)
        if log_file:
            num = len(log_file)
            print u'共找到%d个待转换文件'%num + linespace
            failed = 0
            cnt = 1
            for x in log_file:
                x = unicode(x, 'gbk')
                print u'正在转换：%s...' % x + linespace
                res = RealUpload(x, localpath)
                if res == '':
                    print u'%s转换成功! (%d/%d)' % (x, cnt, num) + os.linesep
                else:
                    print u'转换失败，异常信息：%s'% res + os.linesep
                    failed += 1
                cnt += 1
            print u'转换完成！成功：%d个， 失败：%d个'%(num-failed, failed) + linespace
        else:
            print u'无可转换文件！' + linespace
    else:
        print u'访问日志文件夹失败！' + linespace

def RealUpload(x, localpath):
    #
    filepath = os.path.join(localpath, x)
    while True:
        try:
            # 上传工作
            MyChange(filepath)
            # 上传成功
            return ''
        except Exception, ex:
            import traceback
            return traceback.format_exc(ex)

def formattime(sec):
    second = sec % 60
    sec /= 60
    min = sec % 60
    sec /= 60
    hour = sec
    return '%d:%d:%d'%(hour, min, second)

def deal(x):
    id = reversed(range(len(x)))
    stack = []
    for i in id:
        if x[i]=="}":
            stack.append(i)
        elif x[i]=='{':
            if len(stack)==0:
                return None
            en = stack.pop()
            if stack==[]:
                return x[i:en+1]
    return None


def MyChange(filepath):
    fobj = open(filepath,'r')
    import csv
    file = open(filepath[:-3] + 'csv', 'wb')
    writer = csv.writer(file)
    writer.writerow(['Date', 'Weekday', 'Pid', 'Name', 'Begin Time', 'End Time', 'Last Time'])
    list = fobj.readlines()
    pending = {}

    for x in list:
        import json
        x = deal(x)
        if x == None:
            continue
        message = json.loads(x)
        for j in message['in']:
            pending[(j[0], j[1])] = message['time']
        for j in message['out']:
            process = (j[0], j[1])
            if process in pending:
                b = time.mktime(time.strptime(pending[process], '%Y-%m-%d %H:%M:%S %a'))
                e = time.mktime(time.strptime(message['time'], '%Y-%m-%d %H:%M:%S %a'))
                lo = formattime(e-b)
                # ['Date', 'Weekday', 'Pid', 'Name', 'Begin Time', 'End Time', 'Last Time']
                writer.writerow([pending[process][:10], pending[process][-3:], process[0], process[1], pending[process][-12:-4], message['time'][-12:-4], lo])
                pending.pop(process)
            else:
                # 没有开始时间的
                # ['Date', 'Weekday', 'Pid', 'Name', 'Begin Time', 'End Time', 'Last Time']
                writer.writerow(
                    [message['time'][:10], message['time'][-3:], process[0], process[1], '',
                     message['time'][-12:-4], ''])
    # 没有结束时间的
    for k in pending:
        # ['Date', 'Weekday', 'Pid', 'Name', 'Begin Time', 'End Time', 'Last Time']
        writer.writerow([pending[k][:10], pending[k][-3:], k[0], k[1], pending[k][-12:-4],
                         '', ''])
    file.close()

if __name__ == '__main__':
    Change()
    print u'按任意键结束...'
    import msvcrt
    msvcrt.getch()