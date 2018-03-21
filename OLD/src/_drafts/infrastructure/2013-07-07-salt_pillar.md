---
layout: post
title: "Pillar：定义Salt配置管理的数据"
description: "State定义了Salt配置管理的内容，Pillar则定义了Salt配置管理的数据。Pillar使得同一个配置项在各个minion中可以使用不同的数据，从而不需要在State中定义大量的include, extend等关系。"
category: 基础设施
tags: [devops, salt]
lastmod: 
---

# 为什么需要Pillar

看了[这篇文档](/2013/06/30/salt_sls_sample.html)，你可能已经被Salt State的强大所折服。

是的，Salt State能够解决很多配置管理的问题，但是如下两个场景，如果只用state进行配置就会比较麻烦：

1. 让`apache`配置项适应不同的OS

   [这个例子](/2013/06/30/salt_sls_sample.html#menuIndex1)中的apache配置中通过pkg模块验证`apache`软件包是否安装。但是在RedHat系统的yum包管理器和Debian系统的apt包管理器中，apache的包名字分别为`httpd`和`apache2`。如何避免为apache配置项针对不同的包管理器定义不同的state？

2. 同一个应用在不同环境中的数据库连接

   假如你开发了一个Django应用，数据库连接信息在应用的settings.py中定义：

   {% highlight python %}
   DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'test',
        'USER': 'root',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '3306', 
    }
   }

   {% endhighlight %}

   显然，数据库连接信息在开发环境、测试环境、生成环境中各不相同。如果把该应用作为一个state，如何实现在不同环境中的自动部署？

Salt Pillar就是为了解决类似上述的问题而提供的组件。



# Pillar是什么？

如[这篇文章](/2013/07/02/salt_state_config_structure.html)所述，Salt Sate定义了配置项以及minion和配置项直接的映射关系；与此类似，Pillar定义了数据以及minion和数据的映射关系。Pillar中定义的数据可以在Salt的其他组件中引用，当然最常见的情况是在State中引用Pillar数据。

比如，在上一节的第一个问题中，我们可以这样定义State:

{% highlight yaml %}

  apache:
    pkg.installed:
      - name: {{ pillar['apache'] }}

{% endhighlight %}

其中，`salt.states.pkg.installed`函数的`name`参数就是引用了Pillar中定义的变量`apache`。

而该变量在Pillar中的定义如下：

{% highlight yaml %}

{ % if grains['os_family'] == 'RedHat' % }
apache: httpd
{ % elif grains['os_family'] == 'Debian' % }
apache: apache2
{ % endif % }

{% endhighlight %}


# Pillar的配置结构

Pillar与State就像是配置管理的左右手，所以Pillar的配置结构与[State的配置结构](/2013/07/02/salt_state_config_structure.html)几乎完全一样。

## Pillar Tree和Environment

与[State Tree](/2013/07/02/salt_state_config_structure.html#menuIndex0)一样，Salt中可以定义一棵Pillar Tree，并且将Pillar按照环境进行分组管理。

Pillar Tree定义在salt master的配置文件`/etc/salt/master`的`pillar_roots`变量中：

{% highlight yaml %}

 pillar_roots:
   base:
     - /srv/pillar
 
   ext_pillar:
     - hiera: /etc/hiera.yaml
     - cmd_yaml: cat /etc/salt/yaml

{% endhighlight %}

## Pillar定义

Pillar是一组key-value，使用yaml的语法格式。

简单的定义比如：

    foo: bar

可以使用` { { pillar['foo'] } }`的形式进行引用；

复杂的定义比如：

{% highlight yaml %}
users:
  thatch: 1000
  shouse: 1001
  utahdave: 1002
  redbeard: 1003  

{% endhighlight %}

可以使用包含jinja语法的yaml进行引用：

{% highlight yaml %}

 { % for user, uid in pillar.get('users', {}).items() % }
   { {user} }:
     user.present:
       - uid: { {uid} }
 { % endfor % }

{% endhighlight %}

定义好的pillar数据保存在Pillar Tree下面的某个`sls`文件中。为了能够在State中引用Pillar数据，
Pillar的目录结构和文件名需要与State能够对应。

Pillar可以用于任何数据的定义，比如ssh key、证书、密码口令等敏感数据，minion的模块、状态、信息反馈，以及要传递给minion的任何变量的值等等。
这些数据都会以加密通道安全的分发到minion上面。

Pillar的数据不仅仅可以来自SLS文件，还可以从其他数据源获取数据。相关内容可以自行查阅[官方文档](http://docs.saltstack.com/topics/pillar/index.html)。


## minion与Pillar之间的映射

与[minion与state之间的映射](/2013/07/02/salt_state_config_structure.html#menuIndex2)一样，
在Pillar的base目录中也存在一个名为`top.sls`的入口文件，定义minion与Pillar的映射关系，例如：

{% highlight yaml %}

base:
  '*':
    - packages
  'alpha':
    - database

{% endhighlight %}

上边的例子定义了packages对所有的minion有效，database只对名字为'alpha'的minion有效.



# Pillar数据的查询和使用

1. 查询pillar数据

   {% highlight yaml %}
    salt 'client2' pillar.data
    salt '*' pillar.data
    salt '*' pillar.raw key='roles'
   {% endhighlight %} 

更多的函数可以参考[pillar模块的文档](https://salt.readthedocs.org/en/latest/ref/modules/all/salt.modules.pillar.html)。

2. 刷新pillar数据

   在master上修改Pilla文件后，需要用以下命令刷新minion上的数据（同步到minion）：

       salt '*' saltutil.refresh_pillar


3. 在其他sls文件中引用数据

   Pillar解析后是dict对象，直接使用Python语法，可以用索引（`pillar['pkgs']['apache']`）或get方法（`pillar.get('users', {})`）获取到需要的数据。

4. 在Targetting中使用Pillar

   Targetting中可以用`-I`选项指定用Pillar数据选择minion。




# 参考资料

- [《Pillar Walkthrough》](http://docs.saltstack.com/topics/tutorials/pillar.html)
- [《Pillar of Salt》](http://docs.saltstack.com/topics/pillar/index.html)