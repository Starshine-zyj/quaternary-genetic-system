@echo off
chcp 65001 > nul
echo.
echo ╔═══════════════════════════════════════════════════════════╗
echo ║  四进制基因编程演化系统 v2.0                              ║
echo ║  DNA-Powered Genetic Evolution System                     ║
echo ╚═══════════════════════════════════════════════════════════╝
echo.
echo [启动中] 正在加载图形化界面...
echo.

python gui_app_v2.py

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [错误] 启动失败！
    echo.
    echo 可能的原因：
    echo 1. Python未安装或未添加到PATH
    echo 2. 缺少必要的模块
    echo.
    echo 解决方案：
    echo - 确保已安装Python 3.7+
    echo - 运行: pip install -r requirements.txt
    echo.
    pause
) else (
    echo.
    echo [完成] 程序已退出
)
