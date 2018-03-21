---
TITLE: python 任务调度框架
DATE: 2015-06-04
CATEGORIRES: 开发
TAGS: python, 分布式, MQ
---

# 需求

在自主开发的运维操作平台中，有任务调度的需求，具体如下：
1. 分布式任务系统
   saltstack建立了一套“状态管理体系”，通过集中的配置和操作能够管理成千上万个节点的状态，
   但是saltstack并不适合任务的分发（尽管能够做到）。
   同时，很多操作不能在salt-master节点上完成，需要分布在各处的'Agent'去完成，比如全网段的IP扫描。
2. 异步任务
   一个任务不能阻塞后续的任务
3. 定时调度功能
   有些操作需要定期进行，典型的就是各种备份操作。需要能够针对不同的任务设定不同的周期。
4. 任务分派
   能够快速将任务派发给上百个节点；能够灵活的让不同的Agent执行不同的任务，或者一组Agent共同执行一个任务。
5. 任务监控
   能够查看任务执行情况，包括是否成功，花费的时间等。
6. 任务编排
   目前还没有想到具体的应用场景，但是应该会需要将多个子任务按照一定的关系组成高级的任务。

# 轮子

1. APScheduler
   [APScheduler](http://packages.python.org/APScheduler/index.html)
   是基于[Quartz](http://www.quartz-scheduler.org/)的一个Python定时任务框架。
   APScheduler实现了Quartz的所有功能，提供了基于日期、固定时间间隔以及crontab类型的任务，
   并且可以持久化任务。
   但是 APScheduler不是为了分布式的任务调度设计的，要实现分布式架构，需要与Gearman等配合使用。
2. RQ和Celery
   [RQ(Redis Queue)](http://python-rq.org/)，是一个简单的“任务队列”框架，
   而[Celery](https://github.com/celery/celery)则提供了更加强大的功能和扩展性。

3. gevent


# Celery入门

![](celery-architecture.jpg)

Celery中，三个主要的架构角色为：

- Celery Client
  任务产生者。本文中的环境中，Celery Client内置于Flask App中。
- Celery Workers
  任务执行者, 可以是本地，也可以是远程的python进程。
- Message Broker
  在任务产生者和任务执行者之间传递消息，包括任务的发布和结果的反馈等。
  Celery支持很多消息中间件甚至数据库作为Message
  Broker，但是首推的是`RabbitMQ`。



一个简单的例子：
```
#demotask.py 

import time
from celery import Celery

celery = Celery('tasks', broker='amqp://guest:guest@127.0.0.1:5672//')

@celery.task
def demo(msg):
    print('demo task with message: %s...' % msg)
    time.sleep(2.0)
    print('task finished.')
```

这样就定义了一个`Task`。启动一个可以执行该`Task`的`Worker`:

```
celery -A demotask worker 
```

该`Worker`会一直监听RabbitMQ队列，当收到任务信号是就执行`demo`任务。

发布任务的脚本如下：

```
import demotask

demotask.demo.delay('some messages...')

```

# 芹菜花Celery Flower

Celery [Flower](https://github.com/mher/flower/)是Celery的一个Web监控和管理界面。
对于本应用来说，有两个使用场景：

1. 在应用中嵌入Flower的监控界面
2. 使用Flower提供的[RESTful API](http://flower.readthedocs.org/en/latest/api.html)
   管理任务，代替Celery Python API



# 任务组合
subtask
...


# Celery交换机

exchange，决定哪些任务发送到哪个队列

# 模型

## 任务状态

- 挂起(Suspended)
  任务已经创建，但是还没有触发执行条件
- 就绪(Ready)
  任务已经被调度，等待worker执行 
- 運行中(Running)
  worker已經接受任務並開始執行
- 阻塞(Blocked)
  worker已經接受任務，但還需要等待資源才能開始執行
- 完成(Finished)
  worker已經執行任務。完成的結果可能是成功(sucess)或失敗(fail)

Celery 中内置了几种任务状态：

PENDING
RECEIVED
STARTED
FAILURE
RETRY
SUCCESS
REVOKED

Celery也支持自定义状态。

# 架构


## Broker的选择 

Celery目前支持10种[Broker](http://docs.celeryproject.org/en/latest/getting-started/brokers/index.html)， 
并且建议使用RabbitMQ和Redis。
由于RabbitMQ比Redis更能实现可靠传输，并且这里对于性能没有很变态的要求， 
所以选择RabbitMQ作为Broker。 


celery webhook http://docs.celeryproject.org/en/master/userguide/remote-tasks.html

消息队列

RabbitMQ,ZeroMQ这样的消息队列总是出现在我们视线中, 其实意义是很简单:
消息就是一个要传送的数据,celery是一个分布式的任务队列.这个”任务”其实就是一种消息,
任务被生成到队列中，被RabbitMQ等容器接收和存储，在适当的时候又被要执行的机器把这个消息取走.

celery任务可以使用RabbitMQ/Redis/SQLAlchemy/Django的orm/Mongodb等等容器(这里叫做Broker).我使用的是RabbitMQ,因为作者在github主页的介绍里面很明确的写了这个

所谓队列,你可以设想一个问题,我有一大推的东西要执行,但是我并不是需要每个服务器都执行这个任务,因为业务不同嘛.
所以就要做个队列, 比如任务A,B,C A可以在X,Y服务器执行,
但是不需要或者不能在Z服务器上执行.那么在X,Y你启动worker(下面会说，其实就是消费者和生产者的消费者)加上这个队列,Z服务器就不需要指定这个队列,也就不会执行这个队列的任务

## 并发模式的选择
gevent容易阻塞？ threading更可靠？？？

 celery是支持好几个并发模式的，有prefork，threading，协程（gevent，eventlet）

 prefork在celery的介绍是，用了multiprocess来实现的。多线程就补多少了，估计大家都懂。


 说说协程，进程
 线程经常玩，也算熟悉，话说协程算是一种轻量级进程，但又不能叫进程，因为操作系统并不知道它的存在。什么意思呢，就是说，协程像是一种在程序级别来模拟系统级别的进程，由于是单进程，并且少了上下文切换，于是相对来说系统消耗很少，而且网上的各种测试也表明，协程确实拥有惊人的速度。并且在实现过程中，协程可以用以前同步思路的写法，而运行起来确是异步的，也确实很有意思。话说有一种说法就是说进化历程是多进程->多线程->异步->协程，当然协程也有弊端，但是如果你的任务类型不是那种cpu密集的，那选用协程是个好选择。

 但是需要说明的是，虽然celery官网提示说，只要在启动worker的时候，指明下类型就行了，但是如果你逻辑里面的模块有些不支持协程
 gevent或者是eventlet异步的话，他还是会堵塞的。

 gevent1.x之后虽然是支持subprocess的用法，gevent这个模块给非堵塞了，和他有同样功能的os.popen(‘sleep 10′).read() 是会堵塞的，据说gevent官方不支持popen的协程的用法。


 看了下celery 针对gevent方面的调用，他其实就是引入了gevent的patch  。
 那这样会造成堵塞的问题，如果gevent不支持这些模块，那。。。。

 Python

 from gevent import monkey
 monkey.patch_all()
 1
 2
 3
 4
  
   
   from gevent import monkey
   monkey.patch_all()
    

    反之threading的用法倒是简单明了，支持把任务放在线程pool里面来处理。

    话说回来，我的title为什么说gevent来提高性能。我和小伙伴做一些gevent支持的模块写函数，做多任务处理的时候，性能确实要比threading要高，还要稳定。 

    小计：

    清理celery产生的数据


    Python

    #清空
    celery purge
    #清空
    from celery.task.control import discard_all
    discard_all()
    1
    2
    3
    4
    5
    6
    7
      
       
       #清空
       celery purge
       #清空
       from celery.task.control import discard_all
       discard_all()
        

        查看celery rabbitmq队列信息

        Python

        rabbitmqctl list_queues
        1
        2
        3
          
           
           rabbitmqctl list_queues
            



## 用supervisor管理worker

# 参考资料

1. Python定时任务框架APScheduler http://blog.csdn.net/chosen0ne/article/details/7842421
2. APScheduler + Gearman 构建分布式定时任务调度 http://blog.itpub.net/16582684/viewspace-776753/
3. 使用多线程和gevent来提高celery性能及稳定性 http://xiaorui.cc/2014/09/11/%e5%b0%8f%e8%ae%a1%e4%bd%bf%e7%94%a8%e5%a4%9a%e7%ba%bf%e7%a8%8b%e5%92%8cgevent%e6%9d%a5%e6%8f%90%e9%ab%98celery%e6%80%a7%e8%83%bd%e5%8f%8a%e7%a8%b3%e5%ae%9a%e6%80%a7/
4. 一个任务调度分发服务的架构  http://blog.sina.com.cn/s/blog_5921b17e0101ezfl.html
5. 在Flask中使用Celery http://www.cnblogs.com/ifkite/p/4257721.html
