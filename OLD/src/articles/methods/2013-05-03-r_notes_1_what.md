---
layout: post
title: "R学习笔记(1)：R是什么"
description: "从使用角度，R是一个有着统计分析功能及强大作图功能的软件，在GNU协议General Public Licence4下免费发行。
从编程角度，R语言是面向对象的统计编程语言，是由AT&T贝尔实验室所创的S语言发展出的一种方言。
从计算角度，R 是一种为统计计算和图形显示而设计的语言及环境。
从开发角度，R 是一组开源的数据操作，计算和图形显示工具的整合包有各种方式可以进行编程调用。
从架构角度，R 是为统计计算和图形展示而设计的一个系统。它包括一种编程语言，高级别图形展示函数，和其它语言的接口以及调试工具。"
category: 方法工具
tags: [R, 量化金融]
lastmod: 2013-06-11
---

![0](images/2013/r_notes/0.png)

在学习量化投资的时候，我发现了[R](http://www.r-project.org)。R到底是什么呢？在开始之前，先看看R的神奇之处。

# R初窥

从[CRAN（The Comprehensive R Archive Network）](http://cran.r-project.org—mirrors.html)
中选择一个镜像，然后下载合适的安装包（R支持Linux、Mac OS X和Windows）。
安装并运行R后，可以看到R的控制台（我的操作系统是Mac OS）：

![1](images/2013/r_notes/1.png)

在R的控制台输入如下命令：

{% highlight r %}
install.packages('quantmod') # 安装quantmod包
require(quantmod) #引用quantmod包
getSymbols("GOOG",src="yahoo",from="2013-01-01", to='2013-04-24') #从雅虎财经获取google的股票数据
chartSeries(GOOG,up.col='red',dn.col='green')  #显示K线图
addMACD() #增加MACD图
{% endhighlight %}

就能够看到下图的效果了：

![2](images/2013/r_notes/2.png)

最后，退出R：
{% highlight r %}
q()  # Terminate an R Session
{% endhighlight %}

# R是什么

是不是很神奇？反正当时我完全被Hold住了。

那么R到底是什么？或者说，R到底是做什么用的？从不同的角度出发，对R会有不同的描述。

- 从使用角度

  R是一个有着统计分析功能及强大作图功能的软件，在GNU协议General Public Licence4下免费发行。
- 从编程角度

  R语言是面向对象的统计编程语言，是由AT&T贝尔实验室所创的S语言发展出的一种方言。
- 从计算角度

  R 是一种为统计计算和图形显示而设计的语言及环境。
- 从开发角度

  R 是一组开源的数据操作，计算和图形显示工具的整合包有各种方式可以进行编程调用。
- 从架构角度

  R 是为统计计算和图形展示而设计的一个系统。它包括一种编程语言，高级别图形展示函数，和其它语言的接口以及调试工具。

如果一定要找到一个与R类似的软件，那就是商业软件Matlab。R和Matlab都是基于编程进行数据分析的工具，Matlab适用的领域更广，而R更擅长统计分析领域。

与Matlab相比，R更具备开放性：

- R是自由软件，Matlab是商业软件；
- R可以方便的通过“包”进行扩展，R的核心只有25个包，但是有几千个外部包可以调用，当然你也可以开发自己的；
- R语言比Matlab的要强大；
- R和其他编程语言/数据库之间有很好的接口；其他语言也可以很方便的调用R的API和结果对象。

R常用于金融和统计领域。大多数人使用R就是因为它的统计功能，R的内部实现了很多经典的or时髦的统计技术。

![3](images/2013/r_notes/3.png)

# R的核心概念

## 对象

R语言是一种面向对象的语言，所有的对象都有两个内在属性：元素类型和长度。

元素类型是对象内元素的基本类型，包括：数值(numeric),字符型(character),复数型(complex)、逻辑型（logical）、函数（function）等，通过mode()函数可以查看一个对象的类型。

长度是对象中元素的数目，通过函数length()可以查看对象的长度。

除了元素类型外，对象本身也有不同的“类型”，表示不同的数据结构（struct)。R中的对象类型主要包括：

- 向量(vector): 由一系列有序元素构成。
- 因子(factor）：对同长的其他向量元素进行分类（分组）的向量对象。R 同时提供有序（ordered）和无序（unordered）因子。
- 数组(array)：带有多个下标的类型相同的元素的集合
- 矩阵(matrix)：矩阵仅仅是一个双下标的数组。R提供了一下函数专门处理二维数组（矩阵）。
- 数据框(data frame)：和矩阵类似的一种结构。在数据框中，列可以是不同的对象。
- 时间序列(time series)：包含一些额外的属性,如频率和时间.
- 列表（list）:是一种泛化（general form）的向量。它没有要求所有元素是同一类型，许多时候就是向量和列表类型。列表为统计计算的结果返回提供了一种便利的方法。

## 常量

R中还定义了一些常量，比如：

- NA：表示不可用
- Inf: 无穷
- -Inf: 负无穷
- TRUE：真
- FALSE：假

# R的基本使用

## 命令

R是一种语法非常简单的表达式语言(expression language)。使用者通过命令（command）与R进行交互。

基本命令要么是表达式(expressions)要么就是赋值(assignments)。如果一条命令是表达式,那么它将会被解析(evaluate),并将结果显示在屏幕上,同时清空该命令所占内存。赋值同样会解析表达式并且把值传给变量但结果不会自动显示在屏幕上。

基于命令，可以用交互的方式或者批处理/脚本文件的方式使用R。

## 交互式使用 R

交互式shell是一种很方便的环境，可以进行各种尝试，随时调整过程。与Python、Ruby等语言一样，R也提供了shell环境。本文开始的例子就是以交互的方式使用R。当打开R控制台时，R会显示命令提示符">"，此时可以输入命令。
下面是交互式使用R的几个例子：

例一：

{% highlight r %}

help.start() #启动在线帮助，会打开浏览器。
x <- rnorm(50); y <- rnorm(x)  #产生两个随机向量x和y
plot(x,y) #使用x,y画二维散点图, 会打开一个图形窗口
ls() #查看当前工作空间里面的 R 对象
rm(x,y) #清除x,y对象
x <- 1:20  # 相当于x=(1,2,…,20)

{% endhighlight %}


例二：

{% highlight r %}

x <- 1:20#等价于 x = (1, 2, ..., 20)。
w <- 1 + sqrt(x)/2#标准差的`权重'向量。
dummy <- data.frame(x=x, y= x + rnorm(x)*w)#创建一个由x 和 y构成的双列数据框
dummy #查看dummy对象中的数据。
fm <- lm(y ~ x, data=dummy)#拟合 y 对 x 的简单线性回归
summary(fm)#查看分析结果。
fm1 <- lm(y ~ x, data=dummy, weight=1/w^2)#加权回归
summary(fm1)#查看分析结果。

attach(dummy)#让数据框中的列项可以像一般的变量那样使用。
lrf <- lowess(x, y)#做一个非参局部回归。
plot(x, y)#标准散点图。
lines(x, lrf$y)#增加局部回归曲线。
abline(0, 1, lty=3)#真正的回归曲线：(截距 0，斜率 1)。
abline(coef(fm))#无权重回归曲线。
abline(coef(fm1), col = "red")#加权回归曲线。

detach()#将数据框从搜索路径中去除。

plot(fitted(fm), resid(fm),
     xlab="Fitted values",
     ylab="Residuals",
     main="Residuals vs Fitted")  #显示一个检验异方差性（heteroscedasticity）的标准回归诊断图。

qqnorm(resid(fm), main="Residuals Rankit Plot")#用正态分值图检验数据的偏度（skewness），峰度（kurtosis）和异常值（outlier）。

rm(fm, fm1, lrf, x, dummy)#再次清空。
{% endhighlight %}

例三： Michaelson 和 Morley 测量光速的经典实验

{% highlight r %}

filepath <- system.file("data", "morley.tab" , package="datasets")#从对象 morley 中得到实验数据的文件路径
filepath#查看文件路径
file.show(filepath)#查看文件内容
mm <- read.table(filepath)#以数据框的形式读取数据
mm$Expt <- factor(mm$Expt)
mm$Run <- factor(mm$Run)#将 Expt 和 Run 改为因子。
attach(mm)#让数据在位置 3 (默认) 可见（即可以直接访问）。
plot(Expt, Speed, main="Speed of Light Data", xlab="Experiment No.")#用简单的盒状图比较五次实验。
fm <- aov(Speed ~ Run + Expt, data=mm)#分析随机区组，`runs' 和 `experiments' 作为因子。
summary(fm)

fm0 <- update(fm, . ~ . - Run)
anova(fm0, fm)#拟合忽略 `runs' 的子模型，并且对模型更改前后进行方差分析。
detach()
rm(fm, fm0)#在进行下面工作前，清空数据。

#下面是等高线和影像显示的示例
x <- seq(-pi, pi, len=50)#x 是一个在区间 [-pi\, pi] 内等间距的50个元素的向量
y <- x
f <- outer(x, y, function(x, y) cos(y)/(1 + x^2))#f 是一个方阵，行列分别被 x 和 y 索引，对应的值是函数 cos(y)/(1 + x^2) 的结果。
oldpar <- par(no.readonly = TRUE)
par(pty="s")#保存图形参数，设定图形区域为“正方形”。
contour(x, y, f)
contour(x, y, f, nlevels=15, add=TRUE)#绘制 f 的等高线；增加一些曲线显示细节。
fa <- (f-t(f))/2#fa 是 f 的“非对称部分”(t() 是转置函数)。
contour(x, y, fa, nlevels=15)#画等高线
par(oldpar)# 恢复原始的图形参数
image(x, y, f)
image(x, y, fa)#绘制一些高密度的影像显示
objects();
rm(x, y, f, fa)#在继续下一步前，清空数据。

th <- seq(-pi, pi, len=100)
z <- exp(1i*th)#1i 表示复数 i

par(pty="s")
plot(z, type="l")#图形参数是复数时，表示虚部对实部画图。这可能是一个圆。
w <- rnorm(100) + rnorm(100)*1i#假定我们想在这个圆里面随机抽样。一种方法将让复数的虚部和实部值是标准正态随机数 ...
w <- ifelse(Mod(w) > 1, 1/w, w)#将圆外的点映射成它们的倒数。
plot(w, xlim=c(-1,1), ylim=c(-1,1), pch="+",xlab="x", ylab="y")
lines(z)#所有的点都在圆中，但分布不是均匀的。

#下面采用均匀分布。现在圆盘中的点看上去均匀多了。
w <- sqrt(runif(100))*exp(2*pi*runif(100)*1i)
plot(w, xlim=c(-1,1), ylim=c(-1,1), pch="+", xlab="x", ylab="y")
lines(z)

rm(th, w, z)#再次清空。
q()#离开 R 程序

{% endhighlight %}


## 工作空间(workspace)

R shell 可以任意地保存一个完整的环境,称为工作空间（workspace)。前面的例子中，运行q()命令退出R时，会被询问是否要保存工作空间：

![4](images/2013/r_notes/4.png)

工作空间（workspace)保存了一些环境信息。每次与R的会话(session)可以从一个全新的环境开始，也可以在原来的基础上继续，这些运行信息就保存在工作空间中。
如果在UNIX系统以命令行的方式启动R，则当前目录就是本次会话的工作空间：

