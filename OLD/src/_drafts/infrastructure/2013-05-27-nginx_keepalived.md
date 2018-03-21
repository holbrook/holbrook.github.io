---
layout: post
title: "用nginX+keepalived实现高可用的负载均衡"
description: "实施nginx和keepalived的规划、安装、配置等步骤"
category: 基础设施
tags: [HA, nginx, keepalived, 负载均衡, cluster]
lastmod: 2013-07-30
---

前面的[《统一web访问层方案》](http://thinkinside.tk/weblayer_nginx_keepalived/)中就目的、目标和整体方案进行了讨论，本文讨论具体的实施。简单来说就是在两台服务器上分别部署NginX，并通过keepalived实现高可用。


# 1 规划和准备
---

需要统一访问的应用系统：
<table>
  <tr><th>应用系统</th><th>	域名/虚拟目录</th><th>应用服务器及URL</th></tr>
  <tr><td>svn</td><td>	dev.mycompany.com/svn	</td><td>http://50.1.1.21/svn</td></tr>
  <tr><td>svn web管理</td><td>	dev.mycompany.com/submin	</td><td>http://50.1.1.21/submin</td></tr>
  <tr><td>网站	</td><td>www.mycompany.com	</td><td>http://50.1.1.10; http://50.1.1.11; http://50.1.1.12</td></tr>
  <tr><td>OA</td><td>	oa.mycompany.com	</td><td>http://50.1.1.13:8080; http://50.1.1.14:8080</td></tr>
</table>


web访问服务器

用两台接入服务器50.1.1.3/4分别作为主、备(MASTER、BACKUP)服务器，使用RHEL5.6x64，配置了yum 私服。

两台接入服务器公用一个虚拟IP（VIP）：50.1.1.2





# 2 安装
---

两台接入服务器分别安装NginX和keepalived:

{% highlight bash %}
    #准备依赖包：
    yum -y install gcc pcre-devel zlib-devel openssl-devel
    
    #下载
    wget http://nginx.org/download/nginx-1.2.4.tar.gz 
    wget http://www.keepalived.org/software/keepalived-1.2.7.tar.gz
    
    #安装NginX
    tar zxvf nginx-1.2.4.tar.gz
    cd nginx-1.2.4
    ./configure
    make && make install

    #安装keepalived
    tar zxvf keepalived-1.2.7.tar.gz
    cd keepalived-1.2.7
    ./configure
    make 
    make install

    cp /usr/local/etc/rc.d/init.d/keepalived /etc/rc.d/init.d/
    cp /usr/local/etc/sysconfig/keepalived /etc/sysconfig/
    mkdir /etc/keepalived
    cp /usr/local/etc/keepalived/keepalived.conf /etc/keepalived/
    cp /usr/local/sbin/keepalived /usr/sbin/

    #加入启动
    echo "/usr/local/nginx/sbin/nginx" >> /etc/rc.local
    echo "/etc/init.d/keepalived start" >> /etc/rc.local
 
{% endhighlight %}

# 3 配置
 
## 3.1 配置NginX

两台接入服务器的NginX的配置完全一样,主要是配置/usr/local/nginx/conf/nginx.conf的http。其中多域名指向是通过虚拟主机（配置http下面的server）实现；同一域名的不同虚拟目录通过每个server下面的不同location实现；到后端的服务器在http下面配置upstream,然后在server或location中通过proxypass引用。要实现前面规划的接入方式，http的配置如下：

{% highlight c %}
    http {
        include       mime.types;
        default_type  application/octet-stream;
    
        sendfile        on;
    
        upstream dev.hysec.com {
            server 50.1.1.21:80;
        }
    
    
        upstream www.hysec.com {
          ip_hash;
          server 50.1.1.10:80;
          server 50.1.1.11:80;
          server 50.1.1.12:80;
        }
    
        upstream oa.hysec.com {
          ip_hash;
          server 50.1.1.13:8080;
          server 50.1.1.14:8080;
          
    
        server {
            listen      80;
            server_name dev.hysec.com;
            location /svn {
                proxy_pass http://dev.hysec.com;
            }
    
            location /submin {
                proxy_pass http://dev.hysec.com;
            }
        }
    
        server {
            listen       80;
            server_name  www.hysec.com;
            location / {
                proxy_pass http://www.hysec.com;
            }
        server {
            listen       80;
            server_name  oa.hysec.com;
            location / {
                proxy_pass http://oa.hysec.com;
            }
    }
{% endhighlight %}
 

验证方法：

首先用IP访问前表中各个应用服务器的url，再用域名和路径访问前表中各个应用系统的域名/虚拟路径


## 3.2 配置keepalived

按照上面的安装方法，keepalived的配置文件在/etc/keepalived/keepalived.conf。主、从服务器的配置相关联但有所不同。如下：

- Master配置

  {% highlight c %}

    ! Configuration File for keepalived

    global_defs {
    notification_email {
            wanghaikuo@hysec.com
            wanghaikuo@gmail.com
       }

       notification_email_from wanghaikuo@hysec.com
       smtp_server smtp.hysec.com
       smtp_connect_timeout 30
       router_id nginx_master

    }

    vrrp_instance VI_1 {
        state MASTER
        interface eth0
        virtual_router_id 51
        priority 101
        advert_int 1
        authentication {
            auth_type PASS
            auth_pass 1111
        }
        virtual_ipaddress {
            50.1.1.2
        }
    }
  {% endhighlight %}    

- Backup配置

  {% highlight c %}
    ! Configuration File for keepalived

    global_defs {
    notification_email {
            wanghaikuo@hysec.com
            wanghaikuo@gmail.com
       }

       notification_email_from wanghaikuo@hysec.com
       smtp_server smtp.hysec.com
       smtp_connect_timeout 30
       router_id nginx_backup

    }

    vrrp_instance VI_1 {
        state BACKUP
        interface eth0
        virtual_router_id 51
        priority 99
        advert_int 1
        authentication {
            auth_type PASS
            auth_pass 1111
        }
        virtual_ipaddress {
            50.1.1.2
        }
    }
  {% endhighlight %}    


验证：

1. 先后在主、从服务器上启动keepalived: 

    /etc/init.d/keepalived start

2. 在主服务器上查看是否已经绑定了虚拟IP： 

    ip addr

3. 停止主服务器上的keepalived: 
    
    /etc/init.d/keepalived stop 

4. 然后在从服务器上查看是否已经绑定了虚拟IP

5. 启动主服务器上的keepalived，看看主服务器能否重新接管虚拟IP

## 3.3 让keepalived监控NginX的状态

经过前面的配置，如果主服务器的keepalived停止服务，从服务器会自动接管VIP对外服务；一旦主服务器的keepalived恢复，会重新接管VIP。 但这并不是我们需要的，我们需要的是当NginX停止服务的时候能够自动切换。

keepalived支持配置监控脚本，我们可以通过脚本监控NginX的状态，如果状态不正常则进行一系列的操作，最终仍不能恢复NginX则杀掉keepalived，使得从服务器能够接管服务。

如何监控NginX的状态
最简单的做法是监控NginX进程，更靠谱的做法是检查NginX端口，最靠谱的做法是检查多个url能否获取到页面。

如何尝试恢复服务
如果发现NginX不正常，重启之。等待3秒再次校验，仍然失败则不再尝试。

根据上述策略很容易写出监控脚本。这里使用nmap检查nginx端口来判断nginx的状态，记得要首先安装nmap。监控脚本如下:

{% highlight bash %}

    #!/bin/sh
    # check nginx server status
    NGINX=/usr/local/nginx/sbin/nginx
    PORT=80

    nmap localhost -p $PORT | grep "$PORT/tcp open"
    #echo $?
    if [ $? -ne 0 ];then
        $NGINX -s stop
        $NGINX
        sleep 3
        nmap localhost -p $PORT | grep "$PORT/tcp open"
        [ $? -ne 0 ] && /etc/init.d/keepalived stop
    fi

 {% endhighlight %}

不要忘了设置脚本的执行权限，否则不起作用。

假设上述脚本放在/opt/chk_nginx.sh，则keepalived.conf中增加如下配置：
{% highlight c %}

    vrrp_script chk_http_port {
        script "/opt/chk_nginx.sh"
        interval 2
        weight 2
    }

    track_script {
        chk_http_port
    }
{% endhighlight %}

更进一步，为了避免启动keepalived之前没有启动nginx , 可以在/etc/init.d/keepalived的start中首先启动nginx:
{% highlight c %}

    start() {
        /usr/local/nginx/sbin/nginx
        sleep 3
        echo -n $"Starting $prog: "
        daemon keepalived ${KEEPALIVED_OPTIONS}
        RETVAL=$?
        echo
        [ $RETVAL -eq 0 ] && touch /var/lock/subsys/$prog
    }

 {% endhighlight %}

# 4 还可以做什么

对于简单重复性劳动，人总是容易犯错，这种事情最好交给机器去做。 比如，在这个案例中，作为统一接入服务器，可能经常要修改nginx的配置、nginx下面的html文件等。而且，一定要保证集群中的每台服务器的配置相同。 最好的做法是由配置管理服务器来管理，如果没有，也可以使用简单的linux文件同步来解决。

# 5 支持https

需要安装openSSL：
    
    yum install openssl-devel

在nginx/conf下生成秘钥：

{% highlight bash %}
    #生成RSA密钥
    openssl dsaparam -rand -genkey -out myRSA.key 1024

    #生成CA密钥：(要输入一个自己记得的密码)
    openssl gendsa -des3 -out cert.key myRSA.key

    #用这个CA密钥来创建证书，需要上一步创建的密码
    openssl req -new -x509 -days 365 -key cert.key -out cert.pem

    #把证书设置为root专用
    chmod 700 cert.*

    #生成免密码文件
    openssl rsa -in cert.key -out cert.key.unsecure

{% endhighlight %}    

如果要启用SSL，首先在安装nginx是要增加配置参数：--with-http_ssl_module ，
然后在nginx中进行如下配置：

{% highlight c %}
    # 这里是SSL的相关配置
    server {
      listen 443;
      server_name www.example.com; # 你自己的域名
      root /home/www;
      ssl on;
      ssl_certificate cert.perm;
      #使用.unsecure文件可以在nginx启动时不输入密码  
      ssl_certificate_key cert.key.unsecure;
      location / {
      #...
      }
    }
{% endhighlight %}    

公共证书的申请过程：

1. 生成RSA(私钥)文件：

    `openssl genrsa -des3 -out myRSA.key 2048`

2. 生成csr文件：
 
    `openssl req -new -key myRSA.key -out my.csr`

3. 将csr提交给证书机构，比如GlobalSign。

4. 证书机构会返回私有证书(crt)和中级证书（crt）

5. 到机构网站下载根证书（root_CA.cer), 将根证书拼接到私有证书之后

6. 在nginx中配置证书：

{% highlight c %}
    ssl_certificate /etc/ssl/my.crt;
    ssl_certificate_key /etc/ssl/myRSA.key;
    ssl_client_certificate /etc/ssl/root_CA.cer;

{% endhighlight %}    

# 6 支持webservice

通过chunkin-nginx-module模块支持webservice。

否则会报错：411：http 头中缺少 Conten-Length 参数

步骤：

{% highlight bash %}
    git clone https://github.com/agentzh/chunkin-nginx-module.git

    #重新编译nginx
    cd PATH/TO/NGINX/SOURCE
    ./configure xxx --add-module=/PATH/TO/chunkin-nginx-module
    make && make install

{% endhighlight %}    

在nginx的server{}节点中增加配置：
{% highlight c %}

    chunkin on; 
 
    error_page 411 = @my_411_error; 

    location @my_411_error { 
        chunkin_resume; 
    } 
{% endhighlight %}    

# 7 状态监控

编译时需要增加`--with-http_stub_status_module`参数。

查看编译参数：使用命令`/usr/local/nginx/sbin/nginx -V`

安装好之后增加配置：
{% highlight nginx %}

    location /nginx_status {
        stub_status on;
        access_log   off;
        # deny all;
        allow all;
    }

{% endhighlight %} 

重新加载配置后，会看到一些文本：

Active connections: 1 （对后端发起的活动连接数）

server accepts handled requests

 5 5 5  （处理连接个数，成功握手次数，处理请求数）

Reading: 0 Writing: 1 Waiting: 0 （读取客户端header数，返回客户端header数，等待数即active-reading-writing）

