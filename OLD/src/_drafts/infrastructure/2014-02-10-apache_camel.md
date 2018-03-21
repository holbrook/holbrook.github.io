---
layout: post
title: "Apache Camel的核心概念"
description: ""
category: 企业架构
tags: [SOA, ESB]
lastmod: 
---

# Apache Camel的整体架构

[Apache Camel](http://camel.apache.org/)是一个消息处理引擎，实现了EIP(Enterprise Integration Patterns,企业整合模式)。

Camel能够用来处理来自于不同源的事件和信息，定义规则进行消息的传递和转换等处理，以实现基于消息的应用整合。其整体架构如下图所示：

![](/images/camel/camel-architecture.png)


# Message 和 Exchange

`org.apache.camel.Message`接口是对“消息”的抽象。消息由head、body、attachment等部分组成。

![](/images/camel/message.png)

Camel中提供了一个默认的实现：`org.apache.camel.impl.DefaultMessage`，可以适应大部分的应用场景。

不管是请求、响应，或者异常，都可以作为消息在上下文(CamelContext)的消息处理器(Processor)之间进行交换(Exchange)。

`org.apache.camel.Exchange`接口就是对“消息交换”的抽象。

![](/images/camel/exchange.png)

其中：

- Exchange ID : 区分每次消息交换的标识
- MEP: （message exchange pattern，消息交换模式），分为单向(InOnly)和请求-应答(InOut)两种
- Exception: 用于记录消息交换时发生的异常
- In message: 上一个节点传入的消息
- Out message: 当MEP 是InOut时，需要传出的消息

Camel提供了默认的`org.apache.camel.impl.DefaultExchange`实现。

Camel处理消息时，每个节点都在处理`Exchange`。

# Endpoint 和 Component

Endpoint(端点)，接收或发送消息的通道。通过[URI](http://zh.wikipedia.org/wiki/%E7%BB%9F%E4%B8%80%E8%B5%84%E6%BA%90%E6%A0%87%E5%BF%97%E7%AC%A6)连接消息源或目标。

为了适应各种不同的URI协议，如http,ftp,JMS,smtp等，Camel中提供了多种Endpoint，也支持扩展自己的Endpoint。

![](/images/camel/endpoints.png)

Component(不应该叫做组件，而应该是连接器connector)。`org.apache.camel.Component`接口只定义了两个方法：

- `createConfiguration(String)`
- `createEndpoint(String)`

通常，客户代码不会直接调用`createEndoint()`方法，而是由`CamelContext`对象进行调用。

Camel中提供了大量的Component的实现：

![](/images/camel/components.png)


# Processor

不管是消息路由(Message Routing)、消息转换(Message Transformation)还是消息过滤(Message Filter)，都是对消息的某种处理(Process)。

Camel中，抽象出`org.apache.camel.Processor`接口，表示对消息的处理。该接口只定义了一个方法：

```
    void process(Exchange exchange) throws Exception;
```

从接口定义可以看出，Camel中认为可以处理消息交换(Exchange)的类都是消息处理器(Processor)。


基于Camle的应用可以开发自己的Processor实现，同时Camel提供了大量的内置Processor，以支持[EIP(Enterprise Integration Patterns)](http://camel.apache.org/enterprise-integration-patterns.html)。

![](/images/camel/processor.png)






# CamelContext


![](/images/camel/camel_context.jpg)

CamelContext是对Camel运行时的抽象，提供了API用于管理Component、Endpoint、Processor等节点：

![](/images/camel/context.png)

一般来说，使用Camel的步骤如下：

1. 创建一个CamelContext对象。
2. 向CamelContext对象中添加Endpoints或者是Components
3. 向CamelContext对象中添加路由(routes)规则
4. 调用CamelContext的start()方法启动Camel引擎
5. 通过Endpoint发送或接收消息
6. 调用CamelContext的stop()方法时

# 定义路由(Route)

每个消息处理流程是由一系列的`Processor`连接而成的图(Graph)，每个图称为一个路由(Route)。

在开始使用Camel之前，需要在CamelContext中定义一个或多个路由。Camel支持使用DSL或者Spring XML进行配置。比如：

```
		RouteBuilder builder = new RouteBuilder() {
			public void configure() {
				from("queue:a").filter(header("foo").isEqualTo("bar")).to(
						"queue:b");
				from("queue:c").choice().when(header("foo").isEqualTo("bar"))
						.to("queue:d").when(header("foo").isEqualTo("cheese"))
						.to("queue:e").otherwise().to("queue:f");
			}
		};

		CamelContext myCamelContext = new DefaultCamelContext();
		myCamelContext.addRoutes(builder);
```

或者：

```
  <beans xmlns="http://www.springframework.org/schema/beans"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xsi:schemaLocation="
       http://www.springframework.org/schema/beans http://www.springframework.org/schema/beans/spring-beans.xsd
       http://camel.apache.org/schema/spring http://camel.apache.org/schema/spring/camel-spring.xsd
    ">
 
    <!-- this is an included XML file where we only the the routeContext -->
    <routeContext id="myCoolRoutes" xmlns="http://camel.apache.org/schema/spring">
        <!-- we can have a route -->
        <route id="cool">
            <from uri="direct:start"/>
            <to uri="mock:result"/>
        </route>
        <!-- and another route, you can have as many your like -->
        <route id="bar">
            <from uri="direct:bar"/>
            <to uri="mock:bar"/>
        </route>
    </routeContext>
 
  </beans>
```

# FUSE Mediation Router: 企业级Camel

 FuseSource提供Camel的经测试、认证并提供支持的企业级版本，称作[FUSE Mediation Router](http://fusesource.com/products/enterprise-camel/)。

 