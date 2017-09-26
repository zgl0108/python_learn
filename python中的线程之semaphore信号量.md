 `semaphore`是一个内置的计数器

    每当调用acquire()时，内置计数器-1
    每当调用release()时，内置计数器+1

计数器不能小于0，当计数器为0时，`acquire()`将阻塞线程直到其他线程调用`release()`。
来看下面的代码：
        
        import time
        import threading
        
        def foo():
            time.sleep(2)	#程序休息2秒
            print("ok",time.ctime())
        
        for i in range(20):
            t1=threading.Thread(target=foo,args=())	#实例化一个线程
            t1.start()	#启动线程
执行结果：

	ok Tue Jul 18 20:05:58 2017
	ok Tue Jul 18 20:05:58 2017
	ok Tue Jul 18 20:05:58 2017
	ok Tue Jul 18 20:05:58 2017
	ok Tue Jul 18 20:05:58 2017
	ok Tue Jul 18 20:05:58 2017
	ok Tue Jul 18 20:05:58 2017
	ok Tue Jul 18 20:05:58 2017
	ok Tue Jul 18 20:05:58 2017
	ok Tue Jul 18 20:05:58 2017
	ok Tue Jul 18 20:05:58 2017
	ok Tue Jul 18 20:05:58 2017
	ok Tue Jul 18 20:05:58 2017
	ok Tue Jul 18 20:05:58 2017
	ok Tue Jul 18 20:05:58 2017
	ok Tue Jul 18 20:05:58 2017
	ok Tue Jul 18 20:05:58 2017
	ok Tue Jul 18 20:05:58 2017
	ok Tue Jul 18 20:05:58 2017
	ok Tue Jul 18 20:05:58 2017
	
可以看到，程序会在很短的时间内生成20个线程来打印一句话。

如果在主机执行IO密集型任务的时候再执行这种类型的程序时，计算机就有很大可能会宕机。

这时候就可以为这段程序添加一个计数器功能，来限制一个时间点内的线程数量。

代码如下：

        import time
        import threading
        
        s1=threading.Semaphore(5)	#添加一个计数器
        
        def foo():
            s1.acquire()	#计数器获得锁
            time.sleep(2)	#程序休眠2秒
            print("ok",time.ctime())
            s1.release()	#计数器释放锁
        
        
        for i in range(20):
            t1=threading.Thread(target=foo,args=())	#创建线程
            t1.start()	#启动线程	
执行结果：
    
    ok Tue Jul 18 20:04:38 2017
    ok Tue Jul 18 20:04:38 2017
    ok Tue Jul 18 20:04:38 2017
    ok Tue Jul 18 20:04:38 2017
    ok Tue Jul 18 20:04:38 2017
    ok Tue Jul 18 20:04:40 2017
    ok Tue Jul 18 20:04:40 2017
    ok Tue Jul 18 20:04:40 2017
    ok Tue Jul 18 20:04:40 2017
    ok Tue Jul 18 20:04:40 2017
    ok Tue Jul 18 20:04:42 2017
    ok Tue Jul 18 20:04:42 2017
    ok Tue Jul 18 20:04:42 2017
    ok Tue Jul 18 20:04:42 2017
    ok Tue Jul 18 20:04:42 2017
    ok Tue Jul 18 20:04:44 2017
    ok Tue Jul 18 20:04:44 2017
    ok Tue Jul 18 20:04:44 2017
    ok Tue Jul 18 20:04:44 2017
    ok Tue Jul 18 20:04:44 2017