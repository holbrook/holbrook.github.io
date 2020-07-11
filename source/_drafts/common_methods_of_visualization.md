---
title: 数据可视化的一般方式
date: 2018-03-05
postslug: common_methods_of_visualization
categores: [数据分析]
tags: [数据可视化, seaborn]
---

数据可视化，是为了展示数据的内在特征，或者数据之间的关系。
按照要展示的信息，可以分为：

- 分布(distribution)
  对于连续变量，可以:

  - 直接绘制1维散点图
  - 绘制箱线图/提琴图，观察总体情况
  - 观察直方图/密度曲线

  对于分类变量，可以观察用条形/柱状图观察每个类别出现的次数/频度。


- 比较(Comparison)

- 关系(relationship)




## Profiling

:  pattern comparison.



如果结合数据的维度数，可以整理为下表：





多变量分析
多元分析才是真正有意思并且有复杂性的领域。这里我们分析多个数据维度或属性（2 个或更多）。多变量分析不仅包括检查分布，还包括这些属性之间的潜在关系、模式和相关性。你也可以根据需要解决的问题，利用推断统计（inferential statistics）和假设检验，检查不同属性、群体等的统计显著性（significance）。



将 2 维数据可视化非常简单直接，但是随着维数（属性）数量的增加，数据开始变得复杂。原因是因为我们受到显示媒介和环境的双重约束。

对于 3 维数据，可以通过在图表中采用 z 轴或利用子图和分面来引入深度的虚拟坐标。

但是，对于 3 维以上的数据来说，更难以直观地表征。高于 3 维的最好方法是使用图分面、颜色、形状、大小、深度等等。你还可以使用时间作为维度，为随时间变化的属性制作一段动画（这里时间是数据中的维度）。看看 Hans Roslin 的精彩演讲就会获得相同的想法！


可以使用的元素：

- 两个坐标轴
- 深度、色调、大小
- 子图
- z轴
- 形状


# 2维数据可视化

1维数据可视化用于分析单变量。
从2维数据可视化开始，分析的是多个变量之间的关系。

- 检查不同数据属性之间的潜在关系或相关性的最佳方法之一是利用配对相关性矩阵（pair-wise correlation matrix）并将其可视化为热力图。

- 另一种识别相关关系的方法是配对散点图

- 平行坐标图：点被表征为连接的线段。每条垂直线代表一个数据属性。所有属性中的一组完整的连接线段表征一个数据点。因此，趋于同一类的点将会更加接近。

- 联合分布图，适合可视化两个连续型数值属性，可以观察相关性、关系以及分布。
- 分类条形图，分析两个分类变量
- 多维直方图/kde分布图，分析一个连续属性基于多个类别的分布
- 箱体图
- 小提琴图，使用核密度图显示各类别的概率密度


{% asset_ipynb 2D_visualize.ipynb %}


# 3维

分类散点图，绘制两个属性的散点图，并用颜色标记类别
sns.FacetGrid(df, hue="target", size=5).map(plt.scatter, "sepal_length", "sepal_width").add_legend()

# 小结




- 可视化目标


- 数据维度

  + 1维
  * 特征变量: 直方图(histogram), 密度曲线(KDE)
  * 分类变量: 柱状图(bar chart), 饼图(pie chart)。当类别多时慎用饼图

+ 2维数据
  * 识别相关性: 热力图(heatmap), 配对散点图, 平行坐标图, 联合分布图，分类散点图
  * 分类变量+分类变量：条形图
  * 分类变量+特征变量：多维直方图/kde分布图，箱体图，小提琴图

+ 3维数据
  * 1维分类+2维特征：多维散点图


- 图表的类型
  + 散点图(Scatter)
    * 1维散点图(1D Scatter)
  + 直方图(Histogram)


a) Histogram: It is used for showing the distribution of continuous variables. One of the catch with histogram is ‘number of bins’. Let’s understand it in detail using example below:-



