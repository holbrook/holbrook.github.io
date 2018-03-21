---
layout: post
title: "用python获取历史价格数据并在R中使用"
description: ""
category: 量化金融
tags: [R, python, 量化金融]
lastmod: 2013-06-10
---

# 数据需要

1. 不管是回归、分析或模拟，都需要历史数据
2. 尽管可以在R中实现，但是并不是R的专长。用合适的工具做合适的事情，事半功倍。
3. python是一种简单强大的语言。尽管从语法上来看，R与ruby更接近。


# R与python

## R中的函数

[这篇文章](http://site.douban.com/182577/widget/notes/10568316/note/264808127/)中介绍了R中获取交易数据的一些方法，包括：

- quantmod包的getSymbols()函数
  可以从多个来源下载股票数据，包括yahoo, google, MySQL, FRED, csv, RData和 oanda。
- tseries包的get.hist.quote()函数
  默认下载是yahoo，下载以后的默认对象是zoo，可以进行复权处理
- stockPortfolio包的getReturns()函数
  也是从yahoo下载数据，主要用于计算回报率，同时也包含价格数据

可以直接使用，但是数据下载不是R的主要目的。如果还要考虑数据检查、定期更新等数据相关的功能，用R实现就不大合适了。

## 直接调用
rPython: Python in R
RPy: R in Python

## 间接调用

使用管道、或文件系统、或数据库

什么情况下使用？

# 数据源

更高频度的数据需要采取其他办法，比如hack别的交易软件，或者购买数据源。

# 存储设计

## 数据模型

## 数据实现
同一个模型可以有多种实现


1. 文件or数据库？
2. 文本or二进制？
3. 具体设计


# 实现

## python
	数据源定义（历史数据，实时数据）
	public String getName();
	public int getIntervalSeconds();
	public Date[] check(Security target);
	public boolean validate();//验证数据源是否可用

	数据服务（历史数据，实时数据）

	数据类型：csv, json, xls, bin, html, etc.. 

	数据存储：

## R

	数据读取：



