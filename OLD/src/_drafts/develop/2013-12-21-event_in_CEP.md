---
layout: post
title: "CEP中的事件(Event)"
description: ""
category: 软件开发
tags: [CEP]
lastmod: 
---

[CEP](/2012/11/06/about_cep.html)处理复杂事件。宽泛的事件，是指在应用程序域中的状态的一个有意义改变的一条记录。
而复杂事件处理关注[事件之间的相关性](/2013/12/21/Temporal_of_CEP.html),以及原子事件组合成的复杂(复合)事件。

CEP与规则引擎有类似之处，但CEP中的事件(Event)是一种特殊类型的事实(Fact)。其特殊性在于：

- 不可改变
  
  事件记录了已经发生的事情，而“过去”是不可改变的。

- 强时间约束

  事件有发生的时点，事件之间通常基于事件发生的时点进行关联。

- 被管理的生命周期

  有效时间窗口之外的事件不再有意义，可以被引擎自动回收。  

- 可以通过时间聚合

  因为所有的事件都有与它们关联的时间戳,所以,对它们可以 定义和使用滑动窗口,允许在一个时间段上根据值的聚合创建规则,
  例如, 整个 60 分钟的一个事件的值的平均值。


复杂事件处理(CEP),本质上是一个事件处理概念,涉及处理多个事件的任务与在事件云内部识别有意义事件的目标。

或者说，CEP从事件云/事件流中检测和选择感兴趣的事件, 找出它们之间的关系,根据它们和它们之间的关系推断新的数据。

由于CEP与规则引擎类似之处，CEP通常基于规则引擎。比如，Drools Fusion即是规则引擎，也可以作为CEP。

# 事件声明

DRL中的[declare](/2012/12/06/rule_language.html#menuIndex7)可以用于声明事件，只需要在declare中增加一条`@role(event)`
的元数据。实际上，declare默认隐含了`@role(fact)`的元数据，表面声明的是事实(Fact)。

比如：

```
import some.package.StockTick
declare StockTick
    @role( event )
end

//或者使用内嵌的事件声明
declare StockTick
    @role( event )
    datetime : java.util.Date
    symbol : String
    price : double
end
```

# 事件元数据

除了`@role`之外，事件还有一些Fact不具备的元数据。可以在declare中指定。

## @timestamp

  事件默认的时间戳是在insert到工作空间时，由引擎从Session Clock 获取并分配给事件。如果要指定使用事件的某一个属性作为时间戳，
  可以用`@timestamp`元数据指定。比如：


  ```
  declare StockTick
      @role( event )
      @timestamp( datetime )
      datetime : java.util.Date
      symbol : String
      price : double
  end
  ```

## @duration

  默认事件的期限为0，称为point-in-time 事件。有些事件具有期限性，称为interval-based 事件。

  要声明事件的期限，通过`@duration`指定事件的一个属性，该属性以 **毫秒数** 记录了事件的期限。

## @expires  

  当引擎运行在流(STREAM)模式时，指定一个过期时间可以用于内存管理。其格式为`[#d][#h][#m][#s][#[ms]]`，比如：`@expires( 1h35m )`
