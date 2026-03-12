@echo off
chcp 65001 >nul
echo ========================================
echo 四进制基因编程演化系统 - GitHub 推送脚本
echo ========================================
echo.

cd /d "%~dp0"

echo [步骤 1/7] 检查 Git 是否已安装...
git --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 错误: 未检测到 Git，请先安装 Git
    echo 下载地址: https://git-scm.com/download/win
    pause
    exit /b 1
)
echo ✅ Git 已安装
echo.

echo [步骤 2/7] 初始化 Git 仓库...
if not exist ".git" (
    git init
    echo ✅ Git 仓库已初始化
) else (
    echo ✅ Git 仓库已存在
)
echo.

echo [步骤 3/7] 配置默认分支为 main...
git branch -M main
echo ✅ 默认分支已设置为 main
echo.

echo [步骤 4/7] 添加所有文件到暂存区...
git add .
echo ✅ 文件已添加到暂存区
echo.

echo [步骤 5/7] 查看将要提交的文件...
git status
echo.

echo [步骤 6/7] 提交文件...
git commit -m "Initial commit: 四进制基因编程演化系统 v1.0" -m "- 完整的四进制基因编程演化框架" -m "- 支持 GUI 界面操作" -m "- 包含完整文档和示例" -m "- Apache 2.0 License"
if errorlevel 1 (
    echo ⚠️ 提交失败或没有新的更改
) else (
    echo ✅ 文件已提交到本地仓库
)
echo.

echo [步骤 7/7] 添加 GitHub 远程仓库并推送...
echo.
echo ⚠️ 请先在 GitHub 创建一个新的空仓库
echo    仓库名建议: quaternary-genetic-evolution
echo    不要勾选 "Initialize this repository with a README"
echo.
echo 创建完成后，复制仓库 URL (例如: https://github.com/yingjiezhu/quaternary-genetic-evolution.git)
echo.
set /p REPO_URL="请输入 GitHub 仓库 URL: "

if "%REPO_URL%"=="" (
    echo ❌ 错误: 未输入仓库 URL
    pause
    exit /b 1
)

echo.
echo 正在添加远程仓库...
git remote remove origin >nul 2>&1
git remote add origin %REPO_URL%
echo ✅ 远程仓库已添加
echo.

echo 正在推送到 GitHub (main 分支)...
git push -u origin main
if errorlevel 1 (
    echo.
    echo ❌ 推送失败！可能的原因：
    echo    1. 网络问题
    echo    2. 仓库 URL 错误
    echo    3. 没有权限（需要配置 GitHub 凭据）
    echo    4. 仓库不是空的（已有内容）
    echo.
    echo 💡 解决方法：
    echo    - 如果是权限问题，请配置 GitHub Personal Access Token
    echo    - 如果仓库不为空，可以使用: git push -u origin main --force
    pause
    exit /b 1
)

echo.
echo ========================================
echo ✅ 成功！项目已推送到 GitHub
echo ========================================
echo.
echo 🎉 你的项目现在可以通过以下地址访问:
echo    %REPO_URL%
echo.
echo 📝 后续操作建议:
echo    1. 在 GitHub 上完善项目描述和标签
echo    2. 添加项目封面图片
echo    3. 设置 About 信息
echo    4. 邀请协作者（如需要）
echo.
pause
