---
layout: post
title: "Jekyll建站过程"
description: "本站建立过程中的一些经验，不断完善中..."
category: 杂七杂八
tags: [jekyll, github]
lastmod: 2013-06-17
imgroot: "/images/posts/tools/jekyll_mysite/"
---



早在2012年8月，就通过[这篇文章](http://www.ruanyifeng.com/blog/2012/08/blogging_with_jekyll.html)知道了Jekyll,  但是一直没有去尝试。

直到最近静下心来，才发现使用Jekyll 搭建博客非常简单。当然，上手简单，想用好并不容易。

本文记录在使用Jekyll搭建博客过程中的一些过程和经验，并持续完善和改进。

本文分成3个部分：

- 基础篇：最简单、最快速的使用Jekyll
- 进阶篇：一些个性化定制的选项
- 推广篇：博客推广的一些手段和方法


# 基础篇

## 关于Jekyll

![Jekyll](images/posts/tools/jekyll_mysite/jekyll.jpg)

已经有太多的文章介绍了[Jekyll](http://jekyllrb.com/)(/'dʒiːk əl/)。
简单的说，Jekyll是用ruby语言实现的一个静态网站生成器，可以将[Markdown][1] (或者[Textile][2])编辑的文档生成html。
当然也可以用来生成博客。
我使用Markdown标记语言，其语法可以参考[这里](http://wowubuntu.com/markdown)。

Jekyll支持[Liquid][3]模板语言，写文档时的感觉很像是在写Django模板。Jekyll定义了一些[内置的变量][4]，包括全局变量、页面变量等。
[在文档中可以设置页面变量的值][5]。

与RoR类似，Jekyll也可以通过插件来增加额外的功能。


[1]:http://daringfireball.net/projects/markdown/
[2]:http://textile.sitemonks.com/
[3]:http://wiki.shopify.com/Liquid
[4]:http://jekyllrb.com/docs/variables/
[5]:http://jekyllrb.com/docs/frontmatter/


## 关于github Pages

[github][]是程序员的facebook。[github Pages][6]是github提供的静态网页托管。可以为用户或者项目创建站点。
有意思的是，github Pages对于上传的静态文件会通过Jekyll进行处理后再发布出来。

于是，一些”不务正业“的程序员就开始使用github Pages建立博客，现在这股风潮已经愈演愈烈，一些程序员聚集的博客站点可能要小心应对了。

[github]:https://github.com/
[6]:http://pages.github.com/

## 使用github Pages写博客的好处

为什么说”一些程序员聚集的博客站点可能要小心应对了“呢？ 因为github Pages简直是为程序员量身定制的博客系统。
（当然，估计也只有程序员会愿意折腾这些事情）。

对我来说，使用github Pages写博客的好处主要体现在以下方面：
1. 自由，随意定制
2. 方便，在github上托管
3. 可控，有版本管理
4. 直接，只需提交，不需要先导出再提交，让人愿意持续更新文章
5. 高效，使用markdown语言能提高写作的效率（但是个人觉得不如org-mode)
6. 免费，无限流量，无限空间

## 关于Jekyll Bootstrap

[jekyll-bootstrap](http://jekyllbootstrap.com/)是用Jekyll建立博客的一套模板，提供了主题（themes)、评论、。。等功能，

对于Jekyll的初学者能提供很大的帮助，其网站上号称“基于GitHub Pages建博客的最快方式”，可以“用3分钟就建立一个博客”。


## 3分钟建立博客

让我们看看上述工具的组合如何用3分钟建立博客。假设你已经有git的基础，在github上托管过项目。并且使用的不是windows。

    # 检查ruby版本
    ruby -v
    #更换更快的gem源，可选
    gem sources --remove http://rubygems.org/
    gem sources -a http://ruby.taobao.org/
    gem sources -l

    #如果不是1.9.3+，需要升级到1.9.3
    bash < <(curl -s https://raw.github.com/wayneeseguin/rvm/master/binscripts/rvm-installer )
    source ~/.bashrc

    rvm install 1.9.3
    # 安装jekyll, 并使用rdiscount作为markdown解析器
    sudo gem install jekyll
    gem install rdiscount

    # 使用Jekyll-Bootstrap，其实就是一个复制的过程。下面的USERNAME代表你在github上的用户名
    git clone https://github.com/plusjade/jekyll-bootstrap.git USERNAME.github.com


    # 使用GitHub Pages的账户主页建立博客，必须使用如下形式的项目名称并使用主分支
    # 如果使用项目主页，必须使用项目的gh-pages分支
    cd USERNAME.github.com
    git remote set-url origin git@github.com:USERNAME/USERNAME.github.com.git
    git push origin master

    好了，等上几分钟，你的主页就发布在了https://USERNAME.github.com。

## 其他操作

### jekyll命令

安装jekyll会产生一个命令行工具：jekyll，提供以下功能：

    build                Build your site
    doctor               Search site and print specific deprecation warnings
    help                 Display global or [command] help documentation.
    import               Import your old blog to Jekyll
    new                  Creates a new Jekyll site scaffold in PATH
    serve                Serve your site locally

### Rakefile

Jekyll-Bootstrap提供了一个Rakefile（ruby的makefile），包含一些博客相关的任务（task），包括：

    $ rake -T
    rake page           # Create a new page.
    rake post           # Begin a new post in ./_posts
    rake preview        # Launch preview environment
    rake theme:install  # Install theme
    rake theme:package  # Package theme
    rake theme:switch   # Switch between Jekyll-bootstrap themes.





# 进阶篇

## 放弃Jekyll bootstrap

Jekyll bootstrap确实能带来一些变量，但是和RoR一样，充满了各种puzzle。
更加让中国人不爽的是，作者将其缩写定义为“JB”。

经过初步的尝试后，我决定放弃JB，也不想尝试[Octopress](http://octopress.org/)。我的选择是用原生的Jekyll来构建博客，让一切都在掌控之中。


## Jekyll的目录结构

使用Jekyll创建一个干净的站点：

    $ jekyll new clearly
    $ tree clearly/
    clearly/
    ├── _config.yml
    ├── _layouts
    │   ├── default.html
    │   └── post.html
    ├── _posts
    │   └── 2013-05-29-welcome-to-jekyll.markdown
    ├── css
    │   ├── main.css
    │   └── syntax.css
    └── index.html


其中，博客文章放在_posts目录中，可以使用子目录。
博客文章必须使用
    YEAR-MONTH-DAY-title.MARKUP
的形式命名，比如：
    2011-12-31-new-years-eve-is-awesome.md

 _layouts目录存放页面模板，其他还可以使用html、css、image等静态资源。

Jekyll会把任何不以下划线开头的文件和目录都复制/生成到网站（在本地是生成到_site/目录)。

## 设计模板

jekyll把_layouts目录中的文档看做是模板，如果某个文档中的头部变量声明中指定了layout：

    ---
    layout: post
    ...
    ---

则Jekyll在生成页面时会使用该模板进行渲染，用文档的内容替换模板中的{{ content }}部分。

模板本身也是文档，所以一个模板也可以用layout变量指定使用一个模板作为布局，这就是模板的继承。

此外，在设计模板时，利用好Liquid语言的include语法能够带来很大的变量。被包含的页面部件需要放在_includes文件夹中。

因为Jekyll生成的是静态站点，可能会需要大量的js以增加动态特性，在设计模板时要遵循[Unobtrusive JavaScript原则](http://dev.opera.com/articles/view/the-seven-rules-of-unobtrusive-javascrip/)。

## 灵活的导航

使用静态的导航菜单会带来两个问题：

1. 文档过长
2. “当前项”的高亮不好处理

可以在_config.yml中设置一个导航菜单的变量：

{% highlight yaml %}
    menuitems:
    - name:			首页
      url:          /index.html
    - name:		  	分类
      url:          /categories.html
    - name:		  	标签
      url:          /tags.html
    - name:		  	归档
      url:		  	/archive.html
    - name:		  	读书
      url:		  	/reading.html
    - name:		  	工作
      url:		  	/working.html
    - name:		  	关于
      url:		  	/about.html
{% endhighlight %}

然后在模板的导航部分可以这样写：
{% highlight html %}
<ul class="nav">
  {/% for item in site.menuitems %/}
    {/% if item.url == page.url %/}
    <li class="active">
    {/% else %/}
    <li>
    {/% endif %/}
    <a href="{{item.url}}">{{item.name}}</a>
    </li>
  {/% endfor %/}
</ul>
{% endhighlight %}

## 分类、标签、归档和RSS

这些都是博客站点必须有的元素。分类、标签和归档可以安装不同的方式检索博客文章；RSS可以订阅博客。

用Jekyll的变量和模板很容易实现这些元素。

注意：不管文件的扩展名是md、html还是xml、txt，只要文件的头部包含变量声明，Jekyll的模板引擎就会对其进行处理。
其中md和html文件都会处理为html，其他类型会保持扩展名。

但如果不是写文档，最好不要使用md，否则会按照markdown语法进行渲染，带来一些意想不到的麻烦。

具体的例子可以参考JB中的代码。

你可能需要对每个分类、每个标签建立单独的索引页面，这个活手工做比较麻烦，可以使用Jekyll插件或者自己写脚本生成文件，
但这不符合“KISS”原则，这里不进行探讨。

对于标签云(tag cloud)，在不使用插件的情况下，可以使用js实现，参考如下代码：
{% highlight html %}
    <div class="tag-cloud">
       {/% for tag in site.tags %/}
          <a href="/pages/tags.html#{/{ tag[0] }/}-ref" id="{/{ forloop.index }/}" class="__tag" style="margin: 5px">{/{ tag[0] }/}</a>
       {/% endfor %/}
    </div>

    <script type="text/javascript">
       $(function() {
          var minFont = 15.0,
              maxFont = 40.0,
              diffFont = maxFont - minFont,
              size = 0;

          {/% assign max = 1.0 %/}
          {/% for tag in site.tags %/}
             {/% if tag[1].size > max %/}
                {/% assign max = tag[1].size %/}
             {/% endif %/}
          {/% endfor %/}

          {/% for tag in site.tags %/}
             size = (Math.log({{ tag[1].size }}) / Math.log({{ max }})) * diffFont + minFont;
             $("#{{ forloop.index }}").css("font-size", size + "px");
          {/% endfor %/}
       });
    </script>
{% endhighlight %}

关于分类和标签的设计，可以参考[这篇文章](http://thinkinside.tk/2012/11/05/blog_design_categories_and_tags.html)


## 分页

TODO: ajax分页
TODO: 浮动标题 on paginator

## 语法高亮

对于程序员，博客中难免会包含一些代码。实现代码高亮可以有几种方法：

- 利用外部资源，比如[GitHub Gist](https://gist.github.com/)

  简单，但是需要使用外部链接或通过js嵌入到页面，不利于文档和代码的统一维护

- 使用js在前端渲染，比如[google-code-prettify](https://code.google.com/p/google-code-prettify/)

  简单高效，对语言的支持不够多

- 使用Jekyll插件，比如调用[pygments](http://pygments.org/)

  推荐方式。支持[100多种语言](http://pygments.org/languages/)。



~~~本站采取js的方式。只需要在post的模板中进行配置，就可以为所有博文的代码进行渲染~~~

~~~Jekyll在编译markdown时，会将符合“代码格式”的内容放到一个< pre>< code></ code>< /pre>标签中。~~~
~~~而prettify提供的js会对html中的所有< pre>< /pre>或< code></ code>区块进行处理，甚至会自动判断使用的语言。~~~

~~~在post模板的合适位置中增加以下内容：~~~
{% highlight html %}
<link href="/js/google-code-prettify/prettify.css" rel="stylesheet">
<script src="/js/google-code-prettify/prettify.js"></script>
<script>
$(document).ready(function(){
     prettyPrint();
});
</script>
{% endhighlight %}

~~~如果要更改配色方案，只需要修改css文件。~~~

本站采用pygments的方式：

- 安装pygments

{% highlight bash %}

pip install pygments

{% endhighlight %}

- 在_config.yml中设置

{% highlight yaml %}

pygments:       true

{% endhighlight %}

- 在代码的前后增加过滤器：

{% highlight ruby linenos %}

{/% highlight ruby linenos %/}
def foo
  puts 'foo'
end
{/% endhighlight %/}

{% endhighlight %}

- 更改样式

  从[这里](https://github.com/mojombo/tpw/blob/master/css/syntax.css)获取css样例，并自行更改。

## 文档目录(TODO)

如果写比较长的文章，提供一个类似于developerworks上的文档目录进行导航可以方便阅读。

## 使用公式

[MathJax](http://www.mathjax.org/) is an open source JavaScript display engine for mathematics that works in all modern browsers.

使用maruku来解析markdown文件，可以把LaTeX解析成图片，

优点是网页加载速度快。但是在windows下安装复杂，且需要安装有LaTeX
        Mathjax  <http://www.mathjax.org/>，缺点是动态加载，速度慢。

参考：http://chen.yanping.me/cn/blog/2012/03/10/octopress-with-latex/


## 处理图片

设置一个IMAGE_ROOT变量，可以可以在post中设置，也可以在post的模板中通过指定的规则capture（或者assign）。

则引可以使用{{page.IMAGE_ROOT}}/xxx.png的形式插入图片，便于以后的调整和管理。

{{page.url}}
page_url

## 处理表格(TODO)

## 博客搬家（TODO）

用Jekyll写博客的，通常不会是新博主，会存在博客搬家的需求。

Jekyll提供了一个import的子命令(需要插件jekyll-import），可以将旧的博客导入到Jekyll。


[exitwp](https://github.com/thomasf/exitwp)是一个用python开发的工具，号称是将wordpress的博客导出并转换成markdown，但实际上
任何能导出rss/atom的博客都可以用这个工具进行转换。

    git clone https://github.com/thomasf/exitwp
    sudo pip install --upgrade  -r pip_requirements.txt
    cd exitwp/wordpress-xml/
    wget http://your/atom/file/xml
    cd ..
    python exitwp.py


# 推广篇

## 使用域名

Github Pages会为站点分配类似"USERNAME.github.com"的二级域名。你也可以使用自己的域名。

1. 申请域名

   免费的域名(.tk)可以在[DotTK](http://www.dot.tk/zh/index.html)申请。

   .tk是南太平洋岛国托克劳的国家域名，支持域名转发（可隐藏原URL）、电邮转发、A记录解析、CNAME别名记录、MX邮件记录、设置DNS服务器等服务。

   收费的域名到处有，是否使用国内的域名商随你。

2. 域名解析服务

   一般来说域名提供商会提供简单的解析服务，也支持将解析服务指向到其他的提供者。

   国外的如[Godaddy](http://www.godaddy.com/)，可能被墙。

   国内的如[DNSPod](https://www.dnspod.cn/)，有免费版。

3. 配置

   - 在jekyll站点中增加CNAME文件，记录使用的域名
   - 如果使用顶级域名，在域名解析服务提供商那里将A记录指向[204.232.175.78](1)
   - 如果使用二级域名，在域名解析服务提供商那里增加CNAME记录，指向[204.232.175.78](1)

[1]:https://help.github.com/articles/my-custom-domain-isn-t-working


## 社会化网络

Jekyll生成的是静态网站，诸如评论、推荐、关注之类的功能就无法实现了。

不过好在现在有很多社会化网络应用，通过混搭(marshup) 可以把各种各样第三方的功能部件（widgets）加到你的博客中。

与博客相关的Widget主要有几类：

1. 社会化评论

   专门提供评论功能的网站，可以为博客增加评论功能。也可能附带着关注、相关文章、推荐等功能。

   国外的有[disqus](http://disqus.com/)，国内的有[友言](http://www.uyan.cc/)，[多说](http://duoshuo.com/)

2. 社会化推荐

   自动推荐跨站的相关文章。包括自动推相关文章。

   国内的有[友荐](http://www.ujian.cc/publishers)，[无觅](http://www.wumii.com/widget/relatedItems.htm)。

   Jekyll本身也可以实现站内文章推荐的功能。

3. 社会化分享

   将自己喜欢的网址分享给别人，通常附带推荐功能。

   国内的有[加网](http://www.jiathis.com/) ，[百度分享](http://share.baidu.com/)等。其中加网提供了划词分享功能。

4. 社交网站

   可以发布简短的动态。比如Twitter, Facebook, Google Plus, 新浪微博等网站。与博客的联动可以是自己发布博客动态，
   也可以是由别人推荐（这种方式即为社会化推荐）。

   如果是自己发布动态，需要让别人能够方便的“关注/Follow”你，最好提供“一键关注的按钮”，或者提供连接能够让别人在这些网上方便的找到你。

5. 社会化登录

   没懂，感觉也就是OpenID或OAuth的集合。暂时不予考虑。





由于存在着伟大的墙，我只好尽量选择国内的社会化网络资源。对于更喜欢的国外的资源，尽量考虑如何不拖慢墙内用户的访问速度。

我对社会化网络资源的利用方式如下：

- 评论功能

  只选一个，我选择了[友言](http://www.uyan.cc/)。

- 推荐功能

  可以有多个，那么先加上友荐和无觅，Jekyll自带的相关文章功能也在测试中。

- 分享功能

  只选一个，还是选择[百度分享](http://share.baidu.com/)吧，与[百度统计](http://tongji.baidu.com/web/welcome/login)可以勾搭在一起，而且据说有利于百度的SEO。

## 流量分析和统计

第三方的流量分析和统计工具可以说是最古老的marshup，尽管没有社会化网络的功能。

可以选择的有国外的[Google Analysis](http://www.google.cn/intl/zh-CN_ALL/analytics/)、[SiteMeter](http://www.sitemeter.com)和国内的[百度统计](http://tongji.baidu.com/web/welcome/login)、
   [量子恒道统计](http://linezing.com)等。

出于种种无奈，还是选择了百度。




