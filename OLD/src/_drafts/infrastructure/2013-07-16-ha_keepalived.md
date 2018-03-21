---
layout: post
title: "keepalived实现双机互备"
description: ""
category: 基础设施
tags: [HA, keepalived, 负载均衡, cluster]
lastmod: 
---

# 目标：高可用

“高可用性”（High Availability）通常来描述一个系统经过专门的设计，从而减少停工时间，而保持其服务的高度可用性。

通过高可用性设计，可以提高系统的平均无故障时间(MTTF)，
对于重要的系统或系统中重要的节点，必须有高可用性的设计来保证系统的平均无故障时间达到预期的要求。

前面的[NginX负载均衡方案](/2013/05/27/nginx_keepalived.html)中就使用了keepalived实现NginX节点的高可用，但那只是高可用性设计中的一种工作方式。
通常来说，高可用设计中多个冗余设备可以采用以下三种工作方式：

- 主从方式 （非对称方式）

  主机工作，备机处于监控准备状况；当主机宕机时，备机接管主机的一切工作，待主机恢复正常后，按使用者的设定以自动或手动方式将服务切换到主机上运行，数据的一致性通过共享存储系统解决。

- 双机双工方式（互备互援）

  两台主机同时运行各自的服务工作且相互监测情况，当任一台主机宕机时，另一台主机立即接管它的一切工作，保证工作实时，应用服务系统的关键数据存放在共享存储系统中。

- 集群工作方式（多服务器互备方式）

  多台主机一起工作，各自运行一个或几个服务，各为服务定义一个或多个备用主机，当某个主机故障时，运行在其上的服务就可以被其它主机接管。

显然，主从方式最简单但存在资源浪费的情况；双工方式可以充分利用资源，但配置较复杂，两个节点之间要进行心跳监测；集群工作方式与双工方式并没有本质的区别，但复杂度急剧增加，除了健康状态要多播外，还需要考虑脑裂、仲裁、法定人数等问题。

本文只讨论双机互备的工作方式。


# keepalived简介

[keepalived](http://www.keepalived.org/)是[LVS](/2013/07/04/lvs_intro.html)的扩展项目，最初是为了解决LVS负载调度器的单点故障问题，但由于其适用性较强，配置简洁，也被用在许多其他场合，比如NginX负载均衡的高可用设计。

keepalived的设计如下图：

![keepalived_architecture](/images/2013/lvs/keepalived_architecture.jpg)

- WatchDog：监控checkers和vrrp 进程
- Checkers：服务器健康状态检查(healthchecking)。可以编写自定义的健康检查脚本。
- VRRP STACK：当健康检查失败（服务不可用）时，在节点见进行切换。使用[VRRP(Virtual Router Redundancy Protocol, 虚拟路由器冗余协议）](http://en.wikipedia.org/wiki/Virtual_Router_Redundancy_Protocol)的组播实现。
- IPVS wrappers：生成ipvs规则。专门为LVS所用。
- Netlink Reflector：设定vrpp的vip地址。

keepalived可以在每个节点配置相同的VRRP实例(vrrp_instance)，并指定状态为MASTER或BACKUP。

当Checkers监测到本节点的服务不可用时，使本机的VRRP实例停止工作，并通知另外节点的VRRP STACK接管VRRP实例，从而对外保证服务继续可用。


# 双机互备方式的实现

keepalived实现主备工作的资料到处都有，我这里也有一个[NginX主备机制的例子](/2013/05/27/nginx_keepalived.html)，这里就不再重复了。

其实，只要稍微动点脑筋，在主备的基础上就可以实现双机互备甚至集群的工作方式。因为有两个前提：

- keepalived并没有限定节点的个数只能是2个
- keepalived没有限定每个节点只能有一个VRRP实例

那么，双机互备的实现原理就是：

- 在每个节点配置两个VRRP实例
- 两个实例分别以一个节点为主(MASTER)，另一个节点为备(BACKUP)
- 通过外部的其他机制，如DNS轮询，使得两个VRRP实例同时对外提供服务

# 配置实例

keepalived的配置文件（`/etc/keepalived/keepalived.conf`)中包含3部分内容：

- global_defs： 全局配置
- vrrp_instance：vrrp实例，用来定义虚拟路由组
- virtual_server：定义LVS虚拟服务器

这里面只例举一下vrrp实例的配置。

- 节点1

{% highlight nginx %}

vrrp_instance VI_1 { 
    state MASTER 
    interface eth0 
    virtual_router_id 51 
    priority 100 
    advert_int 1 
    authentication { 
        auth_type PASS 
        auth_pass password 
    } 
    virtual_ipaddress { 
        192.168.1.8 
    } 
} 
vrrp_instance VI_2 { 
    state BACKUP 
    interface eth0 
    virtual_router_id 52 
    priority 99 
    advert_int 1 
    authentication { 
        auth_type PASS 
        auth_pass password 
    } 
    virtual_ipaddress { 
        192.168.1.9 
    } 
}

{% endhighlight %}

- 节点2

{% highlight nginx %}

vrrp_instance VI_1 { 
    state BACKUP 
    interface eth0 
    virtual_router_id 51 
    priority 99 
    advert_int 1 
    authentication { 
        auth_type PASS 
        auth_pass password 
    } 
    virtual_ipaddress { 
        192.168.1.8                   
    } 
} 
vrrp_instance VI_2 { 
    state MASTER 
    interface eth0 
    virtual_router_id 52 
    priority 100 
    advert_int 1 
    authentication { 
        auth_type PASS 
        auth_pass password 
    } 
    virtual_ipaddress { 
        192.168.1.9                   
    } 
}

{% endhighlight nginx %}
