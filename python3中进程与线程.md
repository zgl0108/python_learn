**1.进程的概念**

平时在使用电脑的过程中，可能会登陆QQ，一边开着网易云音乐，一边开着chrome浏览器或者火狐浏览器在网页上看视频，甚至还会打开word软件，编辑文档。

假设现在电脑上同时打开这四个程序，QQ，网易云音乐，chrome浏览器，word软件，此时对电脑主机来说，CPU(中央处理器)会在这打开的四个程序中依次循环切换。

现在一颗主流的CPU的主频为2.5Ghz，其意思就是说在1秒钟内，这颗CPU可以在程序中切换2.5乘以10的9次方次，所以使用电脑的人眼中，电脑可以同时执行这四个程序一样。

在CPU运行的过程中，每一个时间点内，一颗cpu只能运行一个程序。

当QQ在执行的过程中，其余的三个程序都会被暂停。

同样的，当chrome浏览器在运行的过程中，其余的三个程序也会被暂停。

当程序切换的时候，需要一个媒介来保存程序的运行，暂停，恢复等信息，这就是进程的概念。

```
进程是计算机中的程序关于某数据集合上的一次运行活动，是系统进行资源分配和调度的基本单位，是操作系统的结构基础。
进程是系统进行资源分配和调度的一个独立单位。

进程一般由程序。数据集，进程控制块三部分组成：
程序用来描述进程要完成哪些功能以及如何完成 
数据集是程序在执行过程中所需要使用的资源
进程控制块用来记录进程的外部特征，描述进程的执行变化过程，操作系统可以利用它来控制和管理进程，控制块是系统感知进程存在的唯一标志
```
**2.线程的概念**

假设在用浏览器打开一个网页，这时浏览器一边把网页下载到硬盘上，浏览器一边对网页进行渲染，生成用户看到网页。

在这同时，浏览器还要与网页服务器保持连接。在这个过程中，浏览器会生成多个进程，同时会在这多个进程之间来回切换。

这多个进程的协作涉及到进程间通信问题，进程间不停的切换造成主机性能上的损失。这时就需要一种机制来保存和恢复进程间的通信内容，减少通信所带来的性能损耗，这种机制就是线程

线程的出现是为了降低上下文切换的消耗，提高系统的并发性，并突破一个进程在一个时间点只能服务一个程序的缺陷，拿到进程内并发成为可能。

线程也叫轻量级进程 ，是一个基本的CPU执行单元，也是程序执行过程中的最小单元，由线程ID，程序讲数器，寄存器集合和堆栈共同组成。

线程是进程的一个实体，是cpu调度和分派的基本单位，是比进程更小的能独立运行的基本单位。

线程的引入减小了程序 并发执行时的开销，提高了操作系统的并发性能。线程没有自己的系统资源。

**3.进程与线程的关系**
```
1.一个线程只能属于一个进程 ，而一个进程可以有多个线程，但至少有一个线程
2.资源分配给进程，同一个进程的所有线程共享该进程 的所有资源
3.CPU分给线程，即真正在CPU上运行的是线程
4.线程在进程之间是共享内存空间的，是通过进程创建的，进程拥有它自己的独立空间
5.线程直接访问进程的数据块，进程是将父进程中的数据再复制出一份使用
6.进程中的线程间是可以直接通信的，子进程与父进程不能直接通信，但可以通过队列管道相互交流数据
7.一个新的线程创建很容易，一个新的进程创建需要从父进程里重新拷贝父进程的所有数据，耗费资源
8.一进程中的多线程间可以控制其它进程，进程只能控制它的子进程 
9.改变主线程优先级会影响线程的在进程中的行为，改变父进程不会影响子进程 
```
**4.线程的创建**

***1.通过`thread`类直接创建***

        import threading
        import time
        
        def foo(n):
            time.sleep(n)
            print("foo func:",n)
        
        def bar(n):
            time.sleep(n)
            print("bar func:",n)
        
        s1=time.time()
        
        #创建一个线程实例t1,foo为这个线程要运行的函数
        t1=threading.Thread(target=foo,args=(3,))
        t1.start()    #启动线程t1
        
        #创建一个线程实例t2,bar为这个线程要运行的函数
        t2=threading.Thread(target=bar,args=(5,))
        t2.start()    #启动线程t2
        
        print("ending")
        
        s2=time.time()
        
        print("cost time:",s2-s1)

在这段程序里，一个函数会先休眠几秒钟，然后再打印一句话，第二个函数也是先休眠几秒钟，然后打印一句话。

接着程序会实例化两个线程，并调用两个函数来执行，最后会打印程序问总共执行了多少时间 

程序运行结果如下：

    ending
    cost time: 0.002000093460083008
    foo func: 3
    bar func: 5
    
程序会先运行父线程，打印`"ending"`,然后打印程序执行父线程的时间，最后才会运行子线程

***2.通过`thread`类来继承式创建***

        import threading
        import time
        
        class MyThread(threading.Thread): #定义MyThread类，其继承自threading.Thread这个父类
        
            def __init__(self):
                threading.Thread.__init__(self)
        
            def run(self):
                print("ok")
                time.sleep(2)
                print("end t1")
        
        t1=MyThread()	#对类进行实例化
        t1.start()	#启动线程
        print("ending")

