:: �޸ļƻ���������������ĵ�������������ǰ���û����ҳ���437 MS-DOS ����Ӣ��
@echo off
chcp 437
schtasks /Create /TN SmartLogger /TR "\"%~dp0SL.exe\"" /RL HIGHEST /SC ONLOGON /F
::��ʼ��������Ϊsmdb_agent������ƻ�����
schtasks.exe /query /xml /tn SmartLogger > c:\SLTMP.xml
goto modifyAgent

:modifyAgent
::���µ��޸Ĳ�����Ҫ���޸�xml���run directory������str1����Ҫ��ӵ����ݣ�����ڴ���"Command"�ַ����еĺ���һ��
set "str1=^<WorkingDirectory^>%~dsp0^<^/WorkingDirectory^>"
for /f "delims=!" %%i in ('type c:\SLTMP.xml') do (
echo %%i >> c:\SLTMPN.xml
echo "%%i"|findstr "Command" >nul&&echo %str1%>>c:\SLTMPN.xml)
goto import

::�޸���ɺ�Ϳ��Ը��ǵ�����
:import
schtasks.exe /create /tn SmartLogger /xml c:\SLTMPN.xml /f
del c:\SLTMP.xml /F
del c:\SLTMPN.xml /F
schtasks /Run /TN SmartLogger
