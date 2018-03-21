---
layout: post
title: "基于Java代码配置Spring容器"
description: "Spring支持用Java代码配置"
category: 软件开发
tags: [spring]
lastmod: 
---


[前面](/2013/12/31/jsr330.html)，用[JSR330](https://jcp.org/en/jsr/detail?id=330)
中规定的annotation定义了对象之间的依赖关系和注入机制，
但是仍然使用了一个[xml配置](/2013/12/31/jsr330.html#menuIndex4)，用于初始化ApplicationContext。

该例子中使用`GenericXmlApplicationContext`创建应用上下文。实际上，Spring提供了很多种应用上下文：

![ApplicationContext](/images/spring/ApplicationContext.png)

使用其中的AnnotationConfigApplicationContext，可以不依赖xml配置文件，而是用java代码的方式初始化应用上下文。


应用配置类中要记录与xml配置文件中相同的要素。

[前面的例子]((/2013/12/31/jsr330.html#menuIndex4))中，xml主要定义了以下内容：

```
<!--启用annotation注册-->
<context:annotation-config/>
<!--扫描指定的包中用annotation定义的bean-->
<context:component-scan base-package="org.example"/>
```

使用Java类可以实现通用的功能：

```
@Configuration
public class AppConfig {
	@Bean
	public String message() {
		return "You are running JSR330!";
	}
}
```

其中，

- @configuration表明这个类包含Bean的定义
- @Bean标记创建bean的函数。其中函数名相当于beanID

此时，可以不依赖xml文件使用bean，前提是使用AnnotationConfigApplicationContext创建应用上下文：

```
public static void main(String[] args) {
	AnnotationConfigApplicationContext ctx = 
			new AnnotationConfigApplicationContext(AppConfig.class);
	
	ctx.scan("demo");    
	
	MessageRenderer renderer = ctx.getBean("messageRenderer",
			MessageRenderer.class);
	renderer.render();
	ctx.close();
}
```	

同样，在Spring Web应用中也可以使用`AnnotationConfigWebApplicationContext`来代替`XmlWebApplicationContext`。

关于spring基于Java代码配置容器的更多内容，可以参考[官方文档](http://docs.spring.io/spring/docs/3.0.x/spring-framework-reference/html/beans.html#beans-java)。
