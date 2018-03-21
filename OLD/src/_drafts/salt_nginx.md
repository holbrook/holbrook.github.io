---
layout: post
title: "用Salt管理NginX"
description: "结合Salt中的模块、state、pillar等功能解决NginX的配置和监控等问题"
category: 基础设施
tags: [salt, NginX]
lastmod: 
---



学习了[Salt简介](http://thinkinside.tk/2013/06/24/salt_intro.html)、[Salt的主要功能](http://thinkinside.tk/2013/06/25/salt_usage.html)、[State配置](http://thinkinside.tk/2013/07/02/salt_state_config_structure.html)及[State实例](http://thinkinside.tk/2013/06/30/salt_sls_sample.html)，还有[Pillar介绍](http://thinkinside.tk/2013/07/07/salt_pillar.html)，已经可以用Salt解决实际问题了。

# 配置需求

自从设计了[统一web访问层方案](http://thinkinside.tk/2012/10/16/weblayer_nginx_keepalived.html)并进行[实施](http://thinkinside.tk/2013/05/27/nginx_keepalived.html)之后，我就要经常修改或查看nginx的配置。我部署了两个NginX集群，每个集群现在只有两个节点，就已经让我苦不堪言。其实每次都在做一些同样的事情。以其中一个集群为例：

1. 登录到其中一个节点
2. 打开NginX配置文件
3. 查看或修改配置（主要是增加`upstream`，`server`配置项）
4. 使用`nginx -t`命令测试配置
5. 使用`nginx -s reload`命令重新加载配置
6. 登录到另一个节点
7. 重复上述2--5步骤

上述只是最经常的重复性工作。让人厌烦且容易出错。此外还有其他的配置项和配置参数，以及静态文件都要在多个节点间保持一致。

在[这篇文章](/2013/05/27/nginx_keepalived.html)中，我就提到可以用配置管理工具或者文件同步工具解放自己。
尽管可以使用分布式文件系统，比如[DRBD](/2013/07/17/ha_drbd.html)或[MooseFS](/2013/08/02/moosefs.html)来解决配置文件的同步，
但对于nginx进程的reload, stop, start等，还是需要到各个节点重复操作。

使用Salt，既可以实现文件的同步，还可以进行批量操作。带来的一个附加的好处是：通过yaml生成配置文件，使得配置变得“结构化”，从而可以通过编程的方式管理这些配置。

# 配置标准化

## 内容的拆分

nginx的配置文件可以是一个单独的nginx.conf，也可以include其他配置文件。比如，一个通常的做法是在主配置文件中`include conf.d/*.conf`。

一般会通过nginx管理大量的`upstream`和`server`，对于复杂的配置情况，upstream和server之间可能是多对多的映射关系。

为了更灵活，我将nginx的配置拆分成三个部分：

- 基本参数



## 配置项

两个集群都属于生成环境，一个用于内部，一个用于外部。分别

   将每个虚拟主机改为单独的配置文件，并在`nginx.conf`中include

   静态文件：从版本库获取

## 配置数据




# State设计

## Salt的nginx模块
salt.modules.nginx
Support for nginx

salt.modules.nginx.configtest()
test configuration and exit

CLI Example:

salt '*' nginx.configtest
salt.modules.nginx.signal(signal=None)
Signals nginx to start, reload, reopen or stop.

CLI Example:

salt '*' nginx.signal reload
salt.modules.nginx.version()
Return server version from nginx -v

CLI Example:

salt '*' nginx.version

# 使用实例

## 增加虚拟服务器(server)

## 修改静态文件

## 增加NginX节点

## 检查配置状态

## 查看性能指标

# 小结
