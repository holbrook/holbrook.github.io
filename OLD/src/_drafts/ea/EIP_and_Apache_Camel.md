---
layout: post
title: "Apache Camel与EIP(企业集成模式）"
description: ""
category: 
tags: []
lastmod: 
---

《企业集成模式》认为，对于企业应用集成，与文件传输、共享数据库和远程过程调用等传统方式相比，使用异步的消息传递机制是更好的实现方式。

对于消息系统，《企业集成模式》定义了一些基本概念，包括：

- 通道(Channel)：一个传递数据的虚拟管道，连接消息发送者和接收者。
- 消息(Message)：可以通过通道传送的一个原子数据包
- 管道(Pipe)：
- 路由(Route)：
- 转化(Transform)
- 端点(Endpoint)

# 消息模式MEP（Message Exchange Patterns ）

- 请求/应答
- 单程
- 请求/回调
- 发布/订阅

SOAP[edit]

The term "Message Exchange Pattern" has a specific meaning within the SOAP protocol.[2][3] SOAP MEP types include:
In-Only: This is equivalent to one-way. A standard one-way messaging exchange where the consumer sends a message to the provider that provides only a status response.
Robust In-Only: This pattern is for reliable one-way message exchanges. The consumer initiates with a message to which the provider responds with status. If the response is a status, the exchange is complete, but if the response is a fault, the consumer must respond with a status.

In-Out: This is equivalent to request-response. A standard two-way message exchange where the consumer initiates with a message, the provider responds with a message or fault and the consumer responds with a status.
In Optional-Out: A standard two-way message exchange where the provider's response is optional.

Out-Only: The reverse of In-Only. It primarily supports event notification. It cannot trigger a fault message.
Robust Out-Only: similar to the out-only pattern, except it can trigger a fault message. The outbound message initiates the transmission.

Out-In: The reverse of In-Out. The provider transmits the request and initiates the exchange.

Out-Optional-In: The reverse of In-Optional-Out. The service produces an outbound message. The incoming message is 
optional ("Optional-in").


ØMQ[edit]

The ØMQ message queueing library provides a so-called sockets (a kind of generalization over the traditional IP and Unix sockets) which require to indicate a messaging pattern to be used, and are particularly optimized for that kind of patterns. The basic ØMQ patterns are:[4]
Request-reply connects a set of clients to a set of services. This is a remote procedure call and task distribution pattern.[clarification needed]
Publish-subscribe connects a set of publishers to a set of subscribers. This is a data distribution pattern.[clarification needed]
Push-pull connects nodes in a fan-out / fan-in pattern that can have multiple steps, and loops. This is a parallel task distribution and collection pattern.[clarification needed]
Exclusive pair connects two sockets in an exclusive pair. This is a low-level pattern for specific, advanced use cases.
Each pattern defines a particular network topology. Request-reply defines so-called "service bus", publish-subscribe defines "data distribution tree", push-pull defines "parallelised pipeline". All the patterns are deliberately designed in such a way as to be infinitely scalable and thus usable on Internet scale. [5]