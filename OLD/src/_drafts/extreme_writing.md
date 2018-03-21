---
title: '“极限写作”实践'
date: 2014-11-21
abstract: |
    摘要。。。
    摘要第二行。。。

category: 方法
tags: [markdown, pandoc, vim, ]
---

已经半年多没有写新的博客了，借口是工作比较忙；内因是这段时间比较懈怠；外因就是原来的写作方法不够方便。
继续开始写博客的第一篇文章，我想先整理一下我的写作方法和工具。暂且命名为“极限写作”吧。


# 写作的需求

写作的目的是“记录、抒发、批判、反省”[^1]。就我个人而言，写作主要分为两类：工作文档和技术文章。

工作文档自然是为了满足工作需要，比如方案、建议书、白皮书、API文档、计划和总结等，有时也需要一些幻灯片。

而技术文章写作的目的首先是对已经掌握的知识进行梳理、加深理解，以备查阅。下面这句话说得非常到位[^2]：

> When you move from your head to "paper," a lot of the hand-waveyness goes away and you are left to really defend your position to yourself.

写作的另外一个目的就是分享。所以我需要将技术文章发布为博客，pdf, 电子书等形式。
当然，将工作文档提交给别人也可以看作一种广义的“分享”，只不过是是出于某种强制。

明确了目的，也就明确了需求。那么我的写作需求主要包括：

1. 统一的编辑格式

   我需要一种统一的格式，不管是写工作文档、博客文章、制作幻灯片，还是思维导图、计划任务，都使用同一种格式。
   这种格式必须是基于文本的“所想即所得”方式。其好处在《Markdown 写作浅谈》[^3] 中已经总结过了，这里不再赘述。

   这种编辑格式还必须支持“富文本”，比如图片、超链接、参考文献等，都要有很好的支持，
   如果有可能，最好能支持嵌入graphviz代码。

2. 写作与发布分离

   这是“所想即所得”思想的延续。既然在编辑内容时不应该考虑格式，那么在编辑文档时也不应该考虑发布。
   比如Jekyll的文档元数据中，`TITILE`、`TAGS`等是文档本身的元数据，但是`LAYOUT`确是发布相关的元数据，应该在文档中去除。

   除了元数据之外，文档的组织也不应该绑定到某种特定的发布形式。比如，我之前用Jekyll的`_posts`，`_drafts`来组织文件，
   文件的命名也遵循了Jekyll的“日期-文件名.md”格式。对于不属于博客文章的文档，这样管理非常别扭，必须进行改进。

   总而言之，在编辑文档时，一切与发布相关的事情都不作考虑。

3. 内容复用

   既然实现了“写作与发布分离”，那么内容当然可以复用——通用的内容即可以作为独立的博客文章，也可以作为电子书/工作文档中的一个章节，
   甚至还可以发布为幻灯片（当然，文章与幻灯片的差异还是比较大的）。

4. 版本管理

   这个不用多说。如果还在用文件名来区分文档的不同版本，那就干脆转行吧。

# 解决方案

   明确需求之后，就是进行方案设计，以及工具/产品的选型。结合网上大量的资料及个人的特点和实际需要，我认为下述方案最能提高我的写作效率。
   
针对以上需求,反复比较各种解决方案,比如github托管,octopress,emacs org,docbook,evernote等等,最终决定采用emacs org方式,虽然有些地方还有缺陷,比如移动终端的全文搜索,但是相比其他而已,这个更适合与我
编辑,采用emacs-orgmode, 各种语言都有很好的支持,orgmode本身的outline非常强大
采用dropbox同步到各种设备
采用org export , public发布到blog,导出成pdf,html等


## 文件组织

