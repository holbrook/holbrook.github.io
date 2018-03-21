---
layout: post
title: "交易策略与规则引擎"
description: ""
category: 量化金融
tags: [交易系统, 规则引擎]
---

# 交易策略的要点

[前面](/2013/12/16/trade_system.html)提到，交易策略是系统化交易的核心。但是要注意的是，风险管理比交易策略要重要10倍。


交易策略的一些要点整理如下：

- 交易策略是一套完整的交易规则体系
- 这些规则对投资决策的各个环节做出明确规定
- 这些规则必须客观、唯一
- 所谓完整，至少要包括入场和出场两个规则——完成一个完整的交易周期，入场和出场信号必须确定会发生
- 出场策略比入场策略要重要10倍
- 越简单的策略越可靠
- 要有错误处理机制


# 交易策略的种类

所谓[规则，规定了一组确定的条件和此条件所产生的结果](/2012/03/20/rule_engine_1.html)。根据条件的类别不同，可以把交易策略分成以下几种：

## 基于技术指标

1. 例1
   - 规则定义
     + 入场规则：短期均线上穿长期均线
     + 出场规则：短期均线下穿长期均线
   - 评价

     简单但完整的交易策略
     
2. 例2
   - 规则定义
     + 入场规则：RSI<10
     + 出场规则：RSI>90
   - 评价

     有严重的设计缺陷。因为RSI可能长期不能趋近于某一极值，从而得不到对应的操作信号，长期无法完成完整的买卖周期。
              
## 基于统计分析

此类策略要研究市场数据的统计分布特征，需要较强的数学功底

1. 例1
   - 规则定义
     + 入场规则：跳空高开若干
     + 出场规则：利润达到x值或收盘价，或者损失达到y止损
   - 评价
     
     其思想是捕捉跳空开盘对后市的影响

2. 例2
   - 规则定义
     + 入场规则：突破跳空
     + 出场规则：衰竭跳空
   - 评价
     两个问题：1）跳空不一定会出现，从而导致交易周期不完整；2）过于主观随意

3. 例3
   - 规则定义
     + 入场规则：迪马克波动系数终点
     + 出场规则：反向迪马克波动系数终点
   - 评价
     
     交易周期不完整
              
              
## 基于图形分析

这类是最传统、最常见的交易策略

1. 例1
 
   - 规则定义
     + 入场规则：维克多突破
     + 出场规则：反向维克多突破
   - 评价
   
     简单但完整

2. 例2
 
   - 规则定义
     + 入场规则：罗斯钩式突破
     + 出场规则：反向罗斯钩式突破
   - 评价
   
     完整

3. 例3
 
   - 规则定义
     + 入场规则：卡尔汉数突破
     + 出场规则：反向卡尔汉数突破
   - 评价
   
     
4. 例4
 
   - 规则定义
     + 入场规则：W型反转
     + 出场规则：M型反转
   - 评价

     不一定会发生，交易周期不完整

5. 例5
 
   - 规则定义
     + 入场规则：晨星式
     + 出场规则：昏星式
   - 评价

     不一定会发生，交易周期不完整

              

## 基于数学理论
              
   需要较强的金融投资理论背景

1. 例1：飞镖系统

   - 规则定义
     + 入场规则：飞镖击中的股票
     + 出场规则：持有至规定期限

   - 评价
     
     其收益战胜了华尔街股票分析家，验证了投资学术界的随机行走理论


2. 例2：以满月为买入信号，以新月为卖出信号。

   这是一个以金融占星术理论为基础的交易系统。该方法以月球引力场的变化来解释地球生态系统的周期性变比。
              
3. 例3：硬币法——以随机选择过程为基础

   （略）

## 基于基本分析

1. P/E小于某一值时买入，P/E大于某一值时卖出
2. 收益增长率大于某一值时买入，收益增长率小于某一值时卖出
3. 每年某月买入白糖合约，若干月后平仓（季节波动）
4. 新建住房开工率持续上升若干月买入铜合约，若干月后平仓（因果关系）

## 基于心理分析

例： 传言开始是进场，传言证实后出场

## 其他

基于人工智能、神经网络、混沌理论（Chaos)等






# 用规则引擎驱动交易策略

尽管要求交易策略要尽可能简单，但是交易信号产生的条件可能五花八门。为了使交易系统具备更好的适应性，还是应该使用[规则引擎](/2012/03/20/rule_engine_1.html)来驱动。这就需要将交易策略规则化。

一般来说，交易策略的规则化需要经过确定规则（定性）、确定参数（定量）以及用规则语言描述（实现）三个步骤。


- 策略定性

  将交易策略表示为条件与交易信号。对于最简单的交易策略，可能只有入场信号和出场信号。但也会有一些稍复杂的情况需要处理：
  
  + 对于期货交易，入场信号可以区分为“做多”和“做空”，出场信号均为“平仓”
  + 有些交易策略的入场、出场信号可能会划分出不同的风险级别——风险越高的信号，产生的时间越早，可能的获利越大，但判断失误的风险也更大
  + 完善的交易系统，对于(正确入场,正确出场)、(正确入场,错误出场)、(错误入场,正确出场)、(错误入场,错误出场)  等情况都要考虑到，针对这些情况都要及时给出交易信号


