---
layout: post
title: "在SWT中用JFreeChart实现K线图"
description: ""
category: 软件开发
tags: [chart]
lastmod: 
---

# 目标

在[R学习笔记](/2013/05/03/r_notes_1_what.html)中，展示了这样一张图表：

![](/images/2013/r_notes/2.png)

现在需要在Eclipse e4应用中实现这样的图表。

# SWT图表组件的选择

在RCP/JFace/SWT中，可以选择的图表组件包括：

- Eclipse BIRT

  [Eclipse BIRT](http://www.eclipse.org/birt/phoenix/)是Eclipse平台下的报表框架。其中的图表组件可以单独使用。
  由于BIRT依赖于GEF、EMF等Eclipse插件，所以非常重，不适合简单轻量的应用。 

- SWT Chart
 
  从名字就可以看出，[SWT Chart](http://www.swtchart.org/)是专为SWT环境开发的报表组件。设计很清晰，使用起来也方便。但是目前支持的图表类型比较少。

- JFreeChart

  [JFreeChart](http://www.jfree.org/jfreechart/)是Java世界的老牌图表组件，其强大无以言表。JFreeChart支持AWT、Swing等
GUI环境，也可以生成图片在Web环境中使用。后来又增加了对SWT环境的支持，从此不再需要SWT_AWT的桥接方式。


综上所述，这里选择JFreeChart作为绘图组件。



# 获取股票数据

由于需要的数据量比较大，不能再使用[前面]()的模拟数据方法了。这里使用[雅虎财经](http://finance.yahoo.com/)的数据。

雅虎财经提供了查询股票历史数据的接口：

```
  http://table.finance.yahoo.com/table.csv?ignore=.csv&....
```
参数包括：

- s: 股票代码/名称。对于国内的股票，使用类似`000001.ss`的编码
- a、b、c: 开始时间的月、日、年
- d、e、f: 结束时间的月、日、年
- g：时间周期，分别为`d`:日， `w`:周，`m`：月， `v`:dividends only

其中，月份是从0开始。比如，9月数据写为08。

本文中使用2013年上证综合指数的日线数据：

```
  http://table.finance.yahoo.com/table.csv?ignore=.csv&s=000001.ss&a=00&b=01&c=2013&d=11&e=31&f=2013&g=d
```

获取到的CSV文件包含的数据列为`Date,Open,High,Low,Close,Volume,Adj Close`，其中Date的格式为`yyyy-MM-dd`。数据按照日期倒序排列。

处理代码如下：

```
	OHLCSeries ohlcSeries = new OHLCSeries("");
	TimeSeries volumeSeries =new TimeSeries("");
	
	try{
		URL url = new URL("http://table.finance.yahoo.com/table.csv?ignore=.csv&s=000001.ss&a=00&b=01&c=2013&d=11&e=31&f=2013&g=d");
		InputStream is = url.openStream();
		InputStreamReader reader = new InputStreamReader(is,"UTF-8");
		
		BufferedReader buffer = new BufferedReader(reader);
		
		
		String newLine = buffer.readLine();// 标题行
		
		
		while ((newLine = buffer.readLine()) != null) {
            String item[] = newLine.trim().split(",");
            Date date = df.parse(item[0]);
            float open = Float.valueOf(item[1]);
            float high = Float.valueOf(item[2]);
            float low = Float.valueOf(item[3]);
            float close = Float.valueOf(item[4]);
            float volume = Float.valueOf(item[5]);
            float adj_close = Float.valueOf(item[6]);
            
            ohlcSeries.add(new Day(date), open,high,low,close);
            volumeSeries.add(new Day(date),volume);
        }
		
	}catch(Exception e){
		e.printStackTrace();
	}
```	




# 联合图表

目标中的图表是一种联合图表(Combined Chart)：多个图表共用横坐标或纵坐标。JFreeChart中提供了`CombinedDomainXYPlot`和`CombinedRangeXYPlot`，分别用于联合横坐标和联合纵坐标的图表。

由于各种图表类型都有可能组成联合图表，JFreeChart没有在`ChartFactory`中提供工厂方法进行创建，
只能按照[JFreeChart中的图表模型](/2014/01/17/jfreechart.html#menuIndex1)进行手工创建。下面是例子：

```
  //创建横坐标轴，作为联合坐标
  DateAxis timeAxis = new DateAxis();

  //创建两个纵坐标，用于上下两个Plot
  NumberAxis ohlcAxis = new NumberAxis();
  NumberAxis volumeAxis = new NumberAxis();

  //创建两个Plot对应的Renderer
  CandlestickRenderer ohlcRenderer = new CandlestickRenderer();
  XYBarRenderer volumeRenderer = new XYBarRenderer();

  //创建K线图的Plot，使用“数据”一节中的ohlcSeries
  ////其中横坐标设为"null"，以使用联合横坐标
  OHLCSeriesCollection ohlcDataset = new OHLCSeriesCollection();
  ohlcDataset.addSeries(ohlcSeries);
  XYPlot ohlcPlot = new XYPlot(ohlcDataset,timeAxis,ohlcAxis,ohlcRenderer);

  //创建成交量柱状图的Plot，使用“数据”一节中的volumeSeries
  //其中横坐标设为"null"，以使用联合横坐标
  TimeSeriesCollection volumeDataset = new TimeSeriesCollection();
  volumeDataset.addSeries(timeSeries);
  XYPlot volumePlot=new XYPlot(volumeDataset,null,volumeAxis,volumeRenderer;

  //创建联合图表
  CombinedDomainXYPlot combineddomainxyplot = new CombinedDomainXYPlot(timeAxis());

  //上下两个图表占据的高度比例为2:1，间隔为10
  combineddomainxyplot.add(ohlcPlot, 2);
  combineddomainxyplot.add(volumePlot, 1);
  combineddomainxyplot.setGap(10);
  JFreeChart chart = new JFreeChart("xx股票", JFreeChart.DEFAULT_TITLE_FONT, combineddomainxyplot, false);
        
```

创建的图表如下所示：

![](/images/chart/sample1.png)

# 设置样式


上面的图表默认样式与国内的习惯不大一样。不过JFreeChart提供了丰富的API进行样式的设置。下面对样式进行简单调整(目前对SWT的支持不够完全。比如，颜色值仍需要使用AWT的`Color`类)：

```
//图表
chart.setBackgroundPaint(Color.BLACK);
chart.getTitle().setPaint(Color.WHITE);
chart.setBorderVisible(false);

//Plot
combineddomainxyplot.setBackgroundPaint(Color.BLACK);
ohlcPlot.setBackgroundPaint(Color.BLACK);
volumePlot.setBackgroundPaint(Color.BLACK);

//渲染
ohlcRenderer.setUpPaint(Color.RED);
ohlcRenderer.setDownPaint(Color.GREEN);

volumeRenderer.setShadowVisible(false);

//坐标轴
timeAxis.setTickLabelPaint(Color.GRAY);
ohlcAxis.setTickLabelPaint(Color.GRAY);
volumeAxis.setTickLabelPaint(Color.GRAY);

```

调整后的图表如下所示：

![](/images/chart/sample2.png)

# 去除非交易时段

前面的例子中，K线是不连续的，因为会有非交易日的存在。如果是小时、分钟级别的K线图，该问题会更加明显。

要去除非交易时段，使得K线连续，大体有两个思路：

- 实现一个自定义的`DateAxis`，根据数据的序号产生坐标，根据实际时间产生标签
- 实现一个`Timeline`，并设置给`DateAxis`
- 更改Renderer

看起来方法1更容易，但由于没有相关的文档，需要自己分析`DateAxis`的代码，类似一种“Hack”的模式，很难保证向后兼容；
方法2是官方指定的方法，可行性更高，但是要同时支持日线、小时线、分钟/5分钟线，实现起来有点难度。
此外，[Timeline的接口说明](http://www.jfree.org/jfreechart/api/javadoc/org/jfree/chart/axis/Timeline.html)读起来有些费解；方法3需要改变数据源(Dataset)，使用序号作为数据，设置Renderer的`ItemLabelGenerator`，根据序号产生时间格式的坐标标签。

这里采用方法3，实例代码如下：

```
//TODO

```

# 修正高度和宽度(TODO)

- 固定每根K线的宽度，根据图表宽度决定显示多少根K线

- 使用“时间窗口”作为数据


# 横向滚动和实时曲线(TODO)








