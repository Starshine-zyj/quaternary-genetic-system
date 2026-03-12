@echo off
chcp 65001 >nul
echo ============================================
echo 四进制基因编程演化系统 - 打包工具
echo by yingjiezhu
echo ============================================
echo.

REM 检查 Python 环境
echo [1/6] 检查 Python 环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 错误: 未找到 Python，请先安装 Python 3.8+
    pause
    exit /b 1
)
echo ✓ Python 环境正常

REM 安装依赖
echo.
echo [2/6] 检查并安装依赖包...
pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo 正在安装 PyInstaller...
    pip install pyinstaller
) else (
    echo ✓ PyInstaller 已安装
)

pip show pillow >nul 2>&1
if errorlevel 1 (
    echo 正在安装 Pillow...
    pip install pillow
) else (
    echo ✓ Pillow 已安装
)

REM 转换图标为 ICO 格式
echo.
echo [3/6] 转换 DNA 图标为 ICO 格式...
python convert_icon.py
if errorlevel 1 (
    echo ⚠ 警告: 图标转换失败，将使用默认图标
) else (
    echo ✓ 图标转换成功
)

REM 清理旧文件
echo.
echo [4/6] 清理旧的构建文件...
if exist build rd /s /q build
if exist dist rd /s /q dist
if exist QuaternaryGeneticSystem.spec del /q QuaternaryGeneticSystem.spec
echo ✓ 清理完成

REM 开始打包
echo.
echo [5/6] 开始打包 EXE 文件...
echo 这可能需要几分钟时间，请耐心等待...
pyinstaller build_exe.spec

if errorlevel 1 (
    echo ❌ 打包失败！请检查错误信息。
    pause
    exit /b 1
)

REM 检查生成的文件
echo.
echo [6/6] 检查生成的文件...
if exist dist\QuaternaryGeneticSystem.exe (
    echo ✓ 打包成功！
    echo.
    echo ============================================
    echo 生成的文件位置:
    echo %CD%\dist\QuaternaryGeneticSystem.exe
    echo.
    echo 文件大小:
    for %%A in (dist\QuaternaryGeneticSystem.exe) do echo %%~zA 字节
    echo ============================================
    echo.
    echo 按任意键打开输出目录...
    pause >nul
    explorer dist
) else (
    echo ❌ 错误: 未找到生成的 EXE 文件！
    pause
    exit /b 1
)
