@echo off
REM 导航到虚拟环境目录
cd /d %~dp0

set LOG_FILE=logfile.txt

REM 激活虚拟环境
call .venv\Scripts\activate

REM 记录开始时间
call :log Script started

REM 运行 Python 脚本
python wall_barrier.py >> %LOG_FILE% 2>&1

REM 记录结束时间
call :log Script ended

pause


REM 日志记录函数
:log
echo [%date% %time%] %* >> %LOG_FILE%
exit /b