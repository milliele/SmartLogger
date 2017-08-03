# -*- coding: utf-8 -*-

import wx
import wx.xrc
import watchProcess
import Logger
import win32api
import win32gui
import win32con

class TaskBarIcon(wx.TaskBarIcon):

    def __init__(self, frame):
        wx.TaskBarIcon.__init__(self)
        self.frame = frame
        self.SetIcon(wx.Icon(name='sl.ico', type=wx.BITMAP_TYPE_ICO), u'进程记录器')
        # self.Bind(wx.EVT_TASKBAR_LEFT_DCLICK, self.OnTaskBarLeftDClick)

    def is_background(self):
        loop = wx.App.Get().watchprocess.loop_thread
        if hasattr(loop, 'upload') and hasattr(loop.upload, 't') and loop.upload.t.isAlive():
            return True
        return False

    def OnCheck(self, event):
        if self.is_background():
            wx.MessageBox(u'正在后台上传日志中...', u"FTP上传")
        else:
            wx.MessageBox(u'FTP后台上传未运行', u"FTP上传")

    def OnFTP(self, event):
        # FTP前准备
        import FTP
        if self.is_background():
            wx.MessageBox(u'正在后台上传日志中，请勿手动上传', u"FTP上传", wx.ICON_EXCLAMATION)
        else:
            # 上传前准备
            app = wx.App.Get()
            process = app.watchprocess
            is_toup = FTP.FTP_pending(process.loop_thread.GetSetting('localpath'))
            if is_toup:
                import os
                message = u'检测到有未上传的日志' + os.linesep + u'确认上传吗？' + os.linesep + u'为了顺利上传，上传前请关闭所有打开的日志文件后再点击“是”！' + os.linesep + u'上传过程中请勿打开任何临时文件！'
                res = wx.MessageBox(message, u"FTP上传",
                                    wx.YES | wx.NO | wx.YES_DEFAULT | wx.CENTRE | wx.STAY_ON_TOP | wx.ICON_EXCLAMATION)
                if res == wx.YES:
                    upload = FTP.FTPFrame(self.frame)
                    upload.Show(True)
                    upload.upload = FTP.FTPup(process.loop_thread.log_lock, upload.Status, upload.Progess,
                                        (upload.ButtonsOK, upload.ButtonsCancel))
                    upload.ButtonsOK.Enable(False)
                    upload.upload.Begin(
                        (process.loop_thread.GetSetting('ftp'), process.loop_thread.GetSetting('localpath')))
            else:
                wx.MessageBox(u'没有未上传的日志！', u"FTP上传")

    # def OnB_And_S(self, event):
    #     app = wx.App.Get()
    #     process = app.watchprocess
    #     if self.b_and_s.IsChecked():
    #         process.restore_scanning()
    #     else:
    #         process.pause_scanning()

    def OnSetting(self, event):
        import SettingFrame
        settingframe = SettingFrame.SettingFrame(self.frame)
        settingframe.Show(True)
        settingframe.Centre()

    # def OnQuit(self, event):
    #     self.frame.Close()

    # override
    def CreatePopupMenu(self):
        menu = wx.Menu()
        # # ***************************** 监控的开关 ********************
        # BS_ID = wx.NewId()
        # self.b_and_s = wx.MenuItem(menu, BS_ID, u'进程监控', u'控制是否开启进程监控', kind=wx.ITEM_CHECK)
        # self.Bind(wx.EVT_MENU, self.OnB_And_S, self.b_and_s)
        # menu.AppendItem(self.b_and_s)
        # app = wx.App.Get()
        # process = app.watchprocess
        # isactive = process.is_running() and process.is_pause()
        # self.b_and_s.Check(isactive)
        # # ***************************** 监控的开关 ********************

        # ***************************** FTP ********************
        submenu = wx.Menu()
        item = submenu.Append(wx.NewId(), u'检查是否后台上传中')
        self.Bind(wx.EVT_MENU, self.OnCheck, item)
        item = submenu.Append(wx.NewId(), u'手动上传日志')
        self.Bind(wx.EVT_MENU, self.OnFTP, item)
        menu.AppendMenu(wx.NewId(), u'FTP上传',submenu)
        # ***************************** FTP ********************

        # ***************************** 选项设置 ********************
        item = menu.Append(wx.NewId(), u'选项')
        self.Bind(wx.EVT_MENU, self.OnSetting, item)
        # ***************************** 选项设置 ********************

        # quit = menu.Append(wx.ID_EXIT, u"退出", u"退出程序")
        # self.Bind(wx.EVT_MENU, self.OnQuit, quit)
        return menu