- 确定参数

  将策略中可变的部分定义为参数。这些参数可以在引擎中进行设置，以调整策略的具体行为。

  参数可能要经过实际检验，才能得出最优的参数。

- 定义事件

  交易信号都是由某些数据触发，[如前](#menuIndex1)所述，这些数据可能是行情、指标、基本面等。

  不管是哪种数据，从规则引擎的角度，都需要定义为[事件(Event)](/2013/12/21/event_in_CEP.html)。

- 定义操作

  规则匹配的结果就是产生某种[操作](/2012/12/06/rule_language.html#menuIndex4)。
  考虑到交易策略要与后续的[资金管理]()等策略结合，这里将操作也定义为事件，作为资金管理策略的输入。

- 描述规则

  使用前面定义好的参数、事件和操作，用[规则描述语言](http://thinkinside.tk/2012/12/06/rule_language.html)将定性的策略描述为定量的规则。


# 实例

以“简单算术平均线”策略为例，其实现过程如下：

- 规则定性

  1. 规则1：当短期平均线向上穿越长期平均线时，买入
  2. 规则2：当短期平均线向下穿越长期平均线时，卖出

- 确定参数

  这个策略中，可以作为参数的变量包括：

  1. 选用哪种价格，比如开盘价、收盘价、最高价、最低价等
  2. 短期和长期均线的长度

  为简单起见，这里只把均线的长度作为参数。

  可以在DRL的global部分用全局变量定义规则的参数。这些参数将用于事件属性或规则条件中，用于调整策略的具体行为。如下：

  ```
  global java.lang.Integer SHORT_LENGTH;
  global java.lang.Integer LONG_LENGTH;
  ```

  global参数可以使用在规则引擎会话中，使用[KnowledgeSession](/2013/12/20/drools_API.html#menuIndex1)的`setGlobal()`方法进行设置。

  

- 事件定义

  定义一个“均线事件”(MAEvent):

  ```
  public class MAEvent {
    
    public Date datetime;
    public long duration;

    public int length;
    public double average;
    public double price;

    
    
    public String toString(){
      return ""+this.getDatetime().toLocaleString()+":MA"+this.length+"="+average+"\t("+price+")";
    }
  
  }
  ```

  并在规则文件中进行声明：

  ```
  import my.package.MAEvent
  ……
  declare MAEvent
    @role(event)
    @timestamp( datetime )
    @duration( duration )
  end
  ```

- 定义操作

  这里使用一个“操作信号事件”(SingalEvent)作为操作，符合条件时将该事件[insert](/2012/12/06/rule_language.html#menuIndex4)到规则引擎：

  ```
  public class SignalEvent extends AbstractEvent{

    public enum SignalType{LONG,SHORT}

    public Date datetime;
    public long duration;

    
    public SignalType type;
    public String strategyName; 
  }  
  ```

  在规则文件中声明：

  ```
  declare SignalEvent
    @role(event)
    @timestamp(datetime)
    @duration(duration)
  end
  ```

- 描述规则
  
  ```
  rule "LONG SIGNAL"
      when
          $MA5_1:MAEvent(length==SHORT_LENGTH);
          $MA5_0:MAEvent(length==SHORT_LENGTH,this meets[1d] $MA5_1);
          $MA20_1:MAEvent(length==LONG_LENGTH,this coincides $MA5_1,average>=$MA5_1.average);
          $MA20_0:MAEvent(length==LONG_LENGTH,this meets[1d] $MA20_1,this coincides $MA5_0,
            average<=$MA5_0.average
          );
          
      then
        
        SignalEvent e = new SignalEvent();
        e.datetime = $MA5_1.datetime;
        e.strategyName = "简单移动平均线策略";
        e.type = SignalEvent.SignalType.LONG;
        e.price = $MA5_1.price;
          insert(e);
  
      System.out.println(e);
  end
  
  rule "SHORT SIGNAL"
      when
          $MA5_1:MAEvent(length==SHORT_LENGTH);
          $MA5_0:MAEvent(length==SHORT_LENGTH,this meets[1d] $MA5_1);
          $MA20_1:MAEvent(length==LONG_LENGTH,this coincides $MA5_1,average<=$MA5_1.average);
          $MA20_0:MAEvent(length==LONG_LENGTH,this meets[1d] $MA20_1, this coincides $MA5_0,
            average>=$MA5_0.average
          );
          
      then
          SignalEvent e = new SignalEvent();
        e.datetime = $MA5_1.datetime;
        e.strategyName = "简单移动平均线策略";
        e.type = SignalEvent.SignalType.SHORT;
        e.price = $MA5_1.price;
          insert(e);
          
          System.out.println(e);
  
  end
```

