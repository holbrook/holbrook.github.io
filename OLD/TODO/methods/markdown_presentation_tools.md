用 Markdown 写幻灯片


pandoc 1.12+（此版本开始支持revealjs）


# 好处

- 用 Markdown 写幻灯片
  
  没有比 Markdown 更简洁的书写方式了
  采用” 轻文本标记型语言 “，主要是 Markdown语言 。文档和格式分开，轻便简单方便操作


- css,js, html5 用 CSS 设计样式

  内容和展示分离

  内容和展示分离不仅可以让用户更专注于幻灯片的写作，还能够提高“展示层”的复用机会。用户可以选择自己喜欢的主题或模板，而不用自己去布局。

  采用HTML5技术，先进快捷。在浏览器中打开投影片，非常简单易行。大多数现代浏览器（IE浏览器和国产山寨浏览器除外）都是支持的。
  非常酷，因为大多是用Javascript脚本实现的，所以想要多酷就有多酷，完全自由！

- 用 Github Pages 托管

  版本控制，自由分享

  所以目前有越来越多的项目在github上弄个网页来展示投影片。


- 用浏览器进行展示

  用 LaTeX + Beamer 也可以实现写作与展示分离的效果，但 PDF 是一种刻板的展示方式。相反，由于浏览器有 JavaScript 和 HTML5 支持，幻灯片就可以实现一些很酷的效果。最重要的是，浏览器和 PDF 一样，也是跨平台的。

  使用浏览器的另一个好处是，无论我们在哪里，只要能够上网可以进行 presentation，而不用跑到哪都带一个 U 盘（以防万一，有时还要带两个），也避免了大会上人们排队往电脑上拷贝幻灯片的麻烦。

  易于分享，只要放到网站上即可，看的人不需要安装任何软件！


# demo

http://blog.chengyichao.info/weakpoint/

# 要点


既然是要用Markdown，那么首先用markdown来写一个演讲稿大纲，并把这个大纲按照投影片的方式整理一下：

```
% 主标题
% 演讲人
% 日期时间

----
# 投影片的标题
## 副标题
- 列表
- 列表项**强调的内容**
- 列表项3

----

#又一个投影片的标题
1. 有序列表1
2. 有序列表2 *斜体的内容*

----

# 第三张投影片
！ [图片](image/press.jpg)
```

# 工具

- 目前最常用的解决方案： pandoc????

  pandoc这个奇妙的工具，那么所有涉及到书写的工作基本上都可以由markdown完成了。


- Impress.js： 简单快捷

  有个项目叫 [mdpress](https://github.com/egonSchiele/mdpress) ，
  可以实现Markdown+ Impress.js 的结合，
  可以参考 [这篇文章](https://chronicle.com/blogs/profhacker/markdown-and-mdpress-for-presentations/46343) 。

  左右键控制翻页，大多数浏览器用F11来全屏浏览。
  Impress.js还有恨多非常酷的特效，在markdown写的投影片里用至少三个连续短线”—-”来分割投影片，在短线下面可以写上一些impress.js提供的特效参数。 最终版 ， 源文件
  

mdpress项目还有一些示例可以看看，项目主页：https://github.com/egonSchiele/mdpress

- Pandoc+Reveal.js：效果更炫

  这是最近刚刚发现的一个，实现的最终效果和上一个差不多，但是我觉得更炫。

  这是由[Reveal.js](https://github.com/hakimel/reveal.js) 提供的，
  自带了好几个主题包，其3D效果非常炫。

  我这里还要用到Pandoc，所以安装略有点复杂。可以看 [这篇文章](https://github.com/jgm/pandoc/wiki/Using-pandoc-to-produce-reveal.js-slides) 和 [这篇文章](https://gist.github.com/aaronwolen/5017084) 。


  reveal.js 使用起来比较麻烦，不过
  [liquidluck-theme-reveal](https://github.com/popomore/liquidluck-theme-reveal/)
  可自动将 markdown 文件生成基于 reveal 的页面。他需要有一些约定，ppt 的每一页是由 --- 分开的

  (http://chuo.me/2012/11/markdown-to-ppt.html)

- deck.js

  keydown(ruby)KeyDown，是基于Markdown和 deck.js 的用ruby开发的“单页HTML讲义（给予浏览器的幻灯片）”的工具。它方便我们创建依赖于deck.js的工程，编写Markdown文档，最后将Markdown文档转化为HTML网页。 Showoff, Slidedown, HTML5 Rocks, with a little Presentation Zen thrown in.

示例地址：http://infews.github.com/keydown/#slide-0


- slideshow(ruby)

  slideshow这个ruby gem，易用而且支持上面提到的各种template，特此推荐。

  slideshow可以将markdown或textile等文件解析成ppt，所有的ppt页面都在一个html页中，因此你可以直接把这个html放在自己的网站上，供别人访问。


  slideshow默认为s6模版。安装其他模版输入命令以deck.js为例：
  ‘slideshow -f deck.js’

  http://sleefd.github.io/blog/2013/03/07/markdown-ppt/
  自己做了一个demo，关于密度聚类算法的ppt。示例markdown。
  slideshow参考:slideshow
  推荐网站 reveal，支持在线ppt编辑，可直接生成一个在线浏览链接，非常方便。


- [remark.js](https://github.com/gnab/remark)

# 5 of the Best Free HTML5 Presentation Systems

http://www.sitepoint.com/5-free-html5-presentation-systems/


Reveal.js(3D cube)

This is my current favorite. Slides look great and can be positioned horizontally or vertically. It’s also easy to change the CSS to add your own effects — I managed to add a rudimentary notes facility doing just that.

Slides are defined in separate section tags and Reveal.js offers a choice of several 3D slide transitions … although they look fairly similar.

Download the reveal.js files…

Impress.js(电影手法)

Impress.js is, well, impressive. It’s been influenced by the commercial prezi.com; slides are arranged in a 3-dimensional space and your view rotates and pans accordingly. I won’t attempt to explain it further — just try it and you’ll understand what I mean.

Slides are defined in div elements with data attributes controlling the x, y, z locations and rotations. That’s the only drawback; it’s a little difficult to visualize and define those values. Persevere, though, and you’ll be able to create some stunning and original slide shows.

Download the Impress.js files…

Deck.js(简单，传统)

Deck.js was one of the first HTML5 presentation systems. It looks similar to Google’s offering — perhaps a little prettier, but without slide transition effects.

Slides are defined within semantically correct section blocks in an outer article. There’s also a documented API so it’s possible to create your own extensions.

Download the Deck.js files…


Other worthy mentions:

S5 — A Simple Standards-Based Slide Show System (download)
CSSS — CSS-based SlideShow System (download)
Slides (download)
HTML5Rocks (no direct downloads, but you can copy the source)
Have I neglected to mention your favorite HTML5 presentation system…


