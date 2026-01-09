@echo off
chcp 65001 >nul
REM Android APK 打包脚本 - 直接使用系统 Gradle

echo ========================================
echo           Android APK 打包工具
echo ========================================
echo.

REM 检查Java是否安装
java -version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到Java，请先安装Java JDK
    echo 下载地址: https://adoptium.net/
    pause
    exit /b 1
)

REM 检查Gradle是否安装
gradle --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到Gradle
    echo.
    echo 解决方法 1: 安装 Gradle
    echo   下载地址: https://gradle.org/install/
    echo.
    echo 解决方法 2: 使用 Android Studio 生成 Gradle Wrapper
    echo   1. 用 Android Studio 打开项目
    echo   2. 等待 Gradle 同步完成
    echo   3. 项目会自动生成 gradlew 文件
    echo.
    pause
    exit /b 1
)

REM 获取构建类型
set BUILD_TYPE=debug
if "%1"=="release" set BUILD_TYPE=release
if "%1"=="all" set BUILD_TYPE=all

REM 执行构建
echo [INFO] 开始构建 %BUILD_TYPE% 版本APK...
echo.

if "%BUILD_TYPE%"=="debug" (
    gradle assembleDebug
) else if "%BUILD_TYPE%"=="release" (
    gradle assembleRelease
) else if "%BUILD_TYPE%"=="all" (
    gradle clean assembleDebug assembleRelease
)

echo.
if errorlevel 1 (
    echo [错误] 构建失败！
) else (
    echo [成功] 构建完成！
    echo.
    echo APK 文件位置:
    if "%BUILD_TYPE%"=="debug" (
        echo   app\build\outputs\apk\debug\
    ) else if "%BUILD_TYPE%"=="release" (
        echo   app\build\outputs\apk\release\
    ) else (
        echo   app\build\outputs\apk\debug\
        echo   app\build\outputs\apk\release\
    )
)

pause
