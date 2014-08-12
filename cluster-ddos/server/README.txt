控制端
1. 修改config.txt参数，其中config.txt名称随意，比如test.txt，要输入控制端机器的用户名密码
2. 运行gen-install会生成install-client文件，将其拷贝到被控制端运行
	./install-client 客户端IP
3. 运行attack开始攻击
	./attack config.txt
	或者
	./attack test.txt
