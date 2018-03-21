---
layout: post
title: "配置LVS所必需的网络知识"
description: ""
category: 基础设施
tags: []
lastmod: 
---

# 配置详解

## DR方式，RS配置

[root@zzh /]# vim /etc/sysctl.conf
net.ipv4.conf.lo.arp_ignore = 1
net.ipv4.conf.lo.arp_announce = 2
net.ipv4.conf.all.arp_ignore = 1
net.ipv4.conf.all.arp_announce = 2
[root@zzh /]# sysctl -p

配置VIP地址
[root@zzh /]# ifconfig  lo:0  192.168.0.100  broadcast  192.168.0.100  netmask 255.255.255.255 up
[root@zzh /]# route  add  -host  192.168.0.100  dev   lo:0




http://linux.vbird.org/linux_server/0110network_basic.php

# 路由

## 基础知识

http://linux.vbird.org/linux_server/0230router.php

## linux上的路由操作



查看路由表：

{% highlight bash %}

[root@www ~]# route -n
Kernel IP routing table
Destination     Gateway         Genmask         Flags Metric Ref  Use Iface
192.168.0.0     0.0.0.0         255.255.255.0   U     0      0      0 eth0
127.0.0.0       0.0.0.0         255.0.0.0       U     0      0      0 lo
0.0.0.0         192.168.0.254   0.0.0.0         UG    0      0      0 eth0

{% endhighlight %}


## 开启路由功能

在Linux上开启路由功能其实很简单，只需要执行一条命令就OK了。其实这个命令的作用是修改/proc/sys/net/ipv4/ip_forward文件，默认这个文件里的值是0，就是不转发数据包，我们要做的就是修改这个文件把0修改成1就OK了。
　　[root@localhost ~]# echo 1 > /proc/sys/net/ipv4/ip_forward
　　[root@localhost ~]# more /proc/sys/net/ipv4/ip_forward
　　1
　　[root@localhost ~]#
　　这个如果系统重启的话就不生效了，如果想永久加上去就需要把这个指令添加到/etc/rc.d/rc.local文件里了，
　　或者修改/etc/sysctl.conf
　　把net.ipv4.ip_forward = 0   0修改成1就OK了


linux发行版默认情况下是不开启ip转发功能的。这是一个好的做法，因为大多数人是用不到ip转发的，但是如果我们架设一个linux路由或者vpn服务我们就需要开启该服务了。下面我会通过几种方式开通它。检查ip转发是否开启
我们需要通过访问sysctl的内核ipv4.ip_forward来判断转发是否开启。
使用 sysctl:
sysctl net.ipv4.ip_forward net.ipv4.ip_forward = 0
或者检查/proc下的文件:
cat /proc/sys/net/ipv4/ip_forward 0
正如我们所见，ipv4转发没有开启 (值为 0).
启动ip转发
通过sysctl我们可以开启ipv4的转发功能 (无需重启):
sysctl -w net.ipv4.ip_forward=1
或者
echo 1 > /proc/sys/net/ipv4/ip_forward
这种设置只是暂时的; 它的效果会随着计算机的重启而失效。
通过在 /etc/sysctl.conf 设置参数
如果你想使ip转发永久生效，就请修改 /etc/sysctl.conf ，在这里我们可以增加一条 net.ipv4.ip_forward = 1
/etc/sysctl.conf: net.ipv4.ip_forward = 1
如果你的ipv4转发项已被设为0那么你只需要将它改为1.
要想是更改生效，你需要执行以下指令：
sysctl -p /etc/sysctl.conf
在红帽系列的发行版上可以通过重启网络服务使之生效：
service network restart
而在debian/ubuntu系列的发行版则用这样的命令：
/etc/init.d/procps.sh restart


# ARP

ARP(Address Resolution Protocol，地址解析协议)是获取物理地址的一个TCP/IP协议。某节点的IP地址的ARP请求被广播到网络上后，这个节点会收到确认 其物理地址的应答，这样的数据包才能被传送出去。RARP(逆向ARP)经常在无盘工作站上使用，以获得它的逻辑IP地址。