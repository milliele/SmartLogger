#SmartLogger
##Setup.exe
安装程序，安装说明见`SmartLogger/Readme.html`
## SL.exe
真正的监控程序
## SmartLogger.exe
主要做两件事：
1. 将开机启动`SL.exe`任务添加到电脑里
2. 启动`SL.exe`

## 系统日志
存在安装目录的`ExeLog`文件夹下
## 进程日志
存在自己设定的目录下，文件名为`机器名-IP-日期.log`

#Log2CSV
把`.log`文件转换为`.csv`文件
>需要在把`.log`文件从云服务器上下载下来之后使用

1. 将`Log2CSV.exe`与日志文件放在同一目录下
2. 保证待转换的日志文件与上文所述格式相同
3. 运行程序

>CSV文件的Date栏若显示`#####`，将列宽加大即可正常显示
