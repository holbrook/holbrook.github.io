title: 利用Python进行数据分析(10)：时间序列
date: 2017-07-20
postslug: python_data_analysis10
category: 数据分析
tags: python

---



《[利用Python进行数据分析](https://book.douban.com/subject/25779298/)》读书笔记。
第 10 章：时间序列。

时间序列(time series)，是一种重要的结构化数据形式，在很多领域都有应用。

<!-- more -->

时间序列数据的形式主要有：

- 时间戳(timestamp), 特定的时刻数据，时点数据。
- 固定时期(period)，如2007年1月份， 2010年全年，阶段数据。
- 时间间隔(interval)，由起始和终止的时间戳表示。 period可以看做特殊的interval。
- 过程时间。 相对于特定起始时间的时间点。比如，从放入烤箱时起，每秒钟的饼干直径。
  过程时间可以用起始时间戳加上一系列整数（表示从起始时间开始经过的时间）来表示。

其中，最简单、最常见的时间序列是用时间戳进行索引。

pandas提供了一组标准的时间序列处理工具和算法，可以高效处理非常大的时间序列，进行
切片/切块，聚合，定期/不定期采样等操作。

这些数据对金融和经济数据尤为有用，也可以用于日志分析。



# 日期和时间数据类型及工具


{% asset_ipynb python_data_analysis10-1.ipynb %}


# 时间序列基础


{% asset_ipynb python_data_analysis10-2.ipynb %}


# 日期的范围、频率以及移动


{% asset_ipynb python_data_analysis10-3.ipynb %}



# 时区处理


{% asset_ipynb python_data_analysis10-4.ipynb %}



# 时期及其算数运算


{% asset_ipynb python_data_analysis10-5.ipynb %}



# 重采样及频率转换



{% asset_ipynb python_data_analysis10-6.ipynb %}


# 时间序列绘图


{% asset_ipynb python_data_analysis10-7.ipynb %}



# 移动窗口函数


{% asset_ipynb python_data_analysis10-8.ipynb %}



# 性能和内存使用方面的注意事项


{% asset_ipynb python_data_analysis10-9.ipynb %}





