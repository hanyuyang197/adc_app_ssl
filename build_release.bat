@echo off
REM 构建 Release 版本 APK
chcp 65001 >nul

echo ========================================
echo      构建 Release 版本 APK
echo ========================================
echo.

cd /d "%~dp0"

REM 清理旧的构建
echo [1/3] 清理旧构建...
call gradlew.bat clean
if errorlevel 1 (
    echo [错误] 清理失败
    pause
    exit /b 1
)

REM 构建 Release 版本
echo.
echo [2/3] 构建 Release APK...
call gradlew.bat assembleRelease
if errorlevel 1 (
    echo [错误] 构建失败
    pause
    exit /b 1
)

REM 复制 APK 到根目录
echo.
echo [3/3] 复制 APK 文件...
if exist "app\build\outputs\apk\release\app-release.apk" (
    copy /Y "app\build\outputs\apk\release\app-release.apk" "app-release.apk"
    echo.
    echo [成功] Release APK 已生成！
    echo.
    echo 文件位置:
    echo   项目根目录: app-release.apk
    echo   构建目录: app\build\outputs\apk\release\app-release.apk
    echo.
    dir app-release.apk | find "app-release.apk"
) else (
    echo [警告] 未找到 Release APK，尝试从 intermediates 复制...
    if exist "app\build\intermediates\apk\release\app-release.apk" (
        copy /Y "app\build\intermediates\apk\release\app-release.apk" "app-release.apk"
        echo [成功] Release APK 已生成（来自 intermediates）！
    ) else (
        echo [错误] 未找到 Release APK
    )
)

echo.
echo ========================================
pause
