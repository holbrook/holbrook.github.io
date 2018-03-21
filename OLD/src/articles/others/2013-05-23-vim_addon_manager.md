---
layout: post
title: "重拾vim"
description: "从emacs切换回vim"
date: 2013-05-23
category: 杂七杂八
tags: [vim , vundle]
lastmod: 2013-06-17
---

以前在[博客园][1]时，用[emacs org-mode][2] 写博客，并且写了一系列[《emacs 学习笔记》][3]。
emacs 和 org-mode 的强大毋庸置疑，但是经过1年多的使用，还是有些不适应：

1. 小手指很受伤。

2. 过于依赖配置。

   由于我的工作要经常登录到linux服务器进行操作，这就带来了一个问题：
   服务器上的emacs在不配置的情况下几乎无法使用，但是在服务器上使用vim，又不符合手指中记忆的快捷键。

3. emacs有点重，比如不得不使用的ecb,cedet,jdee等等，都是大块头。

4. 我还没有做好准备去掌握Erlang语言。但是对于vim，我可以使用我喜欢的python去写插件。




经过艰难的取舍，还是决定在个人工作领域也回到vim。保护手指，保护大脑。

[1]:http://www.cnblogs.com/holbrook/ "心内求法"
[2]:http://www.cnblogs.com/holbrook/archive/2012/04/12/2444992.html "Emacs学习笔记(9):org-mode，最好的文档编辑利器，没有之一"
[3]:http://www.cnblogs.com/holbrook/tag/emacs/ "emacs 学习笔记"

# 插件管理器(Vundle)

重新关注vim后，首先发现了一系列插件管理器。主要有：

1. [Vundle](https://github.com/gmarik/vundle)
2. [vim-addon-manager](http://www.vim.org/scripts/script.php?script_id=2905)
3. [pathogen.vim](http://www.vim.org/scripts/script.php?script_id=2332)
4. [vvundle](http://www.vim.org/scripts/script.php?script_id=3458)
5. [vvimana](https://github.com/c9s/Vimana)

经过简单的比较，我选择了Vundle。这里不想对上述插件管理器做一个完整的对比，只是简单说一个我看中的Vundle的特点：

1. 只需要维护需要的插件列表就可以统一安装，同样，复制环境时也只需要复制一个文件(.vimrc)
2. 支持git更新
3. 支持插件搜索功能
4. 自动管理插件依赖关系

## 安装Vundle

安装Vundle只需要一条命令：

    $ git clone https://github.com/gmarik/vundle.git ~/.vim/bundle/vundle

如果你使用git管理vim配置，还可以使用git submodule：

    git submodule add https://github.com/gmarik/vundle.git vim/bundle/vundle

会在.gitmodule中增加如下配置：

    [submodule "vim/bundle/vundle"]
        path = vim/bundle/vundle
        url = https://github.com/gmarik/vundle.git

之后运行git命令：

    git submodule init
    git submodule update

即可。


## 配置插件

在.vimrc中配置需要的插件，作者给出了一个例子：

    set nocompatible               " be iMproved
    filetype off                   " required!
    set rtp+=~/.vim/bundle/vundle/
    call vundle#rc()


    " let Vundle manage Vundle
    " required!
    Bundle 'gmarik/vundle'


    " My Bundles here:
    "
    " original repos on github
    Bundle 'tpope/vim-fugitive'
    Bundle 'Lokaltog/vim-easymotion'
    Bundle 'rstacruz/sparkup', {'rtp': 'vim/'}
    Bundle 'tpope/vim-rails.git'
    " vim-scripts repos
    Bundle 'L9'
    Bundle 'FuzzyFinder'
    " non github repos
    Bundle 'git://git.wincent.com/command-t.git'
    " ...


注意：

1. 对于重名的Vim插件，需要在插件后面加上作者的姓氏， 比如 Bundle 'Javascript-Indentation'
2. 对于插件名称中包含空格和斜杠的情况， 需要将空格和斜杠替换为 -


## 安装插件

只需要在启动vim后，运行命令：

    :BundleInstall

Vbundle就会自动安装或更新前面配置好的插件

## 其他操作

使用帮助：

    :h vundle
查看插件清单：

    :BundleList
搜索插件：

    :BundleSearch markdown
清理不用的插件：

    :BundleClean
    #或者
    :BundleClean markdown

# 必备插件（TODO）

下面是我使用的一些vim插件，直接在.vimrc中配置。可以在 [github](https://github.com/holbrook/macENV/blob/master/vimrc) 查看。



## 编辑器增强

- [NERDTree](https://github.com/scrooloose/nerdtree)（Bundle 'The-NERD-tree'）可以在窗口左侧打开文件浏览器

- Bundle 'vim-orgmode'
- Bundle 'winmanager'
- Bundle 'SuperTab'

## 语法高亮

- Markdown（Bundle 'Markdown'） markdown文件的语法高亮


# vim基本操作

以前整理过一个 [vim 常用命令备忘](http://www.cnblogs.com/holbrook/archive/2009/05/13/2357377.html), 如下：

[vim_cheet_sheet.xlsx](images/2013/vim_addon_manager/vim_cheet_sheet.xlsx)

别人的一个更详细的版本：

[vi-vim-cheat-sheet-list](images/2013/vim_addon_manager/vi-vim-cheat-sheet-list.png)


如果已经有一定的基础，还可以使用vim cheat sheet。下面的图分别可以用于打印版或者桌面背景。

![打印版，Eng](images/2013/vim_addon_manager/vi-vim-cheat-sheet.gif)

![打印版，Chs](images/2013/vim_addon_manager/vi-vim-cheat-sheet-sch.gif)

![桌面版，Eng](images/2013/vim_addon_manager/vi-vim_cheat_sheet_dark.png)

