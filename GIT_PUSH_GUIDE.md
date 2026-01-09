# Git 推送指南

## 当前状态

✅ 代码已成功提交到本地 Git 仓库
✅ 提交信息：`Initial commit: Android WebView App with splash screen`
✅ 分支：`main`

## 推送到 GitHub

### 方法 1：使用 HTTPS（推荐）

```bash
cd c:/code/ssl_apk_test
git push -u origin main
```

如果提示输入用户名和密码/Token：
- **用户名**：您的 GitHub 用户名
- **密码**：使用 GitHub Personal Access Token（不是登录密码）

### 创建 GitHub Personal Access Token：

1. 访问：https://github.com/settings/tokens
2. 点击 **Generate new token (classic)**
3. 选择权限：
   - ✅ `repo`（完整仓库权限）
   - ✅ `workflow`（如果需要 GitHub Actions）
4. 点击 **Generate token**
5. **复制生成的 token**（只显示一次，请保存好）
6. 在 Git 推送时使用这个 token 作为密码

### 方法 2：使用 SSH

```bash
cd c:/code/ssl_apk_test
git remote set-url origin git@github.com:hanyuyang197/adc_app_ssl.git
git push -u origin main
```

**前提条件：**
- 已配置 SSH 密钥到 GitHub
- SSH 公钥已添加到 GitHub 账户

## 提交的文件清单

### 已提交的核心文件：
- ✅ `.gitignore` - Git 忽略配置
- ✅ `app/` - 应用模块源码
  - `src/main/` - 源代码和资源
  - `build.gradle.kts` - 应用构建配置
  - `proguard-rules.pro` - 混淆规则
- ✅ `build.gradle.kts` - 项目级构建配置
- ✅ `settings.gradle.kts` - Gradle 设置
- ✅ `gradle/` - Gradle Wrapper 配置
- ✅ `gradlew` / `gradlew.bat` - Gradle Wrapper 脚本
- ✅ `build_apk.py` - Python 打包脚本
- ✅ `build.bat` - Windows 批处理脚本
- ✅ `gradle.properties` - Gradle 属性配置
- ✅ `local.properties.template` - 本地配置模板
- ✅ `小白入门手册.md` - 项目说明文档
- ✅ 各种快捷构建脚本

### 已忽略的文件（不会提交）：
- ❌ `.gradle/` - Gradle 缓存
- ❌ `.idea/` - Android Studio 配置
- ❌ `.vscode/` - VS Code 配置
- ❌ `app/build/` - 构建输出
- ❌ `build/` - 构建输出
- ❌ `*.apk` - APK 文件
- ❌ `local.properties` - 本地配置（包含 SDK 路径）

## 项目信息

- **应用 ID**: `com.example.webviewapp`
- **包名**: `com.example.webviewapp`
- **最低 SDK**: 21 (Android 5.0)
- **目标 SDK**: 34 (Android 14)
- **Java 版本**: 17
- **Gradle 版本**: 9.0-milestone-1
- **AGP 版本**: 8.2.0

## 后续开发建议

1. **创建新分支进行开发：**
   ```bash
   git checkout -b feature/new-feature
   ```

2. **提交更改：**
   ```bash
   git add .
   git commit -m "描述你的更改"
   ```

3. **推送到远程：**
   ```bash
   git push origin feature/new-feature
   ```

4. **合并到主分支：**
   ```bash
   git checkout main
   git merge feature/new-feature
   git push origin main
   ```

## 构建 APK

在克隆仓库后首次构建：

```bash
# 1. 复制配置模板
cp local.properties.template local.properties

# 2. 编辑 local.properties，设置 SDK 路径
# sdk.dir=C:\\Users\\你的用户名\\AppData\\Local\\Android\\Sdk

# 3. 构建 APK
gradlew.bat assembleDebug
```

或使用 Android Studio 打开项目直接构建。
