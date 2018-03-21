---
layout: post
title: "JFreeChart概述"
description: "JFreeChart的图表模型及使用示例"
category: 软件开发
tags: [chart]
lastmod: 
---

[JFreeChart](http://www.jfree.org/jfreechart/)是Java世界的老牌图表组件，其强大无以言表。JFreeChart支持AWT、Swing等
GUI环境，也可以生成图片在Web环境中使用。后来又增加了对SWT环境的支持，从此不再需要SWT_AWT的桥接方式。

不同的图表组件可能对图表有不同的抽象。本文介绍JFreeChart中的图表模型。

# 对图表的分析

一个典型的图表如下所示：

![](/images/chart/chart.png)

通常，图表会包含以下组成部分：

- 标题
- 绘图区
- 序列
- 坐标轴
- 坐标轴标题
- 图例


# JFreeChart的模型

针对一个分析模型，可能有不同的实现模型。JFreeChart中的图表模型如下：


![](/images/chart/jfreechart.png)


- Chart

  整个图表的逻辑组件。Chart需要绘制在UI组件上，比如用于SWT的`ChartComposite`或用于Swing的`ChartPanel`等。


- Title

  标题。一个Chart可以有一个标题和多个子标题。JFreeChart中，标题和子标题都集成自`Title`类：

  ![](/images/chart/title.png)

  比如，主标题使用的就是`TextTitle` 类型。

- Plot和ChartFactory
  
  图形的绘制结构。包含坐标轴、绘图区和数据序列。由于[各种不同类型的图表](http://en.wikipedia.org/wiki/Chart)的特性和所需要的要素不同，比如饼图没有坐标轴，快速散点图需要使用二维数组作为数据源等等。JFreeChart中实现了很多的Plot类型：

  ![](/images/chart/plot.png)

  如果觉得手工创建各种类型的Plot过于繁琐，JFreeChart还提供了`ChartFactory`类，可以快速创建各种类型的图表（包括其Plot、坐标轴等元素）：


  ![](/images/chart/chartfactory.png)

- Axis

  坐标轴。有的Plot类型不含有Axis，如饼图。有的Plot有多个Axis。比如，
  基于二维坐标的图(`XYPlot`)通常会有`RangeAxis`(范围轴，一般表现为y轴)和
  `DomainAxis`(区域轴，一般表现为x轴)。

  为了适应不同的坐标数据，JFreeChart中提供了多种坐标轴：

  ![](/images/chart/axis.png)  

- DataSet

  数据集。是要进行可视化的数据。不同的Plot类型会需要不同的DataSet。比如：

  + CategoryDataset 维护了一个三元组`<value,row,col>`的列表结构
  + PieDataset 维护了一个二元组`<key,value>`的列表结构
  + SeriesDataset 维护基于序列的列表。比如，TimeSeriesCollection包含一组TimeSeries列表，每个TimeSeries对象维护一个`<time,value>`列表
  
  出于不同的目的，SeriesDataset会需要不同的序列(`Series`)类型。JFreeChart中提供的Series类型包括：

  ![](/images/chart/series.png) 
  

- Renderer  

  渲染器。决定了如何将DataSet展现为图形。与Axis一样，不同的Plot类型也需要不同类型的。JFreeChart提供了
  提供了`CategoryItemRenderer`和`XYItemRenderer`两个系类下近50种Renderer：


  ![](/images/chart/CategoryItemRenderer.png) 

  ![](/images/chart/XYItemRenderer.png) 









# 使用JFreeChart

前面也提到过，使用JFreeChart最简单的办法是使用其`ChartFactory`方法生成图表对象(`JFreeChart`)。以最常用的折线图为例：

```
  	import org.eclipse.swt.SWT;
  	import org.eclipse.swt.layout.FillLayout;
  	import org.eclipse.swt.widgets.Display;
  	import org.eclipse.swt.widgets.Shell;
  	import org.jfree.chart.ChartFactory;
  	import org.jfree.chart.JFreeChart;
  	import org.jfree.data.category.CategoryDataset;
  	import org.jfree.data.category.DefaultCategoryDataset;
  	import org.jfree.experimental.chart.swt.ChartComposite;
  	
  	public class ColumnChartDemo {
  		private static CategoryDataset createDataset() {
  	
  			// row keys
  			String series1 = "序列1";
  			String series2 = "序列2";
  			String series3 = "序列3";
  			// column keys
  			String category1 = "分组 1";
  			String category2 = "分组 2";
  			String category3 = "分组 3";
  			String category4 = "分组 4";
  			String category5 = "分组 5";
  			// create the dataset
  			DefaultCategoryDataset dataset = new DefaultCategoryDataset();
  			dataset.addValue(1.0, series1, category1);
  			dataset.addValue(4.0, series1, category2);
  			dataset.addValue(3.0, series1, category3);
  			dataset.addValue(5.0, series1, category4);
  			dataset.addValue(5.0, series1, category5);
  			dataset.addValue(5.0, series2, category1);
  			dataset.addValue(7.0, series2, category2);
  			dataset.addValue(6.0, series2, category3);
  			dataset.addValue(8.0, series2, category4);
  			dataset.addValue(4.0, series2, category5);
  			dataset.addValue(4.0, series3, category1);
  			dataset.addValue(3.0, series3, category2);
  			dataset.addValue(2.0, series3, category3);
  			dataset.addValue(3.0, series3, category4);
  			dataset.addValue(6.0, series3, category5);
  	
  			return dataset;
  	
  		}
  	
  		public static void main(String[] args) {
  			JFreeChart chart = ChartFactory.createBarChart("折线图Demo", "横坐标", "纵坐标",
  					createDataset());
  			Display display = new Display();
  			Shell shell = new Shell(display);
  			shell.setSize(600, 300);
  			shell.setLayout(new FillLayout());
  			shell.setText("Test for jfreechart running with SWT");
  			final ChartComposite frame = new ChartComposite(shell, SWT.NONE, chart,
  					true);
  			frame.pack();
  			shell.open();
  			while (!shell.isDisposed()) {
  				if (!display.readAndDispatch())
  					display.sleep();
  			}
  		}
  	}

```
