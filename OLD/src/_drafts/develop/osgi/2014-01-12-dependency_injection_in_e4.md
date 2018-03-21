---
layout: post
title: "Eclipse e4：从OSGi-DS到依赖注入"
description: "e4开始，可以不使用代码或xml进行服务注册和寻找，而使用依赖注入进行装配"
category: 软件开发
tags: [OSGi]
lastmod: 
---



# MANIFEST.MF

为了管理一组Java类和资源，通常我们会将其打包为JAR(Java Archive File，java存档文件)，该文件以ZIP格式进行打包。
在JAR文件中，会包含一个`META-INF/MANIFEST.MF`文件，作为该JAR包的清单文件，设置执行入口类和支持库的路径等信息。
主要内容包括：

- Manifest-Version
- Class-Path
- Created-By
- Main-Class

# OSGi bundle

OSGi的目标是实现Java应用的模块化，其目标是：

- 将程序封装成一个个的模块(在OSGi中叫做bundle)
- 模块向外只暴露特定的接口，内部实现对外不可见
- OSGi容器管理模块的接口，包括服务发布、寻找和版本管理等
- OSGi容器管理模块的生命周期，比如启动、停止、热插拔等


OSGi将每个模块打包为一个JAR文件。为了实现上述目标，
OSGi规范利用了`MANIFEST.MF`文件，在其中增加了一些bundle的描述信息，比如：

- Bundle-ManifestVersion
- Bundle-Name
- Bundle-SymbolicName
- Bundle-Version
- Bundle-ClassPath
- Bundle-Vendor
- Bundle-Localization
- Bundle-RequiredExecutionEnvironment
- Export-Package
- Require-Bundle
- Bundle-Activator
- Bundle-ActivationPolicy
- Import-Package

# OSGi服务的注册和寻找

OSGi模块中，只有`Export-Package`中声明的包才可以被其他模块访问。为了避免一个模块对其他模块的直接引用，
通常会实现一个“接口定义”模块和多个“接口实现”模块。通过服务注册和发现的方式进行服务的使用。

OSGi还可以为模块指定一个"激活类(`Bundle-Activator`)“，
这个类会在模块启动时被执行，通常在这里进行本模块的接口实现(服务)的发布，以及向本模块内的类注入其他模块实现的接口(服务).
比如：

```
public class MyActivator implements org.osgi.framework.BundleActivator{ 

	@Override
	public void start(BundleContext context) throws Exception { 
		context.registerService(MyService.class.getName(), new MyServiceImpl(), null);
		System.out.println(MyService.class.getName() + " has been registred as a service");
	}
	……
}
```

这样，其他使用该服务的模块可以寻找服务。通常，也是在"激活类(`Bundle-Activator`)“中进行：

```
public class ClientActivator implements BundleActivator{          
	public static MyService helloService;         

	@Override         
	public void start(BundleContext context) throws Exception {
		ServiceReference ref = context.getServiceReference(MyService.class.getName());                  
		MyService service = (MyService) context.getService(ref);             
		MyClient.setService(service);         
	}
	……
}

```


# Declarative Service

上面通过代码的方式进行服务的注册和寻找，实现起来比较繁琐。为了简化编码，从OSGi4.0版本开始，提出了”Declarative Service“标准，
使用xml文件进行服务发布和引用的描述。

首先，在`MANIFEST.MF`文件中增加一个新的属性`Service-Component`，用来指定服务声明文件的路径，比如：
```
Service-Component: OSGI-INF/component.xml
```

然后编写服务声明配置：

```
	<?xml version="1.0" encoding="UTF-8"?>
	<scr:component xmlns:scr="http://www.osgi.org/xmlns/scr/v1.1.0" name="myservice">
		<implementation class="MyServiceImpl"/>
		<service>
			<provide interface="MyService"/>
		</service>
	</component> 
```

该文件中也可以配置服务引用：

```
	 <reference bind="setMyService" cardinality="1..1" interface="MyService" name="myservice" policy="static" unbind="unsetMyService"/>
```

可以用如下的代码使用所引用的服务：

```
// Method will be used by DS to set the service
  public synchronized void setMyService(MyService service) {
    System.out.println("Service was set. Thank you DS!");
    this.service = service;
  }

  // Method will be used by DS to unset the service
  public synchronized void unsetMyService(MyService service) {
    System.out.println("Service was unset.");
    if (this.service == service) {
      this.service = null;
}
```


# e4中的依赖注入

Declarative Service的方式与Spring的服务组装很类似。但是Spring中已经开始[使用注解代替繁琐的XML配置](/2014/01/05/spring_annotations.html)。

从Eclipse e4开始，已经支持使用[JSR330:依赖注入规范](/2013/12/31/jsr330.html)实现服务的注入。

![](/images/e4/e4_inject.png)

在e4增加的服务编程模型中，引入了上下文（context），所有的依赖对象都被上下文管理并通过上下文获取：

![](/images/e4/e4_context.png)

在Eclipse e4中，将全局的上下文分成了多个层次：

![](/images/e4/e4_context_hierarchy.png)

下层的context可以获取上层context中定义的对象，比如：

![](/images/e4/e4_context_hierarchy_example.png)


e4中，可以使用[JSR330中基本的`@Inject`、`@Named`等注解](/2013/12/31/jsr330.html#menuIndex3),用于构造器、方法和属性。同时,e4在`org.eclipse.e4.core.di.annotations`包中也定义了一些扩展的注解，包括：

- `@Optional`：声明一个注入(`@Inject`)为可选
- `@GroupUpdates`：声明一个注入的对象是批量更新的，使用这个注解对于RCP应用的性能有很大好处
- `@Execute`
- `@CanExecute`
- `@Creatable`

下面是e4中依赖注入的一些例子：

```
// Tracks the active part
@Inject
@Optional
public void receiveActivePart(@Named(IServiceConstants.ACTIVE_PART) MPart activePart) {
  if (activePart != null) {
  System.out.println("Active part changed "
    + activePart.getLabel());
  }
} 


// tracks the active shell
@Inject
@Optional
public void receiveActiveShell(@Named(IServiceConstants.ACTIVE_SHELL) Shell shell) {
  if (shell != null) {
    System.out.println("Active shell (Window) changed");
  }
} 
```

在`org.eclipse.e4.core.contexts`包中定义的`@Active`注解可以获取活动(actived)组件。比如：

```
public class MyOwnClass {
  @Inject
  void setChildValue(@Optional @Named("key_of_child_value") @Active String value) {
    this.childValue = value;
  }
} 
```

# 创建自己的可注入对象

`@Creatable`