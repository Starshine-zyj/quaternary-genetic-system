@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo 正在初始化 Git 仓库...
git init
if errorlevel 1 goto error

echo 正在设置默认分支为 main...
git branch -M main
if errorlevel 1 goto error

echo 正在添加所有文件...
git add .
if errorlevel 1 goto error

echo 正在创建初始提交...
git commit -m "Initial commit: 四进制基因编程演化系统 v1.0" -m "- 完整的四进制基因编程演化框架" -m "- 支持 GUI 界面操作" -m "- 包含完整文档和示例" -m "- Apache 2.0 License"
if errorlevel 1 goto error

echo.
echo ========================================
echo ✅ 成功！本地仓库已准备就绪
echo ========================================
echo.
echo 📝 提交历史:
git log --oneline
echo.
echo 📝 分支信息:
git branch
echo.
echo 📝 接下来请运行: git_push_to_github.bat
echo    来推送到 GitHub
echo.
pause
exit /b 0

:error
echo.
echo ❌ 错误: 操作失败
pause
exit /b 1
