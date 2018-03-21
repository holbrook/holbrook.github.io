---
layout: post
title: "python的环境管理"
description: "用python开发软件时，由于操作系统中可能存在多个不同的python版本，并且在不同版本、不同目录下安装了各种各样的python包，导致开发环境的不一致，也会带来发布软件时运行环境的问题。通过python的包管理器pip和环境管理器virtualenv，可以很容易解决这些问题。"
category: 软件开发
tags: [python, pip, virtualenv]
lastmod: 2013-06-20
---

# 包管理器pip

任何强大的体系结构都是提供一个基本的框架，并制定扩展的规范。
随着成千上万的开发者在其框架的基础上开发出越来越多的扩展，又提出了针对这些扩展进行管理的工具，
并建设出一个中心的“仓库”进行统一的登记以便检索和获取。


我们能举出很多这样的例子：

大到操作系统，可以有linux + 包管理器(apt, yum)， iOS + App Store, Android + Market;

应用软件，如 eclipse + marketplace, R + [CRAN](http://cran.r-project.org/mirrors.html), 

编程语言如 perl + cpan, ruby + gem, python + easy_install/pip。


为了分享和管理用python开发的大量模块，python阵营也建立了PyPI(the Python Package Index)仓库 ，并且在setuptools包中提供了easy_install命令，可以与PyPI配合实现python模块的自动安装。

pip是easy_install的改进版, 提供更好的提示信息，删除package等功能。

pip的主要用法：

- 搜索模块

  `pip search <package_name>`

- 安装模块

  `pip install <package_name>`

  `pip install <package_name>==<version>`

- 升级模块 (如果不提供version号，升级到最新版本）

  `pip install --upgrade <package_name>>=<version>`

- 卸载模块
 
  `pip uninstall <package_name>`



老版本的python中只有easy_install, 没有pip。但是我们可以用easy_install来安装pip:

`sudo easy_install pip`



# 环境管理器virtualenv

有了包管理器确实方便，但却难免乐极生悲。当我们在很多项目中快乐的下载安装python模块时，系统的环境已经变得一团糟。

更加麻烦的是，对于类UNIX系统，Python通常作为操作系统的组成部分。我们即可以使用操作系统的包管理器(apt,yum)安装python模块，
也可以通过pip进行安装。但是两个来源的模块可能会安装到不同的路径，使得模块的管理更加混乱。

如果再考虑不同版本的python并存的问题，我们似乎已经无法使用python进行开发工作了。

于是就有了virtualenv——python的环境管理器（类似于ruby的gemset)。

virtualenv可以创建很多个独立的python运行环境，用于不同的用途。每个运行环境都有自己的模块路径，可以互不干扰。

不同的运行环境还可以使用不同版本的python。

你可以为每个python项目创建一个干净的环境进行开发和调试。

virtualenv的使用举例如下：

{% highlight bash %}

 # 安装virtualenv
 sudo pip install virtualenv
 
 # 为虚拟环境创建目录
 mkdir /PATH/TO/YOUR/VIRTUAL_ENV
 cd /PATH/TO/YOUR/VIRTUAL_ENV
 
 # 创建一个虚拟环境，不使用系统的site-packages中的模块
 virtualenv --no-site-packages ENV_NAME
 
 # 激活虚拟环境，注意激活后命令行的提示符变化
 source /PATH/TO/YOUR/VIRTUAL_ENV/ENV_NAME/bin/active
 
 # 在虚拟环境安装需要的模块
 pip install MODULE_NAME
 
 # 进行一些操作
 # ...
 
 # 退出虚拟环境
 deactivate

{% endhighlight %}




# 复制环境

尽管virtualenv创建虚拟环境很容易，但是在协同开发时要保证环境的同步还是比较麻烦。

包管理器pip可以为创建虚拟环境提供支持。

pip有一个子命令`pip freeze`，可以查看当前环境中包的清单，比如：


> Django==1.3

> distribute==0.6.14

> wsgiref==0.1.2

> yolk==0.4.1

我们可以将该内容重定向到一个文本文件：`pip freeze > req.txt`, 
然后在另一个环境中按照该文件中的内容安装需要的包：`pip install -r req.txt`。

只要将这个文件加入到版本控制，所有开发者的环境就很容易保持一致。