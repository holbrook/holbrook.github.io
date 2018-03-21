---
layout: post
title: "《统计学》读书笔记(8/17:列连表，x^2检验和对数线性模型)"
description: "统计学：从数据到结论，ISBN：9787503749964，作者：吴喜之"
category: 理论学习
tags: [统计学]
lastmod: 
---
# 列连表数据

列连表研究2个或以上的变量，每个变量的取值是离散的，取值的总数量称为该变量的“水平”。

列连表记录这些变量的各种取值组合出现的次数，以研究这些变量之间的相关性。

比如：

![sample-contingency-table](/images/2013/statistics_intro/sample-contingency-table.png)

上图记录了一个3x2x2的列连表，三个变量分别为收入（高、中、低）、观点（同意、反对）、性别（男，女）。

软件处理时通常将列连表处理成二维表格，比如：


![sample-contingency-table1](/images/2013/statistics_intro/sample-contingency-table1.png)

# 二维列连表的检验

比如以下的二维列连表：


![sample-contingency-table2](/images/2013/statistics_intro/sample-contingency-table2.png)

设定零假设和备选假设：

H0:观点和收入不相关<=>H1:相关

检验逻辑:

检验统计量在零假设下有（大样本时）近似的x<sup>2</sup>分布。

当该统计量很大时或p-值很小时，就可以拒绝零假设，认为两个变量相关。


x<sup>2</sup>检验量还可以使用Pearson x^2统计量和似然比（likelihood ratio) x<sup>2</sup> 统计量

(公式：略）

# 高维列联表和(多项分布)对数线性模型

高维列联表的检验和两维类似

但高维列联表可以构造一个(多项分布)对数线性模型(loglinear model)来进行分析。

好处：不仅可以直接进行预测，而且可以增加定量变量作为模型自变量的一部分。

## 对数线性模型

ln(m<sub>ij</sub>)= a<sub>i</sub> + b<sub>j</sub> + e<sub>ij</sub>

其中：

- a<sub>i</sub>： 行变量的第i个水平对ln(m<sub>ij</sub>)的影响
- b<sub>j</sub>：列变量的第j个水平对ln(m<sub>ij</sub>)的影响
- e<sub>ij</sub>: 随机误差。 

## （多项分布）对数线性模型


ln(m<sub>ij</sub>)= a<sub>i</sub> + b<sub>j</sub> + (ab)<sub>ij</sub> + e<sub>ij</sub>

增加了交叉效应(ab)<sub>ij</sub>，代表第一个变量的第i个水平和第二个变量的第j个水平对ln(m<sub>ij</sub>)的共同影响

# Poisson对数线性模型

很多事件符合Poisson分布，需要使用 Poisson对数线性模型进行分析。

ln(l) = u + a<sub>i</sub> + b<sub>j</sub> + gx

其中：

- u: 常数项

……


