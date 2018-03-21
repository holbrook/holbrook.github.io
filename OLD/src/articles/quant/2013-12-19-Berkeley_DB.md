---
layout: post
title: "使用Oracle Berkeley DB持久化股票行情数据"
description: ""
category: 量化金融
tags: [交易系统, NoSQL]
---

# 关系数据库，数据文件 还是 NoSQL

股票行情数据具有如下特点：

1. 数据量大

   对于分析来说，至少需要5分钟数据。如果每天交易时间为4小时，每年250个交易日，则一支股票一年的行情数据量为60/5*4*250= 12k。20年则为240k。如果是1分钟数据，则20年的数据量为240k*5 = 1.2M。

   所以，如果用于分析，行情数据将是百万量级。如果记录3000只股票/指数的数据，数据量会非常大。

2. 数据很少变化

   由于都是历史数据，行情数据很少需要修改。主要的操作是查询和增加。

3. 数据结构简单

   主要考虑[成交数据](/2013/12/18/quotation_model.html#menuIndex2)，是一种简单的一维结构。价格数据只在发生交易信号时有一定的参考意义，不需要保留所有的历史记录。

由于行情数据的这些特点，通常不适合使用关系数据库。传统上一般采用数据文件进行存储。

但是用数据文件需要自己处理写入锁，随机读写，序列化等问题，比较麻烦。于是[NoSQL](/2013/12/18/nosql_list.html#menuIndex1)成了比较好的一种选择。

对于单机的分析软件，[NoSQL选型要素](/2013/12/18/nosql_list.html#menuIndex2)为：

- key/value儲存
- 支持持久化
- 支持嵌入式
- 接口方便

# Oracle Berkeley DB

[Berkeley DB](http://www.oracle.com/technetwork/cn/products/berkeleydb/overview/index.html)是满足上述4点要求的比较好的一款产品。Berkeley DB分为BDB、BDB Java版和BDB XML版。其总体架构如下图：

![Berkeley DB](images/trade-system/berkeley-db.png)

BDB的三个版本的功能不完全相同。


我选择BDB Java版，不支持SQL API和XQuery API，可以使用底层的键/值API、Java 直接持久层 (DPL) API和Java 集合 API。三种API的应用场景如下：


- 当 Java 类是用来代表应用中的域对象(domain objects),也就是说,该模式是相对 稳定的,建议用直接持久层。
- 当在Berkeley DB和Berkeley DB Java 版之间移植应用程序时,或当实现自己的 动态模式(举例来说,一个 LDAP 服务器),那么建议用基础 API。您也可能喜欢使用这 个基础API如果您有极少数域类(domain class)。
- 集合API有利于和外部组件交互,因为它遵从Java集合框架标准。继而,和基础API 以及直接持久层结合后会很有用。您可能会喜欢这个 API,因为它提供了熟悉的 Java 集 合接口。

在行情数据的持久化中，可以选用直接持久层（DPL）。直接持久层API 可以持久化以及还原相互关联的 Java 对象，但是比ORM更加简单高效。

# 实现过程

## 获取开发包

可以从[这里](http://www.oracle.com/technetwork/cn/products/berkeleydb/downloads/index.html)下载需要的jar包，也可以使用maven：

{% highlight xml %}

<dependency>
      <groupId>com.sleepycat</groupId>
      <artifactId>je</artifactId>
      <version>5.0.73</version>
</dependency>

{% endhighlight %}

如果要使用最新版（目前的最新版是5.0.97），需要引入oracle的maven库：

{% highlight xml %}
<repositories>
    <repository>
      <id>oracleReleases</id>
      <name>Oracle Released Java Packages</name>
      <url>http://download.oracle.com/maven</url>
      <layout>default</layout>
    </repository>
</repositories>
{% endhighlight %}


## 定义持久化模型

### 实体和值对象

Berkeley DB支持DDD(领域驱动设计)中的实体和值对象的持久化。

- 实体：拥有长期不变的标识符,可以被跟踪的对象。
- 值对象：没有标识符，主要关注其属性的对象。

在BDB中，分别使用 **@Entity** 和 **@Persistent** 来声明实体和值对象。
声明了 **@Persistent** 的对象可以直接作为 **@Entity** 对象中的属性使用。

任何Java类一旦增加了持久化声明，其所有字段（任何作用域）都会被持久化。需要持久化的类需要缺省的无参数构造函数。

比如：


{% highlight java %}

@Entity
public class Transaction {
	……
	public OHLC ohlc;
	……
}


@Persistent
public class OHLC {
	public float open,high,low,close;
}

{% endhighlight %}


### 主键和“次键”声明

每个实体类(@Entity)可以定义一个主键(PrimaryKey)和多个次键(SecondaryKey)，从而可以按照主键或次键进行索引。例如：

{% highlight java %}

@Entity
public class Security implements Instrument{
	@PrimaryKey
	private String code;

	@SecondaryKey(relate=Relationship.ONE_TO_ONE)
	private String name;
	……
}
{% endhighlight %}

### 关联关系

关联关系也是通过次键(SecondaryKey)声明的。需要同时指定多重性（relate）和关联到的实体（relatedEntity）。
relate可以是ONE_TO_ONE,ONE_TO_MANY,MANY_TO_ONE或MANY_TO_MANY(在com.sleepycat.persist.model.Relationship中定义)。

需要注意的是，次键的属性类型需要是relatedEntity指定的对端实体的主键类型，而不能直接使用对端实体。

如果relate是ONE_TO_MANY或MANY_TO_MANY，可以使用集合类型。比如（不属于股票行情数据模型，而是BDB官方例子）：

{% highlight java %}

@Entity
class Employer {
    @PrimaryKey(sequence="ID")
    long id;

	@SecondaryKey(relate=ONE_TO_ONE) String name;
	……
}


@Entity
class Person {
    @PrimaryKey
    String ssn;

	@SecondaryKey(relate=MANY_TO_ONE, relatedEntity=Person.class)
	String parentSsn;

	@SecondaryKey(relate=ONE_TO_MANY)
	Set<String> emailAddresses = new HashSet<String>();

	@SecondaryKey(relate=MANY_TO_MANY, relatedEntity=Employer.class, onRelatedEntityDelete=NULLIFY)
	Set<Long> employerIds = new HashSet<Long>();
	……
}

{% endhighlight %}



## 使用DPL API

### 设计Accessor(TODO)

类似于DAO，BDB中通常将对实体的访问封装到Accessor中。例如：

1. EntityStore

2. 获取索引

3. CRUD

4. 访问关联对象

通过索引可以得到关联的对象，无论是单个关联对象还是集合。

- 关联到单个对象
- 关联到集合

{% highlight java %}
EntityCursor<Person> employees = dao.personByEmployerIds.subIndex(gizmoInc.id).entities();
try {
    for (Person employee : employees) {
System.out.println(employee.ssn + ' ' + employee.name); }
} finally {
    employees.close();
}
{% endhighlight %}

- 等值连接

通过 EntityJoin 类可以进行等值连 接(equality join)操作。

比如，以下代码查询所有Bob的孩子中为gizmo公司工作的 员工:

{% highlight java %}
EntityJoin<String,Person> join = new EntityJoin(dao.personBySsn);
join.addCondition(dao.personByParentSsn, "111-11-1111"); join.addCondition(dao.personByEmployerIds, gizmoInc.id);
ForwardCursor<Person> results = join.entities(); try {
for (Person person : results) { System.out.println(person.ssn + ' ' + person.name);
}
} finally {
    results.close();
}
{% endhighlight %}

### 建立连接

### 事务支持

{% highlight java %}
Transaction txn = env.beginTransaction(null, null); dao.employerById.put(txn, gizmoInc); dao.employerById.put(txn, gadgetInc);
txn.commit();
{% endhighlight %}

### 模型变化

对于增加实体或值对象的属性，改变属性类型等变化，一般不需要对BDB进行额外的处理，而是会自动适应。

对于一些特殊的、无法自动适应的变化，比如重命名字段或优化单个的类(如:使用通用类型,模块复用等改变),可以使用Mutations。

Mutations 操作是延迟的:只在存取数据时自动改变,故避免了软件升级时大型数据库转换导致的长时间停机。
复杂的类优化可能涉及到多个类,使用 ConversionStore 进行。因而,无论持久化类作出何种 改变,直接持久层都始终提供可靠数据存取。

### 性能选项

Berkeley DB在API的很多地方提供了性能调优的选项。常见的包括：

- DatabaseConfig参数

  通过DatabaseConfig参数可以用来调整Berkeley DB引擎的性能。
  比如,可指定内部B树节点的大小来调整性能,通过如下方式来指定:
{% highlight java %}
    DatabaseConfig config = store.getPrimaryConfig(Employer.class);
    config.setNodeMaxEntries(64);
    store.setPrimaryConfig(config);
{% endhighlight %}

- CRUD操作参数

  例如, “脏读”可通过LockMode参数实现:


    Employer employer = employerByName.get(null, "Gizmo Inc", LockMode.READ_UNCOMMITTED);




