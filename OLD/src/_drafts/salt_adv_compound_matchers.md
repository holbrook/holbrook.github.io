## 复合匹配

[复合匹配方式(Compound matchers)](http://docs.saltstack.com/topics/targeting/compound.html)
可以同时使用多种匹配规则。

上面的例子中都是通过salt命令的参数（如`-E`，`-L`）来指定匹配方式，复合匹配通过字母+“@”+字符串来指定规则。包括：

- G: 通配符
- E: 正则表达式
- P: [PCRE](http://pcre.org/)类型的正则表达式，匹配
G@os:Ubuntu
E
PCRE Minion id匹配
E@web\d+\.(dev|qa|prod)\.loc
P
Grains PCRE匹配
P@os:(RedHat|Fedora|CentOS)
L
minions列表
L@minion1.example.com,minion3.domain.com or bl*.domain.com
I
Pillar glob匹配
I@pdata:foobar
S
子网/IP地址匹配
S@192.168.1.0/24 or S@192.168.1.100
R
Range cluster匹配
R@%foo.bar
D
Minion Data匹配
D@key:value
匹配中可以使用and、or及not等boolean型操作

例如，想匹配所有minion中主机名(minion id)以webserv开头并且运行在Debian系统上或者minion的主机名(minion id)匹配正则表达式web-dc1-srv.*:

salt -C 'webserv* and G@os:Debian or E@web-dc1-srv.*' test.ping
在top.sls中可以如下使用:

base:
  'webserv* and G@os:Debian or E@web-dc1-srv.*':
    - match: compound
    - webserver


G
Grains glob匹配
G@os:Ubuntu
E
PCRE Minion id匹配
E@web\d+\.(dev|qa|prod)\.loc
P
Grains PCRE匹配
P@os:(RedHat|Fedora|CentOS)
L
minions列表
L@minion1.example.com <mailto:L@minion1.example.com>,minion3.domain.com or bl*.domain.com
I
Pillar glob匹配
I@pdata:foobar
S
子网/IP地址匹配
S@192.168.1.0 <mailto:S@192.168.1.0>/24 or S@192.168.1.100 <mailto:S@192.168.1.100>
R
Range cluster匹配
R@%foo.bar
D
Minion Data匹配
D@key:value
匹配中可以使用and、or及not等boolean型操作
例如，想匹配所有minion中主机名(minion id)以webserv开头并且运行在Debian系统上或者minion的主机名(minion id)匹配正则表达式 <http://docs.python.org/2/library/re.html#module-re>web-dc1-srv.*:
salt -C 'webserv* and G@os:Debian or E@web-dc1-srv.*' test.ping
在top.sls中可以如下使用:
base:
  'webserv* and G@os:Debian or E@web-dc1-srv.*':
    - match: compound
    - webserver



混合匹配
混合匹配(Compound matchers)是指在操作时使用多种预定义的匹配方法。默认匹配规则是glob <http://docs.python.org/2/library/fnmatch.html>. 在使用混合匹配时，需要先匹配前指定letter， 当前支持的“letter”有：
Letter
含义
例子
G
Grains glob匹配
G@os:Ubuntu
E
PCRE Minion id匹配
E@web\d+\.(dev|qa|prod)\.loc
P
Grains PCRE匹配
P@os:(RedHat|Fedora|CentOS)
L
minions列表
L@minion1.example.com <mailto:L@minion1.example.com>,minion3.domain.com or bl*.domain.com
I
Pillar glob匹配
I@pdata:foobar
S
子网/IP地址匹配
S@192.168.1.0 <mailto:S@192.168.1.0>/24 or S@192.168.1.100 <mailto:S@192.168.1.100>
R
Range cluster匹配
R@%foo.bar
D
Minion Data匹配
D@key:value
匹配中可以使用and、or及not等boolean型操作
例如，想匹配所有minion中主机名(minion id)以webserv开头并且运行在Debian系统上或者minion的主机名(minion id)匹配正则表达式 <http://docs.python.org/2/library/re.html#module-re>web-dc1-srv.*:
salt -C 'webserv* and G@os:Debian or E@web-dc1-srv.*' test.ping
在top.sls中可以如下使用:
base:
  'webserv* and G@os:Debian or E@web-dc1-srv.*':
    - match: compound
    - webserver

