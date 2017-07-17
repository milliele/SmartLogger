# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version Jun 17 2015)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
from ftplib import FTP
import ftplib
import os
import time
import threading
import inspect
import ctypes
import Logger


###########################################################################
## Class FTPup
###########################################################################

class FTPFrame(wx.Dialog):
    def __init__(self, parent=None):
        wx.Dialog.__init__(self, parent, id=wx.ID_ANY, title=u"FTP上传", pos=wx.DefaultPosition, size=wx.Size(434, 341),
                           style=wx.DEFAULT_DIALOG_STYLE)

        self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)

        bSizer3 = wx.BoxSizer(wx.VERTICAL)

        self.m_staticText11 = wx.StaticText(self, wx.ID_ANY, u"上传进度", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText11.Wrap(-1)
        bSizer3.Add(self.m_staticText11, 0, wx.ALL, 5)

        self.Progess = wx.Gauge(self, wx.ID_ANY, 100, wx.DefaultPosition, wx.DefaultSize,
                                wx.GA_HORIZONTAL | wx.GA_SMOOTH)
        self.Progess.SetValue(0)
        bSizer3.Add(self.Progess, 0, wx.ALL | wx.EXPAND, 5)

        self.Status = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize,
                                  wx.TE_MULTILINE | wx.TE_READONLY)
        bSizer3.Add(self.Status, 1, wx.ALL | wx.EXPAND, 5)

        Buttons = wx.StdDialogButtonSizer()
        self.ButtonsOK = wx.Button(self, wx.ID_OK)
        Buttons.AddButton(self.ButtonsOK)
        self.ButtonsCancel = wx.Button(self, wx.ID_CANCEL)
        Buttons.AddButton(self.ButtonsCancel)
        Buttons.Realize();

        bSizer3.Add(Buttons, 0, wx.ALIGN_RIGHT, 5)

        self.SetSizer(bSizer3)
        self.Layout()

        self.Centre(wx.BOTH)

        # Connect Events
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        self.ButtonsCancel.Bind(wx.EVT_BUTTON, self.OnCancel)
        self.ButtonsOK.Bind(wx.EVT_BUTTON, self.OnCancel)


    def __del__(self):
        pass

    # Virtual event handlers, overide them in your derived class
    def OnClose(self, event):
        if hasattr(self, 'upload') and self.upload.t.isAlive():
            Res = wx.MessageBox(u'正在上传中，确定要退出？', u"FTP上传", wx.YES_NO | wx.YES_DEFAULT | wx.CENTRE | wx.STAY_ON_TOP | wx.ICON_EXCLAMATION)
            if Res == wx.YES:
                if self.upload.t.isAlive():
                    self.upload.t.terminate()
                    self.Destroy()
        else:
            self.Destroy()

    def OnCancel(self, event):
        self.Close()

def endWith(*endstring):
    ends = endstring

    def run(s):
        f = map(s.endswith, ends)
        if True in f:
            return s

    return run

def FTP_pending(localpath):
    if os.path.exists(localpath):
        list_file = os.listdir(localpath)
        a = endWith('.log', '.log~p')
        f_file = filter(a, list_file)
        if f_file:
            return True
    return False

def _async_raise(tid, exctype):
    """raises the exception, performs cleanup if needed"""
    if not inspect.isclass(exctype):
        raise TypeError("Only types can be raised (not instances)")
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        # """if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect"""
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, 0)
        raise SystemError("PyThreadState_SetAsyncExc failed")

class Thread(threading.Thread):
    def _get_my_tid(self):
        """determines this (self's) thread id"""
        if not self.isAlive():
            raise threading.ThreadError("the thread is not active")
        # do we have it cached?
        if hasattr(self, "_thread_id"):
            return self._thread_id
        # no, look for it in the _active dict
        for tid, tobj in threading._active.items():
            if tobj is self:
                self._thread_id = tid
                return tid
        raise AssertionError("could not determine the thread's id")
    def raise_exc(self, exctype):
        """raises the given exception type in the context of this thread"""
        _async_raise(self._get_my_tid(), exctype)
    def terminate(self):
        """raises SystemExit in the context of the given thread, which should 
        cause the thread to exit silently (unless caught)"""
        self.raise_exc(SystemExit)

