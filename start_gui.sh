#!/bin/bash

echo "===================================="
echo "四进制基因编程演化系统"
echo "===================================="
echo ""
echo "正在启动图形化界面..."
echo ""

python3 gui_app.py

if [ $? -ne 0 ]; then
    echo ""
    echo "[错误] 程序启动失败！"
    echo ""
    echo "可能的原因："
    echo "1. Python3未安装"
    echo "2. tkinter模块缺失"
    echo ""
    echo "解决方案："
    echo "Ubuntu/Debian: sudo apt-get install python3-tk"
    echo "CentOS/RHEL: sudo yum install python3-tkinter"
    echo "macOS: brew install python-tk"
    echo ""
    read -p "按任意键退出..."
fi
