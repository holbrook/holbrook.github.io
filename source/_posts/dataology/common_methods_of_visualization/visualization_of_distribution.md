---
title: 数据分布信息的可视化
date: 2018-03-05
postslug: visualization_of_distribution
categores: [数据分析]
tags: [数据可视化, seaborn]
---

数据可视化，是为了展示数据的内在特征，或者数据之间的关系。通常，数据探索最先的步骤就是观察特征数据的分布情况(distribution)。

对于连续变量，可以:

- 直接绘制1维散点图
- 绘制箱线图/提琴图，观察总体情况
- 观察直方图/密度曲线

对于分类变量，可以观察用条形/柱状图观察每个类别出现的次数/频度。

<!--more-->

{% asset_ipynb distribution.ipynb %}

# 参考资料

- [Seaborn(sns)官方文档学习笔记（第五章 分类数据的绘制）](https://zhuanlan.zhihu.com/p/27683042)