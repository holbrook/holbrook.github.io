---
layout: post
title: "Blueprint: OSGi的依赖注入(DI)容器"
description: "曾几何时，你在Spring和OSGi之间摇摆不定；曾几何时，你对SpringDM感到迷惑不解。你是否向往OSGi的动态特性，又为遗留代码（尤其是基于Spring的代码）感到不舍？现在，这些都不再是问题！"
category: 软件开发
tags: [OSGi, maven]
lastmod: 
---



曾几何时，你在Spring和OSGi之间摇摆不定；曾几何时，你对SpringDM感到迷惑不解。
你是否向往OSGi的动态特性，又为遗留代码（尤其是基于Spring的代码）感到不舍？

现在，这些都不再是问题！

在[OSGi Service Platform Release 4](http://www.osgi.org/Release4/HomePage) V4.2中，
提到了很多的[企业级规范(Enterprise Specification)](http://www.osgi.org/download/r4v42/r4.enterprise.pdf)，
其中包括了规范121：Blueprint容器规范(Container Specification)。

Buleprint容器规范规定了一个OSGi容器(不是OSGi rumtime)的方方面面：

![](/images/fuse/Blueprint_Container_Specification_list.png)

Buleprint(或者说，OSGi Enterprise)目前有两个主要的实现：[Eclipse Gemini](http://www.eclipse.org/gemini/)和[Apache Aries](http://aries.apache.org/)。

其中Gemini的代码最初来自Spring DM，其实Blueprint规范的最早版本也来自Spring；而Aries已经用在Apache的众多企业级产品中。

在本文中，使用Aries Blueprint。

# 依赖注入

Blueprint Container 规范为 OSGi 定义了一个 依赖性注入（DI,Dependency Injection）框架，可以处理OSGi 的动态特性。
与[OSGi服务](/2014/01/12/dependency_injection_in_e4.html#menuIndex2)或[OSGi Declarative Service](/2014/01/12/dependency_injection_in_e4.html#menuIndex3)，不同，Blueprint依赖注入可以处理POJO对象的装配，使得POJO能够在OSGi中跨bundle访问。

这与[JSR330:Java依赖注入规范](http://thinkinside.tk/2013/12/31/jsr330.html)很像，是该规范在OSGi环境下的扩展。
这也就是Spring DM(Spring Dynamic Modules)干的事情。实际上，Buleprint容器规范最初就来自于Spring，
而其Gemini实现更是来自SpringDM的捐赠。

无奈，如今[Spring已经宣布放弃OSGi](http://www.infoq.com/cn/news/2012/11/spring-osgi-gradle)正所谓造化弄人，让人唏嘘不已。


# Blueprint XML

Blueprint使用XML文件描述装配关系，下面是一个例子：

```
 <?xml version="1.0" encoding="UTF-8" standalone="no"?>
 <blueprint xmlns="http://www.osgi.org/xmlns/blueprint/v1.0.0">

   <!-- Bean Manager Examples -->

   <bean id="accountOne" class="org.apache.aries.samples.Account">
       <argument value="1"/>
       <property name="description" value="#1 account"/>
   </bean>

   <bean id="accountTwo" class="org.apache.aries.samples.StaticAccountFactory" 
         factory-method="createAccount">   
       <argument value="2"/>
       <property name="description" value="#2 account"/>     
   </bean>

   <bean id="accountFactory" class="org.apache.aries.samples.AccountFactory">  
       <argument value="account factory"/>      
   </bean>

   <bean id="accountThree"
         factory-ref="accountFactory" 
         factory-method="createAccount">   
       <argument value="3"/>
       <property name="description" value="#3 account"/>      
   </bean>

   <bean id="prototypeAccount" class="org.apache.aries.samples.Account"
         scope="prototype">
       <argument value="4"/>
   </bean>

   <bean id="singletonAccount" class="org.apache.aries.samples.Account"
         scope="singleton">
       <argument value="5"/>
   </bean>

   <bean id="accountFour" class="org.apache.aries.samples.Account" 
         init-method="init" destroy-method="destroy">
       <argument value="6"/>
       <property name="description" value="#6 account"/> 
   </bean>



   <!-- Service Manager Examples -->

   <bean id="myAccount" class="org.apache.aries.samples.MyAccount">
       <argument value="7"/>
       <property name="description" value="MyAccount"/> 
   </bean>

   <service id="serviceOne" ref="myAccount" interface="java.io.Serializable"/>

   <service id="serviceTwo" ref="myAccount">
      <interfaces>
          <value>java.io.Serializable</value>
      </interfaces>
   </service>

   <service id="serviceThree" ref="myAccount" auto-export="all-classes"/>

   <service id="serviceFour" ref="myAccount" auto-export="all-classes">
      <service-properties>
          <entry key="mode" value="shared"/>
          <entry key="active">
              <value type="java.lang.Boolean">true</value>
          </entry>
      </service-properties>
   </service>

   <service id="serviceFive" ref="myAccount" auto-export="all-classes" ranking="3"/>

   <service id="serviceSix" ref="myAccount" auto-export="all-classes">
      <registration-listener 
              registration-method="register" unregistration-method="unregister">
          <bean class="org.apache.aries.samples.RegistrationListener"/>         
      </registration-listener>
   </service>



   <!-- Service Reference Manager Examples -->

   <reference-list id="serviceReferenceListTwo" interface="java.io.Serializable" 
                   availability="optional">
      <reference-listener 
              bind-method="bind" unbind-method="unbind">
          <bean class="org.apache.aries.samples.ReferenceListener"/>        
      </reference-listener>
   </reference-list>



   <!-- Environmental Manager Example -->

   <bean id="accountManagerOne" class="org.apache.aries.samples.AccountManager">
      <property name="managerBundle" ref="blueprintBundle"/>
   </bean>



   <!-- Object Values Examples -->

   <bean id="accountManagerTwo" class="org.apache.aries.samples.AccountManager">
       <property name="managedAccount">
           <ref component-id="accountOne"/>
       </property>
   </bean>

   <bean id="accountManagerThree" class="org.apache.aries.samples.AccountManager">
       <property name="managedAccount">
           <bean class="org.apache.aries.samples.Account">
               <argument value="10"/>
               <property name="description" value="Inlined Account"/> 
           </bean>
       </property>
   </bean>

   <bean id="accountManagerFour" class="org.apache.aries.samples.AccountManager">             
       <property name="accountNumbers">
           <list>
               <value>123</value>
               <value>456</value>
               <value>789</value>
           </list>
       </property>
   </bean>

 </blueprint>

```
可以看出，这个文件与Spring的配置文件非常类似。

Blueprint XML中可以标记`bean`，`service`、`reference-list`等元素，用于bean管理、service管理和service引用管理。

![](/images/fuse/blueprint_config.png)

- Bean管理

  通过`<bean>`标签定义Bean，容器可以创建bean、设置属性。bean的创建可以基于构造函数、静态工厂或工厂方法；属性可以是基本类型，也可以引用其他的bean。可以设置bean的scope为singleton或prototype。

- Service管理
  
  bean只能在当前bundle中使用。要跨bundle引用，必须定义服务。服务可以依赖bean或其他服务。

  服务管理用于在OSGi服务注册表中注册服务。容器会根据服务的依赖关系是否满足，自动注册或注销服务。

- Service引用管理

  通过`<reference>`和`<reference-list>`标签可以引用其他bundle中发布的服务。两个标签分布用于引用单个服务和引用服务列表。

一个bundle可以有一个或多个xml配置，通常位于`OSGI-INF/blueprint/`目录下，也可以在`META-INF/MANIFEST.MF`文件中通过
`Bundle-Blueprint`属性进行指定。

更多关于Blueprint XML配置的内容和例子，可以参考[Apache Aries官方的例子](http://aries.apache.org/documentation/tutorials/blueprinthelloworldtutorial.html)，以及[developerWorks上的这篇文章](https://www.ibm.com/developerworks/cn/opensource/os-osgiblueprint/)

# 工作原理


Blueprint Container 使用扩展器（extender）模式，监视OSGi框架中的bundle的状态。当新的bundle被激活时，
Blueprint根据该bundle是否有Blueprint XML配置文件判断是否需要容器进行处理。

处理的过程是为该bundle创建一个容器，通过容器解析XML文件，并将组件装配到一起。如果bundle中的服务依赖得到满足，容器还会调用[OSGi DS](/2014/01/12/dependency_injection_in_e4.html#menuIndex3)发布服务。

在停止bundle时，也会进行相反的销毁过程。

# 在Eclipse中运行和调试

可以在前面[通过maven手工创建Felix运行环境](/2014/01/21/tycho_vs_maven_bundle_plugin.html#menuIndex2)的基础上，
增加Blueprint需要的bundle:

```
	<!-- for aries blueprint -->
	<artifactItem>
		<groupId>org.apache.aries.blueprint</groupId>
		<artifactId>org.apache.aries.blueprint</artifactId>
		<version>1.1.0</version>
	</artifactItem>
	<artifactItem>
		<groupId>org.apache.aries.proxy</groupId>
		<artifactId>org.apache.aries.proxy</artifactId>
		<version>1.0.1</version>
	</artifactItem>
	<artifactItem>
		<groupId>org.apache.aries</groupId>
		<artifactId>org.apache.aries.util</artifactId>
		<version>1.1.0</version>
	</artifactItem>
	<artifactItem>
		<groupId>org.apache.felix</groupId>
		<artifactId>org.apache.felix.configadmin</artifactId>
		<version>1.2.4</version>
	</artifactItem>
	<artifactItem>
		<groupId>org.ops4j.pax.logging</groupId>
		<artifactId>pax-logging-api</artifactId>
		<version>1.4</version>
	</artifactItem>
	<artifactItem>
		<groupId>org.ops4j.pax.logging</groupId>
		<artifactId>pax-logging-service</artifactId>
		<version>1.4</version>
	</artifactItem>
```

# 使用Apache Felix Karaf

自己搭建的Felix+Blueprint环境功能很有限，比如缺失了很多必要的基础组件和管理功能。更好的选择是使用[Apache Felix Karaf](http://karaf.apache.org/)。

Karaf在Felix和Blueprint的基础上，还增加了一些插件，以提供认证和登录、热部署、动态配置、控制台以及一些管理功能。

更贴心的是，Karaf还提供了Eclipse插件：[Eclipse Integration for Karaf (EIK)](http://karaf.apache.org/index/subprojects/eik.html)，从而可以：

- Custom Eclipse perspective for Apache Karaf development:
  + places valuable Karaf runtime information in one location
- Apache Karaf installation management in your workspace:
  + Karaf installations are managed as workspace projects giving the developer visibility in to the runtime 
  + each Karaf installation is automatically synchronized with your workspace, including additional bundles, configuration files
- Run and debug Karaf installations with a single Eclipse Launcher:
  + the launch configuration allows developers to fine tune how Karaf will launch
- Automatic deployment of workspace plugin projects:
  + create plugin-projects and have them deployed automatically
- Advanced instrumentation of the running Karaf instance:
  + watch bundles deploy in real time and examine the OSGi service registry from within the Eclipse IDE
- Access Eclipse platform IDE plugins from within a running Karaf instance:
  + all Eclipse plugins are presented as an OBR

