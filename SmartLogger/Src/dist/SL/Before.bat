:: 修改计划任务程序，由于中文导出报错，所以提前设置活动代码页编号437 MS-DOS 美国英语
@echo off
chcp 437
taskkill /f /t /im SL.exe