Both histograms are showing different distribution of a given set of data which represents age distribution using Count of Passengers vs Age. Look at the histogram at right .We can infer that there are more infants in age group of 0-4 years compared to age group of 4-16 years. However, if you try to make this inference from left graph, I’m sure you would fail to do so. Hence, we should be very careful while selecting number of bins.


## 箱线图/小提琴图
(Box Plot/Violin Plot)

b) Box-Plot: It is used to display full range of variation from min to max and useful to identify outlier values. It shows Min, Q1, Median, Q3 and Max. Any value outside the lower and upper inferences is considered as an Outlier. Formula for calculating lower and Upper inferences are:-

Upper Inference = Q3 + 1.5 * (Q3-Q1), (Q3-Q1) (also known as IQR)

Lower Inference = Q1 – 1.5 * (Q3-Q1)

Box_Plot



We can also visualize distribution between  two continuous variables or one categorical and one continuous variable using scatter plot or multiple box plots by different categories of categorical variables respectively.


## 条形图/柱状图

(Bars/Columns)



## 图表组合和维度

颜色，大小，形状

多组箱线图


# 参考资料

- [5种快速易用的Python Matplotlib数据可视化方法](http://mp.weixin.qq.com/s/LBrlXEhGYOx1aPFZzQcyTQ)
- [从1维到6维，一文读懂多维数据可视化策略](http://mp.weixin.qq.com/s/mD732PqDtqYdFZSxZWtvvg)
- [A classification of chart types](https://excelcharts.com/classification-chart-types/)
- [Ultimate resource for understanding & creating data visualization](https://www.analyticsvidhya.com/blog/2015/05/data-visualization-resource/)


http://blog.csdn.net/weiyudang11/article/details/51549672

https://zhuanlan.zhihu.com/p/27570774
Seaborn(sns)官方文档学习笔记（第一章 艺术化的图表控制） - 知乎专栏

Seaborn(sns)官方文档学习笔记（第二章 斑驳陆离的调色板） - 知乎专栏

Seaborn(sns)官方文档学习笔记（第三章 分布数据集的可视化） - 知乎专栏

Seaborn(sns)官方文档学习笔记（第四章 线性关系的可视化） - 知乎专栏

Seaborn(sns)官方文档学习笔记（第五章 分类数据的绘制） - 知乎专栏

Seaborn(sns)官方文档学习笔记（第六章 绘制数据网格） - 知乎专栏

https://seaborn.pydata.org/tutorial/axis_grids.html#plotting-pairwise-relationships-in-a-dataset



# ref

## What are the common methods of visualization?


{% asset_img Chart_Selection.jpeg %}









Advance Visualization Methods


Till here, we looked at most common methods used to visualize information. Let’s look at some advance methods of visualization. These methods extend the power of storytelling using visualization methods.

a) Heat Map: It uses colors to represent numbers in a spreadsheet or in any other visualization methods like Scatter, Geo-spatial, Area Chart. You can set different color gradient for the lowest, highest and mid-range values, with a corresponding transition (or gradient) between these extremes.

It represents one more variable to existing visualization method and adds additional information about data values.

Heat_Map




c) Grid: It is used in 2D tabular format. In this method, we use two metrics horizontally and vertically. Then, plot a grid against each category of both metrics. After that, use colors to represent the data.

Let’s understand it using an example:

Grid

In above grid, you can represent the skill of a professional across various tools and techniques. In here, Green color represents the expert, Amber to intermediate and Red as beginner. Here we have efficiently represent this information without much hassle.

d) WordCloud: A word cloud is a method to represent text data. It is also known as text or tag cloud. It is a graphical representation of frequently used words in a collection of text files. The height and font style of each word in this picture is an indication of frequency of occurrence of the word in the entire text data. Such diagrams are very useful in working on text analytics.

It is just like any infographic. It makes an impact, easy to understand and can be shared easily. Make a note, before using word cloud, only focus on frequency of word and not on importance of variable.

Word_Coud_1

There is more advance visualization techniques like Venn-diagram, Network Map, Radar Chart and other custom visualization methods to represent data and generate more meaningful insight from them.



## choose of chart

http://labs.juiceanalytics.com/chartchooser/index.html


