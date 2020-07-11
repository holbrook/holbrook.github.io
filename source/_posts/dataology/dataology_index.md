---
title: 数据科学的知识体系
postslug: dataology_index
date: 2017-02-05
category: 数据分析
tags: 数据分析
---

数据科学是利用计算机的运算能力对数据进行处理，从数据中提取信息，进而形成“知识”。
然而要实现这一点并不容易。Swami Chandrasekaran在他的[《Becoming a Data Scientist》](http://nirvacana.com/thoughts/becoming-a-data-scientist/)中，规划了“数据科学家”之路，让我们共勉。

<!-- more -->


先上图：

{% asset_img long-road-to-data-scientist.png MetroMap to Data Scientist %}


# 基本原理(Fundamentals)

## 矩阵和线性代数(Matrices & Linear Algebra)

## 数据存储和处理

- 哈希函数，二叉树，时间复杂度(Hash Functions,Binary Tree,O(n))
- 关系代数和数据库基础(Relational Algebra,DB Basic)
- 内连接、外连接、交叉连接、θ连接(Inner、Outer、Cross、Theta Join)
- CAP定理（CAP Theorem）
- 列表数据(tabular data)
- 数据框和序列(DataFrames & Series)
- 分片(Sharding)
- 联机分析处理（OLAP, Online Analytical Processing）
- 多维数据模型(Multidimensional Data Model)
- ETL
- 报表，商业智能与分析(Reporting vs BI vs Analytics)
- JSON & XML
- NoSQL
- 正则表达式（Regex, Regular Expression）
- 业务背景知识(Vendor Landscape)
- 安装环境(Env Setup)

# 统计学(Statistics)

- 获取数据(Pick a Dataset)

  UCI Repo: UCI数据库。是加州大学欧文分校(University of CaliforniaIrvine)
  提出的用于机器学习的数据库，有大量的数据集。

- 描述性统计Descriptive Statistics

  均值，中位数，极差，标准差，方差(（mean, median, range, SD, Var）

- 探索性数据分析(Exploratory Data Analysis)

  + 直方图(Histograms)
  + 百分位数和极值(Percentiles & Outliers)

- 概率论(Probability Theory)
- 贝叶斯定理(Bayes Theorem)
- 随机变量(Random Variables)
- 累计分布函数（CDF, Cumulative Distribution Function)
- 连续分布(Continuos Distributions)

  正态分布、泊松分布、高斯分布(Normal, Poisson, Gaussian)

- 偏度(Skewness)
- 方差分析(ANOVA)
- 概率密度函数(PDF,Prob Den Fn)
- 中心极限定理(Central Limit THeorem)
- 蒙特卡罗方法(Monte Carlo Method)
- 假设检验(Hypothesis Testing)
- P值(p-Value)
- 卡方检验(Chi2 Test)
- 估计(Estimation)
- 置信区间(CI,Confid Int)
- 极大似然估计(MLE)
- 核密度估计(Kernel Density Estimate)
- 回归(Regression)
- 协方差(Convariance)
- 相关性(Correlation)
- 皮尔逊相关系数(Pearson Coeff)
- 因果性(Causation)
- 最小二乘法(Least2 fit)
- 欧氏距离(Eculidean Distance)


# 编程(Programming)

- python基础(Python Basics)
- R
- Excel
- 数据结构
  Swami Chandrasekaran 给出的是 R 中的数据结构，但可以映射到python中。

  + 变量(Varibles)
  + 向量(Vectors)
  + 矩阵(Matrices)
  + 数组(Arrays)
  + 因子(Factors)
  + 列表(Lists)
  + 数据框(Data Frames)


# 机器学习(Machine Learning)

- 机器学习与数据挖掘的区别(What is ML?)
- 数值变量(Numerical Var)
- 分类变量(Categorical Var)
- 监督学习(Supervised Learning)
- 无监督学习(Unsupervied Learning)
- 概念、输入和特征(Concepts, Inputs & Attributes)
- 训练集和测试集(Traning & Test Data)
- 分类器(Classifier)
- 预测(Prediction)
- Lift曲线
- 过拟合(Overfitting)
- 偏差和方差(Bias & Variance)
- 树分类(Trees & Classification)
- 分类问题(Classification)

  + 分类正确率(Classification Rate)
  + 决策树(Decision Trees)
  + 提升方法(Boosting)
  + 朴素贝叶斯分类(Naive Bayes Classifiers)
  + K近邻分类(K-Nearest Neighbour)

- 回归问题(Regression)

  + 逻辑回归(Logistic Regression)
  + 排序(Ranking)
  + 线性回归(Linear Regression)
  + 感知机(Perceptron)

- 聚类问题(Clustering)

  + 层次聚类(Hierarchical Clustering)
  + K聚类(K-means Clusterning)

- 神经网络(Neural Networks)
- 情感分析(Sentiment Analysis)
- 协同过滤(Collaborative Fitering)
- 标签(Tagging)

# 文本挖掘/自然语言处理(Text Mining / NLP)
- 语料库(Corpus)
- 命名实体识别(Named Entity Recognition)
- 文本分析(Text Analysis)
- UIMA
- 词-文档矩阵(Term Document Matrix)
- 词频和权重(Term Frequency & Weight)
- 支持向量机(Support Vector Machines)
- 关联规则(Association Rules)
- 购物篮分析(Market Basket Analysis)
- 特征提取(Feature Extraction)
- 工具箱
  + Mahout
  + Weka
  + NLTK
- 文本分类(Classify Text)
- 词汇映射(Vocabulary Mapping)


# 数据可视化

- 单变量、双变量和多变量可视化(Uni, Bi & Multivariate Viz)
- ggplot2(R中的一个可视化包，python中使用pyplotlib)
- 直方图和饼图（单变量）(Histogram & Pie(Uni))
- 树图和矩形树图(Tree & Tree Map)
- 散点图（双变量）(Scatter Plot (Bi))
- 折线图（双变量）(Line Charts (Bi))
- 空间图(Spatial Charts)
- Survey Plot
- 时间轴(Timeline)
- 决策树(Decision Tree)
- D3.js(知名的数据可视化前端框架)
- IBM ManyEyes(IBM的一款在线可视化处理工具)
- Tableau(国外知名的商用BI)



# 大数据(Big Data)

- MapReduce框架(Map Reduce Fundamentals)
- Hadoop组件(Hadoop Components)
- HDFS(Hadoop分布式文件系统,Hadoop Distributed FilesSystem）
- 数据复制原理(Data Replication Principles)
- 名称和数据节点(Name & Data Nodes)
- 任务跟踪(Job & Task Tracker)
- Map/Reduce编程(M/R Programming)
- Sqoop工具: Loading Data in HDFS
- Flue, Scribe: 处理非结构化数据
- 利用Pig语言进行SQL操作(SQL with Pig)
- 利用Hive来实现数据仓库(DWH with Hive)
- Scribe, Chukwa For Weblog(日志收集器和数据收集器)
- 使用Mahout
- Zookeeper 和 Avro
- Storm: Hadoop Realtime
- Rhadoop, RHipe, SparkR ： 将R和hadoop结合起来的架构
- rmr: RHadoop的一个包，和hadoop的MapReduce相关
- NoSql数据库
  + Classandra
  + MongoDB
  + Neo4j

# 数据摄取(ingestion)

- 数据格式概要(Summary of Data Formats)
- 数据发现(Data Discovery)
- 数据来源与采集(Data Sources & Acquisition)
- 数据集成(Data Integration)
- 数据融合(Data Fusion)
- 转换和浓缩(Transformation & Enrichament)
- 数据调查(Data Survey)
- Google OpenRefine: Google发布的开源的数据处理软件
- 数据量级(How much Data)
- ETL


# 数据清洗(munging)

- 维度与数值归约(Dimensionality & Numerosity Reduction)
- 数据规范化(Normalization)
- 数据清洗(Data Scrubbing)
- 缺失值处理(Handling Missing Values)
- 无偏估计量(Unbiased Estimators)
- 分箱稀疏值(Binning Sparse Values)
- 特征提取／特征工程(Feature Extraction)
- 去噪(Denoising)
- 抽样(Sampling)
- 分层抽样(Stratified Sampling)
- 主成分分析(PCA,Principal Component Analysis)


# 工具集

- 微软的Excel及其自带的分析工具库(MS Excel / Analysis ToolPak)
- Java, Python
- R, R-Studio, Rattle（Rattle是基于R的数据挖掘工具，提供了GUI）
- Weka(基于JAVA环境下开源的机器学习以及数据挖掘软件)
- Knime(基于Eclipse环境的开源商业智能工具)
- RapidMiner(开源的数据挖掘软件,提供一些可扩展的数据分析挖掘算法的实现。)
- Hadoop发行版选择(Hadoop Dist of Choice)
- Spark, Storm: Hadoop相关的实时处理框架，是对Hadoop的补充和完善
- Flume: 海量日志采集、聚合和传输的系统
- Scribe: Facebook开源的日志收集系统，在Facebook内部已经得到的应用
- Chukwa: 开源的用于监控大型分布式系统的数据收集系统
- Nutch: 一个开源的Java搜索引擎
- Talend： 一家专业的开源集成软件公司，提供各类数据工具
- ScraperWiKi： 致力于数据科学领域维基百科网站，帮助个人和企业获得最专业的可视化数据，并支持对数据进行分析和管理
- Webscraper： 网页爬虫
- Flume: 海量日志采集、聚合和传输的系统
- Sqoop: Haddop套件
- tm: R语言的文本挖掘包
- RWeka: R的weka算法包
- NLTK: 自然语言工具包
- RHIPE: R与Hadoop相关的开发环境
- D3.js
- ggplot2
- Shiny: 在线网页交互可视化工具, 可以将R语言作为半个BI用。
- IBM Languageware: IBM的自然语言处理
- Cassandra, MongoDB: 2种NoSql数据库

# 参考资料

- [知乎上面秦路的回答](https://www.zhihu.com/question/21592677/answer/142800018)
- [Vamei对数据科学的理解](http://www.cnblogs.com/vamei/p/3178534.html)