{% highlight bash %}
mkdir r_test
cd r_test/
R
{% endhighlight %}

看看R能为工作空间保存些什么内容：

{% highlight r %}
> x <- rnorm(50); y <- rnorm(x)  #产生两个随机向量x和y
> q()
Save workspace image? [y/n/c]: y
{% endhighlight %}

如果运行`ls -Al`，会发现R保存了两个隐藏文件：.RData和.Rhistory。
其中RData以二进制的方式保存了会话中的变量值，Rhistory以文本文件的方式保存了会话中的所有命令。

如果在一个已有的工作空间中启动R，会提示：
`原来保存的工作空间已还原`

此时可以用函数`ls()`和`history()`看到之前保存的数据和命令。
使用`rm()`或`remove()`可以删除工作空间中的变量。

在R控制台，也可以使用函数getwd()和setwd()来获取/设置工作空间目录；使用list.files()查看当前目录下的文件。

如果以GUI方式运行R控制台，可以通过菜单来加载或保存工作空间。

## 脚本/批处理

前面提到R可以在工作空间中保存历史命令。其实这就是一个工作空间中的默认脚本，当加载工作空间时自动执行。

我们完全可以写自己的脚本，指定R批量执行一些命令。通常，自己的脚本会以“.R”作为扩展名。一个最简单的例子test.R：

