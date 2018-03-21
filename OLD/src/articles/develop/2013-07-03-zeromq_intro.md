---
layout: post
title: "ZeroMQ简介"
description: "zeroMQ不是TCP，不是socket，也不是消息队列，而是这些的综合体。"
category: 软件开发
tags: [ZeroMQ, 消息中间件]
lastmod:
---

zeroMQ不是TCP，不是socket，也不是消息队列，而是这些的综合体。

![ZeroMQ](images/2013/zeromq/logo.gif)

# ZeroMQ是什么

[ZeroMQ](http://www.zeromq.org/)以嵌入式网络编程库的形式实现了一个并行开发框架（concurrency framework），
能够提供进程内(inproc)、进程间(IPC)、网络(TCP)和广播方式的消息信道，
并支持扇出(fan-out)、发布-订阅(pub-sub)、任务分发（task distribution）、请求/响应（request-reply）等通信模式。
ZeroMQ的性能足以用来构建集群产品，
其异步I/O模型能够为多核消息系统提供足够的扩展性。
ZeroMQ支持30多种语言的API，可以用于绝大多数操作系统。
在提供这些优秀特性的同时，ZeroMQ是开源的，遵循LGPLv3许可。

ZeroMQ的明确目标是“成为标准网络协议栈的一部分，之后进入Linux内核”。

# Zero 之禅（The Zen of Zero）

ZeroMQ是一个很有个性的项目，其名称也暗合禅意：

- Ø 是一种权衡：让一些丹麦人恼火，但是“Ø”本身也降低了google搜索的命中率以及twitter上的关注度
- Ø 暗合“零代理(broker)”、“零延迟”
- Ø 的目标是“零管理、零消耗、零浪费”
- Ø 符合简约主义：力量的源泉是降低复杂度，而不是增加新功能

# ZeroMQ对socket API的封装

与libevent, ACE等项目不同，使用ZeroMQ时可以不关注网络细节。
ZeroMQ的API提供了对于传统socket API的封装，对于套接字类型、连接处理、帧、甚至路由的底层细节都进行了抽象，
使得一套API可以用于进程内通讯、IPC、TCP和广播等多种消息信道。

ZeroMQ自己定位为“智能传输层”（The Intelligent Transport Layer），位于网络层和应用层之间。
ZeroMQ使得构建大型并发应用时，可以将基本单元随意的“组装”，由ZeroMQ解决通信的弹性伸缩，

ZeroMQ的这种设计大大简化了应用程序消息通信的实现，使得在多种场景下重用相同的交互模式成为可能。
使用ZeroMQ可以让编写高性能网络应用程序极为简单和有趣。

与socket相比，ZeroMQ API的特征如下：

- 在后台线程中异步地处理IO。后台线程使用无需锁的数据结构与应用线程通信，所以ZeroMQ应用程序不需要锁、信号量，或者其他等待状态。
- 组件可以动态地加入和退出，ZeroMQ会自动重新连接。这意味着可以以任何次序启动组件。可以创建“面向服务架构（service-oriented architectures)”，其中的服务可以在任何时候加入或者退出网络。
- 在需要的时候自动对消息排队。这种处理是智能的，在排队前会尽量让消息靠近接收者。
- 有处理队列溢出的方法（“高水位标记”）。队列满的时候，ZeroMQ会自动阻塞发送者，或者丢弃消息，取决于你正在使用的消息传递类型（模式）。
- ZeroMQ让应用程序可以使用传输端点相互交流：TCP、多播、进程内、进程间。使用不同的传输端点时不用修改代码。
- 根据消息传递模式的不同，使用不同的策略来安全地处理慢速/阻塞的接收者。
- 使用请求-应答、发布-订阅等多种模式来路由消息。这些模式定义了如何创建网络拓扑结构。
- 需要降低互联的各部分间的复杂性的时候，可以在网络中放置模式扩展的“设备”（小的代理）。
- 通过在线路中使用简单的帧，可以精确地传递整个消息。发送10K的消息，则会收到10K的消息。
- 不对消息格式做任何假定。消息是从零到数G字节的块。需要在高层使用其他产品来表示数据，如Google的Protocol Buffers、XDR等等。
- 智能地处理网络错误。有时候重试，有时候告诉你操作失败。
- 降低能耗。使用较少的CPU时间来做更多事情意味着使用更少的能源，而且较老的机器可以使用更长的时间。


# ZeroMQ的通信协议