class FTPup():
    def __init__(self, lock, writer = None, Progess = None, button = None):
        self.__lock = lock
        self.writer = writer
        self.Progess = Progess
        self.Buttons = button

    def __del__(self):
        pass

    def Begin(self, args):
        print 'Begin upload'
        self.t = Thread(target=self.Upload, args=args)
        self.t.start()

    def Message(self,str):
        if self.writer!=None:
            self.writer.AppendText(str)
        else:
            Logger.logger.info(str)

    def Upload(self, setting, localpath):
        import os
        linespace = os.linesep
        self.Message(u'扫描本地日志文件夹:%s...'%os.path.abspath(localpath)+linespace)
        if os.path.exists(localpath):
            list_file = os.listdir(localpath)
            a = endWith('.log')
            log_file = filter(a, list_file)
            if log_file:
                num = len(log_file)
                self.Message(u'共找到%d个待上传文件'%num + linespace)
                if self.Progess != None: self.Progess.SetRange(num)
                failed = 0
                cnt = 1
                ftp = self.ftpinit(setting)
                if ftp != None:
                    for x in log_file:
                        # x = unicode(x, 'gbk')
                        self.Message(u'正在上传：%s...' % x + linespace)
                        if not self.RealUpload(x, localpath, ftp, cnt, num):
                            failed += 1
                        if self.Progess != None: self.Progess.SetValue(self.Progess.GetValue() + 1)
                        cnt += 1
                    self.Message(u'上传完成！成功：%d个， 失败：%d个'%(num-failed, failed) + linespace)
                    # ftp.quit()
            else:
                self.Message(u'无可上传文件！' + linespace)
        else:
            self.Message(u'访问本地日志文件夹失败！' + linespace)
        if self.Buttons != None:
            self.Buttons[0].Enable(True)
            self.Buttons[1].Enable(False)
        print 'end upload'

    def RealUpload(self, x, localpath, ftp, mycnt, num):
        # 改名
        filepath = os.path.join(localpath, x)
        # if x.endswith('.log'):
        #     new = filepath + '~p'
        #     #*******************************************
        #     while True:
        #         try:
        #             os.rename(filepath, new)
        #             break
        #         except IndentationError, e:
        #             (pa, tmb) = os.path.split(new)
        #             (base, ext) = os.path.splitext(tmb)
        #             li = base.split('+')
        #             if len(li) <= 1:
        #                 tmp = 0
        #             else:
        #                 tmp = int(li[1]) + 1
        #                 new = os.path.join(pa, li[0] + '+' + str(tmp) + ext)
        #             continue
        #         except WindowsError, e:
        #             if e.winerror == 32:
        #                 res = FileCopy(filepath, new, self.__lock)
        #                 if res != '':
        #                     self.Message(u'临时文件生成异常，异常信息：%s' % res + os.linesep)
        #                     return False
        #                 break
        #             else:
        #                 self.Message(u'访问异常，异常信息：%s' % repr(e) + os.linesep)
        #                 return False
        #         except Exception, e:
        #             self.Message(u'访问异常，异常信息：%s'%repr(e) + os.linesep)
        #             return False
        #     filepath = new
        # 代码重试机制
        retry = 5
        cnt = 0
        interval = 2
        while True:
            try:
                # 上传工作
                ftpup(ftp, filepath, self.__lock)
                try:
                    os.remove(filepath.encode('gbk'))
                except Exception,e:
                    pass
                # 上传成功
                self.Message(u'%s上传成功!(%d/%d)' % (x, mycnt, num) + os.linesep)
                return True
            except Exception, e:
                self.Message(u'上传失败，异常信息：%s'%repr(e) + os.linesep)
                if cnt < retry:
                    cnt += 1
                    self.Message(u'%d秒之后重试上传' % interval + os.linesep)
                    time.sleep(interval)
                    continue
                else:
                    return False

    def ftpinit(self, setting):
        ftp = FTP()
        ftp.set_debuglevel(0)
        # 打开调试级别2，显示详细信息;0为关闭调试信息
        try:
            ftp.connect(setting['host'], setting['port'], 600)  # 连接
        except Exception, e:
            self.Message(u'FTP连接失败，错误信息：%s' % str(repr(e)) + os.linesep)
            return None
        self.Message(u'FTP连接成功！' + os.linesep)
        try:
            ftp.login(setting['usr'], setting['pwd'])
        except Exception, e:
            self.Message(u'FTP登录失败，错误信息：%s' % str(repr(e)) + os.linesep)
            return None
        self.Message(u'FTP登录成功！' + os.linesep)
        path = setting['path']
        while True:
            try:
                ftp.cwd(path)
                break
            except ftplib.Error, e:
                if e[:3] == '550':
                    ftpmkds(ftp, path)
                    continue
            except Exception, e:
                self.Message(u'FTP更改当前目录失败， 错误信息：%s' % str(repr(e)) + os.linesep)
                return None
        return ftp

def ftpmkds(ftp, path):
    curr = ftp.pwd()
    head, tail = os.path.split(path)
    if not tail:
        head, tail = os.path.split(head)
    print head, tail
    if head and tail:
        while True:
            try:
                ftp.cwd(head)
                break
            except ftplib.error_perm, e:
                if str(e)[:3] == '550':
                    ftpmkds(ftp, head)
                    if tail == '.':
                        return
                    continue
    print ftp.pwd()
    ftp.mkd(tail)
    ftp.cwd(curr)

def ftpup(ftp,filepath, lock):
    # 选择操作目录
    bufsize = 1024
    # 设置缓冲块大小
    file_handler = open(filepath, 'rb')
    # 以读模式在本地打开文件
    lock.acquire_read()
    ftp.storbinary('STOR %s' % os.path.basename(filepath), file_handler, bufsize)
    lock.release()
    # 上传文件
    file_handler.close()

def FileCopy(oldname, newname, lock=None):
    import win32file
    # 拷文件
    # 文件已存在时，1为不覆盖，0为覆盖
    if lock!=None: lock.acquire_read()
    try:
        win32file.CopyFile(oldname, newname, True)
        if lock != None: lock.release()
        return ''
    except Exception, e:
        if lock != None: lock.release()
        return repr(e)

from ctypes import cdll
import os

_sopen = cdll.msvcrt._sopen
_close = cdll.msvcrt._close
_SH_DENYRW = 0x10

def is_open(filename):
    if not os.access(filename, os.F_OK):
        return False # file doesn't exist
    h = _sopen(filename, 0, _SH_DENYRW, 0)
    if h == 3:
        _close(h)
        return False # file is not opened by anyone else
    return True # file is already open

if __name__ == '__main__':
    pass