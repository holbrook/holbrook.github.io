---
title: 线性回归
postslug: linear_regression
date: 2018-02-28
category: 机器学习
tags: [回归问题, scikit-learn, statsmodels]
---

从机器学习的角度，线性回归是[回归问题](/tags/回归问题)中最简单的模型。回归问题属于监督式机器学习。

<!--more-->

# 回顾线性回归

在线性代数中，我们就学过用最小二乘法做线性回归:

对于平面上的 N 个点$P_i(x_i,y_i)$，满足$min \sum {\Delta Y_i}^{2} = min \sum {|Y_i-f(x_i)|}^2$
的直线$y=f(x)$，是这 N 个点的线性拟合直线。

# 机器学习角度的线性回归

从机器学习的角度，线性回归是[回归问题](/tags/回归问题)中最简单的模型。回归问题属于监督式机器学习：
给定训练样本，「学习」一个函数，每一个样本数据就是需要学习的函数的输入输出数据。
并且这个函数能够很好的泛化到不在训练集中的输入值上。可以通过测试数据来检验泛化的效果。

线性回归通常用于根据符合直线关系的连续变量估计实际数值。
其优点是快速、没有调节参数、可轻易解释、可理解；缺点是相比其他复杂一些的模型，其预测准确率不是太高，
因为它假设特征和响应之间存在确定的线性关系，这种假设对于非线性的关系，线性回归模型显然不能很好的对这种数据建模。

线性回归的两种主要类型是一元线性回归和多元线性回归。

一元线性回归的特点是只有一个自变量，即$y=y=\alpha x+\beta$.
而多元线性回归存在多个自变量，即$y=b_0+b_1x_1+...+b_px_p$

其实多项式回归可以看做是一种特殊的多元线性回归：$y=b_0+b_1x+ b_2x^2...+b_px^p$


# scikit-learn糖尿病数据集

我们用 scikit-learn 的糖尿病数据集来演示线性回归。

{% asset_ipynb data_explore.ipynb %}

# 用 [scikit-learn](/tags.html#scikit-learn)处理线性回归问题

LinearRegression模型在`Sklearn.linear_model`下，
它主要是通过 `fit(x,y)` 的方法来训练模型，其中x为特征，y为标记。
然后通过`predict()` 预测, 以fit()算出的模型参数, 预测特性 x 所对应的预测值y_pred。


{% asset_ipynb linear_regression.ipynb %}

# 模型评价和特征选择

回归问题不能用准确率评价。对于回归这种连续数值，评价测度(evaluation metrics)主要用以下指标：

- 平均绝对误差(Mean Absolute Error, MAE)

- 均方误差(Mean Squared Error, MSE)，即残差平方和

- 均方根误差(Root Mean Squared Error, RMSE)

在数据探索的时候，我们就发现 sex、s1、s2、 s4 与 target 的相关度不高。现在移除这些特征，
看看回归的结果是否更好。

{% asset_ipynb feature_selection.ipynb %}



# 多项式回归

这里，用一个2次函数加上随机的扰动来生成500个点，然后尝试用1、2、100次方的多项式对该数据进行拟合。
拟合的目的是使得根据训练数据能够拟合出一个多项式函数，这个函数能够很好的拟合现有数据，并且能对未知的数据进行预测[^5]。

结果评价：


做回归分析，常用的误差主要有均方误差根（RMSE）和R-平方（R2）。

RMSE是预测值与真实值的误差平方根的均值。这种度量方法很流行（Netflix机器学习比赛的评价方法），是一种定量的权衡方法。

R2方法是将预测值跟只使用均值的情况下相比，看能好多少。其区间通常在（0,1）之间。0表示还不如什么都不预测，直接取均值的情况，而1表示所有预测跟真实结果完美匹配的情况。

R2的计算方法，不同的文献稍微有不同。如本文中函数R2是依据scikit-learn官网文档实现的，跟clf.score函数结果一致。

而R22函数的实现来自Conway的著作《机器学习使用案例解析》，不同在于他用的是2个RMSE的比值来计算R2。

我们看到多项式次数为1的时候，虽然拟合的不太好，R2也能达到0.82。2次多项式提高到了0.88。
而次数提高到100次，R2也只提高到了0.89。

{% asset_ipynb polynomial_regression.ipynb %}




# 参考资料

[^1]: [Linear Regression Example](http://scikit-learn.org/dev/auto_examples/linear_model/plot_ols.html#example-linear-model-plot-ols-py)
[^2]: [scikit-learn : 线性回归，多元回归，多项式回归](http://blog.csdn.net/SA14023053/article/details/51703204)
[^3]: [Coursera公开课笔记: 斯坦福大学机器学习第二课“单变量线性回归(Linear regression with one variable)”](http://52opencourse.com/83/coursera公开课笔记-斯坦福大学机器学习第二课-单变量线性回归-linear-regression-with-one-variable)
[^4]: [用scikit-learn和pandas学习线性回归](http://www.cnblogs.com/pinard/p/6016029.html)
[^5]: [用Python开始机器学习（3：数据拟合与广义线性回归）](http://blog.csdn.net/lsldd/article/details/41251583)
[^6]: [Coursera公开课笔记: 斯坦福大学机器学习第四课“多变量线性回归(Linear Regression with Multiple Variables)”](http://52opencourse.com/108/coursera公开课笔记-斯坦福大学机器学习第四课-多变量线性回归-linear-regression-with-multiple-variables)
[^7]: [sklearn学习笔记之简单线性回归](http://www.cnblogs.com/magle/p/5881170.html)
