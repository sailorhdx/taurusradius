@echo off  
set num = 0  
For /r  . %%i in (*.pyc_dis) do (  
set /a num += 1  
echo %%i  
call echo �� %%num%% ���ļ�����ɹ�  
ren %%i *.py)   
echo ��%num%���ļ�������ɹ�  
pause>nul 