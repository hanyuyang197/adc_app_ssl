#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Android APK一键打包脚本
支持Windows系统，自动检查环境并构建APK
"""

import os
import sys
import subprocess
import platform
from pathlib import Path


class Colors:
    """终端颜色"""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'


def print_info(message):
    """输出信息"""
    print(f"{Colors.BLUE}[INFO]{Colors.RESET} {message}")


def print_success(message):
    """输出成功信息"""
    print(f"{Colors.GREEN}[SUCCESS]{Colors.RESET} {message}")


def print_error(message):
    """输出错误信息"""
    print(f"{Colors.RED}[ERROR]{Colors.RESET} {message}")


def print_warning(message):
    """输出警告信息"""
    print(f"{Colors.YELLOW}[WARNING]{Colors.RESET} {message}")


def check_local_properties():
    """检查local.properties文件"""
    local_properties = Path(__file__).parent / "local.properties"
    if not local_properties.exists():
        print_warning("local.properties文件不存在")
        print_info("将从local.properties.template创建...")
        template = Path(__file__).parent / "local.properties.template"
        if template.exists():
            import shutil
            shutil.copy(template, local_properties)
            print_info("已创建local.properties文件")
            print_warning("请编辑local.properties文件，设置sdk.dir为你的Android SDK路径")
            print_warning("例如: sdk.dir=C:\\Users\\你的用户名\\AppData\\Local\\Android\\Sdk")
            return False
        else:
            print_error("local.properties.template也不存在")
            return False

    # 检查sdk.dir是否配置
    with open(local_properties, 'r', encoding='utf-8') as f:
        content = f.read()
        if 'sdk.dir' not in content or 'sdk.dir=' not in content:
            print_error("local.properties中未找到sdk.dir配置")
            print_info("请在local.properties文件中添加: sdk.dir=你的Android SDK路径")
            return False

    print_success("local.properties配置检查通过")
    return True


def check_gradlew():
    """检查gradlew文件"""
    script_dir = Path(__file__).parent
    system = platform.system()

    if system == "Windows":
        gradlew = script_dir / "gradlew.bat"
    else:
        gradlew = script_dir / "gradlew"

    if not gradlew.exists():
        print_error("gradlew文件不存在")
        print_info("项目缺少gradlew构建脚本，请检查项目结构")
        return False

    # 检查是否可执行
    if system != "Windows":
        if not os.access(gradlew, os.X_OK):
            print_info("添加gradlew执行权限...")
            os.chmod(gradlew, 0o755)

    print_success("gradlew检查通过")
    return True


def check_java():
    """检查Java环境"""
    try:
        result = subprocess.run(
            ['java', '-version'],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.stderr:
            version_line = result.stderr.split('\n')[0]
            print_info(f"Java版本: {version_line}")
            return True
    except FileNotFoundError:
        pass
    except Exception as e:
        print_warning(f"检查Java时出错: {e}")

    print_error("未找到Java，请先安装Java JDK (推荐JDK 8或更高版本)")
    return False


def build_apk(build_type="debug"):
    """
    构建APK

    Args:
        build_type: 构建类型，"debug"或"release"
    """
    print_info(f"开始构建{build_type}版本APK...")

    script_dir = Path(__file__).parent
    system = platform.system()

    if system == "Windows":
        gradlew = "gradlew.bat"
    else:
        gradlew = "./gradlew"

    # 构建命令
    if build_type == "debug":
        task = "assembleDebug"
        apk_pattern = "*-debug.apk"
    else:
        task = "assembleRelease"
        apk_pattern = "*-release.apk"

    print_info(f"执行命令: {gradlew} {task}")

    try:
        # 执行构建
        result = subprocess.run(
            [gradlew, task],
            cwd=script_dir,
            capture_output=True,
            text=True,
            timeout=300  # 5分钟超时
        )

        if result.returncode == 0:
            print_success("构建成功！")

            # 查找生成的APK
            apk_dir = script_dir / "app" / "build" / "outputs" / "apk" / build_type
            apks = list(apk_dir.glob(apk_pattern))

            if apks:
                apk_path = apks[0]
                file_size = apk_path.stat().st_size / 1024 / 1024  # MB
                print_success(f"APK文件: {apk_path}")
                print_success(f"APK大小: {file_size:.2f} MB")

                # 复制到项目根目录（可选）
                dest_apk = script_dir / apk_path.name
                import shutil
                shutil.copy2(apk_path, dest_apk)
                print_success(f"APK已复制到: {dest_apk}")

                return apk_path
            else:
                print_error("未找到生成的APK文件")
                return None
        else:
            print_error("构建失败！")
            print_error(result.stderr)
            return None

    except subprocess.TimeoutExpired:
        print_error("构建超时（超过5分钟）")
        return None
    except Exception as e:
        print_error(f"构建过程中出错: {e}")
        return None


def clean_build():
    """清理构建"""
    print_info("清理构建...")

    script_dir = Path(__file__).parent
    system = platform.system()

    if system == "Windows":
        gradlew = "gradlew.bat"
    else:
        gradlew = "./gradlew"

    try:
        result = subprocess.run(
            [gradlew, "clean"],
            cwd=script_dir,
            capture_output=True,
            text=True,
            timeout=60
        )

        if result.returncode == 0:
            print_success("清理完成")
            return True
        else:
            print_error("清理失败")
            print_error(result.stderr)
            return False
    except Exception as e:
        print_error(f"清理时出错: {e}")
        return False


def print_menu():
    """打印菜单"""
    print("\n" + "="*50)
    print("           Android APK 打包工具")
    print("="*50)
    print("1. 构建Debug版本APK")
    print("2. 构建Release版本APK")
    print("3. 清理构建")
    print("4. 构建Debug + 构建Release")
    print("5. 退出")
    print("="*50)


def main():
    """主函数"""
    print("\n" + "="*50)
    print("           Android APK 一键打包工具")
    print("="*50)
    print_info(f"当前系统: {platform.system()} {platform.release()}")
    print_info(f"Python版本: {sys.version.split()[0]}")

    # 检查环境
    print("\n检查构建环境...")
    checks_passed = True

    if not check_java():
        checks_passed = False

    if not check_local_properties():
        checks_passed = False

    if not check_gradlew():
        checks_passed = False

    if not checks_passed:
        print_error("环境检查失败，请先解决上述问题")
        input("\n按回车键退出...")
        sys.exit(1)

    print_success("所有环境检查通过！")

    # 命令行参数处理
    if len(sys.argv) > 1:
        arg = sys.argv[1].lower()
        if arg == "debug":
            build_apk("debug")
        elif arg == "release":
            build_apk("release")
        elif arg == "clean":
            clean_build()
        elif arg == "all":
            build_apk("debug")
            build_apk("release")
        else:
            print_error(f"未知参数: {arg}")
            print_info("用法: python build_apk.py [debug|release|clean|all]")
        return

    # 交互式菜单
    while True:
        print_menu()
        choice = input("\n请选择操作 (1-5): ").strip()

        if choice == "1":
            build_apk("debug")
        elif choice == "2":
            build_apk("release")
        elif choice == "3":
            clean_build()
        elif choice == "4":
            build_apk("debug")
            build_apk("release")
        elif choice == "5":
            print_info("退出")
            break
        else:
            print_error("无效选择，请重新输入")

        input("\n按回车键继续...")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print_info("\n\n用户中断")
        sys.exit(0)
    except Exception as e:
        print_error(f"程序异常: {e}")
        import traceback
        traceback.print_exc()
        input("\n按回车键退出...")
