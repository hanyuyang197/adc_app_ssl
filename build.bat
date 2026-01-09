@echo off
chcp 65001 >nul
REM Android APK一键打包脚本 - Windows批处理版本

echo ========================================
echo           Android APK 打包工具
echo ========================================
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到Python，请先安装Python
    echo 下载地址: https://www.python.org/downloads/
    pause
    exit /b 1
)

REM 运行Python打包脚本
python build_apk.py %*

pause
