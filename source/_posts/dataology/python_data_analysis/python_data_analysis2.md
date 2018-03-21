title: 利用Python进行数据分析(2)：引言
date: 2017-02-14
postslug: python_data_analysis2
category: 数据分析
tags: python

---

《[利用Python进行数据分析](https://book.douban.com/subject/25779298/)》读书笔记。
第 2 章：引言
介绍数据分析的一般步骤，并用三个实例说明如何用 python 进行数据分析。

<!-- more -->

所有用到的数据可以从[作者的 github](https://github.com/wesm/pydata-book)下载。

# 数据分析的一般步骤

- 数据加载

   从各种格式的数据文件和数据库加载数据

- 数据准备

   对数据进行清理、修整、整合、规范化、重塑、切片切块、变形等处理，以便于进行分析


- 数据转换

  对数据集进行数学和统计运算，产生新的数据集。比如，根据分组变量对一个大表进行聚合


- 建模和计算

  通过统计模型、机器学习算法和其他计算工具，对数据进行分析计算


- 结果展示

  通过静态或交互式的方式，展示结果


# 例子：分析网站的用户访问数据

{% asset_ipynb python_data_analysis2-1.ipynb %}


# 例子：电影评分数据分析

{% asset_ipynb python_data_analysis2-2.ipynb %}


# 例子：全美婴儿姓名分析

{% asset_ipynb python_data_analysis2-3.ipynb %}


