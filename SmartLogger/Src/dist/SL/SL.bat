:: 修改计划任务程序，由于中文导出报错，所以提前设置活动代码页编号437 MS-DOS 美国英语
@echo off
chcp 437
schtasks /Create /TN SmartLogger /TR "\"%~dp0SL.exe\"" /RL HIGHEST /SC ONLOGON /F
::开始导出名字为smdb_agent的任务计划程序
schtasks.exe /query /xml /tn SmartLogger > c:\SLTMP.xml
goto modifyAgent

:modifyAgent
::如下的修改操作主要是修改xml添加run directory，其中str1就是要添加的内容，添加在带有"Command"字符串行的后面一行
set "str1=^<WorkingDirectory^>%~dsp0^<^/WorkingDirectory^>"
for /f "delims=!" %%i in ('type c:\SLTMP.xml') do (
echo %%i >> c:\SLTMPN.xml
echo "%%i"|findstr "Command" >nul&&echo %str1%>>c:\SLTMPN.xml)
goto import

::修改完成后就可以覆盖导入了
:import
schtasks.exe /create /tn SmartLogger /xml c:\SLTMPN.xml /f
del c:\SLTMP.xml /F
del c:\SLTMPN.xml /F
schtasks /Run /TN SmartLogger
