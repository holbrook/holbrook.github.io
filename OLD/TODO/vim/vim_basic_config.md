---
layout: post
title: vim配置基础 
date: 2014-11-21
description: 
category: "工具使用"
tags: [vim, ]
---
# 配置文件的位置

vim 配置文件分为全局配置文件和用户配置文件

1. 全局配置文件查找，在.vim 中输入:echo $VIM,一般为：/usr/share/vim/vimrc
2. 用户配置文件在用户主目录下，如：/home/abeen/.vimrc


# vim配置目录结构

一般，我们安装好vim后，应该会创建一个用户vim文件夹，里面的子目录结构和原vim的目录结构几乎一样，例如在windows平台下这个名称是vimfiles，在unix类平台下是~/.vim。但它们的子目录结构都类似下面这样：

|-after
|—ftplugin
|—syntax
|-autoload
|-colors
|-compiler
|-doc
|-ftplugin
|—latex-suite
|—–dictionaries
|—–macros
|—–packages
|—–templates
|—python
|-indent
|-plugin
|-spell
|-syntax

~/.vim/colors/是用来存放vim配色方案的。

~/.vim/plugin/存放的是每次启动vim都会被运行一次的插件，也就是说只要你想在vim启动时就运行的插件就放在这个目录下。

~/.vim/ftdetect/中的文件同样也会在vim启动时就运行。有些时候可能没有这个目录。ftdetect代表的是“filetype detection（文件类型检测）”。此目录中的文件应该用自动命令（autocommands）来检测和设置文件的类型，除此之外并无其他。也就是说，它们只该有一两行而已。

~/.vim/ftplugin/此目录中的文件有些不同。当vim给缓冲区的filetype设置一个值时，vim将会在~/.vim/ftplugin/ 目录下来查找和filetype相同名字的文件。例如你运行set filetype=derp这条命令后，vim将查找~/.vim/ftplugin/derp.vim此文件，如果存在就运行它。不仅如此，它还会运行ftplugin下相同名字的子目录中的所有文件，如~/.vim/ftplugin/derp/这个文件夹下的文件都会被运行。每次启用时，应该为不同的文件类型设置局部缓冲选项，如果设置为全局缓冲选项的话，将会覆盖所有打开的缓冲区。

~/.vim/indent/这里面的文件和ftplugin中的很像，它们也是根据它们的名字来加载的。它放置了相关文件类型的缩进。例如python应该怎么缩进，java应该怎么缩进等等。其实放在ftplugin中也可以，但单独列出来只是为了方便文件管理和理解。

~/.vim/compiler/和indent很像，它放的是相应文件类型应该如何编译的选项。

~/.vim/after/这里面的文件也会在vim每次启动的时候加载，不过是等待~/.vim/plugin/加载完成之后才加载after里的内容，所以叫做after。

~/.vim/autoload/它是一个非常重要的目录，尽管听起来比实际复杂。简而言之，它里面放置的是当你真正需要的时候才被自动加载运行的文件，而不是在vim启动时就加载。

~/.vim/doc/为插件放置文档的地方。例如:help的时候可以用到。

~/.vim/spell/拼写检查脚本。

~/.vim/syntax/语法描述脚本。

# 插件管理工具

## pathogen

## vundle

## VAM
# 如何调试

# 快捷键映射

