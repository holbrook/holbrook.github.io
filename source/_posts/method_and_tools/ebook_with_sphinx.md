---
title: 用Sphinx制作电子书
postslug: ebook_with_sphinx
date: 2017-11-10
category: 方法工具
tags: [markdown,rst,写作]
---

sphinx的初衷是为开发人员编写文档提供工具，但是用来编写电子书也非常方便。

<!-- more -->

# 需求和工具选择

制作电子书的需求，来自要为自己开发的策略平台编写用户文档，几个要求如下：

- 使用轻量级标记语言
- 能够预览
- 能够生成html和pdf
- 能够嵌入公式
- 能够嵌入graphviz, plantuml等图形描述语言

我找到了[GitBook](https://www.gitbook.com/) 和 [Sphinx Doc](http://www.sphinx-doc.org/en/stable/)。主要的区别在于：

- 设计目的
  GitBook的目的就是制作电子书，而Sphinx Doc的目的是为python项目编写文档
- 开发语言
  GitBook使用javascript开发，Sphinx Doc使用python开发
- 标记语言
  GitBook支持markdown, Sphinx Doc最开始只支持rst, 现在同时也支持markdown

应该说，两个工具都很棒。二者都可以通过进行插件扩展，所以在功能上没有本质上的区别：一方能有的功能，另一方也可以有。

本文整理一下 Sphinx 的使用。Sphinx默认使用rst，下面是一个 .rst 的简单示例:

```
This is a Title
===============
That has a paragraph about a main subject and is set when the '='
is at least the same length of the title itself.

Subject Subtitle
----------------
Subtitles are set with '-' and are required to have the same length
of the subtitle itself, just like titles.

Lists can be unnumbered like:

* Item Foo
* Item Bar

Or automatically numbered:

#. Item 1
#. Item 2

Inline Markup
-------------
Words can have *emphasis in italics* or be **bold** and you can define
code samples with back quotes, like when you talk about a command: ``sudo``
gives you super user powers!

```

# 快速开始

## 安装

```{bash}
pip install sphinx
```

## 初始化

```
mkdir mybook
cd mybook
sphinx-quickstart
```


## 预览

sphinx默认是生成html文件：
```
make html
```

如果要在浏览器中预览，可以使用插件：

```
pip install sphinx-serve
 sphinx-serve -b build -p 4000
```

可以用浏览器访问 <http://localhost:4000>

## 生成

`make html` 命令会生成html 。

生成epub:

```
make epub
```

生成pdf:

sphinx提供了生成latex:

```
make latex
```

如果安装了latex工具，可以在 `build/latex` 目录执行 `make` 命令生成pdf。

可选的LaTeX:

- LaTex
- ReTeX
- MiKTeX


# 发布

可以发布到[readthedocs](https://readthedocs.org/), 当然也可以把 html 发布到 github。


# 扩展

## 配置

生成目录时，会生成一个 `conf.py` 文件，在这里进行所有的配置。



## Math

从GitBook v1.1.0 开始，内置了使用[KaTeX](https://www.gitbook.com/blog/features/katex)支持 数学公式。比如：

```
The quadratic formula is$$-b \pm \sqrt{b^2 - 4ac} \over 2a$$
```

效果：
The quadratic formula is$$-b \pm \sqrt{b^2 - 4ac} \over 2a$$



## graphviz

使用[sphinx.ext.graphviz插件](http://www.sphinx-doc.org/en/stable/ext/graphviz.html)。

安装graphviz后，在 `conf.py`中配置：
```
# 配置graphviz插件
extensions = ['sphinx.ext.graphviz']

# 设置 graphviz_dot 路径
graphviz_dot = 'dot'# 设置 graphviz_dot_args 的参数，这里默认了默认字体
graphviz_dot_args = ['-Gfontname=Georgia',
'-Nfontname=Georgia',
'-Efontname=Georgia']
# 输出格式，默认png，这里我用svg矢量图
graphviz_output_format = 'svg'
```

嵌入式：

```
.. graphviz::

   digraph foo {
      "bar" -> "baz";
   }
```

引用式：

```
.. graphviz:: external.dot
```




## plantuml

使用插件[sphinxcontrib-plantuml](https://pypi.python.org/pypi/sphinxcontrib-plantuml)

安装：
```
pip install sphinxcontrib-plantuml
```

配置：

在 `conf.py`中配置插件：

```
# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = ['sphinx.ext.autodoc']
extensions = ['sphinxcontrib.plantuml']

plantuml = 'java -jar plantuml.2017.08.jar'

```

嵌入式：

```
.. uml::
   :caption: Caption with **bold** and *italic*
   :scale: 50 %
   :align: center

   Foo <|-- Bar
```

引用式：

```
.. uml:: external.uml
```


## 支持markdown

sphinx官方[已经支持Markdown](https://pypi.python.org/pypi/sphinxcontrib-plantuml), 使用[recommonmark](http://recommonmark.readthedocs.io/en/latest/index.html)解析[CommonMark Markdown](http://commonmark.org/)。

安装：

```
pip install recommonmark
```

配置：
```

source_parsers = {
  '.md': 'recommonmark.parser.CommonMarkParser',
}

source_suffix = ['.rst', '.md']
```


## 主题(Theme)

Sphinx支持theme。比如，如果你喜欢[Read the Docs Sphinx Theme](https://github.com/rtfd/sphinx_rtd_theme),

只需安装 `pip install sphinx_rtd_theme` 并配置 `html_theme = "sphinx_rtd_theme"`即可。

也可以配置该主题支持的个性化选项，比如：

```
html_theme_options = {
    'collapse_navigation': False,
    'display_version': False,
    'navigation_depth': 3,
}
```


