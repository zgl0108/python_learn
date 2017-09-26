由于`GIL`的存在，python中的多线程并不是真正的多线程。

如果想要充分的使用多核CPU的资源，在python中大部分情况需要使用多进程。

在计算机中，进程与进程这之间在内存中是相互独立的，是两块完全不同的内存空间，而且相互之间没有任何联系。

在线程之中，在全局定义一个变量，所有的线程都是共用的，但是不同的进程之间的数据则不是公有的。

`multiprocessing`包是python中的多进程管理包。

与`threading.Thread`类似，`myltiprocessing`模块可以利用`multiprocessing.Process`对象来创建一个子进程。

`multiprocessing`的很大一部分用法与`threading`使用同一套`API`。

`Process`对象与`Thread`对象的用法相同，也有`start()`,`run()`和`join()`的方法。

此外`multiprocessing`包中也有`Lock`,`Event`,`Smaphore`,`Condition`类，这些对象可以像多线程那样，通过参数传递给各个进程，以实现同步进程。

**1.进程的创建**

大家在用chrome浏览器浏览网页的时候，打开任务管理器，会看到chrome的进程会不止一个，那么怎么在在一段py程序里面开辟一个子进程呢？？
 
python中子进程的创建有两种方法：

***1.通过Process类调用***

        import multiprocessing
        import time
        
        def func():
            print("hello world------>",time.ctime())
            time.sleep(2)	#让系统休眠2S
            print("func ending------>",time.ctime())
        
        
        if __name__ == "__main__":
            p1=multiprocessing.Process(target=func,args=())	#实例化一个进程
            p1.start()	#启动进程
            print("ending------>",time.ctime())		#计算程序执行所花费的时间 
这样就创建一个进程，如果电脑的CPU是多核的话，这两个程序就会并行执行。

执行程序，程序最后一句`"ending"`和`"hello world"`会同进打印在屏幕上，然后程序休眠2s,又会在屏幕上打印一句`"func ending"`,程序执行结束。

在程序执行期间，打开任务管理器，会看到进程列表中有两个python.exe的进程，等到程序执行完成，这两个python.exe的进程又会消失。
程序执行结果：

	ending------> Thu Jul 20 15:56:17 2017
	hello world------> Thu Jul 20 15:56:17 2017
	func ending------> Thu Jul 20 15:56:19 2017

***2.继承Process类调用***
 
        from multiprocessing import Process
        import time
        
        class MyProcess(Process):	#定义一个类，这个类继承multiprocessing.Process这个类
            def __init__(self,i):
                super(MyProcess,self).__init__()
                self.i=i
        
            def run(self):
                print("%s hello python------>"%self.i,time.ctime())
                time.sleep(2)
        
        if __name__=="__main__":
            p_list=[]
            for i in range(3):
                p1=MyProcess(i)	#实例化进程
                p1.start()		#启动进程
                p_list.append(p1)
        
            for item in p_list:
                item.join()		#阻塞主进程，全子进程执行完毕再执行主进程
        
            print("ending------>",time.ctime())		#计算程序执行所花费的时间
            
利用类的继承，创建了3个进程，这三个进程同时在屏幕在打印自身的编号及一句话,然后程序休眠2s后，又会打印结束话语。

在程序的执行过程中，查看系统进程列表，会看到python解释器的进程编号：

	E:\py_code>tasklist | findstr python
	python.exe                    5760 Console                    1     11,524 K
	python.exe                    3488 Console                    1     11,616 K
	python.exe                    6900 Console                    1     11,672 K
	python.exe                    4384 Console                    1     11,636 K
	
程序执行结果：

	1 hello python------> Thu Jul 20 16:05:07 2017
	2 hello python------> Thu Jul 20 16:05:07 2017
	0 hello python------> Thu Jul 20 16:05:07 2017
	ending------> Thu Jul 20 16:05:09 2017
	
**2.进程的使用方法**

来看下面的例子：

让系统执行一段范围内的累加和累乘操作，计算CPU执行这两个操作所花的时间。

****第一种方式：正常的定义两个函数，然后执行程序。****

        def func1(x):
            res1=0
            for i in range(x):
                res1 += i   #累加计算的结果
            return res1
        
        def func2(y):
            res2=1
            for i in range(1,y):
                res2 *= i    #累乘计算的结果
            return res2
        
        
        s1=time.time()
        func1(100000000)	#执行累加函数
        func2(100000)		#执行累乘函数
        s2=time.time()
        print("cost time:%s"%(s2-s1))	#计算程序执行所花费的时间 
