---
title: 搭建一个“现代化”的web开发环境
postslug: modern_web_dev_env
date: 2015-05-04
category: 软件技术
tags: [web, env]
---

使用yoeman, bower, grunt等工具开发web。

<!-- more -->


#  目标

将要开展的一个项目，使用Angularjs 和 Flask开发一个web界面，
作为saltstack和其他自行开发的python小工具的前端界面，
实现自己的“运维操作平台”。

为了统一框架、工具和开发方式，在本文中描述了项目的一些约定。
这些约定具有通用性，应该是目前基于python的web开发技术中，
比较”主流“和”先进“的方式，所以也可以作为开发其他应用的参考。

# 工具和框架

## 工具

- 版本管理
    基于[gogs](http://gogs.io/) 的私有git
- 问题管理、版本发布、资料共享
    [redmine](http://www.redmine.org/)
- 项目管理
    [redmine的scrum插件](http://www.redminebacklogs.net/)
- nodejs包管理器
    [npm](https://www.npmjs.com/)(node package manager)。

    本文中，npm仅作为安装yoeman, bower，grunt等的基础工具。

- js依赖管理: [bower](http://bower.io/)
    npm可以安装js包，但是没有解决依赖的问题。而bower解决了js包的依赖管理。类似maven中的依赖管理功能。

- 前端构建工具: [grunt](http://gruntjs.com/)
    js开发中的项目构建工具，类似maven/ant/makefile，
    通过配置文件执行压缩,编译, 单元测试, 代码检查以及打包发布的任务。

- 前端脚手架工具
    [yoeman]()。类似maven的archetypes。

-   python开发环境管理
    [virtualenv](http://virtualenv-chinese-docs.readthedocs.org/en/latest/)

## 框架和插件

- 样式库 [Bootstrap](http://getbootstrap.com/)
    + [chartjs](https://github.com/nnnick/Chart.js/)

- 前端框架：[AngularJS](https://angularjs.org/)
- 后端框架：[Flask]()
    + Flask-SQLAlchemy
    + Flask-RESTful

## 环境准备

    本文中仅给出MacOS下的安装方法，其他系统可以阅读官方文档或参考资料。

```bash
#安装npm
brew install npm

#全局安装工具
npm install -g yo grunt-cli grunt bower generator-angular

#安装virtualenv
sudo easy_install pip
sudo pip install virtualenv
```

# 搭建工程

## 创建工程目录

``` bash
mkdir -p PROJ\_ROOT/web \# 前端工程目录 mkdir -p
PROJ\_ROOT/app/APP\_NAME \# 后端工程目录 \#+END
```

## 创建前端工程

``` bash
cd PROJ\_ROOT/web yo angular \# 一些交互，按照自己的需要选择即可。 \#...
```

## 配置前端工程

1. 修改IP地址

    将connect -\> hostname, 由'localhost' 改为 '0.0.0.0'

2. 修改dist目录

    将appConfig -\> dist 有 'dist' 改为 '../app/APP\_NAME/static'

3. virtualenv

``` bash
cd PROJ\_ROOT
virtualenv venv
source venv/bin/activate
pip install flask
pip install sqlalchemy
pip install flask-sqlalchemy
...
pip freeze > app/requirements.txt
```


4. 构建Flask工程

``` bash
mkdir -p PROJ\_ROOT/app/APP\_NAME/common
mkdir -p PROJ\_ROOT/app/APP\_NAME/models
mkdir -p PROJ\_ROOT/app/APP\_NAME/static
mkdir -p PROJ\_ROOT/app/APP\_NAME/templates
mkdir -p PROJ\_ROOT/app/APP\_NAME/views

touch PROJ\_ROOT/app/APP\_NAME/common/__init__.py
touch PROJ\_ROOT/app/APP\_NAME/models/__init__.py
touch PROJ\_ROOT/app/APP\_NAME/views/__init__.py
```

6. 配置git

``` bash
cd PROJ\_ROOT
mv web/.gitattributes .
rm -f web/.gitignore
cat > .gitignore << EOF
web/node_modules
web/.tmp
web/.sass-cache
web/bower_components
dist
venv
EOF
```

# 使用

  以上是工程框架搭建的过程，对于开发人员，不需要要这么麻烦，只要从版本库中获取源代码后进行初始化即可：

``` bash
git clone xxxx cd PROJ_ROOT
virtualenv venv
source venv/bin/activate
pip install -r app/requirements.txt
cd web
npm install
bower install
```

## 启动前端

``` bash
cd PROJ_ROOT/web
grunt serve
```

  然后通过http://0.0.0.0:9000可以访问前端界面。

## 启动后端
``` bash
cd PROJ\_ROOT/app
python run.py
```

    然后通过http://127.0.0.1:5000/ 访问后端应用。

# 知识准备

    在开始开发之前，开发人员最好熟悉以下内容：

    - Bootstrap入门: http://v3.bootcss.com/getting-started/
    - Angularjs入门教程: http://www.ituring.com.cn/article/13471
    - Flask系列教程 :http://www.oschina.net/translate/the-flask-mega-tutorial-part-i-hello-world
    - SQLAlchemy教程:

# 参考资料

1.  NPM小结 chyingp http://www.cnblogs.com/chyingp/p/npm.html
2.  bower解决js的依赖管理 | 粉丝日志
    http://blog.fens.me/nodejs-bower-intro/
3.  getting started with Yeoman http://yeoman.io/learning/index.html
4.  Yeoman自动构建js项目 | 粉丝日志
    http://blog.fens.me/nodejs-yeoman-intro/
5.  grunt让Nodejs规范起来 | 粉丝日志
    http://blog.fens.me/nodejs-grunt-intro/
6.  Bootstrap入门 http://v3.bootcss.com/getting-started/
7.  AngularJS入门教程 http://www.ituring.com.cn/article/13471
8.  Flask系列教程
    http://www.oschina.net/translate/the-flask-mega-tutorial-part-i-hello-world
9.  使用 Flask 和 AngularJS 构建博客 - 1
    http://segmentfault.com/a/1190000000654088
10. 使用 Flask 和 AngularJS 构建博客 - 2
    http://segmentfault.com/a/1190000000665636

---

