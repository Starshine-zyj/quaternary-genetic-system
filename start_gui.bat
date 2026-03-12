@echo off
chcp 65001 > nul
title 四进制基因编程演化系统 - 图形化界面

echo ====================================
echo 四进制基因编程演化系统
echo ====================================
echo.
echo 正在启动图形化界面...
echo.

python gui_app.py

if errorlevel 1 (
    echo.
    echo [错误] 程序启动失败！
    echo.
    echo 可能的原因：
    echo 1. Python未安装或未添加到PATH
    echo 2. tkinter模块缺失
    echo.
    echo 解决方案：
    echo - 确保已安装Python 3.7+
    echo - 运行: python -c "import tkinter"
    echo.
    pause
)
