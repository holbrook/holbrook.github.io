---
layout: post
title: "Salt state实例解析"
description: "在Salt的官方教程中，以apache和sshd的state配置作为例子。掌握这两个例子，就能够触类旁通，处理日常工作中大部分的配置管理问题。
本文对这两个例子进行详细的分析和注释"
category: 基础设施
tags: [salt]
lastmod: 2013-06-30
---

在Salt的[官方教程](http://salt.readthedocs.org/en/latest/topics/tutorials/starting_states.html)中，以apache和sshd的state配置作为例子。掌握这两个例子，就能够触类旁通，处理日常工作中大部分的配置管理问题。
本文对这两个例子进行详细的分析和注释。


# 目录结构

[文档](http://salt.readthedocs.org/en/latest/topics/tutorials/starting_states.html)
中的例子包含了多个文件。这些文件之间互相引用和关联。目录结构及文件清单如下：

- apache/init.sls
- apache/httpd.conf

- ssh/init.sls
- ssh/server.sls
- ssh/banner
- ssh/ssh_config
- ssh/sshd_config
- ssh/custom-server.sls

两个配置分别放在了`apache`和`ssh`文件夹。一个Salt状态可以使用单个的SLS文件，或者使用一个文件夹。后者更加灵活方便。

# apache/init.sls

{% highlight yaml %}

 apache:
    pkg:
      - installed
    service:
      - running
      - watch:
        - pkg: apache
        - file: /etc/httpd/conf/httpd.conf
        - user: apache
    user.present:
      - uid: 87
      - gid: 87
      - home: /var/www/html
      - shell: /bin/nologin
      - require:
        - group: apache
    group.present:
      - gid: 87
      - require:
        - pkg: apache
 
  /etc/httpd/conf/httpd.conf:
    file.managed:
      - source: salt://apache/httpd.conf
      - user: root
      - group: root
      - mode: 644
      - template: jinja
      - context:
        custom_var: "override"
      - defaults:
        custom_var: "default value"
        other_var: 123
 
{% endhighlight %}

说明：

1. sls文件使用[YAML](http://yaml.org/spec/1.1/)格式定义，最外面的层级定义配置项。
2. 一个sls文件中可以有多个配置项，配置项的ID可以起任意的名字。本例中包含ID为`apache`和`/etc/httpd/conf/httpd.conf`两个配置项。
3. 配置项内是一系列的状态声明。所有的状态项来自Salt状态模块。即可以使用[Salt内置的状态模块](http://docs.saltstack.com/ref/states/all/index.html)，也可以[编写自定义的状态模块](http://docs.saltstack.com/ref/states/writing.html)
4. 状态声明内部指定状态函数的调用。状态函数是每个Salt状态模块中定义的函数。


- apache配置项
  + [pkg模块](http://docs.saltstack.com/ref/states/all/salt.states.pkg.html#module-salt.states.pkg)，使用操作系统的包管理器(如yum, apt-get)安装软件包
    * [salt.states.pkg.installed函数](http://docs.saltstack.com/ref/states/all/salt.states.pkg.html#salt.states.pkg.installed), 验证软件包是否安装以及是否为指定的版本
  + [service模块](http://docs.saltstack.com/ref/states/all/salt.states.service.html#module-salt.states.service)管理服务/守护进程(daemon)的启动或停止
    * [salt.states.service.running函数](http://docs.saltstack.com/ref/states/all/salt.states.service.html#salt.states.service.running)检查服务是否已经启动
    * [service模块](http://docs.saltstack.com/ref/states/all/salt.states.service.html#module-salt.states.service)定义了[salt.states.service.mod_watch](http://docs.saltstack.com/ref/states/all/salt.states.service.html#salt.states.service.mod_watch)函数，可以使用[`watch`要素](http://docs.saltstack.com/ref/states/ordering.html#the-watch-requisite)监控其他的模块是否满足。这里监控以下情况：
      1. `apache`[软件包(pkg)](http://docs.saltstack.com/ref/states/all/salt.states.pkg.html#module-salt.states.pkg)是否已安装
      2. `/etc/httpd/conf/httpd.conf`[文件(file)](http://docs.saltstack.com/ref/states/all/salt.states.file.html#module-salt.states.file)是否存在
      3. `apache`[用户(user)](http://docs.saltstack.com/ref/states/all/salt.states.user.html#module-salt.states.user)是否存在
    * `user.present`是简写形式，直接调用[`user`](http://docs.saltstack.com/ref/states/all/salt.states.user.html#module-salt.states.user)模块的[`present`](http://docs.saltstack.com/ref/states/all/salt.states.user.html#salt.states.user.present)函数检查是否存在如下属性的`apache`用户：
      1. uid=87
      2. gid=87
      3. home目录为`/var/www/html`
      4. 登录脚本为`/bin/nologin`
      5. 检查依赖项：`apache`[用户组](http://docs.saltstack.com/ref/states/all/salt.states.group.html#module-salt.states.group)
    * `group.present`是简写形式，直接调用[`group`](http://docs.saltstack.com/ref/states/all/salt.states.group.html#module-salt.states.group)模块的[`present`](http://docs.saltstack.com/ref/states/all/salt.states.group.html#salt.states.group.present)函数检查是否存在如下属性的`apache`用户组：
      1. gid=87
      2. 检查依赖项：`apache`[软件包](http://docs.saltstack.com/ref/states/all/salt.states.pkg.html#module-salt.states.pkg)
- `/etc/httpd/conf/httpd.conf`配置项
  + `file.managed`是简写形式，直接调用[file模块](http://docs.saltstack.com/ref/states/all/salt.states.file.html#module-salt.states.file)的[managed方法](http://docs.saltstack.com/ref/states/all/salt.states.file.html#salt.states.file.managed)根据需要从master获取文件并可能会通过模板系统(templating system)进行渲染。文件要满足如下要求：
    1. 使用master上面的apache/httpd.conf文件
    2. user=root
    3. group=root
    4. mode=644
    5. 使用[`jinja`](http://jinja.pocoo.org/)模板渲染
    6. 上下文变量：
       * custom_var="override"
    7. 默认值:
       * custom_var="default value"
       * other_var=123

# ssh/init.sls

{% highlight yaml %}
 openssh-client:
    pkg.installed
 
  /etc/ssh/ssh_config:
    file.managed:
      - user: root
      - group: root
      - mode: 644
      - source: salt://ssh/ssh_config
      - require:
        - pkg: openssh-client

{% endhighlight %}

说明：


# ssh/server.sls

{% highlight yaml %}

 include:
    - ssh
 
 openssh-server:
   pkg.installed

 sshd:
   service.running:
     - require:
       - pkg: openssh-client
       - pkg: openssh-server
       - file: /etc/ssh/banner
       - file: /etc/ssh/sshd_config

 /etc/ssh/sshd_config:
   file.managed:
     - user: root
     - group: root
     - mode: 644
     - source: salt://ssh/sshd_config
     - require:
       - pkg: openssh-server

 /etc/ssh/banner:
   file:
     - managed
     - user: root
     - group: root
     - mode: 644
     - source: salt://ssh/banner
     - require:
       - pkg: openssh-server

{% endhighlight %}

说明：

- include语句将别的state添加到当前文件中，使得state可以跨文件引用。
   
  使用include相当于把被引用的内容文件添加到自身，可以require、watch或extend被引用的SLS中定义的内容。

  这里引用了`ssh`state。

- `openssh-server`配置项
- `sshd`
- `/etc/ssh/sshd_config`配置项
- `/etc/ssh/banner`配置项

# ssh/custom-server.sls

{% highlight yaml %}
 include:
   - ssh.server

 extend:
   /etc/ssh/banner:
     file:
       - source: salt://ssh/custom-banner
{% endhighlight %}

说明：

- 引用`ssh`state的server配置项
- `extend`可以复用已有的state，在原来的基础上进行扩展，增加新的配置或修改已有的配置。
  1. 将`/etc/ssh/banner`配置项的文件修改为`salt://ssh/custom-banner`

