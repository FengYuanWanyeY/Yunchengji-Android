# 云成绩查询 - Android 应用

这是一个基于 Kivy 框架开发的 Android 应用，用于查询云成绩系统的考试成绩数据。

## 功能特性

- 美观的图形用户界面
- 登录云成绩系统
- 查看考试列表
- 查看详细的考试成绩
- 导出成绩数据到 Excel 文件
- 支持多科目成绩分析

## 项目结构

```
云成绩/
├── main.py              # 原始命令行版本
├── main_gui.py          # GUI 版本（用于打包 APK）
├── api.py               # API 接口封装
├── buildozer.spec       # Buildozer 配置文件
├── requirements.txt     # Python 依赖
├── create_assets.py     # 创建应用图标和启动画面
├── assets/              # 资源文件
│   ├── icon.png         # 应用图标
│   └── presplash.png    # 启动画面
└── output/              # 导出的 Excel 文件目录
```

## 使用 GitHub Actions 自动打包 APK（推荐）

这是最简单的方式，无需在本地安装任何构建工具，GitHub 会自动为你构建 APK。

### 操作步骤

1. **创建 GitHub 仓库**

   - 访问 https://github.com/new
   - 创建一个新的公开或私有仓库
   - 仓库名称可以设置为 `yunchengji` 或其他名称

2. **上传代码到 GitHub**

   在项目根目录执行以下命令：

   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/FengYuanWanyeY/Yunchengji-Android.git
   git push -u origin main
   ```

3. **查看构建状态**

   - 访问你的 GitHub 仓库
   - 点击 "Actions" 标签
   - 你会看到 "Build Android APK" 工作流正在运行

4. **下载 APK**

   构建完成后（大约需要 30-60 分钟），你可以通过以下方式下载 APK：

   **方式一：从 Actions 下载**
   - 进入 "Actions" 标签
   - 点击最新的工作流运行
   - 滚动到底部，找到 "Artifacts" 部分
   - 点击 "yunchengji-apk" 下载 ZIP 文件
   - 解压后即可获得 APK 文件

   **方式二：从 Releases 下载**
   - 进入 "Releases" 标签
   - 找到最新的 Release（例如 v1, v2 等）
   - 下载 APK 文件

5. **手动触发构建**

   除了自动触发，你也可以手动启动构建：

   - 进入 "Actions" 标签
   - 点击 "Build Android APK" 工作流
   - 点击 "Run workflow" 按钮
   - 选择分支并点击 "Run workflow"

### 工作流说明

GitHub Actions 工作流会在以下情况下自动运行：
- 推送代码到 `main` 或 `master` 分支
- 创建 Pull Request
- 手动触发

每次构建都会：
1. 安装所有必要的依赖
2. 编译 Android APK
3. 上传 APK 到 Artifacts（保留 30 天）
4. 如果推送到 main 分支，还会创建 Release

### 优势

- ✅ 无需本地安装 Android SDK、NDK 等工具
- ✅ 自动化构建，节省时间
- ✅ 构建结果自动上传，方便下载
- ✅ 支持手动触发构建
- ✅ 构建历史记录完整

## 在 Windows 上打包 APK

### 前置要求

1. 安装 Python 3.8 或更高版本
2. 安装 Git
3. 安装 Java JDK 11 或更高版本
4. 安装 Android SDK 和 NDK

### 安装步骤

1. **安装依赖**
```bash
pip install -r requirements.txt
```

2. **安装 Buildozer**
```bash
pip install buildozer
```

3. **初始化 Buildozer**
```bash
buildozer init
```
（如果已有 buildozer.spec 文件，可跳过此步）

4. **配置环境变量**

设置以下环境变量：
- `ANDROID_SDK_ROOT`: Android SDK 路径
- `ANDROID_NDK_ROOT`: Android NDK 路径
- `JAVA_HOME`: Java JDK 路径

5. **打包 APK**

在项目根目录运行：
```bash
buildozer android debug
```

首次运行会下载 Android SDK、NDK 和其他依赖，可能需要较长时间。

打包完成后，APK 文件位于 `bin/` 目录下。

## 在 Linux 上打包 APK（推荐）

在 Linux 系统上打包 APK 更稳定，推荐使用以下方法：

### 使用 Docker

1. **安装 Docker**

2. **运行 Buildozer 容器**
```bash
docker run --rm -v $(pwd):/home/user/appcode buildozer
```

3. **在容器内打包**
```bash
cd /home/user/appcode
buildozer android debug
```

### 直接在 Linux 上安装

1. **安装依赖**
```bash
sudo apt update
sudo apt install -y build-essential git python3 python3-pip openjdk-11-jdk
sudo apt install -y automake libtool pkg-config libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev
sudo apt install -y autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 libltdl-dev libssl-dev
sudo apt install -y python3-setuptools
```

2. **安装 Buildozer**
```bash
pip3 install --user buildozer
```

3. **打包 APK**
```bash
buildozer android debug
```

## 测试应用

在打包前，可以先在电脑上测试 GUI 版本：

```bash
python main_gui.py
```

## 安装 APK 到 Android 设备

1. 将 APK 文件传输到 Android 设备
2. 在设备上启用"未知来源"安装
3. 点击 APK 文件进行安装

## 使用说明

1. 打开应用
2. 输入云成绩系统的用户名和密码
3. 点击"登录"按钮
4. 选择要查看的考试
5. 查看成绩详情
6. 点击"导出Excel"按钮导出成绩数据

导出的 Excel 文件保存在应用的 `output` 目录下。

## 注意事项

- 首次打包需要下载大量依赖，请确保网络连接稳定
- 打包过程可能需要 30-60 分钟
- 如果遇到问题，请检查：
  - Python 版本是否正确
  - Java JDK 版本是否正确
  - Android SDK 和 NDK 是否正确安装
  - 环境变量是否正确设置

## 故障排除

### 常见问题

1. **Buildozer 找不到 Java**
   - 确保 JAVA_HOME 环境变量已正确设置

2. **Android SDK 下载失败**
   - 检查网络连接
   - 尝试使用代理或镜像源

3. **打包失败**
   - 查看错误日志
   - 确保所有依赖已正确安装
   - 尝试清理缓存：`buildozer android clean`

## 许可证

本项目仅供学习和个人使用。
