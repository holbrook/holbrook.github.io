title: 利用Python进行数据分析(11)：金融和经济数据应用
date: 2017-07-24
postslug: python_data_analysis11
category: 数据分析
tags: python

---

《[利用Python进行数据分析](https://book.douban.com/subject/25779298/)》读书笔记。
第 11 章：金融和经济数据应用



自2005年开始，python在金融行业中的应用越来越多。

这主要得益于越来越成熟的函数库（NumPy和pandas）以及大量经验丰富的程序员。

许多机构发现python不仅非常适合成为交互式的分析环境，也非常适合开发文件的系统，所需的时间也比Java或C++少得多。

Python还是一种非常好的粘合层，可以非常轻松为C或C++编写的库构建Python接口。

金融分析领域的内容博大精深。在数据规整化方面所花费的精力常常会比解决核心建模和研究问题所花费的时间多得多。

在本章中，术语截面（cross-section）来表示某个时间点的数据。

例如标普500指数中所有成份股在特定日期的收盘价就形成了一个截面。

多个数据在多个时间点的截面数据就构成了一个面板（panel）。

面板数据既可以表示为层次化索引的DataFrame，也可以表示为三维的Panel pandas对象。

<!-- more -->

# 数据规整化方面的话题


{% asset_ipynb python_data_analysis11-1.ipynb %}

# 分组变换和分析


{% asset_ipynb python_data_analysis11-2.ipynb %}


# 更多示例应用


{% asset_ipynb python_data_analysis11-3.ipynb %}




