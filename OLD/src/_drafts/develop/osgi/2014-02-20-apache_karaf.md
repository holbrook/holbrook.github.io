---
layout: post
title: "Apache Karaf：OSGi中间件"
description: ""
category: 软件开发
tags: [OSGi, maven]
---

# 为什么需要“OSGi中间件”

尽管在OSGi Runtime(Felix, Equinox等)的基础上，OSGi组织又规定了[Blueprint规范以实现OSGi环境下的依赖注入](/2014/01/22/osgi_blueprint_container.html)，
但这还不够——没有提供类似Web开发框架那样的一些“平台级”的功能。比如日志，控制台，配置文件等。

很难想象没有Tomcat这样的Web中间件，开发Java Web应用的工作量有多大。同样的，OSGi应用也需要一种“中间件”，来实现各应用共性的一些功能，并管理应用的部署。

[Apache Karaf](http://karaf.apache.org/)就是这样的一个"OSGi中间件"。最早，Karaf只是[Apache ServiceMix](http://servicemix.apache.org/)的Kernel子项目，后来独立出来成为Apache的顶级项目。
目前，Apache Karaf已经用于Apache Geronimo, Apache ServiceMix, Fuse ESB等项目。

Apache Karaf的主要竞争对手是[Eclipse Virgo](http://www.eclipse.org/virgo/)。

# Apache Karaf的功能

![](/images/fuse/Karaf.jpg)

Apache Karaf提供了如下“开箱即用”的功能：

- 热部署

  尽管OSGi支持热部署，但并不是自动热部署，需要调用一些API去执行插拔的动作。Karaf在运行时可以自动处理`[home]/deploy`文件夹中的OSGi bundle，能够自动加载并在满足依赖关系时自动启动。

- 动态配置

  Karaf在`$KARAF_HOME/etc`文件夹中存储配置文件。这些配置内容可以在Karaf运行时动态修改。

- 日志处理

  基于Log4J的日志系统，同时支持多种日志API，如JDK 1.4, JCL, SLF4J, Avalon, Tomcat, OSGi等。

- 系统服务

  Karaf可以作为系统服务运行。

- 控制台

  可以在控制台进行服务管理、安装bundle等操作。还可以扩展自己的控制台命令。

  可以通过SSH远程访问其他服务器上的Karaf控制台。

- 多实例管理

  一个服务器上可以运行多个Karaf实例。对实例的管理可以在Karaf控制台中进行。

- Bundle仓库
  
  Karaf中内置了[Pax URL](https://ops4j1.jira.com/wiki/display/paxurl/Pax+URL)的MVN协议，可以从Maven中央仓库安装bundle。

- Bundle集合(Feature)

  类似于Eclipse的Feature，Karaf中也支持Feature，即bundle的集合。使用Feature可以简化OSGi应用的部署。



# Karaf初体验

安装好Java环境，加压缩Karaf，执行`$KARAF_HOME/bin/karaf`，可以看到Karaf的启动界面：

![](/images/karaf/karaf1.png)

如图的提示，使用`<tab>`可以列出所有可用的命令，所有的命令支持`--help`参数。

如果执行`list`命令，可以列出所有的bundles:

![](/images/karaf/karaf2.png)

还有很多其他的命令，比如

- `bundle:install` 安装bundle
- `feature:repo-add` 安装feature库
- `feature:install` 安装feature

等等。详情可以参考官方的[Quick Start](http://karaf.apache.org/manual/latest/quick-start.html)。

如果查看Karaf的目录，可以看到如下的目录结构：

- `/bin`: 启动、停止、登录karaf控制台的脚本
- `/etc`: 配置文件
- `/data`: 存放运行时的工作文件，清空这个目录可以使Karaf回到初始状态
- `/cache`: OSGi framework的bundle缓存
- `/generated-bundles`: 开发用的临时目录
- `/log`: 日志
- `/deploy`: 用于bundle的热部署
- `/instances`: 存放karaf的各个实例用到的数据
- `/lib`: 启动Karaf时需要的一些库
- `/lib/ext`: Karaf需要的扩展库
- `/lib/endorsed`: Karaf对其他API的再封装(背书)的一些jar包
- `/system`: OSGi bundles库，使用Maven 2仓库的结构


# Karaf启动模式和实例

- 常规模式(regular mode) 使用命令`bin/karaf`，可以在前端启动Karaf并进入控制台
- 服务模式(server mode) 使用命令`bin/karaf server`，可以在前端启动Karaf，但不进入控制台
- 后台模式(background mode) 使用命令`bin/start`，可以在后台启动Karaf。

如果安装了service-wrapper(可以在Karaf中执行`feature:install service-wrapper`)，还可以将
Karaf安装为系统服务。

一个Karaf节点可以运行多个"Karaf实例"。实际上，默认情况下Karaf会启动一个名为`root`的实例。
实例是包含单独的配置文件、数据文件等信息的一个Karaf副本，每个实例可以单独启动或部署bundle。

Karaf控制台中提供了一些管理实例的命令：

- `instance:create` 创建实例
- `instance:clone` 从现有的实例克隆一个新的实例
- `instance:start` 启动实例
- `instance:status` 查看实例状态
- `instance:connect` 连接(切换)到某个实例
- `instance:stop` 停止实例
- `instance:destroy` 删除实例

# ssh、客户端和Web控制台


Karaf内置了一个SSHd server，可以通过ssh远程访问Karaf控制台。
要启动远程控制台服务，需要在控制台中启动bundle: `bundle:restart -f org.apache.karaf.shell.ssh`。此时，远端可以使用ssh远程访问控制台，比如: `ssh -p 8101 karaf@localhost`。默认karaf用户的密码也是karaf。ssh的用户、密码、端口等都可以在`etc/org.apache.karaf.shell.cfg`中配置。

Karaf的客户端'bin/client'即可以连接本地控制台，也可以通过ssh连接远程控制台，甚至可以执行单个的命令。比如：

```
bin/client -u karaf -p karaf -a 8101 hostname osgi:shutdown
```


Karaf还可以安装Web控制台(`feature:install webconsole`)。通过Web控制台能够管理
Karaf的bundle、feature、实例、配置以及查看日志。启动web控制台后，默认可以通过[http://localhost:8181/system/console](http://localhost:8181/system/console)
访问web控制台，默认的用户名/密码为`karaf/karaf`。Web控制台的配置文件位于`etc/org.ops4j.pax.web.cfg`。



# bundle URL和bundle仓库
Karaf在安装bundle时，可以使用多种URL来定位bundle，比如：

- http `http://repo1.maven.org/maven2/org/apache/servicemix/nmr/org.apache.servicemix.nmr.api/1.0.0-m2/org.apache.servicemix.nmr.api-1.0.0-m2.jar`

- file `file:base/bundles/org.apache.servicemix.nmr.api-1.0.0-m2.jar`
- maven库 `mvn:org.apache.servicemix.nmr/org.apache.servicemix.nmr.api/1.0.0-m2`

其中，maven库方式是使用maven库作为bundle仓库，从其中检索需要的bundle。与maven类似，可以自动解决bundle之间的依赖问题。
Karaf提供了OBR (OSGi Bundle Repository)，能够管理bundle仓库。在控制台使用命令`feature:install obr`安装OBR之后，就可以：

- 增加新的bundle仓库

  `obr:url-add file:///user/.m2/repository/repository.xml`

- 查看已安装的bundle仓库

  `obr:url-list`

- 刷新仓库

  `obr:url-refresh`

- 删除仓库

  `obr:url-remove`

- 列出所有可用的bundle

  `obr:list`

- 查找bundle

  `obr:find`



# OSGi应用，Karaf Feature和KAR

OSGi运行的基本单元是bundle，bundle之间有依赖关系。一组满足依赖关系的bundle集合，加上相关的配置信息，称为一个“OSGi应用”。
将OSGi应用部署到Karaf的行为称为“provisioning”。

为了简化OSGi应用的部署，Karaf定义了feature，用于描述OSGi应用的部署信息，包括：

- 名称
- 版本号
- 描述信息
- bundle集合
- 配置文件信息
- 依赖的其他feature

可以看出，Karaf中的feature与Eclipse Feature非常类似。

Karaf控制台中提供了一系列的feature和feature库的管理命令，包括：
- feature:info
- feature:install
- feature:list
- feature:repo-add
- feature:repo-list
- feature:repo-refresh
- feature:repo-remove
- feature:uninstall
- feature:version-list

由于feature中可能使用远端的bundle，Karaf提出了`KAR`格式，可以把一个bundle相关的所有资源打包在一起。
这类似于使用maven定义的web工程，和最终打包的war文件之间的关系。
Karaf控制台中，可以打包(`kar:create`)、安装(`kar:install`)、卸载(`kar:uninstall`)或列出(`kar:list`)KAR文件。


# 企业级特性
Karaf提供了一系列的功能，以支持企业级应用的开发，包括：

- 日志

  Karaf提供了[灵活的日志系统](http://karaf.apache.org/manual/latest/users-guide/log.html)，支持

  + OSGi Log Service
  + Log4j
  + Commons Logging
  + Logback
  + SLF4J
  + java Util Logging

  等日志框架。不管应用中使用了上述哪种日志框架，Karaf中都可以进行统一的管理，如log level, appender等。

- 安全

  Karaf提供了基于JAAS(Java Authentication and Authorization Service)的[安全框架](http://karaf.apache.org/manual/latest/users-guide/security.html)，可以控制对OSGi service、控制台命令、JMX、Web控制台等资源的访问。并且在应用中也可以使用Karaf的安全框架。

- Web

  Karaf可以[作为Web容器](http://karaf.apache.org/manual/latest/users-guide/webcontainer.html)使用，完全支持JSP/Servlet规范。
  Karaf的Web容器同时支持WAR和WAB的部署。

- JNDI

  Karaf[支持OSGi中的JNDI服务](http://karaf.apache.org/manual/latest/users-guide/jndi.html)。


- JDBC、JPA和JTA

  Karaf中即可以[使用JDBC](http://karaf.apache.org/manual/latest/users-guide/jdbc.html)直接连接数据库，
  也可以[使用JPA](http://karaf.apache.org/manual/latest/users-guide/jpa.html)作为持久层框架。Karaf可以通过Blueprint管理JPA的persist Unit。

  Karaf支持[JTA](http://karaf.apache.org/manual/latest/users-guide/jta.html)，以实现容器管理的事务。

- 其他

  Karaf还支持[EJB](http://karaf.apache.org/manual/latest/users-guide/ejb.html)、[CDI](http://karaf.apache.org/manual/latest/users-guide/cdi.html)、[JMX](http://karaf.apache.org/manual/latest/users-guide/monitoring.html)、[JMS](http://karaf.apache.org/manual/latest/users-guide/jms.html)等企业级特性。

  Karaf内置支持主备方式的部署，以保证高可用。使用[Apache Karaf Cellar](http://karaf.apache.org/index/subprojects/cellar.html)可以实现Karaf的集群部署。





