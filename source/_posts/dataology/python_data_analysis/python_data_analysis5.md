title: 利用Python进行数据分析(5)：Pandas 入门
date: 2017-02-23
postslug: python_data_analysis5
category: 数据分析
tags: python

---

NumPy虽然提供了方便的数组处理功能，但是它还是缺少许多数据处理、分析所需的一些快速工具。
Pandas基于NumPy构建，提供众多更高级的数据处理功能，使得以 NumPy 为中心的数据处理工作更便捷。

<!-- more -->

pandas的作者在设计 Pandas 时，主要考虑以下几个方面：

- 按轴自动或显式数据对齐功能的数据结构

  来自不同数据源的数据，由于各数据源的索引方式不同，经常会出现数据未对齐，而这会导致很多常见错误。

- 集成时间序列功能
- 既能处理时间序列数据也能处理非时间序列数据的数据结构
- 数学运算和简约（比如对某个轴求和）可以根据不同的元数据（轴编号）执行
- 灵活处理缺失数据
- 合并及其他出现在常见数据库（例如基于SQL的）中的关系型运算

引入 Pandas 的约定为：

```
from pandas import Series, DataFrame
import pandas as pd
```

本章内容较多，每节的内容拆分成一个 ipython notebook:

# 数据结构

 Pandas中两个主要的数据结构是 Series 和 DataFrame，两个数据结构中都使用了索引(Index)对象。

{% asset_ipynb python_data_analysis5-1.ipynb %}

# 基本功能

{% asset_ipynb python_data_analysis5-2.ipynb %}

# 汇总和描述性统计

{% asset_ipynb python_data_analysis5-3.ipynb %}


# 处理缺失数据

{% asset_ipynb python_data_analysis5-4.ipynb %}

# 层次化索引

{% asset_ipynb python_data_analysis5-5.ipynb %}

# 其他


{% asset_ipynb python_data_analysis5-6.ipynb %}

