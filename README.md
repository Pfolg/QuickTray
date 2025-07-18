<div style="text-align: center;">

![GitHub License](https://img.shields.io/github/license/Pfolg/QuickTray) ![GitHub repo size](https://img.shields.io/github/repo-size/Pfolg/QuickTray) ![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/Pfolg/QuickTray) ![GitHub last commit](https://img.shields.io/github/last-commit/Pfolg/QuickTray) ![GitHub Issues or Pull Requests](https://img.shields.io/github/issues/Pfolg/QuickTray) ![Static Badge](https://img.shields.io/badge/Windows-blue) ![Static Badge](https://img.shields.io/badge/Python3.11-green)

![GitHub Repo stars](https://img.shields.io/github/stars/Pfolg/QuickTray) ![GitHub Release](https://img.shields.io/github/v/release/Pfolg/QuickTray) ![GitHub Downloads (all assets, all releases)](https://img.shields.io/github/downloads/Pfolg/QuickTray/total)

</div>


<!-- ![GitHub language count](https://img.shields.io/github/languages/count/Pfolg/QuickTray) -->


# Quick Tray

**快捷方式的替代：快捷托盘**

如果你不喜欢桌面上放着一堆杂乱的快捷方式，又不想整理。但是呢，平时又有不得不用的工具。于是，我就用Python写了一个这样的工具，目的是为了解放桌面（其实还是练习Python）。

# 下载
![GitHub Release](https://img.shields.io/github/v/release/Pfolg/QuickTray)

https://github.com/Pfolg/QuickTray/releases

# 特点

设置基于json！还有Windows11，也就是说，不能保证这个程序可以在其他操作系统上运行！

使用 **Python 3.11.9** 开发

程序读取 `json` 文件后，然后在托盘创建一个图标，图标里面包含有快捷（链接），每一个链接有相应的功能（需要用户自己设置）。

![alt text](/assets/image.png)

放在 star 区域里面的链接，可以在开机启动后启动（如果连接了电源，这个也可以自定义是否开启）。

# 由DeepSeek总结的特点

### 程序功能分析总结

这是一个基于 PySide6 的系统托盘工具应用，主要提供快速启动、文本展示和系统管理功能。以下是核心功能总结：

---

### **1. 系统托盘功能**
- **托盘图标**：
  - 显示自定义图标（从配置文件中读取）
  - 悬停提示显示程序名、版本号、菜单项数量和自启状态
- **右键菜单**：
  - 多级分类菜单（应用/链接/脚本等）
  - Windows 开始菜单程序动态加载
  - 设置管理（编辑菜单/修改配置）
  - 文本操作（更新/复制/编辑）
  - 搜索功能（调用浏览器搜索）
  - 关于信息（GitHub/检查更新）
  - 退出程序

---

### **2. 桌面组件**
- **随机文本标签**：
  - 桌面置顶透明窗口
  - 从 `lines.json` 随机显示文本
  - 支持手动更新/复制文本内容
- **搜索框**：
  - 圆角透明输入框
  - 回车后使用必应搜索内容
  - 通过托盘菜单呼出
- **右下角提示窗**：
  - ~~固定显示 "Windows Hacked" 提示~~
  - 引导访问本地 URL（模拟勒索信息效果）

---

### **3. 核心功能**
- **快捷启动**：
  - 解析 `applist.json` 配置文件
  - 支持启动本地程序/脚本/网页链接
  - 分类管理（收藏/应用/链接/脚本）
- **自启管理**：
  - 检测电源状态（仅充电时触发）
  - 自动启动标记为 "star" 的程序
- **版本检测**：
  - ~~启动时~~检查 GitHub 版本更新
  - 通过托盘消息通知结果
- **单例运行**：
  - 通过端口占用检测防止多开
- **剪贴板集成**：
  - 一键复制文本标签内容

---

### **4. 配置文件管理**
| 文件                | 功能说明                       |
| ------------------- | ------------------------------ |
| `basic_config.json` | 程序基本设置（图标/端口/自启） |
| `applist.json`      | 菜单项配置（名称/路径/类型）   |
| `lines.json`        | 文本标签的随机语录库           |

---

### **5. 技术亮点**
- **透明界面**：
  - 所有窗口支持透明度和鼠标穿透
  - 圆角设计 + 置顶显示
- **动态菜单**：
  - ~~自动扫描 Windows 开始菜单程序~~
  - JSON 配置实时热加载
- **资源控制**：
  - QTimer 实现定时任务（文本刷新/自启检测）
  - 电源状态检测（psutil）
- **错误处理**：
  - 启动项路径有效性验证
  - 网络请求异常捕获

---

### **程序流程**
```mermaid
graph TD
A[启动程序] --> B[读取配置文件]
B --> C[创建系统托盘]
C --> D[初始化桌面组件]
D --> E[启动定时器]
E --> F[3秒后检测自启]
E --> G[每5分钟刷新文本]
C --> H[进入主循环]
```

> **注**：程序无主窗口，完全通过托盘图标交互，适合后台轻量级使用。代码中留有 "Windows Hacked" 等趣味元素，但核心是实用的快速启动工具。

# 设置

![alt text](/assets/image-1.png)

在目录`app_config`的`basic_config.json`编辑端口以避免端口问题引起的程序无法启动的问题：
```json
{
    "tip": "Quick Tray",
    "version": "1.11.0-25614",
    "logo": "assets\\luabackend.ico",
    "usecount": 0,
    "port": 20082,
    "autorun": true
}
```
在目录`app_config`的`applist.json`中编辑软件配置，仓库中有模板，但是不适合个人用户。
```json
[
{
    "type": [
      "star",
      "app"
    ],
    "name": "clock",
    "icon": "D:/programing/Python_projects/时钟(useless)/QtClock/QC.png",
    "path": "*/Microsoft/Windows/Start Menu/Programs/MyApplication/clock.lnk"
  }
]
```
---
在**ver1.11.2-25718**版本后可使用交互式窗口实现配置。

# 声明

感谢所有本程序涉及的第三方库及Python语言开发者们，未能一一致谢，抱歉！

如果程序中涉及的一些材料侵犯了您的版权，请联系我删除！
