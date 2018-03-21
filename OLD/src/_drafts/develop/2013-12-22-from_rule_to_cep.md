---
layout: post
title: "从规则引擎到复杂事件处理(CEP)"
description: "Drools Fusion既是规则引擎，又可以作为CEP。除了事件定义时间推理之外，对于引擎本身也会有一些不同的使用。主要体现在会话时钟、流模式、滑动窗口和对事件的内存管理。"
category: 软件开发
tags: [规则引擎, CEP]
lastmod: 
---

Drools Fusion既是规则引擎，又可以作为CEP。除了[事件定义](/2013/12/21/event_in_CEP.html)和[时间推理](/2013/12/21/Temporal_of_CEP.html)之外，对于引擎本身也会有一些不同的使用。主要体现在会话时钟、流模式、滑动窗口和对事件的内存管理。


# 会话时钟

由于事件的时间性，处理事件时需要一个参考时钟。
这个参考时钟在会话配置(KnowledgeSessionConfiguration)中指定，所以称为会话时钟(Session Clock)。

有很多种场景需要对时钟进行控制，比如：

- 规则测试

  测试总是需要一个可控的环境,并且当测试包含了带有时间约束的 规则时,不仅需要控制输入规则和事实,而且也需要时间流。

- 定期(regular)执行

  通常,在运行生产规则时,应用程序需要一个实时时 钟,允许引擎对时间的行进立即作出反应。

- 特殊环境

  特殊环境可以对时间的控制有特殊的要求。群集环境可能需要在心 跳中的时钟同步,或 JEE 环境可能需要使用一个应用服务器提供的时钟,等 等。
- 规则重演或模拟

  要重演场景或模拟场景也需要应用程序控制时间流。

Drools中默认使用基于系统时钟的实时时钟(realtime)，也可以使用能被应用程序控制的伪时钟(pseudo)。设置伪时钟的方法如下：

{% highlight java %}
KnowledgeSessionConfiguration conf = KnowledgeBaseFactory.newKnowledgeSessionConfiguration();
conf.setOption( ClockTypeOption.get( "pseudo" ) );

StatefulKnowledgeSession session =kbase.newStatefulKnowledgeSession( conf, null );

SessionPseudoClock clock = session.getSessionClock();

// then, while inserting facts, advance the clock as necessary:
FactHandle handle1 = session.insert( tick1 );
clock.advanceTime( 10, TimeUnit.SECONDS );
FactHandle handle2 = session.insert( tick2 );
clock.advanceTime( 30, TimeUnit.SECONDS );
FactHandle handle3 = session.insert( tick3 );

{% endhighlight %}






# 流模式

Drools默认运行在云(Cloud)模式下。云模式下没有时间流的概念，引擎知道所有的事实(Fact)和事件(Event)。此时引擎将所有的事实/事件看做是一个无序的云。

由于云模式下引擎没有“现在”的概念，尽管事件具有时间戳、期限等元数据，这些数据也仅仅作为事件的属性，
不代表事件发生的顺序，也不能进行[时间推理](/2013/12/21/Temporal_of_CEP.html)。

如果需要处理实时/准实时事件(Event)，需要[时间推理](/2013/12/21/Temporal_of_CEP.html)，Drools必须工作在流(Stream)模式下。
此时要求每个流中的事件必须按照时间顺序插入。

## 启用流模式

Drools默认运行在云模式下，可以通过以下方式启用流模式：

{% highlight java %}
KnowledgeBaseConfiguration config =
KnowledgeBaseFactory.newKnowledgeBaseConfiguration();
config.setOption( EventProcessingOption.STREAM );
{% endhighlight %}

也可以使用属性文件定义：`drools.eventProcessingMode = stream`。

## 入口点

Drools定义了工作空间的多个入口点(WorkingMemoryEntryPoint)，每个入口点可以看做是一个事件流，可以将事件通过不同的入口点插入到工作空间中。

来自同一个入口点的事件通过时间戳被排序。每个流既可以包含单一类型的事件，也可以包含多种类型的事件。

- 声明入口点

  入口点不需要显式声明，在规则中引用的入口点都会在规则编译期间被自动识别和创建。比如：

  ```
  rule "authorize withdraw"
      when
          WithdrawRequest( $ai : accountId, $am : amount ) from entry-point "ATM Stream"
          CheckingAccount( accountId == $ai, balance > $am )
      then
          // authorize withdraw
  end
  ```

  规则编译器会识别"ATM Stream"入口点，并在规则库中创建该入口点。

- 使用入口点

  举例如下：

  {% highlight java %}
    // create your rulebase and your session as usual
    StatefulKnowledgeSession session = ...
    // get a reference to the entry point
    WorkingMemoryEntryPoint atmStream =
    session.getWorkingMemoryEntryPoint( "ATM Stream" );
    // and start inserting your facts into the entry point
    atmStream.insert( aWithdrawRequest );
    
  {% endhighlight %}

  除了这种手工插入事实的方式之外，Drools还提供了一系列的管道API和适配器，可以将其他流(如JMS、IO流、Socket等)之间接入到入口点上。

	
# 滑动窗口

在流模式中，规则的[LHS部分](/2012/12/06/rule_language.html#menuIndex3)
可以使用滑动窗口限定只关注一定范围内的事件。这个范围可以是时间或事件的个数，分别成为滑动时间窗口和滑动长度窗口。

比如：

```
StockTick() over window:time( 2m )

Number( doubleValue > $max ) from accumulate(
	SensorReading( $temp : temperature ) over window:time( 10m ), average( $temp ) 
)

StockTick( company == "IBM" ) over window:length( 10 )

Number( doubleValue > $max ) from accumulate(
	SensorReading( $temp : temperature ) over window:length( 100 ), average( $temp ) 
)

```

# 内存管理

在流模式下，引擎自动执行事件的内存管理。对于不可能再被匹配的事件自动释放。

引擎会关注事件的@expires中指定的到期时间，并分析规则中隐含的到期时间，进行自动释放。
