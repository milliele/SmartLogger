:: �޸ļƻ���������������ĵ�������������ǰ���û����ҳ���437 MS-DOS ����Ӣ��
@echo off
chcp 437
taskkill /f /t /im SL.exe

::goto modifyAgent

:::modifyAgent
::���µ��޸Ĳ�����Ҫ���޸�xml���run directory������str1����Ҫ��ӵ����ݣ�����ڴ���"Command"�ַ����еĺ���һ��
::set "str1=^<Command^>%~dsp0SL.exe^<^/Command^>^<WorkingDirectory^>%~dsp0^<^/WorkingDirectory^>"
::for /f "delims=!" %%i in ('type %~dsp0\SmartLogger.xml') do (
::echo "%%i"|findstr "Command" >nul|| echo "%%i"|findstr "WorkingDirectory" >nul|| echo %%i>>c:\SLTMPN.xml
::echo "%%i"|findstr "StartWhenAvailable" >nul && echo %str2%>>c:\SLTMPN.xml
::echo "%%i"|findstr "<Exec>" >nul&&echo %str1%>>c:\SLTMPN.xml)
goto import

::�޸���ɺ�Ϳ��Ը��ǵ�����
:import
::schtasks.exe /create /tn SmartLogger /xml c:\SLTMPN.xml /f
::del c:\SLTMP.xml /F
::del c:\SLTMPN.xml /F
schtasks /Run /TN SmartLogger
