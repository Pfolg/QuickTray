<div align="center">
  <h2>QuickTray</h3>

<img style="display: inline-block;" src="https://img.shields.io/github/watchers/Pfolg/QuickTray" alt="GitHub watchers" />
  <a href="https://github.com/Pfolg/QuickTray/stargazers"><img style="display: inline-block;" src="https://img.shields.io/github/stars/Pfolg/QuickTray" alt="GitHub stars" /></a>
  <a href="https://github.com/Pfolg/QuickTray/network"><img style="display: inline-block;" src="https://img.shields.io/github/forks/Pfolg/QuickTray" alt="GitHub forks" /></a>
  <a href="https://github.com/Pfolg/QuickTray/issues"><img style="display: inline-block;" src="https://img.shields.io/github/issues/Pfolg/QuickTray" alt="GitHub issues" /></a>
  <a href="https://github.com/Pfolg/QuickTray/pulls"><img style="display: inline-block;" src="https://img.shields.io/github/issues-pr-closed-raw/Pfolg/QuickTray" alt="GitHub closed pull requests" /></a>
  <img style="display: inline-block;" src="https://img.shields.io/github/contributors/Pfolg/QuickTray" alt="GitHub contributors" />
  <a href="https://github.com/Pfolg/QuickTray/blob/main/LICENSE"><img style="display: inline-block;" src="https://img.shields.io/github/license/Pfolg/QuickTray" alt="GitHub license" /></a>
  <img style="display: inline-block;" src="https://img.shields.io/github/repo-size/Pfolg/QuickTray" alt="GitHub repo size" />
</div>

<br>

<!-- ![Anurag's GitHub stats](https://github-readme-stats.vercel.app/api?username=Pfolg&show_icons=true&theme=vue)


[![Top Langs](https://github-readme-stats.vercel.app/api/top-langs/?username=Pfolg)](https://github.com/anuraghazra/github-readme-stats) -->

# QuickTray
QkStart已经使用Qt重写，目前正在懒惰开发中，如果想体验最新版，请前往https://github.com/Pfolg/QuickTray/tree/QuickTray

**快捷方式的替代：快捷托盘**

如果你不喜欢桌面上放着一堆杂乱的快捷方式，又不想整理。但是呢，平时又有不得不用的工具。于是，我就用Python写了一个这样的工具，目的是为了解放桌面（其实还是练习Python）。


[Download](https://github.com/Pfolg/QuickTray/releases)



# Function

设置基于Config.json！还有Windows11，也就是说，不能保证这个程序可以在其他操作系统上运行！

使用 Python 3.11.9 开发

程序读取 config.json 文件后，然后在托盘创建一个图标，图标里面包含有快捷（链接），每一个链接有相应的功能（需要用户自己设置）。

![alt text](/readme_asset/image.png)

放在 star 区域里面的链接，可以在开机启动后启动（如果连接了电源）。

# Set

![alt text](/readme_asset/image-1.png)

可通过`config.ini`编辑端口以避免端口问题引起的程序无法启动的问题：
```ini
[tray]
tip = Quick Tray
logo = assets/luabackend.ico

[infor]
usecount = 0
port = 20082
autorun = True
```
在程序所在目录的`applist.json`中编辑软件配置，仓库中有模板，但是不适合个人用户。
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
# 声明

感谢所有本程序涉及的第三方库及Python语言开发者们，未能一一致谢，抱歉！

如果程序中涉及的一些材料侵犯了您的版权，请联系我删除！
