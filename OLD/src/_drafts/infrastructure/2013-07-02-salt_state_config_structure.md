---
layout: post
title: "Salt state 配置结构"
description: "Salt的state配置比较复杂，官方文档也比较零散。初学者不易掌握。但是如果把Salt的state配置看做是编写代码，就很容易掌握其脉络。
配置的目标是通过master管理多个mision的状态，最终配置的实现是使用文件夹和文件。而Salt state的设计就是在二者之间建立逻辑关系。"
category: 基础设施
tags: [salt]
lastmod: 2013-07-07
---

Salt的state配置比较复杂，官方文档也比较零散。初学者不易掌握。但是如果把Salt的state配置看做是编写代码，就很容易掌握其脉络。

下图是Salt state配置结构的逻辑图：


![salt_functions](/images/2013/salt_usage/salt_state_config_structure.png)

配置的目标是通过master管理多个mision的状态，最终配置的实现是使用文件夹和文件。而Salt state的设计就是在二者之间建立逻辑关系。

# StateTree 和 Environment

每个master上面都会建立一棵state树，将各个state的配置分级管理。

这棵树的第一层就是环境（environment)的划分。salt将环境分为base环境和自定义环境。base环境是必须存在的，其他的环境根据自己的需要进行定义。典型的可以划分开发环境(dev), 用户参与测试环境（uat)，生成环境(prod), 备份环境（backup)等等。

Salt约定base环境必须存在，是其他环境的基础，base环境中定义的state可以在各个自定义环境中使用。

显然，每个环境至少需要一个文件夹来保持多个state配置。事实上，Salt允许一个环境使用多个文件夹。

Salt环境与目录的对应关系在salt master的配置文件`/etc/salt/master`的`file_roots`变量中定义。`/etc/salt/master`文件也是使用YAML格式。

一个典型的配置如下：

{% highlight yaml %}
 file_roots:
   base:
     - /srv/salt/
   dev:
     - /srv/salt/dev/services
     - /srv/salt/dev/states
   prod:
     - /srv/salt/prod/services
     - /srv/salt/prod/states
{% endhighlight %}

# state定义

Salt state即可以使用单个的sls文件(single state)，也可以使用一个文件夹并在其中保持多个sls及其他配置文件（multi-state)。

state之间还可以使用require, include, extend等关系进行关联。

# minion 与 state之间的映射

一个salt master可以管理多个minion, 也可以定义很多个state。需要在minion和state之间建立一种多对多的映射关系。

Salt在一个`top.sls`文件中定义这种映射关系。比如：

{% highlight yaml %}
base:
  '*':
    - servers
dev:
  '*nodb*':
    - mongodb
{% endhighlight %}

# 小结

按环境的不同划分state的存放目录；定义state文件/文件夹并在state之间使用关系实现复用；建立minion和state之间的多对多映射关系。

掌握了这三点，就掌握了Salt state配置的脉络。

实际上，Salt中[Pillar的配置](/2013/07/07/salt_pillar.html)也使用了类似的结构。