***3.Thread类的一些常用方法***

****1. `join()`:在子线程完成之前，父线程将一直被阻塞****

在第一个例子中加入以下两行代码，如下：

        import threading
        import time
        
        
        def foo(n):
            time.sleep(n)
            print("foo func:",n)
        
        def bar(n):
            time.sleep(n)
            print("bar func:",n)
        
        s1=time.time()
        t1=threading.Thread(target=foo,args=(3,))
        t1.start()
        
        t2=threading.Thread(target=bar,args=(5,))
        t2.start()
        
        t1.join()
        t2.join()
        
        print("ending")
        s2=time.time()
        
        print("cost time:",s2-s1)
        
再次执行程序，运行结果如下：

    foo func: 3
    bar func: 5
    ending
    cost time: 5.002285957336426
    
程序运行到t1.join时会被阻塞，等到子线程执行完成之后再执行父线程

****2.setDeamon(True)****

将进程声明为守护线程，必须在`start()`方法调用之前，如果不设置为守护线程，程序会被无限挂起

在程序执行过程中，执行一个主线程，主线程又创建一个子线程时，主线程和子线程会分别运行。

当主线程运行完成时，会检验子线程是否执行完成，如果子线程执行完成，则主线程会等待子线程完成后再退出。

但是的时候只是主线程执行完成之后，不管子线程是否执行完成，都和主线程一起退出，这个就需要调用`setDeamon`这个方法了。

拿第一个例子来说吧，现在我想让子线程t1和t2随同主线程关闭，代码如下：

        import threading
        import time
        
        
        def foo(n):
            time.sleep(n)
            print("foo func:",n)
            
        def bar(n):
            time.sleep(n)
            print("bar func:",n)
        
        s1=time.time()
        t1=threading.Thread(target=foo,args=(3,))
        t1.setDaemon(True)
        t1.start()
        
        t2=threading.Thread(target=bar,args=(5,))
        t2.setDaemon(True)
        t2.start()
        
        print("ending")
        s2=time.time()
        
        print("cost time:",s2-s1)

程序运行结果如下 ：

    ending
    cost time: 0.002000093460083008

****3.其他方法****
```
isAlive()           #判断一个线程是否是活动线程
getName()           #返回线程的名字
setName()           #设置线程的名字
```
        import threading
        import time
        
        
        def foo(n):
            time.sleep(n)
            print("foo func:", n)
        
        
        def bar(n):
            time.sleep(n)
            print("bar func:", n)
        
        
        s1 = time.time()
        t1 = threading.Thread(target=foo, args=(3,))
        t1.setDaemon(True)
        
        print("线程还未启动时，判断t1是否是活动的线程：", t1.isAlive())  # 线程还未启动，所以是False
        t1.start()  # 启动线程
        print("线程已启动时，判断t1是否是活动的线程：", t1.isAlive())  # 线程已启动，所以是True
        print("修改前的线程名为：",t1.getName())  # 获取线程名
        t1.setName("t1")        #设置线程名
        print("修改后的线程名为：",t1.getName())  # 获取线程名
        
        t1.join()
        
        print("线程执行完成时，判断t1是不否是活动的线程：", t1.isAlive())  # 线程已执行完成，所以是False
        
        # print(threading.activeCount())
        print("ending")
        s2 = time.time()
        
        print("cost time:", s2 - s1)

程序执行结果：

    线程还未启动时，判断t1是否是活动的线程： False
    线程已启动时，判断t1是否是活动的线程： True
    修改前的线程名为： Thread-1
    修改后的线程名为： t1
    foo func: 3
    线程执行完成时，判断t1是不否是活动的线程： False
    ending
    cost time: 3.001171588897705



****4.threading模块提供的一些方法****
```
threading.currentThread()   #返回当前的线程变量	
threading.enumerate()       #返回一个包含正在运行的线程的列表，不包括启动前和终止后的线程
threading.activeCount()     #返回正在运行的线程数量，等同于len(threading.enumerate())
```
        import threading
        import time
        
        def foo(n):
            time.sleep(n)
            print("foo func:", n)
        
        def bar(n):
            time.sleep(n)
            print("bar func:", n)
        
        s1 = time.time()
        t1 = threading.Thread(target=foo, args=(3,))
        t1.setDaemon(True)
        t1.start()
        
        t2 = threading.Thread(target=bar, args=(5,))
        t2.setDaemon(True)
        t2.start()
        
        print("程序中正在运行的线程数量：",threading.activeCount())
        print("程序中当前的线程变量：",threading.currentThread())
        print("当前正在运行的线程的列表：",threading.enumerate())
        print("ending")
        s2 = time.time()
        
        print("cost time:", s2 - s1)

程序执行结果：

    程序中正在运行的线程数量： 3
    程序中当前的线程变量： <_MainThread(MainThread, started 7064)>
    当前正在运行的线程的列表： [<_MainThread(MainThread, started 7064)>, <Thread(Thread-1, started daemon 6384)>, <Thread(Thread-2, started daemon 2640)>]
    ending
    cost time: 0.002000093460083008