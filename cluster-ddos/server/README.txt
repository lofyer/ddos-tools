控制端
0. 修改hosts.list，添加被控制端用户名以及密码，形如
	root@192.168.1.2
	demo@192.168.1.3
	test@192.168.1.4
1. 运行gen-pubkey生成公钥，全部直接回车
	./gen-pubkey
2. 运行addhost添加被控制端
	./addhost
3. 修改config.txt参数，其中config.txt名称随意，比如test.txt
4. 运行attack开始攻击
	./attack config.txt
	或者
	./attack test.txt
