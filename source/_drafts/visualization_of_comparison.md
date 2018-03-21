---
title: 数据比较信息的可视化
date: 2018-03-05
postslug: visualization_of_comparison
categores: [数据分析]
tags: [数据可视化, seaborn]
---


数据进行比较，首先要有可比性。一般来说有两种情况：

- 在不同类别上对特征变量进行比较(Comparison)
- 分析特征变量随着时间的演变（Evolution）

本文讨论特征比较(Comparison)信息的可视化。

<!--more-->

在 [分布信息的可视化]()中，已经涉及了比较。




# 特征比较





- Comparison
  + Line chart
  + Bar chart
  + Stacked bar chart
  + Bullet bar chart
  + Column chart
  + Bubble chart
  + Alternating rows table
  + Groupings table
  + Quartiles table



2 ) Comparison
It is used to compare values across different categories and over time (trend).

Common charts to represent these information are Bar and Line chart. Please note: When we compare values across different categories we should go with Bar chart. If it is over quantitative variable, we should go with line chart.

Comparison across various categories

Comparison_1

Comparison across quantitative variable

Comparison_2

We can also compare multiple metrics using bar chart across different categories using stacked bar charts.

crosstab_class_sex

If there are multiple categories, it is a good practice to segregate categories in different groups and then compare accordingly. Decision Tree is one of the useful visualization technique to explore data values as shown below.



Test



## 地理信息图

b) GeoSpatial charts: Data scientists started plotting variables on geographical address to help organisations in making their strategies differently for different cluster based on the spread of data. Here we can also use color index or size as a metric to represent more variables. It is similar to scatter plot. The only difference here is we are plotting data points on map.

Advantages of using Geo-Spatial Visualization are:

We can easily understand the distribution of organizations presence across the map.
Easy to represent high number of locations compare to tabular or graphical representation
More intuitive decision-making for the business owner
Geo

Above, you can see that how easily we are able to present information on map compare to tabular and Bar Charts.
