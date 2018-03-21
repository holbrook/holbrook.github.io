---
layout: post
title: "subversion安装、配置和管理"
description: "尽管svn已经被历史所抛弃，但同样由于历史原因，还要整理一下svn的配置文档。"
category: 基础设施
tags: [版本管理]
lastmod: 
---

# 安装

这个没什么可写的：

```bash
yum install subversion
```



# 管理

通过`svnadmin`可以实现大多数的管理操作

## 创建版本库

```bash
  mkdir $SVN_REPOSITORIES_ROOT
  cd $SVN_REPOSITORIES_ROOT
  
  # 创建dev库
  svnadmin create dev
  
  # 创建文档库
  svnadmin create doc
  
  ……
```

## 更改配置

每个svn库有单独的配置，在每个生成的仓库目录的`conf/svnserve.conf`文件中可以进行更改。

比如，指定用户和权限的配置内容：

```
password-db = passwd
authz-db = authz
```
意思是使用`conf/passwd`文件保存用户密码；

使用`conf/authz-db`文件保存用户组和权限设置。

## 用户管理

通常，将所有库的密码和用户组、权限进行统一管理是比较好的方式。可以将每个svn库的配置文件中的`password-db`、`authz-db`都指到相同的文件。

密码文件的格式为：

```
  [users]
  user1 = pwd1
  user2 = pwd2
```

用户组和权限文件的格式为：

```
  [groups]
  # <用户组名> = <用户1>,<用户2>
  harry_and_sally = harry,sally
  harry_sally_and_joe = harry,sally,&joe
  
  # [<版本库>:/项目/目录]
  # @<用户组名> = <权限>
  # <用户名> = <权限>
  
  [/foo/bar]
  harry = rw
  * = r
  
  [repository:/baz/fuz]
  @harry_and_sally = rw
  * = r
```

用户组和权限配置文件需要手工编辑，而密码文件通过[Apache的`htpasswd`命令](http://httpd.apache.org/docs/2.2/programs/htpasswd.html)进行操作。比如:

```
htpasswd -mb passwd USER_NAME PASSWORD
```

## 启动服务

```
svnserve -d --listen-port 9999 -r $SVN_REPOSITORIES_ROOT
```

即可通过`svn://$SVN_SERVER:9999/dev`访问svn服务。

# 通过Apache提供http访问

svn可以通过WebDAV的方式与Apache集成。配置步骤如下：

1. 安装svn的apache模块：

   `yum install mod_dav_svn`

    该操作会在`/etc/httpd/conf/httpd.conf`中增加模块配置：

   ```
   LoadModule dav_svn_module     modules/mod_dav_svn.so
   LoadModule authz_svn_module   modules/mod_authz_svn.so
   ```
   
   并将相应的模块文件安装到Apache的模块目录(`/etc/httpd/modules/`)。


2. 在Apache中增加svn的虚拟目录配置，比如：

   ```
    <Location /svn>
        DAV svn
        SVNParentPath $SVN_REPOSITORIES_ROOT

        AuthType Basic
        AuthName "Subversion repository"

        AuthUserFile $SVN_CONF_PATH/htpasswd
        AuthzSVNAccessFile $SVN_CONF_PATH/authz

        Satisfy Any
        Require valid-user
    </Location>
   ```

   此时，启动Apache后就可以通过`http://$SVN_SERVER:$APACHE_PORT/svn/dev`访问svn服务，
   并且使用svn中账号配置。

# https支持

因为已经集中使用nginx实现https支持，这部分内容略。

# Web管理工具

登录到svn服务器用`svnadmin`、`htpasswd`等命令进行svn的管理让人非常乏味，且容易出错。

这里选择使用python开发的[Submin](http://supermind.nl/submin/作为Web管理工具。
Submin不仅可以提供svn的Web管理界面，还可以简化svn的安装部署工作；
此外，还提供了与[git](http://git-scm.com/), [Trac](http://trac.edgewall.org/)等集成的功能。


[下载Submin](http://supermind.nl/submin/download.html)并安装。

1. 创建submin运行环境

执行命令：

```
submin2-admin ./submin_root initenv your@email.address
```

2. 配置

使用submin，可以省略手工配置svn的apache支持的步骤：

```
ln -s $PATH_TO_SBMIN_ROOT/conf/apache-webui-cgi.conf /etc/httpd/conf.d/
ln -s $PATH_TO_SBMIN_ROOT/conf/apache-svn.conf /etc/httpd/conf.d/
```

3. 新的认证机制

Submin2开始，使用Apache的mod_dbd模块，从数据库中读取认证信息。

# 备份和恢复

根据网上的内容，svn在不停止服务的情况下，不能基于文件复制(copy, rsync等）进行备份（没有测试过）。

svn备份一般采用三种方式：

1. svnadmin dump

   支持全量和增量备份；备份和恢复的速度较慢。

2. svnadmin hotcopy

   只能用于全量复制，速度非常快，但消耗较大的存储空间。

3. svnsync

   只用于双机热备的场景。


这里采取的策略是：

1. 每周使用svnadmin dump进行全备份
2. 每天使用svnadmin dump进行增量备份，并备份密码和权限文件
3. 每次的备份恢复到svn备机，进行恢复验证
4. 每天同步到灾备中心


关键命令（以`dev`库为例）：

- 读取当前revision

  `cat $SVN_REPOSITORIES_ROOT/dev/db/current |awk '{print $1}'`

- 全备份

  `svnadmin dump --deltas $SVN_REPOSITORIES_ROOT/dev |bzip2 |tee dev_full.bz2  | md5sum >dev_full.md5`

- 备份单个revision(比如，revision 10)

  `svnadmin dump --deltas $SVN_REPOSITORIES_ROOT/dev -r10 |bzip2 |tee dev_10.bz2  | md5sum >dev_10.md5`

- 备份revision区段(比如，revision [10,15])

  `svnadmin dump --deltas $SVN_REPOSITORIES_ROOT/dev -r10:15 –-incremental |bzip2 |tee dev_10-15.bz2  | md5sum >dev_10-15.md5`

- md5校验

  `md5sum -c dev_full.md5 < dev_full.bz2`

- 恢复

  `bzcat dev_full.bz2 | svnadmin load dev`

  注意按顺序恢复；如果是恢复全库备份，最好删除原有的库。
