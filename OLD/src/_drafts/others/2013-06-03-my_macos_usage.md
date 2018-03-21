---
layout: post
title: "我在MacOS下使用的软件"
description: "使用MacOS已经有5年了，在这个过程中积累了一些用得顺手的软件，包括软件开发、思考、绘图、写作、系统工具、互联网工具等。
这里进行一个整理。\n工具在精不在多，在巧不在大，好的工具用起来得心应手、心情愉悦，能够提高工作效率。"

category: 杂七杂八
tags: [macos, resource]
lastmod: 2013-06-20
---

Mac OS 属于UNIX家族，配合[HomeBrew]()，有大量的命令行工具可用。要尽量使用这些命令行工具。

当然有些工作还是需要GUI程序，下面分类列出我使用的GUI工具。一个原则是：要尽量减少GUI工具的数量。

# 开发类
---

## 分析和设计

- ~~~ Archi：一个绘制ArchiMate的工具 ~~~ （ 改用办公类-> 绘图 -> OmniGraffle )
- ~~~ VP-UML ~~~ (用手绘图拍照 + OmniGraffle代替)
- wxFormBuilder: 界面原型工具


## coding

- [Eclipse](http://www.eclipse.org/downloads/): Java开发必不可少的工具
- [Mule Studio](http://www.mulesoft.org/download-mule-esb-community-edition)：专用工具，可以考虑用Eclipse + maven代替
- ~~~ PyCharm ~~~(改用MacVim)
- ~~~ Emacs ~~~ (改用MacVim, 原因见[这里](http://thinkinside.tk/2013/05/23/vim_addon_manager.html))
- ~~~ Sublime Text ~~~(改用MacVim)
- [MacVim](https://github.com/b4winckler/macvim), 编辑器之神。本来Sublime Text在某些方面有望代替Vim，但是从Sublime Text 3开始就没有免费无限期试用了，只好放弃。
- [R](http://www.r-project.org/) 和 [RStudio](http://www.rstudio.com/), 统计分析工具

## 其他工具
- Navicat Premium：多种数据库的客户端


## 版本管理

- [GitHub for Mac]()：GitHub推出的针对Mac OS X的桌面客户端   

## 项目管理

- [OmniPlan]()

  + 可以绘制Gantt图
  + 可以打开M$ Project文件
  + 可以输出到iCal, CSV, MPX, XML, HTML等
  + 功能包含了自定检视表、阶层式的纲要模式、成本追踪、里程碑、任务限制与相关性、资源分配、时程控制、Gantt 图表、违反事项显示、关键路径等等

# 办公类

## 任务计划

- MacVim + Vim-OrgMode: Emacs Org-mode 是[最好的任务管理利器]()，但是既然[放弃了Emacs]()，可以使用Vim 上的替代品。Vim上的各种org-mode插件都只实现了Emacs Org-mode的一部分功能。作为任务管理，目前最好的插件是[Vim-OrgMode](https://github.com/jceb/vim-orgmode)，实现了按标题导航、按标题编辑功能，更主要的是实现了TODO管理以及标题上的标签(tags)，用来管理任务计划足够了。


Bundle 'vim-orgmode'


## 思考

- XMind

  非常不错的思维导图软件

- OmniOutliner
 
  OmniOutliner 是一个创建 收集 和组织信息的工具. 用于帮你开始一项新的工作 并且设计你的想法

## 写作

- Emacs Org-mode
- MacVim/Sublime Text + markdown
- MacTeX
- M$ Office 2011

## 绘图

- 矢量图[OmniGraffle]()
  
  非常轻巧的绘图工具，可以扩展模板(Stencils)，可以在一个文件中绘制多个图形。

  Stencils可以安装在：
  
  - 个人的：~/Library/Application Support/The Omni Group/OmniGraffle/Stencils
  - 系统的：/Library/Application Support/The Omni Group/OmniGraffle/Stencils
    
  在[这里](https://www.graffletopia.com/)可以下载很多的Stencils。比如：

  + [SOA & ESB](https://www.graffletopia.com/stencils/301)
  + [Archimate](https://www.graffletopia.com/search/archimate)
  + [BPMN 2.0](https://www.graffletopia.com/stencils/699)
  + [Mind Map](https://www.graffletopia.com/stencils/29)

  几乎你知道的绘图类型都能找到合适的Stencil。

- 素描图[OmniGraphSketcher]()
  
  一款素描绘制工具，用于个性化的报告，演示等

# 互联网

- Evernote
- Dropbox
- Adium
- Google Chrome

# 系统工具

- Quicksilver: 不用这个软件就不是一个真正的Macer
- CoRD
- HomeBrew
- [TotalTerminal](http://totalterminal.binaryage.com/)：与Linux下面的[Tilda](http://sourceforge.net/projects/tilda/)类似的一个系统级的终端工具。喜欢命令行的人士必备的利器。


  比如：
	brew install tree
- VMware Fusion 和 CrossOver


- 输入法?

- 键盘鼠标共享[SynergyKM]()/ [QuickSynergy]()

# 多媒体

- MPlayerX

