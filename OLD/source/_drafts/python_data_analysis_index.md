title: 《利用Python进行数据分析》小结
date:
category: 数据分析
slug: python_for_data_analysis_index
tags: 读书笔记, python]
---

《[利用Python进行数据分析](https://book.douban.com/subject/25779298/)》读书笔记的总结。

<!-- more -->

《利用Python进行数据分析(Python for　Data Analysis)》，这本书的作者 Wes McKinney 就是 pandas 的作者。

从书中的内容可以分析出来，作者应该是用 Matlab 和 R 比较不爽，又觉得 NumPy 的功能比较有限，
所以开发了 pandas (Python Data Analysis Library)。

顾名思义，pandas 提供了用python进行数据分析的工具集。作者认为，[数据分析的一般步骤包括](/2017/02/14/python_data_analysis2.html)：

- 数据加载：从各种格式的数据文件和数据库加载数据
- 数据准备: 对数据进行清理、修整、整合、规范化、重塑、切片切块、变形等处理，以便于进行分析
- 数据转换：对数据集进行数学和统计运算，产生新的数据集。比如，根据分组变量对一个大表进行聚合
- 建模和计算：通过统计模型、机器学习算法和其他计算工具，对数据进行分析计算
- 结果展示：通过静态或交互式的方式，展示结果

熟悉数据仓库的朋友可能发现，其中前三个步骤类似于传统的ETL(Extract-Transform-Load， 抽取-转换-加载)，后两个步骤类似于数据挖掘和BI。

数据分析的一般步骤
数据加载
从各种格式的数据文件和数据库加载数据

数据准备
对数据进行清理、修整、整合、规范化、重塑、切片切块、变形等处理，以便于进行分析

数据转换
对数据集进行数学和统计运算，产生新的数据集。比如，根据分组变量对一个大表进行聚合

建模和计算
通过统计模型、机器学习算法和其他计算工具，对数据进行分析计算

结果展示
通过静态或交互式的方式，展示结果



从 Pandas本身来说，
NumPy定义了数组ndarray, 而Pandas定义了Series, DataFrame和 Panel。其中：

Series = Index + ndarray ，带索引的数组
DataFrame = Index + N * Series, 一组具有相同索引的Series
Panel = ?

围绕DataFrame，pandas的主要知识点包括：

# 构建DataFrame

1. 将数据加载到 DataFrame

# 操作索引

# 操作列

# 操作行

## 广播

# 操作数据

2. 通过 pandas 提供的方法对数据进行处理

3. 通过 pandas 提供的方法对数据进行转换


## 对DataFrame中的数据建模和计算

	pandas, 一些简单的方法
	satms.
	scik -learn
	transflow?


## 绘图

pandas中简单的展示
   更复杂的：








NumPy(Numerical Python) 提供了大量的数值编程工具，
[可以方便地处理向量、线性代数、矩阵等运算，并支持一些数学和统计方法](/2017/02/17/python_data_analysis4.html)。
NumPy 也是 pandas 的重要基础。

此外，作者还介绍了[NumPy的高级应用](#)。
