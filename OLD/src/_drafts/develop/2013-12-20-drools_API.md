---
layout: post
title: "Drools规则引擎API概述"
description: "与此对应，规则引擎API也分成三个部分。在Drools中，分别叫做Knowledge API，Fact API和Execution API。"
category: 软件开发
tags: [规则引擎]
lastmod: 
---


[如前所述](/2012/03/20/rule_engine_1.html)，
规则引擎中，将知识表达为规则（rules），要分析的情况定义为事实（facts）。二者在内存中的存储分别称为Production Memory和Working Memory。在外围，还会有一个执行引擎（Execution Engine）。

与此对应，规则引擎API也分成三个部分。在Drools中，分别叫做Knowledge API，Fact API和Execution API。


# Knowledge API

Drools将知识库(KnowledgeBase)作为[JSR94](/2012/12/07/jsr94.html)中的规则执行集(RuleExecutionSet)。知识库中的知识以包(KnowledgePackage)为单位组合而成。每个包中聚合多个规则(Rule)。

通常，一个包中的内容会在一个或多个资源(Resource)中保存。资源的类型可以有很多种,如.drl 文件、.dslr 文件或 xls 文件等。

规则包还可以从规则流(rule flow) 文件中获取。


![KnowledgeBase](/images/rule-engine/KnowledgeBase.png)

与此对应，Drools定义了一组Knowledge API来操作知识库。

![KnowledgeBase](/images/rule-engine/KnowledgeAPI.png)

构建知识库的一般过程为：

1. 通过ResourceFactory获取资源。可以从Classpath、URL、File、ByteArray、Reader等输入源中获取
2. 构建KnowledgeBuilder，将资源添加到KnowledgeBuilder中。KnowledgeBuilder通常由KnowledgeBuilderFactory创建
3. 从KnowledgeBuilder中获取规则包
4. 创建KnowledgeBase，可以通过KnowledgeBaseConfiguration定义KnowledgeBase的一些属性，默认的配置位于drools-core-VERSION.jar 包下 META-INF/drools.default.rulebase.conf 文件中
5. 将规则包添加到KnowledgeBase
6. 为KnowledgeBase添加KnowledgeBaseEventListener，可以监控KnowledgeBase中的事件

代码示例：

{% highlight java %}

	KnowledgeBase buildKBase(){
		
		Resource res = ResourceFactory.newClassPathResource("hello.drl", Demo.class);
		
		KnowledgeBuilder kbuilder = KnowledgeBuilderFactory
				.newKnowledgeBuilder();

		kbuilder.add(res,ResourceType.DRL);
		
		//validate
		if (kbuilder.hasErrors()) {
			System.out.println("规则中存在错误,错误消息如下:");
			KnowledgeBuilderErrors kbuidlerErrors = kbuilder.getErrors();
			for (Iterator iter = kbuidlerErrors.iterator(); iter.hasNext();) {
				System.out.println(iter.next());
			}
		}
		
		Collection<KnowledgePackage> kpackages = kbuilder.getKnowledgePackages();
		
		KnowledgeBaseConfiguration kbConf =
				KnowledgeBaseFactory.newKnowledgeBaseConfiguration(); 
		kbConf.setProperty( "org.drools.sequential", "true"); 
		
		//KnowledgeBase kbase=KnowledgeBaseFactory.newKnowledgeBase();
		KnowledgeBase kbase =
				KnowledgeBaseFactory.newKnowledgeBase(kbConf);
		
		kbase.addKnowledgePackages(kpackages);
		
		return kbase;
	}


{% endhighlight %}

# Fact API

要操作Working Memory，首先要建立规则引擎的一个会话。Drools中的有状态会话和无状态会话分别为StatefulKnowledgeSession和StatelessKnowledgeSession，都可以由KnowledgeBase建立。

通过会话可以进行操作Fact对象，执行规则等交互，例如：

{% highlight java %}

KnowledgeBase kbase = buildKBase();
		
StatefulKnowledgeSession statefulKSession=kbase.newStatefulKnowledgeSession();
statefulKSession.setGlobal("globalTest", new Object());

statefulKSession.insert(new Object()); 
statefulKSession.fireAllRules(); 
statefulKSession.dispose();

{% endhighlight %}

StatefulKnowledgeSession中，insert()方法、fireAllRules()方法和 dispose()方法是分开执行的，这个过程中可以进行一定的控制，
而StatelessKnowledgeSession不同，在无状态会话中，上述三个方法被合并为execute()方法，不能分开调用。如果要插入多个Fact对象，只能使用集合，比如：

{% highlight java %}
StatelessKnowledgeSession statelessKSession=kbase.newStatelessKnowledgeSession();
ArrayList list=new ArrayList(); 
list.add(new Object()); 
list.add(new Object()); 
statelessKSession.execute(list);

{% endhighlight %}

这样的特点决定了，无状态会话适合推演和分析，需要事先知道所有的事实(Fact)；而有状态会话可以随时增加事实并进行批评，适合实际应用。

无状态会话中还可以使用execute(Command cmd)方法。比如，如果要在无状态会话中插入一个List，可以用CommandFactory生成一个关于List的Command:

{% highlight java %}
statelessKSession.execute(CommandFactory.newInsert(list));
{% endhighlight %}

同样，无状态会话中如果要设置global，也需要使用Command:

{% highlight java %}
ArrayList<Command> list=new ArrayList<Command>(); 

list.add(CommandFactory.newInsert(new Object())); 
list.add(CommandFactory.newInsert(new Object())); 

list.add(CommandFactory.newSetGlobal("key1", new Object())); 
list.add(CommandFactory.newSetGlobal("key2", new Object()));

statelessKSession.execute(CommandFactory.newBatchExecution(list)) ;
{% endhighlight %}


# Execution API

插入到WorkingMemory中的对象，并不是克隆，而是对原对象的引用。这就意味着引擎中可以改变外部的对象，这是引擎与外部数据交互的一个通道。

此外，insert()方法还会返回一个FactHandler，作为引擎中该Fact对象的一个句柄。

最后，session上可以注册AgendaEventListener、ProcessEventListener和WorkingMemoryEventListener，这也是常用的交互方式。
比如WorkingMemoryEventListener可以监听Fact对象变化的事件：

{% highlight java %}
public interface WorkingMemoryEventListener
    extends
    EventListener {
    void objectInserted(ObjectInsertedEvent event);

    void objectUpdated(ObjectUpdatedEvent event);

    void objectRetracted(ObjectRetractedEvent event);
}

{% endhighlight %}