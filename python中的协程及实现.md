**1.协程的概念**

协程是一种用户态的轻量级线程。协程拥有自己的寄存器上下文和栈。

协程调度切换时，将寄存器上下文和栈保存到其他地方，在切换回来的时候，恢复先前保存的寄存器上下文和栈。

因此，协程能保留上一次调用时的状态(即所有局部状态的一个特定组合)，每当程序切换回来时，就进入上一次离开时程序所处的代码段。

**2.`yield`实现的协程**

传统的生产者－消费者模型是一个线程生成消息，一个线程取得消息，能过锁机制控制队列和等待，但一不小心就有可能死锁。

如果改用协程，生产者生产消息后，直接通过`yield`跳转到消费者开始执行，待消费者执行完毕后，切换加生产者继续生产，效率较高。

代码如下：

        import time
        
        def consumer():
            """
            使用yield生成一个generator生成器
            :return:
            """
            r = " "
            while True:
                # yield接收到变量r,处理之后再把结果返回。函数执行到这一步的时候，函数会停留在这一行上，
                #当别的函数执行next()语句或者generator.send()语句来激活这一句，本函数就会
                #从yield代码的下一行开始继续执行，直到下一次程序循环到yield这里。
                n = yield r
                print("[consumer]<-- %s" % n)
                time.sleep(1)
                r = "ok"
        
        def producer(c):
            next(c)     #启动调用consumer()函数中的生成器
            n = 0
            while n < 10:
                n += 1
                print("[producer]-->%s" % n)
                #生产者生产产品，通过c.send()把程序切换到consumer函数执行
                cr = c.send(n)
                print("[producer] consumer return:%s" % cr)
            c.close()
        
        if __name__ == "__main__":
            c1 = consumer()
            producer(c1)

执行结果：

	[producer]--> 1
	[consumer]<-- 1
	[producer] consumer return:ok
	[producer]--> 2
	[consumer]<-- 2
	[producer] consumer return:ok
	[producer]--> 3
	[consumer]<-- 3
	[producer] consumer return:ok
	...     #中间省略
	[producer]--> 9
	[consumer]<-- 9
	[producer] consumer return:ok
	[producer]--> 10
	[consumer]<-- 10
	[producer] consumer return:ok
	
整个流程是由一个线程执行，`producer`和`consumer`协作完成任务，所以称为协程，而不是线程中的抢占式多任务。


**3.由`greenlet`模块实现的协程**

`greenlet`机制的主要思想是：生成器函数或者协程函数中的`yield`语句挂起函数的执行，直到稍后使用`next()`或`send()`操作进行恢复主止。

可以使用一个调度器循环在一组生成器函数之间协作多个任务。

`greenlet`是python中实现协程的一个模块。

使用方式 ：

        from greenlet import greenlet
        import time
        
        def func1():    
            print("func1,ok1---->",time.ctime())
            gr2.switch()    #程序会切换到func2执行
            time.sleep(5)   #休眠5s
            print("func1,ok2---->",time.ctime())
            gr2.switch()    #程序又会切换到func2执行
        
        def func2():
            print("func2,ok1---->",time.ctime())
            gr1.switch()    #func2执行到这里会切换回func1执行
            time.sleep(3)   #休眠3s
            print("func2,ok2---->",time.ctime())
        
        gr1=greenlet(func1)
        gr2=greenlet(func2)
        
        gr1.switch()
	
程序执行流程：

    1.程序先运行func1，打印第一句话。
    2.func1运行到gr2.switch()这里时，会切换到func2执行，func2函数打印第一句话。
    3.func2执行到gr1.switch()这里时，又切换回func1函数的time.sleep(5)执行，func1函数会休眠5s。
    4.func1先打印第二句话，执行到gr2.switch()这一句时，再次切换回func2函数。
    5.func2函数休眠3s,打印func2函数的第二句话，程序执行完毕。
    
程序执行结果：

    func1,ok1----> Fri Jul 21 16:27:11 2017
    func2,ok1----> Fri Jul 21 16:27:11 2017
    func1,ok2----> Fri Jul 21 16:27:16 2017
    func2,ok2----> Fri Jul 21 16:27:19 2017
    
**4.基于`greenlet`框架，`gevent`模块实现协程**

python通过`yield`提供了对协程的基本支持，但是不完全。第三方的`gevent`模块提供了协程支持。

`gevent`是第三方库，通过`greenlet`实现协程。

当一个`greenlet`遇到IO操作时，比如访问网络，就自动切换到其他的`greenlet`，等到IO操作完成，再在适当的时候切换回来继续执行。

由于IO操作非常耗时，经常使程序处于等待状态，有了`gevent`自动切换协程，就保证总有`greenlet`在运行，而不是等待IO。

代码如下：

        import gevent,time
        
        def func1():
            print("running in func1--",time.ctime())
            time.sleep(2)
            print("running in func1 again--",time.ctime())
        
        def func2():
            print("running in func2--",time.ctime())
            time.sleep(2)
            print("running in func2 again--",time.ctime())
        
        t1=time.time()
        g1=gevent.spawn(func1)
        g2=gevent.spawn(func2)
        gevent.joinall([g1,g2])
        t2=time.time()
        print("cost time:",t2-t1)
	
程序执行结果：

    running in func1-- Fri Jul 21 17:20:17 2017
    running in func1 again-- Fri Jul 21 17:20:19 2017
    running in func2-- Fri Jul 21 17:20:19 2017
    running in func2 again-- Fri Jul 21 17:20:21 2017
    cost time: 4.007229328155518

可以看到程序是按顺序执行的。修改程序，使用`gevent.sleep()`使程序按协程方式执行。

修改后的代码如下：

        import gevent,time
        
        def func1():
            print("running in func1--",time.ctime())
            gevent.sleep(2)
            print("running in func1 again--",time.ctime())
        
        def func2():
            print("running in func2--",time.ctime())
            gevent.sleep(2)
            print("running in func2 again--",time.ctime())
        
        t1=time.time()
        g1=gevent.spawn(func1)
        g2=gevent.spawn(func2)
        gevent.joinall([g1,g2])
        t2=time.time()
        
        print("cost time:",t2-t1)
    
程序执行结果：

    running in func1-- Fri Jul 21 17:17:00 2017
    running in func2-- Fri Jul 21 17:17:00 2017
    running in func1 again-- Fri Jul 21 17:17:02 2017
    running in func2 again-- Fri Jul 21 17:17:02 2017
    cost time: 2.0051145553588867
    
这样，程序会先执行func1接着执行的是func2，再切换回func1执行。

这种方式可以使原本需要4s才能执行完成的程序只需要执行2s就可以了。

	gevent.spawn()方法spawn一些任务，然后通过gevent.joinall将任务加入协程执行队列中等待执行。

**5.协程的优点**

	无需线程上下文切换造成的资源的浪费。
	无需原子操作锁定及同步的开销。
	方便切换控制流，简化编程模型。
	高并发及高扩展性加低成本：一个CPU支持上万的协程都可以，于高并发处理。


**6.协程的缺点**

	无法利用多核资源，协程的本质是单个线程，不能同时使用多核CPU。
	协程需要与进程配合才能运行在多CPU上。
	程序一旦阻塞，会阻塞整个代码段。