{% highlight r %}
x <- rnorm(50); y <- rnorm(x)  #产生两个随机向量x和y
plot(x,y) #使用x,y画二维散点图, 会打开一个图形窗口
{% endhighlight %}

并保存到工作空间，然后在R控制台，使用命令`source('test.R')`就可以执行该脚本，
还可以使用`source('test.R', echo=TRUE)`输出更详细的信息。

编写脚本自动执行一些任务时，sink()函数会比较有用。
`sink("record.lis")`会把所有后续的输出结果从控制台重定向到外部文件 record.lis 中，此时控制台中看不到命令输出的结果。
使用命令`sink()`可以让输出流重新定向到控制台。

# 帮助系统

GNU软件通常都会有非常好的帮助系统，无论对于初学者还是熟练者都能带来很大的帮助。R当然也不例外。R中提供的帮助主要有以下几种：

## 文档和搜索

`help.start()` 命令会打开浏览器，显示帮助文档。包括一些入门的文档，以及[搜索功能](http://127.0.0.1:18099/doc/html/Search.html)。

![5](images/2013/r_notes/5.png)

## 演示

`demo()`会按照包分组，列出所有可用的演示：

![6](images/2013/r_notes/6.png)

按照名称可以开始演示，比如`demo(is.things)`

## 函数帮助

如果已经知道一个函数的名称(比如solve)，需要了解其所属的包、用途、用法、参数说明、返回值、参考文献、相关函数以及范例等，可以使用命令
`help(solve)`或`?solve`。该命令会弹出一个窗口：

![7](images/2013/r_notes/7.png)

## 函数示例

对于函数，还可以使用example()执行示例，比如`example(solve)`。

## 关键字和运算符

与函数的帮助类似，但是需要加上引号，如：

{% highlight r %}
? '[['   # 等价于 help('[[')
?'+'    #等价于 help('+')
?'if'    #等价于 help('if')
{% endhighlight %}

## 搜索

如果不知道函数名称，还可以进行搜索，比如：

{% highlight r %}
??'analysis'  #等价于 search('analysis')
{% endhighlight %}

## 官方搜索

前面的帮助都受限于本地环境已经安装的包。如果要搜索R中所有的资源（包，函数、数学方法等），需要在R的官方网站搜索：

[www.r-project.org—search.html](http://www.r-project.org—search.html)

# 学习资料

- [R官方网站](http://www.R-project.org)
- [官方网站上的一些手册和文档（必看）](http://cran.r-project.org—manuals.html)
- [华盛顿大学的一个R教程](http://staff.washington.edu—Rcourse)
- [下一篇：R学习笔记(2)：R中的数据类型和数据结构](http://thinkinside.tk/2013/05/09/r_notes_2_data_structure.html)