程序返回结果：
	
	cost time:9.273045301437378
****第二种方式，使用程序执行另外两个进程，分别调用系统资源来运算，计算CPU所花费的时间。****

	from multiprocessing import Process
	import time

	def func1(x):
	    res1=0
	    for i in range(x):
	        res1 += i
	    return res1

	def func2(y):
	    res2=1
	    for i in range(1,y):
	        res2 *= i
	    return res2

	if __name__=="__main__":
	    t1=time.time()
	    p1=Process(target=func1,args=(100000000,))  #实例化进程p1
	    p1.start()	#启动进程p1

	    p2=Process(target=func2,args=(100000,))     #实例化进程p2
	    p2.start()	#启动进程pp2

	    p1.join()
	    p2.join()

	    print("ending")
	    t2=time.time()
	    print("cost time:%s"%(t2-t1))		#计算程序运行所花费的时间

执行程序，查看系统的任务管理器，可以看到程序在运行的过程中，生成了三个进程。

	E:\py_code>tasklist | findstr python
	python.exe                    6520 Console                    1     11,536 K
	python.exe                    4340 Console                    1     11,612 K
	python.exe                    6200 Console                    1     12,240 K
程序执行结果：

	ending
	cost time:5.437908697128296

可以看到，第二段代码里面有三个进程(一个主进程和两个子进程p1,p2)，

同时在执行这两个函数，所以CPU在执行这两个运行的时候所花的时间会少一些的原因。

**3.python中，多进程的优缺点**

    优点：
        可以利用多核，以实现并形运算
    	
    缺点：
    
        1.浪费的系统资源比较多
        2.进程之间的通信比较困难
**4.`multiprocessing`中的`Process`类中内置方法及用法**

在系统的提示符下，导入`multiprocessing`模块，使用：

    import multiprocessing
    
查看这个模块的内置的方法：

	help(multiprocessing.Process)
```
    multiprocessing.Process内置方法：
    
    
    构造方法：
        group               线程组
        target              要执行的方法
        name                进程的名
        args/kwargs         执行过程中要传入的参数 
    
    实例方法：
        is_alive()          测试进程是否在运行
        join([timeout])     阻塞当前上下文环境的进程，直到调用此方法的进程终止或到达指定的timeout
        start()             进程准备就绪，等待CPU调度
        run()               start()调用run方法，如果实例进程未制定传入target时，这start执行默认的run()方法	
        terminate()         不管任务是否完成，立即停止工作进程 
    
    属性：
        deamon              和线程的setDeamon功能一样
        name                进程的名字
        pid(ident)          进程号
        ppid                进程的父进程号
```
`Process`内置方法的用法：

代码如下：

	from multiprocessing import Process
	import os
	import time
	def info(name):
	    print("process name:",name)		#打印当前进程的进程名
	    print("parent process:",os.getppid())		#打印当前进程的父进程ID号
	    print("process:",os.getpid())	#打印当前进程的进程ID号
	    print("---------")
	    time.sleep(10)

	def foo(name):
	    info(name)

	if __name__=="__main__":
	    info("main process")

	    p1=Process(target=info,args=("process1",))
	    p1.start()
	    p1.join()

	    p2=Process(target=foo,args=("process2",))
	    p2.start()
	    p2.join()

	    print("ending")

程序执行过程中，打开系统的任务管理器，查找python的进程可以看到：

	E:\py_code>tasklist | findstr python
	python.exe                    2424 Console                    1     11,536 K
	python.exe                    5360 Console                    1     11,632 K
	python.exe                    2532 Console                    1     11,664 K


执行程序，返回结果如下：

	process name: main process line
	parent process: 628
	process: 2424
	---------
	
	process name: process1
	parent process: 2424
	process: 2532
	---------
	process name: process2
	parent process: 2424
	process: 5360
	---------
	ending

可以看到process1和process2的进程名和进程号，这两个进程的父进程号都是一样的，都是主进程的进程号。

**5.注意事项**

需要注意的是，python的进程之间的切换，耗费的系统资源比线程的切换耗费的资源多得多，