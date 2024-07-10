@echo off
:: Create the logs directory if it doesn't exist
if not exist D:\PythonProjects\SmartLeadGenerator\logs mkdir D:\PythonProjects\SmartLeadGenerator\logs

:: Get the current date in the format YYYY-MM-DD
set CURRENT_DATE=%DATE:~10,4%-%DATE:~4,2%-%DATE:~7,2%
set LOGFILE=D:\PythonProjects\SmartLeadGenerator\logs\cronjob_%CURRENT_DATE%.log

echo %DATE% %TIME% >> %LOGFILE%

cd /d D:\PythonProjects\SmartLeadGenerator
call D:\PythonProjects\SmartLeadGenerator\venv\Scripts\activate.bat
python .\manage.py fetch_upwork_jobs >> %LOGFILE% 2>&1

echo %DATE% %TIME% >> %LOGFILE%