---
layout: post
title: "用salt管理成千上万的服务器"
description: "实在是厌倦了对大量服务器日复一日的重复操作。尤其是在虚拟化的时代，系统的每个组件都有很多个相同的节点在运行，更让重复的次数再乘以N。
当我发现Salt的时候，我的眼前一亮：这正是我所需要的东西。"
category: 基础设施
tags: [devops, salt]
lastmod: 2013-06-25
---

# 引言：一个”非专职运维人员“的烦恼

加入到某证券公司的IT部门，尽管所在的部门挂了一个“研发部”的名字，但是我发现有大概40%的时间是在做运维工作。

这来自两种情况：

- 自主开发的应用，需要持续的改进，不断的更新、发布、部署、调整配置，这不是运维部门喜欢的状态。
- 软件商提供的“产品”无法满足运维部门的要求：无法通过简单的 [Q&A](http://en.wikipedia.org/wiki/Q%26A) 文档保证系统的正常运行，经常需要有一定技术能力的人员解决系统运行过程中各种稀奇古怪的问题。

这种情况下只能自己做一个“非专职运维人员”，需要频繁的登录各种服务器，执行一些命令来查看状态或者更改配置（包括配置文件的变更和软件包的安装部署）。很多操作都是不断的重复，日复一日，让人厌烦。

”重复的工作应该交给程序去做“，所以我自己写过一些脚本。为了避免将脚本上传到几十台服务器并且不时进行更改，我使用[Fabric](https://github.com/fabric/fabric)来进行服务器的批量操作。

尽管避免了”批量的人工操作“，但我还是在进行”人工的批量操作“。远远没有实现自动管理。将有限的生命解放出来，投入到更有意义的编码工作是一个奔四程序员应有的追求，所以我又睁大红肿的眼睛，迷茫的搜索这个世界。

我发现了[Puppet](https://puppetlabs.com/)，[Chef]()和[CFEngine]()，但是并不满意。直到我发现了[Salt](http://saltstack.org/),我的眼前一亮：这正是我所需要的东西。

如果说Salt有什么独特之处打动了我，那就是：

- 简单：可能是源于python的简约精神，Salt的安装配置和使用简单到了令人发指的地步。任何稍有经验的linux使用者可以在10分钟之内搭建一个测试环境并跑通一个例子（相比之下，puppet可能需要30--60分钟）。
- 高性能：Salt使用大名鼎鼎的[ZeroMQ](/2013/07/03/zeromq_intro.html)作为通讯协议，性能极高。可以在数秒钟之内完成数据的传递
- 可伸缩：基于[ZeroMQ](/2013/07/03/zeromq_intro.html)通信，具备很强的扩展性；可以进行分级管理，能够管理分布在广域网的上万台服务器。

尽管[twitter](http://www.twitter.com)、[豆瓣](http://www.douban.com/)、[oracle](http://www.oracle.com)、等著名网站的运维团队都在使用puppet，但是我相信，他们切换到salt只是一个时间问题。毕竟不是所有的人都喜欢操纵傀儡(puppet)，但是谁又能离开盐(salt)呢？

关于Salt和Puppet的对比，可以参考[这里](http://www.opencredo.com/blog/a-dive-into-salt-stack)，或者看看[中文版](http://wiki.saltstack.cn/reproduction/dive-into-saltstack)。


# Salt快速入门

Salt的体系结构中将节点区分为: master, minion, syndic。

- master: 老大，管理端
- minion: 马仔，被管理端
- syndic: 头目，对于老大来说是马仔，对于马仔来说是老大

在入门阶段，先不考虑syndic。

## 安装配置

如果将操作系统区分为：

- *NIX
  + Linux
  + Solaris
  + HP Unix
  + FreeBSD
  + OS X

- windows


理论上来说，Salt可以安装在任何*NIX系统上，包括master和minion。除了[源代码](https://github.com/saltstack/salt)之外，
还可以通过Salt提供的[安装脚本](https://github.com/saltstack/salt-bootstrap)，或者[PyPI](https://pypi.python.org/pypi/salt)进行安装。

对于Linux，尤其是企业环境中常用的RHEL,CentOS,Ubuntu，可以通过包管理器非常容易的安装master 和/或 minion。
比如: yum(需要先配置[EPEL](http://fedoraproject.org/wiki/EPEL/zh-cn)), apt(需要增加`http://debian.madduck.net/repo/`库)，yaourt，ports。

Mac OS X 先使用HomeBrew解决依赖包：`brew install swig zmq`，然后用PyPI安装：`pip install salt`。

对于windows，只能安装minion（windows只适合做马仔）。从[官方网站](http://saltstack.com/downloads/)下载合适的安装包。安装过程中可以指定master地址和本机名称。
安装后需要自己启动Salt服务。配置文件在C:\salt\conf\minion。

具体的各操作系统下的安装可以参考[官方文档](http://docs.saltstack.com/topics/installation/index.html)。这里为了简单，只考虑常用的RHEL/CentOS 和 windows。 在下面的例子中，使用一台RHEL/CentOS作为master， 另外一台RHEL/CentOS和一台windows 2003 Server作为 minion。



### 安装管理端(master)

{% highlight bash %}

 # 安装EPEL,注意选择合适的版本
 rpm -ivh http://mirrors.sohu.com/fedora-epel/6/x86_64/epel-release-6-8.noarch.rpm
 yum update
 
 # 安装master
 yum install salt-master      
 
 # 修改配置
 vim /etc/salt/master
 
 # 最基本的设定服务端监听的IP(比如使用VIP做master的高可用时)：
 # interface: 服务端监听IP
 # 其他配置参考[官方文档](http://docs.saltstack.com/ref/configuration/master.html)
 
 # 启动服务(以下命令等效)
 salt-master -d
 /etc/init.d/salt-master start
 service salt-master start

{% endhighlight %}


### 安装被管理端(minion)

{% highlight bash %}

 # 安装EPEL,注意选择合适的版本
 rpm -ivh http://mirrors.sohu.com/fedora-epel/6/x86_64/epel-release-6-8.noarch.rpm
 yum update
 
 # 安装minion
 yum install salt-minion   
 
 # 修改配置
 vim /etc/salt/minion
 
 # 最基本的设定是指定master地址，以及本机标识符：
 # master: master的主机名或IP地址
 # id: 本机标识符
 # 其他配置参考[官方文档](http://docs.saltstack.com/ref/configuration/minion.html)
 
 
 # 启动服务(以下命令等效)
 salt-minion -d
 /etc/init.d/salt-minion start
 service salt-minion start

{% endhighlight %}


### 接受minion的托管请求

minion向master投诚后，还需要master接受才行。这个过程叫做“授信”。

Salt底层使用公钥-私钥证书来保证通信信道的安全。具体的机制可以参考ZeroMQ的相关内容。Salt已经屏蔽了底层的细节，只需要使用封装好的命令：

{% highlight bash %}

 # 在master上运行
 # 查看所有minion
 salt-key -L
 
 Accepted Keys:
 windows
 bond_app_server_main
 mac_os_vm
 salt-master
 Unaccepted Keys:
 minion1
 minion2
 Rejected Keys:

 #其中Unaccepted Keys是未许可的minion。可以使用下面的命令通过认证：
 salt-key -a minion1

{% endhighlight %}



## 测试

安装配置好之后，首先要测试一下联通性：`salt '*' test.ping`。salt会列出每个认证过的minion的联通状态(true 或 false)。


再举一些例子：

{% highlight bash %}

 # 查询主机运行了多长时间
 sudo salt '*' cmd.run "uptime"


 # 批量重启服务
 salt '*' cmd.run "service httpd restart"

 # 让多台机器一起，使用Apache Bench进行压力测试
 salt '*' cmd.run "ab -n 10 -c 2 http://www.google.com/"


{% endhighlight %}


注意，默认情况下master和minion之间使用以下端口进行通信：
 
- 4505(publish_port): salt的消息发布系统   
- 4506(ret_port):salt客户端与服务端通信的端口

网络的设置需要保证这些端口可以访问。


# Salt的强大功能

上面的例子都是用Salt进行批量操作。但是Salt的功能不仅如此。

认真分析一下我的“非专职运维工作”的内容，发现可以分为以下三个方面：

- 变更操作：根据需要对节点中某个资源的某种状态进行调整，并检验变更的结果
- 配置管理：让上述行为变得“可管理”，支持“有关人士”对上述行为的标记、控制、识别、报告、跟踪和归档甚至审批和审计
- 状态监控：随时掌握状态，发现异常。尽量在系统用户发现问题之前解决麻烦

Salt对上述三个方面提供了完美的支持，事实上，Salt提供的功能比我需要的还要多。下图是Salt的主要功能：

![salt_functions](/images/2013/salt_usage/salt_functions.png)

具体的功能使用在[这篇文章](/2013/06/25/salt_usage.html)中详细说明。

  
# Salt的网络资源

## 网站

- [salt官方网站](http://saltstack.org/)，
- [中国SaltStack用户组(CSSUG)网站](http://saltstack.cn/)
- [Into The Salt Mine,关于Salt的各种安装、配置、使用的博客](http://intothesaltmine.org/blog/html/index.html)

## 代码

- [saltstack将代码托管在github上](https://github.com/saltstack),包括：
  + [salt主工程](https://github.com/saltstack/salt)
  + [salt-bootstrap，一个快速安装Salt的脚本](https://github.com/saltstack/salt-bootstrap)
  + [salt states参考配置](https://github.com/saltstack/salt-states)，大量用于监控目标主机状态的配置文件，可以直接使用
  + [Salt Cloud](https://github.com/saltstack/salt-cloud),使得Salt支持各种云服务(Amazon EC2, HP Cloud, OpenStack,Parallels等)的扩展
  + [salty-vagrant](https://github.com/saltstack/salty-vagrant), 用Salt管理[Vagrant虚拟环境](http://www.vagrantup.com/)的扩展
  + [salt-api](https://github.com/saltstack/salt-api)，基于Salt进行二次开发的包
  + [salt-ui](https://github.com/saltstack/salt-ui), 一个图形界面
  + [pepper](https://github.com/saltstack/pepper),  Stand-alone CLI tools that mimic Salt's CLI tools but proxy Salt commands through salt-api 
  + [ salt-contrib](https://github.com/saltstack/salt-contrib), Salt Module Contributions 
  + [ sublime-text](https://github.com/saltstack/sublime-text), Salt-related syntax highlighting and snippets for Sublime Text 
  + [ formulae](https://github.com/saltstack/formulae), 
  + [ salt-vim](https://github.com/saltstack/salt-vim), Vim files for editing Salt files 
  + [ salt-ci](https://github.com/saltstack/salt-ci), Salt-CI — Salt Continuous Integration 
  + [ salt-genesis](https://github.com/saltstack/salt-genesis),
  + [ salt-qa](https://github.com/saltstack/salt-qa),
  + [ saltstack_org](https://github.com/saltstack/saltstack_org),
  + [ salt-windows-install](https://github.com/saltstack/salt-windows-install),


- [中国SaltStack用户组在github上托管的代码](https://github.com/cssug)，包括：
  + [salt的一个分支](https://github.com/cssug/salt), 其目标是实现中心库和配置管理功能。
  + [salt的web管理界面](https://github.com/cssug/salt-dashboard)，基于Django。

