# 初始化项目



http://fsjoy.blog.51cto.com/318484/244803

配置git

在使用git之前你需要配置一下git。git在你创建提交的时候会记录你的名字和email地址，所以你应该告诉git这些内容。可以使用'git config'命令来设置，如果传递参数'-global' ，它会将这些值记录在~/.gitconfig文件里，作为这些配置的默认值。
$ git config --global user.name "Scott Chacon"
$ git config --global user.email "schacon@gmail.com"

在使用git的过程中，经常会用到文本编辑器。默认情况下它使用的是vim。如果你喜欢用其他的编辑器，例如emacs，你可以这样设置：
$ git config --global core.editor 'emacs'

查看设置值可以通过这样的命令：
$ git config user.name

你也可以自己编辑文件内容。git首先会检查'/etc/gitconfig'，然后是'~/.gitconfig'最后是'.git/config'，这些文件里的内容格式类似这样：
$ cat ~/.gitconfig
 
[user]
name = Scott Chacon
email = schacon@gmail.com
 

2.初始化一个新的git仓库
在一个已存在的目录中初始化git存储，只要在目录下输入'git init'命令即可。这样会为这个目录生成一个基本的git存储框架。
$ rails myproject
$ cd myproject
$ git init

现在，就有了一个空的git存储（你可以查看目录下的'.git'目录）。现在就可以stage和提交（commit）文件到这个目录了。分别使用'git add'和'git commit'命令。下一节深入讲解这些命令。
$ git add .
$ git commit -m 'initial commit'

这样你就有了一个完整的提交之后的git存储了，可以运行'git log'（下一节深入讲解）
$ git log
 
commit eac2f939e6a1cb3189fedd19919888d998ab0431
Author: Scott Chacon <schacon@gmail.com>
Date:   Sun Feb 8 07:55:57 2009 -0800
    initial commit


克隆一个git仓库
git可以通过很多的协议进行网络通信，其中有三个最主要的协议，分别是ssh，http，git（专职为git服务的协议）

匿名访问方式：通过git://或者http.
不管使用何种协议克隆git存储，格式都是这样：'git clone uri'， uri的格式：
"git://(hostname)/(path).git"

 
$ git clone git://github.com/schacon/munger.git
$ cd munger
$ git log

当然也可以使用http克隆，跟上面的类似，就是将git换成了http。
$ git clone http://github.com/schacon/munger.git

这仅仅适用于服务器支持这两种协议的情况。如果服务器是GitHub的话，这两种方式都是可以的。








###  aaa

Git 初始化 
2010-08-26 16:53
**********************************************************

为git安装一个远程仓库
2010-05-28 Linux 查看评论 需要将代码push到一个远程仓库

在远程服务器上初始化空的仓库

mkdir /home/git/myapp.git  && cd /home/git/myapp.git
git –bare init
初始化了一个空的仓库

在本地的git仓库添加一个远程仓库
cd  ~/myapp
git remote add origin ssh://myserver.com/home/git/myapp.git
这时候,本地的 .git/config 应该会改变

git push origin master
将本地的 master分支  跟踪到远程的分支

显示远程信息
git remote show origin


**********************************************************
git默认拒绝了push操作，需要进行设置，修改.git/config添加如下代码：

    [receive]
denyCurrentBranch = ignore

 

在初始化远程仓库时最好使用 git --bare init   而不要使用：git init

   如果使用了git init初始化，则远程仓库的目录下，也包含work tree，当本地仓库向远程仓库push时,   如果远程仓库正在push的分支上（如果当时不在push的分支，就没有问题）, 那么push后的结果不会反应在work tree上,  也即在远程仓库的目录下对应的文件还是之前的内容，必须得使用git reset --hard才能看到push后的内容.


*********************************************************

在初始化远程仓库最好使用下面命令来初始化：

git --bare init

而不要使用：

git init


如果使用了git init初始化，则远程仓库的目录下，也包含work tree，当本地仓库向远程仓库push时
如果远程仓库正在push的分支上（如果当时不在push的分支，就没有问题）
那么push后的结果不会反应在work tree上
也即在远程仓库的目录下
对应的文件还是之前的内容，必须得使用git reset --hard才能看到push后的内容