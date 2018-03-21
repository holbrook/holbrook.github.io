Salt的命令行工具


minion:
	salt-call
	salt-minion

master:
	salt
	salt-cp
	salt-key
	salt-master
	salt-run
	salt-syndic



运行和调试Salt States
写好的SLS如何才能应用到minion呢？在SaltStack中，远程执行是一切的基础。执行命令salt '*' state.highstate会让所有的minion到master上来取走自己的SLS定义，然后在本地调用对应的state module（user，pkg，service等）来达到SLS描述的状态。如果这条命令只返回minion的主机名加一个':'，多半是哪一个SLS文件有错。如果minion是以服务进程启动，执行命令salt-call state.highstate -l debug可以看到错误信息，便于调试。minion还可以直接在前台以debug模式运行：salt-minion -l debug。
