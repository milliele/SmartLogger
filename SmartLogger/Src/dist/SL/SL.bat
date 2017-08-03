:: 修改计划任务程序，由于中文导出报错，所以提前设置活动代码页编号437 MS-DOS 美国英语
@echo off
chcp 437
taskkill /f /t /im SL.exe

::goto modifyAgent

:::modifyAgent
::如下的修改操作主要是修改xml添加run directory，其中str1就是要添加的内容，添加在带有"Command"字符串行的后面一行
::set "str1=^<Command^>%~dsp0SL.exe^<^/Command^>^<WorkingDirectory^>%~dsp0^<^/WorkingDirectory^>"
::for /f "delims=!" %%i in ('type %~dsp0\SmartLogger.xml') do (
::echo "%%i"|findstr "Command" >nul|| echo "%%i"|findstr "WorkingDirectory" >nul|| echo %%i>>c:\SLTMPN.xml
::echo "%%i"|findstr "StartWhenAvailable" >nul && echo %str2%>>c:\SLTMPN.xml
::echo "%%i"|findstr "<Exec>" >nul&&echo %str1%>>c:\SLTMPN.xml)
goto import

::修改完成后就可以覆盖导入了
:import
::schtasks.exe /create /tn SmartLogger /xml c:\SLTMPN.xml /f
::del c:\SLTMP.xml /F
::del c:\SLTMPN.xml /F
schtasks /Run /TN SmartLogger
