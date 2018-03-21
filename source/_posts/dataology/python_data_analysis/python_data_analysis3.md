title: 利用Python进行数据分析(3)：IPython
date: 2017-02-16
postslug: python_data_analysis3
category: 数据分析
tags: python

---



《[利用Python进行数据分析](https://book.douban.com/subject/25779298/)》读书笔记。
第 3 章：IPython——一种交互式计算和开发环境。
介绍 IPython 及其使用。

<!-- more -->

IPython 的设计哲学是鼓励一种“执行-探索”(execute explore)的工作模式，而不是传统编程的“编辑-编译-运行”(edit-complie-run)模式。
由于大部分的数据分析工作都需要“探索式操作”(试误法和迭代法)，可以说 IPython 就是为了用 python 进行数据分析而生的。

可能 IPython 的设计灵感来自 R 等软件，但是在 python 的强大能力下，IPython 系已经形成了一整套的数据分析工具链，
已经有一些数据分析工作者转移到了 python 生态下。

# IPython基础

类似于 python解释器，使用命令 `ipython`可以打开一个交互式控制台。如果需要使用 Matplotlib 库，增加参数：`ipython --pylab `。

更吸引人的使用方式是基于 web 的 ipython notebook。
可以使用命令：

```
# ipython notebook
jupyter notebook
```
该命令会自动打开浏览器并访问 notebook。

通常我们需要在页面中直接嵌入显示图片，此时使用命令：

```
# ipython notebook --pylab inline
jupyter notebook --pylab inline
```

ipython notebook 还可以远程运行，可以参考资料1[^1]。

# 使用技巧

- 用 Tab 建可以自动补全
- 内省：在变量的前面或后面加上`?`，可以显示该对象的信息
- 用 `%run`命令可以执行外部 py 脚本
- 用 `%paste`可以按 python 缩进粘贴代码
- IPython 提供了一些方便的快捷键，常用的包括：
  + `Ctrl+F` 光标前移1个字符
  + `Ctrl+B` 光标后移1个字符
  + `Ctrl+A` 光标移至行首
  + `Ctrl+E` 光标移至行尾
  + `Ctrl+U` 删除此行光标之前的所有内容
  + `Ctrl+K` 删除此行光标之后的所有内容
  + `Ctrl+L` 清屏（Mac 下 Cmd+K 也可以）
- IPython 支持调试和跟踪
- `%`开头的命令称为“魔术命令（Magic Command）”，能够实现一些“神奇”的功能

# GUI 方式

使用命令`ipython qtconsole --pylab=inline`，可以打开一个类似 R 的GUI 程序。

# 与操作系统交互

ipython 提供了很多魔术命令，用于与操作系统交互。


# 参考资料

[^1]: [IPython Notebook: 交互计算新时代](http://mindonmind.github.io/2013/02/08/ipython-notebook-interactive-computing-new-era/)