```

DOC_ROOT/
├── articles                        # 保存文章，可以发布到博客，或者作为电子书的组成部分
│   ├── assets -> ../assets/        # 连接到统一的资源(图片等）目录
│   ├── category1                   # 按照分类进行管理
│   ├── category2
│   └── category3
├── assets                          # 为了方便，所有的图片等资源统一管理，在各个分类中建立软连接
├── bin                             # 各种工具，比如发布脚本、统计工具、文档检查工具等，以后可以转成vim插件
├── books                           # 保存电子书
│   └── assets -> ../assets/
├── drafts                          # 保存草稿
│   └── assets -> ../assets/
├── gtd                             # 计划、任务、日程等
├── templates                       # 模板，包括自定义的pandoc转换模板，以及各类文档模板。文档模板以后也可以放到vim插件中
│   └── pandoc
├── tools                           # 第三方工具，比如revealjs等
├── works                           # 保存工作文档
│   ├── projects
│   ├── proposals
│   └── reports
└── publish                         # 发布相关的数据
```

## 编辑格式的选择

我以前使用Emacs org-mode。直到现在，我仍然认为org-mode是最好的文档编辑格式和工具[^4]。
但是现在我选择了Markdown。如同我从Emacs换回Vim的理由[^5] 一样，既然我在很多地方必须使用Markdown，就没有必要让两套语法在我的大脑中打架了。
关于Markdown的介绍及基本语法，在 [Markdown+Pandoc  最佳写作拍档](http://mailp.in/d9gDXg0O/) [^1],  
[Markdown 写作浅谈](http://www.yangzhiping.com/tech/r-markdown-knitr.html) [^3] 等文章中都有叙述；
如果需要语法手册，[Markdown快速入门](http://wowubuntu.com/markdown/basic.html) [^6] 和 
[Markdown 语法说明](http://wowubuntu.com/markdown/) [^7] 是非常棒的资源。

顺便说一句，我觉得与org相比，Markdown使用人群更广泛，也更加开放——可以基于很多工具/编程语言去操作Markdown，而不仅限于Emacs和Elisp，
从而更加适合互联网。

由于基本Markdown的功能实在有限，我选择pandoc扩展的Markdown。pandoc扩展了Markdown的脚注、表格、有序列表、自定义列表；
能够很好的展现代码块、上下标、删除线、标题块、目录，可以嵌入LaTex的公式、参考文献等语法，并支持Markdown的HTML区块[^8]，

完全能够满足我的各种写作需求。一些比较特殊的用法记录如下：

### 文档元数据

我不太习惯pandoc的标题块扩展(Extension: pandoc_title_block)，所以我选择yaml格式的标题块扩展(Extension: yaml_metadata_block)[^8]。
以yaml格式定义的文档元数据既可以放在外部的yaml文件中，也可以放在文档头部。直接嵌入文档头部似乎是个不错的选择，与Jekyll很类似。
我自定义了我需要的一些文档元数据（如前所述，不包含“发布”相关的信息），并制作成vim模板，每次创建Markdown文件时自动插入：


```
---
title: ' ' 
date: 2014-
update: 2014-
category: ' ' 
tags: [, ]
abstract: |
  摘要... 
  ... ...
---
```

### 公式

目前看来，最好的做法就是在Markdown中直接嵌入LaTeX公式。比如：

```
$$\begin{align*} & \phi(x,y) = \phi \left(\sum_{i=1}^n x_ie_i, \sum_{j=1}^n y_je_j \right) = \sum_{i=1}^n \sum_{j=1}^n x_i y_j \phi(e_i, e_j) = \\ & (x_1, \ldots, x_n) \left( \begin{array}{ccc} \phi(e_1, e_1) & \cdots & \phi(e_1, e_n) \\ \vdots & \ddots & \vdots \\ \phi(e_n, e_1) & \cdots & \phi(e_n, e_n) \end{array} \right) \left( \begin{array}{c} y_1 \\ \vdots \\ y_n \end{array} \right) \end{align*}$$
    ```

通过pandoc参数`-s --mathjax`，可以在html中通过js渲染成如下的形式：


$$\begin{align*} & \phi(x,y) = \phi \left(\sum_{i=1}^n x_ie_i, \sum_{j=1}^n y_je_j \right) = \sum_{i=1}^n \sum_{j=1}^n x_i y_j \phi(e_i, e_j) = \\ & (x_1, \ldots, x_n) \left( \begin{array}{ccc} \phi(e_1, e_1) & \cdots & \phi(e_1, e_n) \\ \vdots & \ddots & \vdots \\ \phi(e_n, e_1) & \cdots & \phi(e_n, e_n) \end{array} \right) \left( \begin{array}{c} y_1 \\ \vdots \\ y_n \end{array} \right) \end{align*}$$

    

### 参考资料

尽管pandoc支持严格的参考文献格式(pandoc-citeproc)[^8]，但是对于我等“非科技工作者”来说，有杀鸡用牛刀之嫌。
况且参考资料多半来自互联网，原文也未必有严格的引用说明。所以使用pandoc扩展的脚注(footnote)就完全够用了[^10]。


### 表格

pandoc支持4种格式的表格，分别为简单表格(simple_tables), 带表头的表格(multiline_tables), ASC风格的表格(grid_tables)和管道表格?(pipe_tables)。
其中，pipe_tables可以使用org-mode风格的语法，也可以使用自带的能设置列对齐方式的语法。我选择的是最后一种，pandoc官方文档[^8] 中的例子如下：

```markdown
| Right | Left | Default | Center |
|------:|:-----|---------|:------:|
|   12  |  12  |    12   |    12  |
|  123  |  123 |   123   |   123  |
|    1  |    1 |     1   |     1  |
```

书写起来可能有点麻烦，但是已经有人编写了Vim插件支持表格的编写（下面有介绍），大体可以实现org-mode中编辑表格的体验。

## 文档编辑工具

与org-mode相比，Markdown最显著的优势就是不依赖特定的编辑器。
因为我已经从Emacs换回Vim[^5] ，所以用Vim作为Markdown编辑器就是很自然的选择。
当然，为了用起来更顺手，一些Vim插件是必不可少的，包括但不限于：

- [vim-pandoc](https://github.com/vim-pandoc/vim-pandoc.git): Vim中支持pandoc Markdown文件的编辑，并整合了pandoc命令 
- [vim-pandoc-syntax](https://github.com/vim-pandoc/vim-pandoc-syntax.git): vim-pandoc不支持语法高亮，需要本插件配合
- [vim-pandoc-after](https://github.com/vim-pandoc/vim-pandoc-after.git): 整合vim-pandoc与其他第三方插件，比如：
   + [ultisnips](https://github.com/SirVer/ultisnips.git): 一个强大的代码片段插件
   + [Neosnippet](https://github.com/Shougo/neosnippet.vim.git): 另一个代码片段插件
   + [vim-table-mode](https://github.com/dhruvasagar/vim-table-mode.git): 方便的表格编辑工具
- [vim-markdownfootnotes](https://github.com/vim-pandoc/vim-markdownfootnotes.git): Markdown中方便的脚注支持
- ~~[shareboard.vim](https://github.com/lambdalisue/shareboard.vim.git): 提供Markdown预览功能(需要Qt，比较重)~~
- ~~[vimpreviewpandoc](https://github.com/tex/vimpreviewpandoc.git): 预览Markdown中嵌入的graphviz, R图表等绘图代码(我还未配置成功）~~
- [vim-screencap](https://github.com/holbrook/vim-screencap): 我写的一个方便截图的插件，目前只适用于MacOS


## 强大的转换工具：pandoc

可以说，如果没有pandoc，我绝对不会放弃org-mode。已经有太多的文章赞美pandoc了，比如《Markdown+Pandoc 最佳写作拍档》[^1], 
《Markdown写作进阶：Pandoc入门浅谈》[^11], 《黑魔法利器pandoc》[^12]等等。对于我来说，最大的好处就是：pandoc比org-publish容易定制！
下面列举我用到的一下文档转换方法。


### 生成博客

我仍然使用GitHub Pages发布博客。尽管Jekyll支持插件，但是GitHub Pages禁用了插件功能，所以只能考虑在本地生成html。

可以有两种选择：完全生成静态页面；生成符合Jekyll要求的html。前者的好处是通用，后者的好处是可以利用Jekyll的layout功能，
以及使用变量生成配套的分类、标签、rss等页面。

由于我只需要发布在GitHub Pages，所以我选择后者。这里又有三种选择：

1. 使用total solution(比如octopress, Jekyll Bootstrap，或者干脆使用Hyde[^10])
2. 使用Jekyll+插件，上传本地生成的静态页面
3. 使用转换工具(pandoc), 加上一些自定义的脚本

因为生成其他格式（比如slide, pdf, docx等）时，我以及研究了pandoc，所以不防也使用pandoc生成“Jekyll html”。当然，需要自己编写一点点脚本。

```bash
pandoc -s --mathjax --self-contained --toc -N --template ../templates/pandoc/jekyll.post.tpl POST_NAME.md -o ../holbrook.github.io/_posts/2013-01-01-money.html
```

其中，

- `-s`: 不生成完整的html文档，只生成html片段

其中，我对pandoc的默认模板进行了一点点更改，如下：

```
---
layout: post
$if(title)$title: $title$$endif$
$if(date-meta)$date: $date-meta$$endif$
$if(update)$update: $update$$endif$
$if(description)$description: $description$$endif$
$if(category)$category: $category$$endif$
$if(tags)$tags: [$for(tags)$$tags$, $endfor$]$endif$
---
$if(toc)$
<div id="$idprefix$TOC">
<h3>目录</h3>
$toc$
</div>
$endif$
$body$
$for(include-after)$
$include-after$
$endfor$
```




### 生成docx, pdf, LaTeX


## 方法和工具

### 基本写作




### 发布关联图片

### 链接替换

###本地链接-》发布链接

### 技术文章写作

写技术文章通常需要插入代码。如果想写成质量比较高的技术文章，还会遇到“科技写作”的三个问题，
即公式与图表，LaTeX支持和参考文献管理[^3]。

对于文章中插入代码，Markdown已经定义了专门的语法，pandoc在转换Markdown为html/html5时，会使用`<code>`标签进行标记，
只需定义对应的css就可以有很好的展示。


公式与图表及LaTex支持，[阳志平]推荐的方法是[yihui](https://github.com/yihui)的[knitr](http://yihui.name/knitr/)(R包)，
由于我不是专业的科技人员，我更倾向与使用纯粹的Markdown + pandoc，嵌入praphviz, ...
可以参考这篇文档[^9] 解决 latex的问题



参考文献。
工具： `brew install pandoc-citeproc`

方法：
1. 外部文件 or 文档元数据？


2. 


### 发布博客文章


### 幻灯片


### 电子书



### 自定义工具




# 工具
## pandoc

## ditaa

 Embedded diagrams in pandoc's markdown


##

# 参考资料

[^1]: [Markdown+Pandoc  最佳写作拍档](http://mailp.in/d9gDXg0O/)

[^2]: [Why I blog](http://www.gabrielweinberg.com/blog/2011/08/why-i-blog.html)

[^3]: [Markdown 写作浅谈](http://www.yangzhiping.com/tech/r-markdown-knitr.html), 阳志平

[^4]: [org-mode，最好的文档编辑利器，没有之一](http://holbrook.github.io/2012/04/12/emacs_orgmode_editor.html), Holbrook

[^5]: [重拾vim](http://holbrook.github.io/2013/05/23/vim_addon_manager.html), Holbrook

[^6]: [Markdown快速入门](http://wowubuntu.com/markdown/basic.html) 

[^7]: [Markdown 语法说明](http://wowubuntu.com/markdown/)

[^8]: [Pandoc User’s Guide](http://johnmacfarlane.net/pandoc/README.html)

[^9]: [Markdown+Pandoc：A light-weight solution for academia writing](http://www.douban.com/note/245109923/)

[^10]: [使用hyde+github pages搭建静态站点](http://www.babyishan.com/blog/2012/05/github_pages_with_hyde)

[^11]: [Markdown写作进阶：Pandoc入门浅谈](http://www.yangzhiping.com/tech/pandoc.html)

[^12]: [黑魔法利器pandoc](http://yanping.me/cn/blog/2012/03/13/pandoc/)
