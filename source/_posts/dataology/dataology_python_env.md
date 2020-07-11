---
title: 基于Python的数据科学环境
postslug: dataology_python_env
date: 2017-02-11
Modified: 2017-03-09
category: 数据分析
tags: python, env
---

    在[《数据科学的知识体系》](http://holbrook.github.io/2017/02/05/index.html)中，
    列出了进行数据科学研究所需的知识。但Swami Chandrasekaran明显更喜欢 R 。
    我个人更倾向于 python。而且 python 和 R可以互相调用[]
    本文列出数据科学相关的 python 模块。

<!-- more -->

在[《数据科学的知识体系》](http://holbrook.github.io/2017/02/05/index.html)中，
列出了进行数据科学研究所需的知识。但Swami Chandrasekaran明显更喜欢 R 。
我个人更倾向于 python。至于为什么不是 R 或 Matlib，可以参考
[《R vs Python vs matlab: the quant language war》](https://futures.io/matlab-r-project-python/33828-r-vs-python-vs-matlab-quant-language-war.html)和
[《R和Python的相遇》](http://nbviewer.jupyter.org/gist/xccds/d692e468e21aeca6748a)。

其实，R 和 python 的边界也不是那么的无法逾越，
可以使用[rpy2](https://rpy2.bitbucket.io/)在 python 中调用 R，
也可以使用[rPython](http://rpython.r-forge.r-project.org/)在 R 中调用 python。


# 运行环境

## Anaconda

尽管 Linux 和 Mac OS 自带了 python 环境，但还是推荐安装 [Anaconda](https://www.continuum.io)。

Anaconda是python的一个科学计算发行版，包含了众多流行的科学、数学、工程、数据分析的Python包[^1]。

从官方网站下载有点慢。如果用安装包进行安装，
可以从[清华大学开源软件镜像站(TUNA)](https://mirrors.tuna.tsinghua.edu.cn/help/anaconda/)下载。
但还是建议[使用包管理器](http://holbrook.github.io/2017/02/11/windows_pkg_manager_chocolatey.html)
进行安装，安装后再配置TNUA 上Anaconda 仓库的镜像作为源：

```
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/
conda config --set show_channel_urls yes
```

安装和配置完 Anaconda 后，可以使用其自带的 python 包管理器安装 python 模块，也可以使用常用的 `pip`。
但要注意环境的配置。比如：

```
conda --version  # 查看版本
conda install seaborn #
```

## ipython, jupyter 和 spyder

python 本身提供了类似shell的交互式解释器，但是并不好用， [IPython](http://ipython.org/) 对其进行了极大加强。
IPython是一个增强的 Python Shell，目的是提高编写、测试、调试 Python 代码的速度。
主要用于交互式数据处理和利用matplotlib 对数据进行可视化处理。

不仅如此，IPython 还提供了 web 方式的 IPython notebook(现在叫做[jupyter](https://jupyter.org/))，
已经成为Python科学计算界的标准配置。

如果你喜欢像 R 一样的 GUI 程序，可以使用命令`jupyter qtconsole`打开一个图形界面。

如果喜欢 RStudio，可以使用 `spyder`.

（附：可能是 IPython notebook 太好用了，
RStudio 现在也实现了一个类似的 web 交互工具 [shiny](https://www.rstudio.com/products/shiny/))。


## Cython

编译Python程序，提高性能。


# 底层库

## NumPy

python 中本来提供了 列表(list) 和 数组(array), 可以用来构建矩阵。
但是这些都是通用数据结构，对于纯数值运算来说效率不高。而且没有矩阵运算的函数。

[NumPy](http://www.numpy.org/) 弥补了这些不足，为线性代数的计算提供了极大帮助。
NumPy 定义了ndarray(N维数组对象，N-dimensional array object)和
ufunc(通用函数对象, universal function object)，
分别用于多维数组的存储和处理。
其中，ufunc 是一种能对数组的每个元素进行操作的函数。
Numpy 还支持线性代数运算和随机数生成。

Numpy是下面很多模块的基础模块。

# SciPy

[SciPy](http://www.scipy.org/)在NumPy的基础上增加了众多的数学、科学以及工程计算中常用的模块。
通过不同的子模块，SciPy 提供了线性代数、拟合与优化、差值、数值积分、图像处理、系数矩阵处理等函数。

Numpy 已经提供了线性代数函数库，但是SciPy的线性代数库比NumPy更加全面。

SciPy 的主要子模块包括：

- scipy.integrate: 数值积分例程和微分方程求解器
- scipy.linalg: 扩展了由 numpy.linalg 提供的线性代数例程和矩阵分解功能
- scipy.optimize: 函数优化器以及根查找算法
- scipy.signal: 信号处理工具
- scipy.sparse: 稀疏矩阵和稀疏线性系统求解器
- scipy.special: SPECFUN（这是一个实现了许多常用数学函数的 Fortran 库）的包装器
- scipy.stats: 标准连续和离散概率分布、各种统计检验方法和更好的描述统计法
- scipy.weave: 利用内联 C++ 代码加速数组计算的工具


# matplotlib

[Matplotlib](http://matplotlib.org/)为 python 提供了一整套和MATLAB类似的绘图函数集。

Matplotlib 是众多 Python 可视化包的鼻祖。其功能非常强大，同时也非常复杂。
直接使用 Matplotlib, 可能会需要花费很多工作来获得调整和美化图表。

高级的python 数据处理模块会调用 Matplotlib 实现更简单的绘图函数，
比如后面要提到的 Pandas, Seaborn等。

但是要对图表进行精细的、个性化的调整时，还是需要掌握 Matplotlib 的函数。


# 数据分析和处理


## Pandas

[Pandas](http://pandas.pydata.org/), Python Data Analysis Library,
是 python 数据分析领域里程碑式的一个重要工具。

Pandas 基于 NumPy, 实现了`Series(序列)`和类似 R的 `DataFrame` 对象，
提供了大量能使我们快速便捷地处理数据的函数和方法。

Pandas 很好的解决了数据分析的大部分任务，是所有中等规模数据分析的最有效的工具。

## Statsmodels

[Statsmodels](http://statsmodels.sourceforge.net/)
是 Python 中一个强大的统计分析包，包含了描述统计(mean,median,sd等)、
回归分析、时间序列分析、假设检验、统计推断(t-test,F-test,chi-square..）等功能。

一些主要的功能包括：


- Linear regression models
- Generalized linear models
- Discrete choice models
- Robust linear models
- Many models and functions for time series analysis
- Nonparametric estimators
- A collection of datasets for examples
- A wide range of statistical tests
- Input-output tools for producing tables in a number of formats (Text, LaTex, HTML) and for reading Stata files -into NumPy and Pandas.
- Plotting functions
- Extensive unit tests to ensure correctness of results
- Many more models and extensions in development

更多的统计相关模块，可以参考[这里](http://www.astro.cornell.edu/staff/loredo/statpy/)。

## SymPy

[SymPy]()是Python的数学符号计算库，目标是成为一个全功能的代数系统。
SymPy支持符号计算、高精度计算、模式匹配、绘图、解方程、微积分、组合数学、离散数学、几何学、概率与统计、物理学等方面的功能。

# 可视化

Pandas 本身就基于 Matplotlib 提供了内建的绘图功能，
但一些专门的可视化库提供了更多的功能，或者使用起来更容易。
这些可视化库不一定基于 Matplotlib， 也不一定

## Seaborn

[Seaborn](http://seaborn.pydata.org/)
是基于 Matplotlib 的高级统计绘图工具（类似 Pandas 与 NumPy 的关系），其功能类似 R 中的 lattice。
Seaborn 可以与 pandas 很好地集成，其目标是使默认的数据可视化更加悦目，以及简化复杂图表的创建。
比如，seaborn 支持多样的内置风格，可以快速地修改调色板。

推荐一开始使用 Seaborn ，而不是直接使用 Pandas 进行绘图。


## ggplot

[ggplot](http://ggplot.yhathq.com/)
与 Seaborn 类似，也是基于 Matplotlib 的高级绘图工具。 ggplot 的 API 更接近 R 中的 ggplot,
风格不是很pythonic，不过功能很强大。


## Bokeh

[Bokeh(Bokeh.js)](http://bokeh.pydata.org/en/latest/docs/user_guide.html)
不是基于 Matplotlib，并且其目标不是静态图片，而且基于 Web 浏览器的交互式可视化。

Bokeh 使用 D3.js 样式提供优雅，简洁新颖的图形化风格，
可以快速的创建交互式的绘图，仪表盘和数据应用。

Bokeh 支持大型数据集的高性能交互功能。


## Pygal

[Pygal](http://pygal.org/) 用于创建 svg 格式的图表，如果安装了正确的依赖，也可以保存为 png 格式。

svg 文件在创建交互式图表时非常有用，同时, Pygal 创建的图表风格比较独特，而且极具视觉感染力。

## Plot.ly

[Plot.ly](https://plot.ly/)是一个分析和可视化的在线工具。它具有强大的 API 并包含一个 Python 版本。
Plotly 与 pandas 可以无缝集成， 其绘制出的图表非常吸引人并且具有高度互动性。

所有通过 Plot.ly 所做的东西都会发布到网上。但是，也可以将图表设为私有。


## TVTK

数据的三维可视化


## VPython

制作3D演示动画


## OpenCV

图像处理和计算机视觉


# 机器学习

## scikit-learn

For machine learning and artificial intelligence algorithms

## PyTorch

深度学习


# Enthought Tool Suite

[Enthought Tool Suite](http://code.enthought.com/projects/index.php)是
[Enthought公司](http://code.enthought.com/)开发的开源科学计算一套应用程序开发包。
包含了大量的工具。主要的工具包括：

## Traits

Explicit type declarations; validation; initialization; delegation; notification; visualization.

## TraitsUI

A UI layer that supports the visualization features of Traits. Implementations using wxWidgets and Qt are provided by the TraitsBackendWX and TraitsBackendQt projects.


## Chaco

交互式 2D 图表

## Mayavi

交互式 3D 图表


## 其他

- Enaml
  Library for creating professional quality user interfaces combining a domain specific declarative language with a constraints based layout.
- Envisage
  Python-based framework for building extensible (plugin-based) applications.
- Pyface
  toolkit-independent GUI abstraction layer, which is used to support the "visualization" features of the Traits package.
- BlockCanvas
  Visual environment for creating simulation experiments, where function and data are separated using CodeTools.
- GraphCanvas
  library for interacting with visualizations of complex graphs.
- Enable
  Object drawing library and PDF vector drawing engine.
- SciMath
  Convenience libraries for math, interpolation, and units
- Casuarius
  supports constraints based layout in Enaml by wrapping Cassowary.
- AppTools
  General tools for ETS application development: scripting, logging, preferences, ...
- EnCore
  Core tools for application development (only depends on the Standard library).
- and more...


# 参考资料

[^1]: [Python科学计算发行版—Anaconda](http://www.cnblogs.com/super-d2/p/4725818.html)
[^2]: [用Python做科学计算](http://hyry.dip.jp/tech/book/page/scipy/index.html)
[^3]: [用Python做科学计算(第二版)](http://hyry.dip.jp/tech/book/page/scipynew/index.html)
[^4]: [Comprehensive learning path – Data Science in Python](https://www.analyticsvidhya.com/learning-paths-data-science-business-analytics-business-intelligence-big-data/learning-path-data-science-python/)
[^5]: [Python for statistical computing](http://aliquote.org/memos/2011/02/07/python-for-statistical-computing)
[^6]: [6 种 Python 数据可视化工具](http://www.tuicool.com/articles/mEB3quR)
