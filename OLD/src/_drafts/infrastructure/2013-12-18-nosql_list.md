---
layout: post
title: "NoSQL数据库选型指引"
description: ""
category: 基础设施
tags: [NoSQL]
lastmod: 
---

# 什么是NoSQL

NoSQL可以有两种解释：

- No SQL：“不使用SQL查询语言”。强调其轻量的特点
- Not Only SQL：”不仅仅是查询“。强调其高性能，分布式，大容量等传统关系数据库所不具备的特性

从设计原则上，NoSQL不再强调ACID（酸），而是强调BASE（碱）。

ACID是指：

- atomicity（原子性）：一个事务中的所有操作，要么全部完成，要么全部不完成。如果中途发生错误需要回滚（Rollback）
- consistency(一致性)：在事务开始之前和事务结束以后，数据库的完整性没有被破坏。這表示寫入的資料必須完全符合所有的預設規則，這包含資料的精確度、串聯性以及後續数据库可以自發性地完成預定的工作。
- isolation(隔離性)：当两个或者多个事务并发访问（此处访问指查询和修改的操作）数据库的同一数据时所表现出的相互关系。事务隔离分为不同级别，包括读未提交（Read uncommitted）、读提交（read committed）、可重复读（repeatable read）和串行化（Serializable）
- durability(持久性)：在事务完成以后，该事务对数据库所作的更改便持久地保存在数据库之中，并且是完全的


BASE是指：

- Basically Available（基本可用）
- Soft-state（软状态/柔性事务）
- Eventually Consistent（最终一致性）


NoSQL与关系数据库的原则不同：NoSQL牺牲高一致性，换取获得可用性或可靠性。软状态意味着状态是异步的，在某些时段状态是不一致的；但最终一致保证数据早晚会一致。


# NoSQL选型要素

1. 存储结构

   由于NoSQL的目的和原则的不同，NoSQL中的数据不是按照表存储。根据NoSQL存储结构的不同，可以分为：

   - 文档存储
   - 图存储
   - key/value儲存
   - 列存储
   - 对象数据库

2. 是否持久化
   
   有的NoSQL是纯内存存储，不支持持久化

3. 是否支持嵌入式
4. 是否支持集群部署
5. 操作接口的丰富程度


# 常见的NoSQL数据库

- 文档数据库

<table>
<th><td>名称</td><td>持久化</td><td>部署方式</td><td>操作接口</td><td>备注</td></th>
<tr><td>CouchDB</td><td></td><td>分布式</td><td>JavaScript MapReduce, RESTful JSON API</td><td>HTTP访问，内置了Web管理控制台</td></tr>
<tr><td>JackRabbit</td><td></td><td></td><td>Java</td><td></td></tr>
<tr><td>Lotus Notes</td><td></td><td></td><td>LotusScript, Java</td><td></td></tr>
<tr><td>BaseX</td><td></td><td></td><td></td><td>XQuery, Java</td><td></td></tr>
<tr><td>MongoDB</td><td></td><td>服务，集群</td><td>PHP，Python，Perl，Ruby，JavaScript，C++等</td><td>JSON数据库，支持全文索引，自动分片，跨LAN或WAN扩展</td></tr>
</table>

- 图形数据库

<table>
<th><td>名称</td><td>持久化</td><td>部署方式</td><td>操作接口</td><td>备注</td></th>
<tr><td>Neo4j</td><td></td><td></td><td>Java</td><td></td></tr>
<tr><td>DEX</td><td></td><td></td><td>Java , C#</td><td></td></tr>
<tr><td>AllegroGraph</td><td></td><td></td><td>SPARQL</td><td></td></tr>
<tr><td>FlockDB</td><td></td><td></td><td>Scala</td><td></td></tr>
</table>

- key/value数据库

<table>
<th><td>名称</td><td>持久化</td><td>部署方式</td><td>操作接口</td><td>备注</td></th>
<tr><td>BigTable</td><td></td><td></td><td></td><td></td></tr>
<tr><td>memcached</td><td></td><td></td><td></td><td></td></tr>
<tr><td>Redis</td><td></td><td></td><td></td><td></td></tr>
<tr><td>Oracle Berkeley DB</td><td></td><td></td><td></td><td></td></tr>
</table>



- 列数据库

<table>
<th><td>名称</td><td>持久化</td><td>部署方式</td><td>操作接口</td><td>备注</td></th>
<tr><td>Cassandra</td><td></td><td></td><td></td><td></td></tr>
<tr><td>HBase</td><td></td><td></td><td></td><td></td></tr>
<tr><td>Hypertable</td><td></td><td></td><td></td><td></td></tr>
</table>

- 对象数据库

<table>
<th><td>名称</td><td>持久化</td><td>部署方式</td><td>操作接口</td><td>备注</td></th>
<tr><td>db4o</td><td></td><td></td><td></td><td></td></tr>
<tr><td>iBoxDB</td><td></td><td></td><td></td><td></td></tr>
<tr><td>JADE</td><td></td><td></td><td></td><td></td></tr>
<tr><td>ZODB</td><td></td><td></td><td></td><td></td></tr>
<tr><td>ObjectStore</td><td></td><td></td><td></td><td></td></tr>
</table>