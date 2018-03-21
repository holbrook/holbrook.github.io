---
layout: post
title: "lvs+nginx的负载均衡实验"
description: "LVS+NginX是构建大型B/S应用的典型方式。本文记录在实验环境搭建这样一个架构，并进行功能、可靠性、性能等方面的测试的过程。"
category: 基础设施
tags: [负载均衡, cluster, lvs, nginx]
lastmod: 2013-07-03
---

# 准备环境

2 LVS(cluster) + 2 NginX 
（图）

# 配置

## LVS服务器配置

1. 安装软件包

- pulse: LVS守护进程
- piranha: LVS的web管理工具，包括状态监控和配置

{% highlight bash %}
yum install pulse piranha
{% endhighlight %}



2. 打开IP转发功能（ip_forward）

- 在`/etc/sysctl.conf`中设置`net.ipv4.ip_forward = 1`
- `/sbin/sysctl -w net.ipv4.ip_forward=1` 或者`echo 1 > /proc/sys/net/ipv4/ip_forward`
- 查看状态：`/sbin/sysctl net.ipv4.ip_forward` 或者`cat /proc/sys/net/ipv4/ip_forward`
 
3. 配置LVS

配置文件位于`/etc/sysconfig/ha/lvs.cf`，使用piranha可以以图形界面的方式进行配置。

{% highlight bash %}
 # 设置管理密码
 piranha-passwd
 
 # 启动piranha服务
 /etc/init.d/piranha-gui start

{% endhighlight %}

接下来可以用浏览器访问: http://IP_OF_LVS:3636（记得配置LVS上的防火墙，否则只能本机访问）。

点击"Login"按钮，使用用户名`piranha`和刚才设置的密码登录，可以看到管理界面：

![1](/images/2013/lvs_nginx_practice/piranha1.png)

依次配置全局设置(GLOBAL SETTINGS), 备机设置(REDUNDANCY, 可选)，虚拟服务器(VIRTUAL SERVERS)，即可。

其中虚拟服务器可以配置基本信息(VIRTUAL SERVER)、真实服务器(REAL SERVER)和监控脚本(MONITORING SCRIPTS)。

4. 启动服务

配置完成后，启动lvs服务(`/etc/init.d/pulse start`)，在监控界面(CONTROL/MONITORING)可以看到"Daemon"的状态为"running"。

如果要设置pulse为开机自动启动，可以使用命令：`/sbin/chkconfig --level35 pulse on`。


## RS（Real Server，真实服务器）配置

这里使用nginx作为Real Server，参考[这篇文章](http://thinkinside.tk/2013/05/27/nginx_keepalived.html)进行最简单的配置，能够看到nginx默认的欢迎界面即可。

RS需要进行一系列的设置才能与LVS协同工作，参考如下脚本：

{% highlight bash %}

#!/bin/bash

VIP=VIP_OF_LVS

/sbin/ifconfig lo:0 $VIP broadcast $VIP netmask 255.255.255.255 up

/sbin/route add -host $VIP dev lo:0

echo "1" >/proc/sys/net/ipv4/conf/lo/arp_ignore

echo "2" >/proc/sys/net/ipv4/conf/lo/arp_announce

echo "1" >/proc/sys/net/ipv4/conf/all/arp_ignore

echo "2" >/proc/sys/net/ipv4/conf/all/arp_announce

sysctl -p

/sbin/service iptables stop

{% endhighlight %}


## 启动LVS服务

LVS和RS都配置好之后，可以启动LVS服务。前面提到，pulse是LVS的守护进程(Daemon)。使用如下的命令启动LVS：

    /etc/init.d/pulse start

# 命令行工具：ipvsadm

`ipvsadm`是LVS的命令行管理工具，可以用于更改运行时状态或更改配置文件。主要功能包括：

{% highlight bash %}

 # 增加/编辑虚拟服务器（VS）
 ipvsadm -A|E -t|u|f virutal-service-address:port [-s scheduler] [-p [timeout]] [-M netmask]

 # 删除虚拟服务器
 ipvsadm -D -t|u|f virtual-service-address

 # 清除内核虚拟服务器表中的所有记录。
 ipvsadm -C

 # 放弃内存中的修改，读取配置文件
 ipvsadm -R

 # 将内存中的修改保存为配置文件
 ipvsadm -S [-n]

 # 增加/编辑真实服务器（RS）
 ipvsadm -a|e -t|u|f service-address:port -r real-server-address:port

 # 删除真实服务器
 ipvsadm -d -t|u|f service-address -r server-address

 # 显示虚拟服务器表
 ipvsadm -L|l [options]

 # 虚拟服务表计数器清零（清空当前的连接数量等）
 ipvsadm -Z [-t|u|f service-address]

 # 设置连接超时值
 ipvsadm –set tcp tcpfin udp

 # 启动守护进程, 可以是master或backup方式
 ipvsadm –start-daemon state [--mcast-interface interface]

 # 停止守护进程
 ipvsadm –stop-daemon

 # 查看帮助
 ipvsadm -h

{% endhighlight %}

# 功能验证

1. 检查LVS启动过程： `tail -f /var/log/messages`，可以看到虚拟服务启动、连接到各个真实服务器等记录。
2. 将两台真实服务器的nginx欢迎界面（index.html）修改成不同的内容，重复刷新对虚拟服务器的访问，能看到内容变化
3. 使用命令`ipvsadm`检查分流状况
4. 关闭一台nginx, `/var/log/messages`中会记录服务器连接失败，此时通过`ipvsadm`检查会发现所有的流量被分流到另一个nginx上面
5. 重新启动刚才关闭的nginx, `/var/log/messages`中会记录服务器连接成功，此时通过`ipvsadm`检查会发现恢复了负载分担
6. lvs+keepalived的故障切换测试（未测试）


# 性能测试

使用Apache Bench进行简单的性能测试，得出如下结论：

1. 单个nginx的最佳并发：1900，最大并发：2900；使用LVS+2台nginx的最佳并发：3000，最大并发：5900。
   
   说明通过LVS做负载均衡能提高并发能力，但不是线性增加，会有一定的损失。具体数据需要进一步测试。

2. 经过LVS访问nginx比直接访问nginx会增加50毫秒左右的响应时间。

3. 官方的测试数字是：VS/NAT方式达到1112并发，VS/DR或VS/TUN方式可以达到25,000并发。

4. F5的并发处理能力超过10万，可以保持的连接数能达到几百万。

