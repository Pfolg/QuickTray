<div align="center">

# Quick Tray

![GitHub License](https://img.shields.io/github/license/Pfolg/QuickTray) ![GitHub repo size](https://img.shields.io/github/repo-size/Pfolg/QuickTray) ![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/Pfolg/QuickTray) ![GitHub last commit](https://img.shields.io/github/last-commit/Pfolg/QuickTray) ![GitHub Issues or Pull Requests](https://img.shields.io/github/issues/Pfolg/QuickTray) ![Static Badge](https://img.shields.io/badge/Windows-blue) ![Static Badge](https://img.shields.io/badge/Python3.11-green)

![GitHub Repo stars](https://img.shields.io/github/stars/Pfolg/QuickTray) ![GitHub Release](https://img.shields.io/github/v/release/Pfolg/QuickTray) <img src="https://visitor-badge.laobi.icu/badge?page_id=Pfolg.QuickTray" /> ![GitHub Downloads (all assets, all releases)](https://img.shields.io/github/downloads/Pfolg/QuickTray/total)

|[Features](#features) | [Download](#download) | [Declaration](#declaration) | [LICENSE](LICENSE)|[简体中文](docs/README.zh.md)|
|:--:|:--:|:--:|:--:|:--:|

_A system tray utility based on PySide6, providing quick launch and text display functions._

</div>

# Features

+ System tray functionality
+ Desktop widgets
+ Quick launch
+ Autostart management

---

**Program Workflow**

```mermaid
graph TD
A[Start Program] --> B[Read Config Files]
B --> C[Create System Tray]
C --> D[Initialize Desktop Widgets]
D --> E[Start Timers]
E --> F[Check Autostart after 3s]
E --> G[Refresh Text every 5min]
C --> H[Enter Main Loop]
```

>[!NOTE]
> The program has no main window and operates entirely through the system tray icon, suitable for lightweight background use. Core functionality is quick application launching.
>
> A simple window was added starting from **ver1.11.2-25718**.

# Download

![GitHub Release](https://img.shields.io/github/v/release/Pfolg/QuickTray)

>[!WARNING]
> Not compatible with versions prior to v1.11

| Windows | [releases](https://github.com/Pfolg/QuickTray/releases) |
|:-------:|:-------------------------------------------------------:|

Alternatively:

Clone this repository and run the source code from `src`

**Configuration File Management**
| File | Description |
| ------------------- | ------------------------------ |
| `basic_config.json` | Basic settings (icons/port/autostart) |
| `applist.json`      | Menu items configuration (name/path/type) |
| `lines.json`        | Random quotes database for text labels |

# Declaration

This program absolutely never collects user information. Source code is open for inspection.

If you encounter any issues during use, please don't hesitate to file an Issue. Developers with unique ideas are welcome to submit pull requests!

Gratitude to all third-party libraries involved and Python language developers. Apologies for not acknowledging everyone individually! <!-- Will be optimized in future updates -->

If any materials used in this program infringe your copyright, please contact me for removal!
