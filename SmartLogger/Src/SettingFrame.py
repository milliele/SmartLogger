# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version Jun 17 2015)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import Logger
import os

###########################################################################
## Class SettingFrame
###########################################################################

class SettingFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"选项", pos=wx.DefaultPosition, size=wx.Size(584, 435),
                          style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)

        MainSizer = wx.BoxSizer(wx.VERTICAL)

        Info_Host = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"本机信息"), wx.VERTICAL)

        HostSizer = wx.FlexGridSizer(0, 2, 0, 0)
        HostSizer.SetFlexibleDirection(wx.BOTH)
        HostSizer.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.l_machine = wx.StaticText(Info_Host.GetStaticBox(), wx.ID_ANY, u"计算机名：", wx.DefaultPosition,
                                       wx.DefaultSize, 0)
        self.l_machine.Wrap(-1)
        HostSizer.Add(self.l_machine, 0, wx.ALL | wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, 5)

        self.v_machine = wx.TextCtrl(Info_Host.GetStaticBox(), wx.ID_ANY, u"123434", wx.DefaultPosition,
                                     wx.Size(200, -1), 0)
        self.v_machine.SetMaxLength(255)
        HostSizer.Add(self.v_machine, 0, wx.ALL, 5)

        self.l_ip = wx.StaticText(Info_Host.GetStaticBox(), wx.ID_ANY, u"IP地址：", wx.DefaultPosition, wx.DefaultSize, 0)
        self.l_ip.Wrap(-1)
        HostSizer.Add(self.l_ip, 0, wx.ALL | wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, 5)

        self.v_ip = wx.TextCtrl(Info_Host.GetStaticBox(), wx.ID_ANY, u"12412312", wx.DefaultPosition, wx.Size(200, -1),
                                0)
        self.v_ip.SetMaxLength(20)
        HostSizer.Add(self.v_ip, 0, wx.ALL, 5)

        Info_Host.Add(HostSizer, 1, wx.EXPAND, 5)

        MainSizer.Add(Info_Host, 1, wx.EXPAND, 5)

        Info_FTP = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"FTP设置"), wx.VERTICAL)

        FTPSizer = wx.GridBagSizer(0, 0)
        FTPSizer.SetFlexibleDirection(wx.BOTH)
        FTPSizer.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.l_host = wx.StaticText(Info_FTP.GetStaticBox(), wx.ID_ANY, u"主机名：", wx.DefaultPosition, wx.DefaultSize, 0)
        self.l_host.Wrap(-1)
        FTPSizer.Add(self.l_host, wx.GBPosition(0, 0), wx.GBSpan(1, 1),
                     wx.ALL | wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, 5)

        self.v_host = wx.TextCtrl(Info_FTP.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                  wx.Size(300, -1), 0)
        self.v_host.SetMaxLength(20)
        FTPSizer.Add(self.v_host, wx.GBPosition(0, 1), wx.GBSpan(1, 4), wx.ALL, 5)

        self.l_port = wx.StaticText(Info_FTP.GetStaticBox(), wx.ID_ANY, u"端口号：", wx.Point(-1, -1), wx.Size(50, -1),
                                    wx.ALIGN_RIGHT)
        self.l_port.Wrap(-1)
        FTPSizer.Add(self.l_port, wx.GBPosition(0, 5), wx.GBSpan(1, 1),
                     wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT | wx.TOP | wx.BOTTOM | wx.RIGHT, 5)

        self.v_port = wx.SpinCtrl(Info_FTP.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                  wx.Size(50, -1), wx.SP_ARROW_KEYS, 0, 65526, 0)
        FTPSizer.Add(self.v_port, wx.GBPosition(0, 6), wx.GBSpan(1, 1), wx.ALL, 5)

        self.l_usr = wx.StaticText(Info_FTP.GetStaticBox(), wx.ID_ANY, u"用户名：", wx.DefaultPosition, wx.DefaultSize, 0)
        self.l_usr.Wrap(-1)
        FTPSizer.Add(self.l_usr, wx.GBPosition(1, 0), wx.GBSpan(1, 1),
                     wx.ALL | wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, 5)

        self.v_usr = wx.TextCtrl(Info_FTP.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                 wx.Size(200, -1), 0)
        self.v_usr.SetMaxLength(255)
        FTPSizer.Add(self.v_usr, wx.GBPosition(1, 1), wx.GBSpan(1, 2), wx.ALL, 5)

        self.l_pwd = wx.StaticText(Info_FTP.GetStaticBox(), wx.ID_ANY, u"密码：", wx.DefaultPosition, wx.Size(50, -1),
                                   wx.ALIGN_RIGHT)
        self.l_pwd.Wrap(-1)
        FTPSizer.Add(self.l_pwd, wx.GBPosition(1, 3), wx.GBSpan(1, 1),
                     wx.ALL | wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, 5)

        self.v_pwd = wx.TextCtrl(Info_FTP.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                 wx.Size(200, -1), wx.TE_PASSWORD)
        self.v_pwd.SetMaxLength(255)
        FTPSizer.Add(self.v_pwd, wx.GBPosition(1, 4), wx.GBSpan(1, 3), wx.TOP | wx.BOTTOM | wx.RIGHT, 5)

        self.l_ftppath = wx.StaticText(Info_FTP.GetStaticBox(), wx.ID_ANY, u"路径：", wx.DefaultPosition, wx.DefaultSize,
                                       0)
        self.l_ftppath.Wrap(-1)
        FTPSizer.Add(self.l_ftppath, wx.GBPosition(2, 0), wx.GBSpan(1, 1), wx.ALL | wx.ALIGN_RIGHT, 5)

        self.v_ftppath = wx.TextCtrl(Info_FTP.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                     wx.Size(465, -1), 0)
        self.v_ftppath.SetMaxLength(1000)
        FTPSizer.Add(self.v_ftppath, wx.GBPosition(2, 1), wx.GBSpan(1, 6), wx.ALL, 5)

        self.v_onshutdown = wx.CheckBox(Info_FTP.GetStaticBox(), wx.ID_ANY, u"关机前进行FTP上传", wx.DefaultPosition,
                                        wx.DefaultSize, 0)
        self.v_onshutdown.Disable()
        FTPSizer.Add(self.v_onshutdown, wx.GBPosition(3, 1), wx.GBSpan(1, 2), wx.ALL, 5)

        Info_FTP.Add(FTPSizer, 1, wx.EXPAND, 5)

        MainSizer.Add(Info_FTP, 1, wx.EXPAND, 5)

        Info_Scan = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"扫描设置"), wx.VERTICAL)

        ScanSizer = wx.GridBagSizer(0, 0)
        ScanSizer.SetFlexibleDirection(wx.BOTH)
        ScanSizer.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.l_path = wx.StaticText(Info_Scan.GetStaticBox(), wx.ID_ANY, u"日志存储路径：", wx.DefaultPosition, wx.DefaultSize,
                                    0)
        self.l_path.Wrap(-1)
        ScanSizer.Add(self.l_path, wx.GBPosition(0, 0), wx.GBSpan(1, 1),
                      wx.ALL | wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, 5)

        self.v_path = wx.DirPickerCtrl(Info_Scan.GetStaticBox(), wx.ID_ANY, wx.EmptyString, u"Select a folder",
                                       wx.DefaultPosition, wx.Size(450, -1), wx.DIRP_DEFAULT_STYLE | wx.DIRP_SMALL)
        ScanSizer.Add(self.v_path, wx.GBPosition(0, 1), wx.GBSpan(1, 2), wx.ALL, 5)

        self.l_interval = wx.StaticText(Info_Scan.GetStaticBox(), wx.ID_ANY, u"扫描时间间隔：", wx.DefaultPosition,
                                        wx.DefaultSize, 0)
        self.l_interval.Wrap(-1)
        ScanSizer.Add(self.l_interval, wx.GBPosition(1, 0), wx.GBSpan(1, 1),
                      wx.ALL | wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, 5)

        self.v_interval = wx.SpinCtrl(Info_Scan.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                      wx.DefaultSize, wx.SP_ARROW_KEYS, 1, 604800, 0)
        ScanSizer.Add(self.v_interval, wx.GBPosition(1, 1), wx.GBSpan(1, 1), wx.ALL, 5)

        self.m_staticText15 = wx.StaticText(Info_Scan.GetStaticBox(), wx.ID_ANY, u"秒", wx.DefaultPosition,
                                            wx.DefaultSize, 0)
        self.m_staticText15.Wrap(-1)
        ScanSizer.Add(self.m_staticText15, wx.GBPosition(1, 2), wx.GBSpan(1, 1), wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        Info_Scan.Add(ScanSizer, 1, wx.EXPAND, 5)

        MainSizer.Add(Info_Scan, 1, wx.EXPAND, 5)

        Buttons = wx.BoxSizer(wx.HORIZONTAL)

        self.confirm = wx.Button(self, wx.ID_ANY, u"确定", wx.DefaultPosition, wx.DefaultSize, 0)
        self.confirm.SetDefault()
        Buttons.Add(self.confirm, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.cancel = wx.Button(self, wx.ID_ANY, u"取消", wx.DefaultPosition, wx.DefaultSize, 0)
        Buttons.Add(self.cancel, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        MainSizer.Add(Buttons, 0, wx.ALIGN_RIGHT, 5)

        self.SetSizer(MainSizer)
        self.Layout()

        self.Centre(wx.BOTH)

        # Connect Events
        self.Bind(wx.EVT_SHOW, self.OnShow)
        # self.v_onshutdown.Bind(wx.EVT_CHECKBOX, self.OnFTPShut)
        self.confirm.Bind(wx.EVT_BUTTON, self.ChangeSetting)
        self.cancel.Bind(wx.EVT_BUTTON, self.CancelSetting)

    def __del__(self):
        pass

    # Virtual event handlers, overide them in your derived class
    def OnShow(self, event):
        if event.IsShown():
            print 'reload settings'
            # 出现之前把以前的参数加载
            try:
                loop = wx.App.Get().watchprocess.loop_thread
                self.v_machine.ChangeValue(str(loop.GetSetting('machine')))
                self.v_ip.ChangeValue(str(loop.GetSetting('ip')))
                self.v_path.SetPath(str(loop.GetSetting('localpath')))
                self.v_interval.SetValue(loop.GetSetting('interval'))
                ftp = loop.GetSetting('ftp')
                self.v_host.ChangeValue(str(ftp['host']))
                self.v_port.SetValue(ftp['port'])
                self.v_usr.ChangeValue(str(ftp['usr']))
                self.v_pwd.ChangeValue(str(ftp['pwd']))
                self.v_ftppath.ChangeValue(str(ftp['path']))
                self.v_onshutdown.SetValue(loop.GetSetting('onshut'))
            except Exception, e:
                wx.MessageBox(u'选项读取出错，错误信息请察看日志', u'选项显示出错')
                self.Close()

    def CheckInput(self):
        list = {u'FTP主机名': self.v_host,
                u'FTP用户名':self.v_usr }
        First = True
        message =''
        for k in list:
            if list[k].IsEmpty():
                if not First:
                    message += u'、'
                    First = False
                message += k
        if message != '':
            wx.MessageBox(u'%s不能为空！'%message, u"警告")
            return False
        else:
            return True

    def OnFTPQuit(self, event):
        event.Skip()

    def OnFTPShut(self, event):
        event.Skip()

    def ChangeSetting(self, event):
        # 先检查输入
        if self.CheckInput():
            # 然后调用watchprocess改
            loop = wx.App.Get().watchprocess.loop_thread
            args = {}
            args['machine'] = self.v_machine.GetValue()
            args['ip'] = self.v_ip.GetValue()
            args['localpath'] = self.v_path.GetPath()
            args['interval'] = self.v_interval.GetValue()
            args['ftp'] = {}
            args['ftp']['host'] = self.v_host.GetValue()
            args['ftp']['port'] = self.v_port.GetValue()
            args['ftp']['usr'] = self.v_usr.GetValue()
            args['ftp']['pwd'] = self.v_pwd.GetValue()
            args['ftp']['path'] = self.v_ftppath.GetValue()
            args['onshut'] = self.v_onshutdown.IsChecked()
            self.Close()
            for k in args:
                loop.ChangeSetting(k, args[k])
            loop.setconf()
            print 'end changing'

    def CancelSetting(self, event):
        self.Close()

def ipFormatChk(ip_str):
    import re
    pattern = r"\b(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b"
    if re.match(pattern, ip_str):
        return True
    else:
        return False

if __name__ == '__main__':
    os.mkdir('Conf')