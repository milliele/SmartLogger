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
        if self.is_background():
            wx.MessageBox(u'正在后台上传日志中，请勿手动上传', u"FTP上传", wx.ICON_EXCLAMATION)
        else:
            import FTP
            upload = FTP.FTPFrame(self.frame)
            upload.Show(True)

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
    app = MyApp()
    app.MainLoop()