class Frame(wx.Frame):
    def __init__(
            self, parent=None, id=wx.ID_ANY, title='TaskBarIcon', pos=wx.DefaultPosition,
            size=wx.DefaultSize, style=wx.DEFAULT_FRAME_STYLE):
        wx.Frame.__init__(self, parent, id, title, pos, size, style)
        # wx.Frame.SetIcon(wx.Icon('Wand.ico', wx.BITMAP_TYPE_ICO))
        # The above line is invalid: method become callable after bounding to the instance
        # self.SetIcon(wx.Icon('../back.ico', wx.BITMAP_TYPE_ICO))

        # panel = wx.Panel(self, wx.ID_ANY)

        # button = wx.Button(panel, wx.ID_ANY, 'Hide Frame', pos=(60, 60))
        # self.Bind(wx.EVT_BUTTON, self.OnHide, button)
        # button = wx.Button(panel, wx.ID_ANY, 'Close', pos=(60, 100))
        # self.Bind(wx.EVT_BUTTON, self.OnClose, button)
        self.Bind(wx.EVT_CLOSE, self.OnClose)

        self.Bind(wx.EVT_ICONIZE, self.OnIconfiy)  # What is the meaning?
        self.taskBarIcon = TaskBarIcon(self)

        # Set the WndProc to our function
        self.oldWndProc = win32gui.SetWindowLong(self.GetHandle(),
                                                 win32con.GWL_WNDPROC,
                                                 self.MyWndProc)
        # Make a dictionary of message names to be used for printing below
        self.msgdict = {}
        for name in dir(win32con):
            if name.startswith("WM_"):
                value = getattr(win32con, name)
                self.msgdict[value] = name

        # sizer = wx.BoxSizer()
        # sizer.Add(button, 0)
        # panel.SetSizer(sizer)

    def MyWndProc(self, hWnd, msg, wParam, lParam):
        # Display what we've got.
        Logger.logger.debug((self.msgdict.get(msg), msg, wParam, lParam))
        # 关机前
        if msg == win32con.WM_ENDSESSION or msg == win32con.WM_QUERYENDSESSION:
            # 隐式上传
            try:
                loop = wx.App.Get().watchprocess.loop_thread
                loop.setconf()
                # 结束时间当成关机时间
                import time, json, os
                clock = time.strftime('%Y-%m-%d %H:%M:%S %a', time.localtime(time.time()))
                if hasattr(loop, 'fobj') and hasattr(loop,'last_info') and loop.last_info!={}:
                    Logger.logger.info(u'把未结束进程的结束时间当成关机时间')
                    loop.log_lock.acquire_write()
                    json.dump({
                        'time': clock,
                        'in': {},
                        'out': loop.last_info
                    }, loop.fobj)
                    loop.fobj.write(os.linesep)
                    loop.fobj.flush()
                    loop.log_lock.release()
                if loop.GetSetting('onshut'):
                    is_up = False
                    Logger.logger.info(u'关机前进行FTP上传')
                    while hasattr(loop, 'upload') and hasattr(loop.upload, 't') and loop.upload.t.isAlive():
                        is_up = True
                    if not is_up:
                        ### *********************** 此处应该隐式唤醒ftp
                        import FTP
                        loop.upload = FTP.FTPup(loop.log_lock)
                        loop.upload.Begin((loop.GetSetting('ftp'), loop.GetSetting('localpath')))
                        ### *********************** 此处应该隐式唤醒ftp
                    else:
                        Logger.logger.info(u'关机时已经在进行FTP上传')
            except Exception, e:
                import traceback
                Logger.logger.warning(u'关机前上传出错，错误信息：%s' % traceback.format_exc(e))
            import msvcrt
            msvcrt.getch()

        # Restore the old WndProc. Notice the use of wxin32api
        # instead of win32gui here. This is to avoid an error due to
        # not passing a callable object.
        if msg == win32con.WM_DESTROY:
            win32api.SetWindowLong(self.GetHandle(),
                                   win32con.GWL_WNDPROC,
                                   self.oldWndProc)

        # Pass all messages (in this case, yours may be different) on
        # to the original WndProc
        return win32gui.CallWindowProc(self.oldWndProc,
                                       hWnd, msg, wParam, lParam)

    def OnHide(self, event):
        self.Hide()

    def OnIconfiy(self, event):
        # wx.MessageBox('Frame has been iconized!', 'Prompt')
        event.Skip()

    def OnClose(self, event):
        # print 'enter close'
        self.taskBarIcon.Destroy()
        self.Destroy()

class MyApp(wx.App):
    def OnInit(self):
        try:
            self.watchprocess = watchProcess.watchProcess()
            # 初始设置
            key = win32api.RegOpenKeyEx(win32con.HKEY_LOCAL_MACHINE, 'Software\\SmartLogger', 0, win32con.KEY_ALL_ACCESS)
            v = win32api.RegQueryValueEx(key, 'Launch')[0]
            if v == 'False':
                import SettingFrame
                settingframe = SettingFrame.SettingFrame(None)
                settingframe.Show(True)
                settingframe.Centre()
                win32api.RegSetValueEx(key, 'Launch', 0, win32con.REG_SZ, 'True')
                win32api.RegCloseKey(key)
                #
        except Exception, e:
            import traceback
            Logger.logger.warning(u'初始化出错， 出错信息：%s' % traceback.format_exc(e))
        self.mainframe = Frame(size=(640, 480))
        # 开始运行
        self.watchprocess.restore_scanning()
        self.mainframe.Show(False)
        return True

    def OnExit(self):
        # print "OnExit"
        del self.watchprocess


if __name__ == '__main__':
    import sys
    reload(sys)
    sys.setdefaultencoding('utf8')
    app = MyApp()
    app.MainLoop()
