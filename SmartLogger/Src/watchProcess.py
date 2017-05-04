# -*- coding: utf-8 -*-
# Filename : watchProcess.py
#author by :morespeech
#python2.7
#platform:pycharm,windows
#topic: practice every day
#detial: watch process


import os
import psutil
import time
import RWLock
import Logger
import FTP
import threading
import json

class Loop(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.__flag = threading.Event()  # 用于暂停线程的标识
        self.__running = threading.Event()  # 用于停止线程的标识
        self.__running.set()  # 将running设置为True
        self.log_lock = RWLock.RWLock() # 日志的读写锁
        self.setting_lock = RWLock.RWLock() # 设置的读写锁
        # ******************************** 初始化 ***********************************
        self.getconf() # 从配置文件里读取设置

        is_up = False
        while hasattr(self, 'upload') and hasattr(self.upload, 't') and self.upload.t.isAlive():
            is_up = True
        if not is_up:
            ### *********************** 此处应该隐式唤醒ftp
            Logger.logger.info(u'开机扫描')
            self.upload = FTP.FTPup(self.log_lock)
            self.upload.Begin((self.GetSetting('ftp'), self.GetSetting('localpath')))
            ### *********************** 此处应该隐式唤醒ftp

    def watchProcess(self):
        now_process = []
        for proc in psutil.process_iter():
            try:
                pinfo = proc.as_dict(attrs=['pid', 'name'])
                now_process.append((pinfo['pid'], pinfo['name']))
            except psutil.NoSuchProcess:
                pass
        return now_process

    def getconf(self):
        if not os.path.exists('Conf/default.conf'):
            Logger.logger.error("WatchProcess Configuration file not found!")
        while True:
            try:
                settings = json.load(open('Conf/default.conf', 'r'))
                break
            except ValueError,e:
                Logger.logger.warning("Reading watchProcess confugiration: " + repr(e)+ "[Returned to default setting]")
                fobj = open('Conf/default.conf', 'w')
                fobj.write('{"machine": "Zeus", "ftp": {"port": 21, "path": "", "pwd": "11", "host": "localhost", "usr": "uftp"}, "last_date": "20170503", "onshut": true, "ip": "192.168.17.1", "interval": 6, "localpath": "./"}')
                fobj.close()
                continue
        if 'localpath' not in settings:
            settings['localpath'] = ''
        # 获取时间间隔
        if not ('interval' in settings and settings['interval'] != ''):
            settings['interval'] = 5
        # 获取FTP设置
        if 'ftp' not in settings: settings['ftp']= {'host':'localhost',
                   'port': 21,
                   'path':'',
                   'usr':'uftp',
                   'pwd':'11'}
        if 'onshut' not in settings: settings['onshut'] = True
        # 获取最后日期
        if 'last_date' not in settings:
            settings['last_date'] = ''
        for k in settings:
            self.ChangeSetting(k, settings[k])
        self.setconf()

    def setconf(self):
        Logger.logger.info(u'保存设置到文件...')
        settings = {'machine': self.GetSetting('machine'),
                    'ip': self.GetSetting('ip'),
                    'interval': self.GetSetting('interval'),
                    'localpath': self.GetSetting('localpath'),
                    'ftp':self.GetSetting('ftp'),
                    'last_date': self.GetSetting('last_date'),
                    'onshut':self.GetSetting('onshut')}
        json.dump(settings, open('Conf/default.conf', 'w'))

    def ChangeSetting(self, key, value):
        self.setting_lock.acquire_write()
        if key == 'machine':
            if value == '':
                import socket
                self.machine = socket.gethostname()
            else:
                self.machine = value
        if key == 'ip':
            if value =='':
                import socket
                self.ip = socket.gethostbyname(socket.gethostname())  # 得到本地ip
            else:
                self.ip = value
        if key == 'localpath':
            if not os.path.exists(os.path.abspath(value)):
                os.makedirs(value)
            if hasattr(self, 'path') and not samepath(value, self.path):
                Logger.logger.info(u'修改后与修改前是同一路径')
                if hasattr(self, 'fobj') and not self.fobj.closed:
                    self.fobj.close()
                import thread
                import copy
                tmp = copy.deepcopy(self.path)
                thread.start_new_thread(deliver_file, args=(tmp, value))
            self.path = value
        if key == 'interval':
            self.interval = value
        if key == 'ftp':
            self.ftp = value
        if key == 'last_date':
            self.last_date = value
        if key == 'onshut': self.onshut = value
        self.setting_lock.release()

    def GetSetting(self, key):
        self.setting_lock.acquire_read()
        if key == 'machine': res = self.machine
        if key == 'ip': res = self.ip
        if key == 'localpath': res = self.path
        if key == 'interval': res = self.interval
        if key == 'ftp': res = self.ftp
        if key == 'last_date': res = self.last_date
        if key == 'onshut': res = self.onshut
        self.setting_lock.release()
        return res

    def Filename(self):
        date = time.strftime('%Y%m%d', time.localtime(time.time()))
        # 新的一天
        filename = os.path.join(self.GetSetting('localpath'), '-'.join([self.GetSetting('machine'), self.GetSetting('ip'), date]) + '.log')
        if not hasattr(self, 'filename') or filename != self.filename:
            print filename
            if hasattr(self, 'fobj') and not self.fobj.closed:
                self.fobj.close()
            if date != self.GetSetting('last_date'):
                ### *********************** 此处应该隐式唤醒ftp
                Logger.logger.info(u'新的一天上传前天文件...')
                self.upload = FTP.FTPup(self.log_lock)
                self.upload.Begin((self.GetSetting('ftp'), self.GetSetting('localpath')))
                ### *********************** 此处应该隐式唤醒ftp
                self.ChangeSetting('last_date', date)
            self.filename = filename
        if not hasattr(self, 'fobj') or self.fobj.closed:
            self.fobj = open(self.filename, 'a')

    def run(self):
        # ******************************** 不断刷新扫描 ***********************************
        last_info = {}
        while self.__running.isSet():
            try:
                self.__flag.wait()
                # if self.pending_settings != {}:
                #     self.ChangeSetting(**self.pending_settings)
                #     self.pending_settings={}
                self.Filename()
                clock = time.strftime('%Y-%m-%d %H:%M:%S %a', time.localtime(time.time()))
                print clock
                now_info = self.watchProcess()
                new_in = list(set(now_info).difference(set(last_info)))  # 新启动的
                new_out = list(set(last_info).difference(set(now_info)))  # 消失的
                last_info = now_info
                if new_in or new_out:
                    self.log_lock.acquire_write()
                    json.dump({
                        'time': clock,
                        'in': new_in,
                        'out': new_out
                    }, self.fobj)
                    self.fobj.write(os.linesep)
                    self.log_lock.release()

            # ************************************* 捕获异常 *******************************
            except Exception, e:
                import traceback
                Logger.logger.error(u'扫描程序错误，错误信息：%s' % traceback.format_exc(e))
                if hasattr(self,'fobj') and not self.fobj.closed:
                    self.fobj.close()
                continue
            time.sleep(self.GetSetting('interval'))
        # ******************************** 不断刷新扫描 ***********************************

    def pause(self):
        if hasattr(self, 'fobj') and not self.fobj.closed:
            self.fobj.close()
        self.__flag.clear()  # 设置为False, 让线程阻塞

    def resume(self):
        self.__flag.set()  # 设置为True, 让线程停止阻塞
        if not (hasattr(self, 'fobj') and not self.fobj.closed) and hasattr(self, 'filename'):
            self.fobj = open(self.filename, 'a')

    def stop(self):
        self.__flag.set()  # 将线程从暂停状态恢复, 如何已经暂停的话
        self.__running.clear()  # 设置为False
        print 'enter stop'
        if hasattr(self, 'fobj') and not self.fobj.closed:
            self.fobj.close()
        self.setconf()

    def is_running(self):
        return self.__running.is_set()

    def is_pause(self):
        return self.__flag.is_set()

    def __del__(self):
        pass

class watchProcess(object):

    def __init__(self):
        # 开线程
        self.loop_thread = Loop()
        # 初始信号为False，阻塞
        self.loop_thread.start()

    def pause_scanning(self):
        self.loop_thread.pause()

    def restore_scanning(self):
        self.loop_thread.resume()

    def is_running(self):
        return self.loop_thread.is_running()

    def is_pause(self):
        return self.loop_thread.is_pause()

    def __del__(self):
        # 被销毁前记得退出子线程
        # print 'destroy watch process'
        if hasattr(self, 'loop_thread'):
            self.loop_thread.stop()
            self.loop_thread.join()

def samepath(path1, path2):
    normpath1 = os.path.normcase(os.path.abspath(path1))
    normpath2 = os.path.normcase(os.path.abspath(path2))
    return normpath1 == normpath2

def deliver_file(path1, path2):
    import FTP
    if os.path.exists(path1):
        p1 = os.path.abspath(path1)
        p2 = os.path.abspath(path2)
        Logger.logger.info(u"开始把%s路径下的日志移至%s",p1, p2)
        list_file = os.listdir(path1)
        a = FTP.endWith('.log', '.log~p')
        f_file = filter(a, list_file)
        for x in f_file:
            old = os.path.join(p1, x)
            new = os.path.join(p2, x)
            try:
                FTP.FileCopy(old, new)
            except Exception, e:
                Logger.logger.warning(u'将%s复制到%s失败，错误信息：%s' % (old, new, str(e)))
            try:
                os.remove(old)
            except Exception, e:
                Logger.logger.warning(u'删除%s失败，错误信息：%s' % (old, str(e)))
        Logger.logger.info(u"转移完成")

if __name__ == '__main__':
    print os.path.abspath('C:\\副本')