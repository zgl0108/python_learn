`socketserver`是标准库中的一个高级模块，用于简张网络客户与服务器的实现．模块中，已经实现了一些可供使用的类.

在python3中，导入`socketserver`模块使用的命令：
    
    import socketserver
    
`socketserver`模块包括许多可以简化`TCP`,`UDP`,`UNIX`域套接字服务器实现的类．

**1.处理程序**

 使用`socketserver`模块 ,必须先定义一个继承自`BaseRequestHandle`的处理程序类.
 
`BaseRequestHandle`类的实例化可以实现以下方法:
 
* `sock.handle()`调用该方法执行实际的请求操作.调用函数可以不带任何参数,但是几个实例变量包含有用的值.`sock.request`包含请求,`sock.client_address`包含客户端的地址,`sock.server`包含调用处理程序的实例.对于TCP之类的数据流服务,`sock.request`属性是套接字对象.
 
 对于数据报服务,还是包含收到数据的字节字符串.
 
* `sock.setup()`该方法在`handle()`之前调用.默认情况下,不执行任何操作.如果希望服务器实现更多连接设置(如建立SSL连接),则无需调用该方法.

* `sock.finish()`调用本方法可以在执行完`handle()`之后执行清除操作.默认情况下,不执行任何操作.如果`setup()`和`handle()`方法都不生成异常,则无需调用该方法.

如果知道应用程序只能操纵面向数据流的连接(如TCP),那么应从`StreamRequestHandle`继承,而不是`BaseRequestHandler.StreaRequestHandler`类设置了两个属性,`sock.wfile`是将数据写入客户端的类文件对象,`sock.rfile`是从客户端读取数据的类文件对象.
	
如果编写针对数据包操作的处理程序并将响应持续返回给发送方,那么它应当从`DategramRequestHandler`继承.它提供的类接口与`StreamREquestHandler`相同.

**2.服务器**

要使用处理程序,必须将其插入到服务器对象.

定义了四个基本的服务类.

	* TCPServer(address,handler)          支持使用IPV4的TCP协议的服务器,address是一个(host,port)元组.Handler是BaseRequestHandler或StreamRequestHandler类的子类的实例.
	* UDPServer(address,handler)          支持使用IPV4的UDP协议的服务器,address和handler与TCPServer类似.
	* UnixStreamServer(address,handler)   使用UNIX域套接字实现面向数据流协议的服务器,继承自TCPServer.
	* UnixDatagramServer(address,handler) 使用UNIX域套接字实现数据报协议的服务器,继承自UDPServer.
	
所有四个服务类的实例都有以下方法和变量:

	* sock.socket               用于传入请求的套接字对象
	* sock.server_address       监听服务器的地址.比如元组("127.0.0.1",80)
	* sock.RequestHandlerClass  传递给服务器构造函数并由用户提供的请求处理程序类.
	* sock.serve_forever()      处理无限的请求.
	* sock.shutdown()           停止serve_forever()循环.
	* sock.fileno()             返回服务器套接字的整数文件描述符.该方法可以有效的通过轮询操作(如select()函数)使用服务器实例.

**3.定义自定义服务器**

服务器往往需要特殊的配置来处理不同的网络地址簇.超时期,并发和其他功能,可以通过继承上面四个基本服务器类来自行定义.

可以通过混合类获得更多服务器功能,这也是通过进程或线程分支添加并发的方法.为了实现并发性,定义了以下类:

	* ForkingMinIn          将UNIX进程分支添加到服务器的混合方法,使用该方法可以让服务器服务多个客户.
	* ThreadingMinIn        修改服务器的混合类,可以使用多线程服务多个客户端.
	
要向服务器添加这些功能,可以使用多重继承,其中首先列出了混合类.

由于并发服务器很常用,为了定义它,`SockServer`预定义了以下服务器类:

	* ForkingUDPServer(address,handler)
	* ForkingTCPServer(address,handler)
	* TthreadingUDPServer(address,handler)
	* ThreadingTCPServer(address,handler)
	
`SockerServer`模块中的类主要有以下几个:

    BaseServer                      包含服务器的核心功能与混合类(min-in)的钩子功能.这个类主用于派生,不要直接生成这个类的类对象,可以考虑使用TCPServer和UDPServer类.
    TCPServer                       基本的网络同步TCP服务器
    UDPServer                       基本的网络同步UDP服务器
    ForkingMinIn                    实现了核心的进程化功能,用于与服务器类进行混合(min-in),以提供一些异步特性.不要直接生成这个类的对象
    ThreadingMinIn                  实现了核心的线程化功能,用于与服务器类进行混合(min-in),以提供一些异步特性,不要直接生成这个类的对象
    ForkingTCPServer                ForkingMinIn与TCPServer的组合
    ForkingUDPServer                ForkingMinIn与UDPServer的组合
    BaseRequestHandler		
    StreamRequestHandler            TCP请求处理类的一个实现
    DataStreamRequestHandler        UDP请求处理类的一个实现
	 
使用`socketserver`模块编写的TCP服务器端代码:
```
    # !/usr/bin/env python
    # _*_coding:utf-8_*_
    
    import socketserver
    
    class MyServer(socketserver.BaseRequestHandler):
    
        def handle(self):
            print("from conn:",self.request)
    
    s1=socketserver.ThreadingTCPServer(("127.0.0.1",9999),MyServer)
    s1.serve_forever()
```