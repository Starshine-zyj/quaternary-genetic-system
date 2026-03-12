#!/bin/bash

echo ""
echo "╔═══════════════════════════════════════════════════════════╗"
echo "║  四进制基因编程演化系统 v2.0                              ║"
echo "║  DNA-Powered Genetic Evolution System                     ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""
echo "[启动中] 正在加载图形化界面..."
echo ""

python3 gui_app_v2.py

if [ $? -ne 0 ]; then
    echo ""
    echo "[错误] 启动失败！"
    echo ""
    echo "可能的原因："
    echo "1. Python3未安装"
    echo "2. 缺少必要的模块"
    echo ""
    echo "解决方案："
    echo "- 确保已安装Python 3.7+"
    echo "- 运行: pip3 install -r requirements.txt"
    echo ""
    read -p "按Enter键退出..."
else
    echo ""
    echo "[完成] 程序已退出"
fi
