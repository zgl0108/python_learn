`multiprocessing`模块为进程间通信提供了两种方法

**1.进程队列queue**

    The Queue class is a near clone of queue.Queue。
    Queues are thread and process safe。

使用进程队列，可以在两个进程间传递消息。其用法跟`queue.Queue`类似。

使用方法：

        from multiprocessing import Process,Queue
        def func(q):
            q.put([42,None,"hello"])    #把一个列表放入一个队列中
        
        if __name__=="__main__":
            q1=Queue()        #定义一个队列
            p1=Process(target=func,args=(q1,))		#实例化一个进程
            p1.start()	#启动进程 
            print(q1.get())		#从队列中取出一个项目，并打印 
            p1.join()	#阻塞进程

返回值：

    [42, None, 'hello']
在进程间通信可以使用python中所有的数据类型，但这种方式并不是真正意义上的进程间的通信。

**2.管道pipe**

	The Pipe() function returns a pair of connection objects connected by a pipe which by default is duplex (two-way).
	The two connection objects returned by Pipe() represent the two ends of the pipe. Each connection object has send() and recv() methods (among others).
	Note that data in a pipe may become corrupted if two processes (or threads) try to read from or write to the same end of the pipe at the same time. 
	Of course there is no risk of corruption from processes using different ends of the pipe at the same time.
`pipe()`返回两个连接对象代表`pipe`的两端。每个连接对象都有`send()`方法和`recv()`方法。

但是如果两个进程或线程对象同时读取或写入管道两端的数据时，管道中的数据有可能会损坏。

当进程使用的是管道两端的不同的数据则不会有数据损坏的风险。

使用方法：

        from multiprocessing import Process,Pipe
        
        def func(conn):
            conn.send([42,None,"hello"])	#连接发出信息
            conn.close()		#关闭连接 
        
        if __name__=="__main__":
            parent_conn,child_conn=Pipe()		#定义一个管道
            p1=Process(target=func,args=(child_conn,))	#实例化一个进程
            p1.start()		#启动进程 
            print(parent_conn.recv())		#连接接收信息并打印
            p1.join()	#阻塞进程 
返回结果：

	[42, None, 'hello']