ZeroMQ定义了[ZMTP（ZeroMQ Message Transport Protocol, ZeroMQ消息传输协议）](http://rfc.zeromq.org/spec:13)，在TCP协议之上定义了向后兼容性的规则，可扩展的安全机制，命令和消息分帧，连接元数据，以及其他传输层功能。

相对于其他的消息传输协议/通信协议，ZeroMQ有明显的优势：

- TCP：ZeroMQ基于消息，使用消息模式而不是字节流。
- XMPP：ZeroMQ更简单、快速、更底层。Jabber可建在ØMQ之上。
- AMQP：完成相同的工作，ZeroMQ要快100倍，而且不需要代理（规范更简洁——比AMQP的规范文档少278页）
- IPC：ZeroMQ可以跨主机通信
- CORBA：ZeroMQ不会将复杂到恐怖的消息格式强加于你。
- RPC：ZeroMQ完全是异步的，你可以随时增加/删除参与者。
- [RFC 1149](http://www.faqs.org/rfcs/rfc1149.html)：ZeroMQ比它快多了！
- 29west LBM：ZeroMQ是自由软件！
- IBM Low-latency：ZeroMQ是自由软件！
- Tibco：ZeroMQ仍然是自由软件！


# ZeroMQ不是消息队列

在摩尔定律的魔咒下，“分布式处理”逐渐成为主流，随之而来的是关于消息通讯、消息中间件的项目层出不穷。

其中最有名的应该是ZeroMQ和RabbitMQ，Thrift。
[RabbitMQ](http://www.rabbitmq.com/)是符合[AMQP(Advanced Message Queuing Protocol, 高级消息队列协议)](http://www.amqp.org/)的消息中间件，
而[Thrift](http://thrift.apache.org/)是出自于Facebook的跨语言服务访问的框架。

2011年，[欧洲核子研究组织（CERN）](http://zh.wikipedia.org/wiki/%E6%AD%90%E6%B4%B2%E6%A0%B8%E5%AD%90%E7%A0%94%E7%A9%B6%E7%B5%84%E7%B9%94)
调查了统一用于操作CERN加速器的中间件解决方案的方式，欧洲核子研究组织的研究比较了
[CORBA](http://zh.wikipedia.org/wiki/CORBA)、
[Ice](http://zh.wikipedia.org/w/index.php?title=Internet_Communications_Engine&action=edit&redlink=1)，
[Thrift](http://zh.wikipedia.org/w/index.php?title=Apache_Thrift&action=edit&redlink=1)，
ZeroMQ,
YAMI4，
[RTI](http://zh.wikipedia.org/w/index.php?title=Run-Time_Infrastructure_(simulation)&action=edit&redlink=1)和
[Qpid/AMQP](http://zh.wikipedia.org/w/index.php?title=Apache_Qpid&action=edit&redlink=1)，
ZeroMQ得到了最高的分数。


但ZeroMQ最大的特点不在性能，而是机制。尽管名字中包含了"MQ"，但ZeroMQ并不是“消息队列/消息中间件”。ZeroMQ是一个传输层API库，
更关注消息的传输。与消息队列相比，ZeroMQ有以下一些特点：

1 点对点无中间节点

  传统的消息队列都需要一个消息服务器来存储转发消息。而ZeroMQ则放弃了这个模式，把侧重点放在了点对点的消息传输上，并且（试图）做到极致。以为消息服务器最终还是转化为服务器对其他节点的点对点消息传输上。ZeroMQ能缓存消息，但是是在发送端缓存。ZeroMQ里有水位设置的相关接口来控制缓存量。当然，ZeroMQ也支持传统的消息队列（通过zmq_device来实现）。

2 强调消息收发模式

  在点对点的消息传输上ZeroMQ将通信的模式做了归纳，比如常见的订阅模式（一个消息发多个客户），分发模式（N个消息平均分给X个客户）等等。下面是目前支持的消息模式配对，任何一方都可以做为服务端。
  - PUB and SUB
  - REQ and REP
  - REQ and XREP
  - XREQ and REP
  - XREQ and XREP
  - XREQ and XREQ
  - XREP and XREP
  - PUSH and PULL
  - PAIR and PAIR

3 以统一接口支持多种底层通信方式

  不管是线程间通信，进程间通信还是跨主机通信，ZeroMQ都使用同一套API进行调用，只需要更改通信协议名称（如，从"ipc:///xxx"改为"tcp://*.*.*.*:****"）即可。

4 异步，强调性能

  ZeroMQ设计之初就是为了高性能的消息发送而服务的，所以其设计追求简洁高效。它发送消息是异步模式，通过单独出一个IO线程来实现，所以消息发送调用之后不要立刻释放相关资源哦，会出错的（以为还没发送完），要把资源释放函数交给ZeroMQ让ZeroMQ发完消息自己释放。



# ZeroMQ的应用案例
ZeroMQ如何拯救世界

由于ZeroMQ的强大，我们可以用ZeroMQ搭建出非常强悍的应用。比如：

- [Salt](/2013/06/24/salt_intro.html)的底层就使用了ZeroMQ作为通信机制
- [Mongrel2](http://mongrel2.org/home)是使用ZeroMQ开发的一个Web服务器

  Mongrel2是应用ZeroMQ的一个有趣的案例：所有入站消息通过“Push”套接字路由到Mongrel2，套接字可以自动实现负载均衡，将消息分发到连接处理器。反过来，连接处理器处理入站消息（通过Pull套接字），然后将处理结果发布到一个“Pub”套接字，Mongrel2服务器本身已订阅了该套接字，并且通过主题（topic）过滤器监听该套接字的进程号。如下图：

  ![zmq-mongrel2](images/2013/zeromq/zmq-mongrel2.png)

ZeroMQ带来了一种新的分布式应用架构的思考方式。善用ZeroMQ，可以为应用带来非常强大的特性。

# 参考资料

- [官方指南](http://zguide.zeromq.org/page:all)，这篇巨长的文档不仅介绍了ZeroMQ的主要方面，网络编程，还融入了ZeroMQ作者对于编程的理念，很值得精读
- [An Introduction to ØMQ (ZeroMQ)](http://www.infoq.com/news/2010/09/introduction-zero-mq),InfoQ上面对于ZeroMQ的一篇介绍性文章
- [ZeroMQ社区](http://www.zeromq.org/community)，
- [ZeroMQ：云计算时代最好的通讯库](http://hi.baidu.com/ah__fu/item/bdff1d88d236f8c299255f65)
- [ZeroMQ 的模式](http://blog.codingnow.com/2011/02/zeromq_message_patterns.html)
