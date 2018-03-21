Salt的不足之处和解决思路


# 资源关系管理
尽管同一个minion的多个state之间有逻辑关系，但是跨minion的关系没有有效管理

# dashboard
Puppet使用Puppet dashboard. Salt目前没有图形化的界面。我知道，我们都大爱命令行。不过，有时看到满屏幕的绿色或是点点按钮也是很惬意的。 认真的讲，dashboard是获得你所管理的节点网络state概览的好工具。Salt的路线图中没有图形界面，希望最终会出现。

1. 管理终端作为master , 管理节点作为管理终端的
2. dashboard(web)
3. 其他，比如用vim 做外壳？