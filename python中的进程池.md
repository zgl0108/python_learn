**1.进程池的概念**

python中，进程池内部会维护一个进程序列。当需要时，程序会去进程池中获取一个进程。

如果进程池序列中没有可供使用的进程，那么程序就会等待，直到进程池中有可用进程为止。

**2.进程池的内置方法**

+ apply         从进程池里取一个进程并同步执行
+ apply_async	从进程池里取出一个进程并异步执行
+ terminate		立刻关闭进程池
+ join			主进程等待所有子进程执行完毕，必须在close或terminete之后
+ close			等待所有进程结束才关闭线程池

> 同步是指一个进程在执行某个请求的时候，必须要到收到对方返回的信息才继续执行下去

> 异步是指进程在执行某个请求时，不管其他的进程的状态，这个进程就执行后续操作；
当有消息返回时系统会通知进程进行处理，这样可以提高执行的效率

> 例如：打电话就是同步通信，发信息就是异步通信。

**3.进程池的使用**

代码如下：

        from multiprocessing import Pool
        import time
        
        def func(args):
            time.sleep(1)                               #程序休眠1s
            print("%s------>%s"%(args,time.ctime()))    #打印参数及时间
        
        if __name__=="__main__":
            p1=Pool(2)                                  #设定开启2个进程池
            for i in range(10):
                p1.apply_async(func=func,args=(i,))     #设定异步执行任务
        
            p1.close()                                  #关闭进程池
            time.sleep(2)                               #程序休眠2s
            p1.terminate()                              #关闭进程池
            p1.join()                                   #阻塞进程池
            print("ending")                             #打印结束语句
            
程序执行结果：

	0------>Thu Jul 20 20:18:43 2017
	1------>Thu Jul 20 20:18:43 2017
	ending

可以看到，在程序执行过程中，关闭进程池，则程序会立即停止，不会再继续执行后续语句。

**4.修改程序，使程序能够执行全部的任务**

代码如下：

        from multiprocessing import Pool
        import time
        
        def func(args):
            time.sleep(1)	#休眠1s
            print("%s------>%s"%(args,time.ctime()))	#打印传递的参数及时间 
        
        if __name__=="__main__":
            p1=Pool(2)	#定义2个进程池
            for i in range(10):	#定义循环10次
                p1.apply_async(func=func,args=(i,))	#异步执行任务
        
            p1.close()		#等待所有的任务都完成才关闭进程池
            p1.join()
            print("ending")
执行结果如下：
	
	0------>Thu Jul 20 20:19:12 2017
	1------>Thu Jul 20 20:19:12 2017
	2------>Thu Jul 20 20:19:13 2017
	3------>Thu Jul 20 20:19:13 2017
	4------>Thu Jul 20 20:19:14 2017
	5------>Thu Jul 20 20:19:14 2017
	6------>Thu Jul 20 20:19:15 2017
	7------>Thu Jul 20 20:19:15 2017
	8------>Thu Jul 20 20:19:16 2017
	9------>Thu Jul 20 20:19:16 2017
	ending


