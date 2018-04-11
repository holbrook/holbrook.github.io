---
title: 数据演变信息的可视化
postslug: visualization_of_evolution
categores: [数据分析]
tags: [数据可视化, seaborn]
date: 2018-04-11
---

数据演变信息(evolution)的可视化，是为了观察同一特征变量在不同时间的值。

# 数据准备

# 时点数据与折线图(Line Chart)

## 一个特征变量的折线图

如果只有一个随时间变化的特征变量，最直观的方式，是以时间作为横坐标，绘制折线图。又可以分为：

- 数据点按时间均匀分布

  比如股票的分时图

- 数据点的时间分布不均匀

  如Tick图，又叫阶梯图（step chart)

## 多个特征变量的折线图

如果有很多个特征变量，可以在一张这些图上绘制多个线段来表示

## 变体：地平线图( Horizon Chart)

https://docs.splunk.com/Documentation/HorizonChart/1.1.0/HorizonChartViz/HorizonChartIntro

# 时段数据与柱状 图 / 条形图(Column Chart/ Bar Chart)

## 单个特征变量的柱状图

如，每日成交量



## 多个特征变量的柱状图

如

### 堆叠柱状图(Stacked bar chart)

如果多个特征变量是某一个总量的组成部分，可以绘制堆叠柱状图

### 变体： Candle Stick


# 两个特征变量的连接散点图(  connected scatterplot)

如果要表示两个特征变量随时间的变化，但又不关注具体的时间间隔，只是关注变化趋势，可以。。。

如：申万的大小盘。。。四个象限


# 循环时间周期与循环面积图(  Circular Area Chart )



# 时间

  + Line chart
  + Bar chart
  + Stacked bar chart
  + Bullet bar chart
  + Column chart
  + Bubble chart
  + Alternating rows table
  + Groupings table
  + Quartiles table


## 趋势(trend)


- trend
  + Line chart
  + Column chart
  + Stacked column chart
  + Stacked column volume chart
  + Stacked column volume with total chart
  + Two axis column line chart
