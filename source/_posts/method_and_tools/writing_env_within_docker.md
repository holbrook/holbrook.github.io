---
title: 使用docker搭建写作环境
postslug: writing_env_within_docker
date: 2017-12-05
category: 方法工具
tags: [env, docker]
---

众所周知，在windows下面使用有些工具等于自虐，比如python, nodejs, pandoc ...
所以，在windows下面，使用markdown写文档变成了一种非常不好的体验。

偏偏有时候又不得不使用windows。比如单位的某上网助手软件，只有windows版本。

幸好有了docker。

<!--more-->

# 目的

在windows下愉快的使用 python (如 anaconda, jupyter-notebook, sphinx等)， nodejs(如 hexo, gitbook 等)，pandoc, git。

# docker简介

`Docker` 是基于 `Linux`的一个 Sandbox 环境，通过模拟整个 `Linux` 的系统文件来实现。`Docker`不是虚拟机，更类似于在`Linux`中模拟`Windows`的`Wine`。

关于 docker 的基本概念和教程，可以参考[这里](https://yeasy.gitbooks.io/docker_practice/content/)。


# Windows7 搭建 docker环境

由于 windows10以下还不支持 Hyper-V，所以在windows10以下(Mac OS X 10.10.3 以下也是同样的问题)使用docker，是通过 Virtualbox变相实现的。

最早的工具是`boot2docker`，现在则使用`docker-machine`。

## 安装

国内访问官网比较慢，可以使用镜像站点 <https://get.daocloud.io/>。
对于Windows7，下载并安装 `Docker Toolbox`。

## 创建及启动 docker 虚拟机

如前所述，Windows7 下面是创建了一个 Virtualbox 虚拟机启动docker，所以要先创建 docker 虚拟机：

```
#查看 docker虚拟机
$docker-machine ls
# 如果没有，可以创建一个
$docker-machine create box
# 启用 docker虚拟机
$docker-machine.exe env box

export DOCKER_TLS_VERIFY="1"
export DOCKER_HOST="tcp://192.168.99.100:2376"
export DOCKER_CERT_PATH="C:\Users\XXXXXXX\.docker\machine\machines\box"
export DOCKER_MACHINE_NAME="box"
export COMPOSE_CONVERT_WINDOWS_PATHS="true"
# Run this command to configure your shell:
# eval$("C:\Program Files\Docker Toolbox\docker-machine.exe" env box)

# 注意输出的信息，还要执行一个命令：
$eval$("C:\Program Files\Docker Toolbox\docker-machine.exe" env box)

# 启动 docker虚拟机
$docker-machine start

# 此时就可以使用docker命令了
$docker images
```


如果此时打开Virtualbox，会发现有一个名为 `box` 的虚拟机并处于启动状态。这个就是docker的运行环境。可以登录到该虚拟机：

```
$docker-machine ssh
                        ##         .
                  ## ## ##        ==
               ## ## ## ## ##    ===
           /"""""""""""""""""\___/ ===
      ~~~ {~~ ~~~~ ~~~ ~~~~ ~~~ ~ /  ===- ~~~
           \______ o           __/
             \    \         __/
              \____\_______/
 _                 _   ____     _            _
| |__   ___   ___ | |_|___ \ __| | ___   ___| | _____ _ __
| '_ \ / _ \ / _ \| __| __) / _` |/ _ \ / __| |/ / _ \ '__|
| |_) | (_) | (_) | |_ / __/ (_| | (_) | (__|   <  __/ |
|_.__/ \___/ \___/ \__|_____\__,_|\___/ \___|_|\_\___|_|
Boot2Docker version 17.11.0-ce, build HEAD : e620608 - Tue Nov 21 18:11:40 UTC 2017
Docker version 17.11.0-ce, build 1caf76c
```

# 交互式创建容器(container)

容器是以镜像(iamge)为模板的。可以查看或加载镜像：

```
$docker images
REPOSITORY          TAG                 IMAGE ID           CREATED       SIZE

# 获取一个镜像作为模板
$docker pull ubuntu

# 基于镜像启动容器
$docker run -it ubuntu bash

# 如果使用 gitbash , 可能需要增加前缀
winpty docker run -it ubuntu bash

# 配置环境

# 安装基础环境
apt-get install bzip2 tzdata locales ttf-wqy-microhei git 

echo "Asia/Shanghai" > /etc/timezone
dpkg-reconfigure  -f noninteractive tzdata

locale-gen en_US.UTF-8


apt-get install pandoc graphviz



apt-get install npm
npm install -g hexo-cli gitbook-cli
ln -s /usr/bin/nodejs /usr/bin/node

```

# 保存到镜像

上面的改动都发生在容器内。也可以把这些改动提交到一个新的容器。

```
# 找到容器的ID
docker ps -a

# 提交到镜像，这个过程可以多次重复
docker commit a30595f088d8 blog_env

# 查看镜像
docker images

REPOSITORY                    TAG                 IMAGE ID            CREATED             SIZE
blog_env                      latest              46365a6c0926        4 seconds ago       112MB
ros                           latest              a674644c9bd3        11 days ago         1.18GB
ubuntu                        latest              0458a4468cbc        11 days ago         112MB
vnpy                          latest              35431482bc9c        8 weeks ago         2.7GB
hub.c.163.com/public/ubuntu   16.04-tools         1196ea15dad6        10 months ago       336MB
```



# 挂载主机文件夹

如果使用了 docker-machine，需要先将本地文件夹挂载到 docker 虚拟机上。
比如 d:\ --> /data。

然后在启动 docker 容器时，通过命令挂载：

```
docker run -it -v /data:/mydata blog_env

cd /mydata
```

这样在容器中，就可以通过　`/mydata` 访问到主机的文件夹了。



# 后台运行和网络访问

```
docker run -d -p 4000:4000 cd /data/holbrook.github.io && hexo s
```

# 使用

```
docker run -d -p 8888:8888 jupyter notebook --ip=0.0.0.0 --no-browser --allow-root
```

然后就可以使用http://docker-machine-ip:8888?token=xxxxxx 访问

winpty docker run -it -p 8888:8888 pyenv

# 编写Dockerfile

所有这些操作，都可以编写成一个 Docker 的 Makefile —— Dockerfile.

{% asset_path Dockerfile 这里 %} 是一个例子。

```
# 先清理容器，以免空间不足
docker rm$(docker ps -a -q)
# 通过dockerbuild制作镜像
docker build -t blog_env .     
```

需要注意的是，当通过dockerfile创建挂载点(mount)时，
所有通过该镜像创建的容器都自动有了挂载点，
但是不能指定主机上的目录。

需要通过`docker inspect`查看过载点的` Source`，然后在主机中创建相应的目录。


# 提交镜像