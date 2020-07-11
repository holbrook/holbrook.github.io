---
title: windows下面的包管理器：Chocolatey
postslug: windows_pkg_manager_chocolatey
date: 2017-02-11
category: 方法工具
tags: env
---

操作系统级别的包管理器，Linux 下面有 yum, apt, Mac OS 下面有 Homebrew。
Windows 下面可以使用 windows下面的包管理器：[Chocolatey](https://chocolatey.org/)。

<!-- more -->

# 系统级别的包管理器

开发人员一般都喜欢命令行操作，因为效率更高。在管理系统上的软件时，更喜欢用包管理器(`package manager`)。
Linux 下面我们已经熟悉了 `yum`, `apt`等，在 Mac OS 下面，`Homebrew` 最终战胜了 `MacPort`。
但是有时候我们不得不使用 windows，比如 万德。

Windows 的软件管理，以前是一些第三方的“软件仓库”，比如 百度软件管理等，但是难保上面没有地雷。
Windows 10 自己提供了“软件商店”，安全性应该大有改观，但是使用仍很受限制，尤其是开发用的软件很不全。

我们需要一个 Windows 下面的包管理器。所幸，现在有了 [Chocolatey](https://chocolatey.org/)。
使用包管理的好处不仅仅是提高效率，更重要的是使得 Windows 的自动运维成为可能。
比如，原来 `SaltStack`的很多脚本在 Windows 下很难实现，但有了 Chocolatey ，
用 SaltStack 管理Windows 服务器的难度大大降低。

# 原理

[Chocolatey](https://chocolatey.org/)使用 Nuget 协议，将软件的官方链接封装到描述文件中。
可以查看 [软件包列表](https://chocolatey.org/packages)。


# 安装

[Chocolatey](https://chocolatey.org/)需要的环境为：

- Windows 7+ / Windows Server 2003+
- PowerShell v2+
- .NET Framework 4+
- 管理员权限

以管理员的权限安装。可以使用 `PowerShell`，但先要修改 PowerShell的执行策略：

```
Set-ExecutionPolicy unrestricted
iwr https://chocolatey.org/install.ps1 -UseBasicParsing | iex
```

也可以使用`Cmd` 、`CygWin`、。。。 等命令行工具：

```
@powershell -NoProfile -ExecutionPolicy Bypass -Command "iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))" && SET "PATH=%PATH%;%ALLUSERSPROFILE%\chocolatey\bin"
```

# 使用

安装好 Chocolatey 后，可以通过如下命令查看使用帮助：

```
choco help
```

Chocolatey 的命令一般提供两种格式，比如安装软件可以使用长格式 `choco install` , 或者短格式 `cinst`。
可以根据需要选择。但我个人更喜欢长格式，因为跟其他包管理器的命令更接近。

Chocolatey 的常用命令包括：

- 搜索: `choco search`，用 `-all `参数会显示所有可用的版本
- 安装: `choco install`, 用 `-version` 参数可以安装指定版本
- 查找更新: `choco version`
- 升级: `choco upgrade`
- 卸载: `choco uninstall`

# 小结

使用 Chocolatey 可以管理很多软件包，比如 Linux 下面常用的 ~curl~, 一些小工具如 ~7zip~，
各种开发环境和工具如 ~git~, ~nodejs~, 甚至一些大型 GUI程序如
 ~SublimeText3~, ~virtualbox~, ~VisualStudio2013Ultimate~.
通过命令行的方式，可以将按照操作纳入到 SaltStack 的管理中。

相信通过深入挖掘，Chocolatey 能够发挥很大的作用。
