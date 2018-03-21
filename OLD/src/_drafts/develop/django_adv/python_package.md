# 包信息管理器


[yolk](https://pypi.python.org/pypi/yolk)。
Command-line tool querying PyPI and Python packages installed on your system.

yolk可以查询某个虚拟环境或系统环境中已经安装了哪些包：

{% highlight bash %}

  # 安装yolk
  sudo pip install yolk

  # 激活某个虚拟环境
  source /PATH/TO/YOUR/VIRTUAL_ENV/ENV_NAME/bin/active

  # 查看包信息
  yolk -l

{% endhighlight %}




Usage Examples:

$ yolk -l
     List all installed Python packages

$ yolk -a
     List only the activated packages installed (Activated packages are normal packages on sys.path you can import)

$ yolk -n
     List only the non-activated (--multi-version) packages installed

$ yolk -l -f License,Author nose==1.0
     Show the license and author for version 1.0 of the package `nose`

$ yolk --entry-map nose
     Show entry map for the nose package

$ yolk --entry-points nose.plugins
     Show all setuptools entry points for nose.plugins
These options query PyPI:

$ yolk -U pkg_name
     Shows if an update for pkg_name is available by querying PyPI

$ yolk -U
     Checks PyPI to see if any installed Python packages have updates available.

$ yolk -F Paste
     Download source tarball for latest version of Paste to your current directory

$ yolk -F Paste -T svn
     Do a subversion checkout for Paste to a directory named Paste_svn in your current directory.

$ yolk -L 2
     Show list of CheeseShop releases in the last two hours

$ yolk -C 2
     Show detailed list of changes in the CheeseShop in the last two hours

$ yolk -M Paste==1.0
     Show all the metadata for Paste version 1.0

$ yolk -M Paste
     Show all the metadata for the latest version of Paste listed on PyPi

$ yolk -D cheesecake
     Show all (source, egg, svn) URL's for the latest version of cheesecake packages

 $ yolk -T source -D cheesecake
     Show only source code releases for cheesecake

 $ yolk -H twisted
     Launches your web browser at Twisted's home page

# 自动部署

Febric