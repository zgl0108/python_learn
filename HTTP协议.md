**1. HTTP概述**

`HTTP`(`HyperText Transport Protocol`),超文本传输协议。

其规定了浏览器和万维网服务器之间互相通信的规则。  

`HTTP`是一个基于`TCP/IP`协议的通信规则，规定了客户端与服务器内之间互相通信的内容格式。

    * 客户端发送给服务器的格式叫“请求协议(request)”
    * 服务器发送给客户端的格式叫“响应协议(response)”
    
HTTP协议的特点：

	1.简单快速：由于HTTP协议简单，因此客户向服务器请求服务时，只需传送请求方法和路径，使得发送和接收的头部信息长度比较短，因而通信速度很快。
	2.灵活：HTTP允许传输任意类型的数据对象。正在传输的类型由Content-Type加以标记。
	3.无连接：无连接的含义是限制每次连接只处理一个请求。服务器处理完客户的请求，并收到客户的应答后，即断开连接。
	4.无状态：HTTP协议是无状态协议。HTTP协议对于事务处理没有记忆能力,这样下次通信又必须重新发送请求，这样可能导致每次连接传送的数据量增大。
	5.支持B/S及C/S模式。
	
**2. HTTP之URL**

`URL`的全称是：统一资源标识符URL,是互联网上用来标识某一处资源的地址。

以`http://www.360doc.com/content/10/0930/17/3668821_57590979.shtml`这个URL为例，介绍下普通URL的各部分组成：

从上面的URL可以看出，一个完整的URL包括以下几部分：

	1.协议部分：该URL的协议部分为“http：”，这代表网页使用的是HTTP协议。在"HTTP"后面的“//”为分隔符
	2.域名部分：该URL的域名部分为“www.360doc.com”。一个URL中，也可以使用IP地址作为域名使用
	3.端口部分：跟在域名后面的是端口，域名和端口之间使用“:”作为分隔符。端口不是一个URL必须的部分，如果省略端口部分，将采用默认端口80
	4.虚拟目录部分：从域名后的第一个“/”开始到最后一个“/”为止，是虚拟目录部分。虚拟目录也不是一个URL必须的部分。
	5.文件名部分：从域名后的最后一个“/”开始到结束，都是文件名部分。一个URL中文件名部分可以省略，使用默认的文件名
	6.锚部分：从“#”开始到最后，都是锚部分。锚部分也不是一个URL必须的部分
	7.参数部分：从“？”开始到“#”为止之间的部分为参数部分，又称搜索部分、查询部分。参数可以允许有多个参数，参数与参数之间用“&”作为分隔符。
	
**3.请求协议** 

请求协议的格式如下：  

	请求首行:包括请求方式,请求路径,协议和版本，例如：GET /index.html HTTP/1.1 
	请求头信息:包括请求头内容，即为key:value格式，例如：Host:localhost 
	空行:来与请求体分隔开 
	请求体:GET没有请求体，只有POST有请求体。 
	
不管是任何浏览器，与服务端通信时，发送给服务器的内容就这个格式的,如果不是这个格式服务器将无法解读！

在`HTTP`协议中,请求有很多请求方法,其中最为常用的就`GET`和`POST`。

***3.1　GET请求*** 

`HTTP默认的请求方法就是GET`

`GET`请求的特点是:

    没有请求体
    数据必须在1K之内
    GET请求数据会暴露在浏览器的地址栏中
    
`GET`请求常用的操作：

	 1. 在浏览器的地址栏中直接给出URL，那么就一定是GET请求
	 2. 点击页面上的超链接也一定是GET请求
	 3. 提交表单时，表单默认使用GET请求，但可以设置为POST 
	 
例子:

	GET 127.0.0.1:8090/login    #HTTP/1.1：GET请求，请求服务器路径为127.0.0.1:8090/login ，协议为1.1； 
	Host:localhost		        #请求的主机名为localhost； 
	User-Agent: Mozilla/5.0 (Windows NT 5.1; rv:5.0) Gecko/20100101 Firefox/5.0	#与浏览器和OS相关的信息。
	Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8		#告诉服务器，当前客户端可以接收的文档类型，这里包含了*/*，就表示什么都可以接收； 
	Accept-Language: zh-cn,zh;q=0.5		#当前客户端支持的语言，可以在浏览器的工具选项中找到语言相关信息； 
	Accept-Encoding: gzip, deflate	#支持的压缩格式。数据在网络上传递时，可能服务器会把数据压缩后再发送； 
	Accept-Charset: GB2312,utf-8;q=0.7,*;q=0.7	#客户端支持的编码； 
	Connection: keep-alive	#客户端支持的链接方式，保持一段时间链接，默认为3000ms； 
	Cookie: JSESSIONID=369766FDF6220F7803433C0B2DE36D98	#因为不是第一次访问这个地址，所以会在请求中把上一次服务器响应中发送过来的Cookie在请求中一并发送过去；
	
***3.2　POST请求***

用`GET`方法将数据附加到`URL`中传送给服务器，但在很多情况下使用`GET`方法不安全，例如用户输入的用户名和密码等敏感信息．这时就可以使用`POST`请求来发送数据．

客户端发送一个`POST`请求到服务器的请求消息包括以下格式：

    请求行      request line
    请求头部    request header
    空行
    请求体

 我们都知道`Http`协议中参数的传输是`"key=value"`这种简直对形式的，如果要传多个参数就需要用""符号对键值对进行分割。
 
 如"`?name1=value1&name2=value2`"，这样在服务端在收到这种字符串的时候，会用“”分割出每一个参数，然后再用“`=`”来分割出参数值。     
 
 `URL`编码只是简单的在特殊字符的各个字节前加上`%`
 
 使用表单可以发`POST`请求，但表单默认是`GET`  

	 <form action="" method="post">   
	 关键字：<input type="text" name="keyword"/>   
	 <input type="submit" value="提交"/> </form> 
	 
 输入`"hello"`后点击提交，查看请求内容如下：  

    Request Headers 
    Accept:text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8 
    Accept-Encoding:gzip, deflate 
    Accept-Language:zh-CN,zh;q=0.8 
    Cache-Control:no-cache 
    Connection:keep-alive 
    Content-Length:13 
    Content-Type:application/x-www-form-urlencoded 
    Cookie:csrftoken=z5H43ZwARx7AIJ82OEizBOWbsAQA2LPk 
    Host:127.0.0.1:8080 
    Origin:http://127.0.0.1:8080 
    Pragma:no-cache 
    Referer:http://127.0.0.1:8080/index.html
    Upgrade-Insecure-Requests:1 User-Agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1)            
    AppleWebKit/537.36 (KHTML, like Gecko)Chrome/53.0.2785.89 Safari/537.36  
    Form Data username:hello 
    
`POST`请求是可以有体的，而`GET`请求不能有请求体。  

    Referer:http://localhost:8080/hello/index.html：请求来自哪个页面.
    Content-Type: application/x-www-form-urlencoded：表单的数据类型，说明会使用url格式编码数据；url编码的数据都是以“%”为前缀。 
    Content-Length:13：请求体的长度，这里表示13个字节。 
    keyword=hello：请求体内容！hello是在表单中输入的数据，keyword是表单字段的名字。  
    Referer请求头是比较有用的一个请求头，它可以用来做统计工作，也可以用来做防盗链。 
    
***3.3 `GET`和`POST`请求的区别***

****3.3.1 `GET`请求****

    GET /books/?sex=man&name=Professional HTTP/1.1
    Host: www.wrox.com
    User-Agent: Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.7.6)
    Gecko/20050225 Firefox/1.0.1
    Connection: Keep-Alive
    注意最后一行是空行
    
****3.3.2 `POST`请求****

    POST / HTTP/1.1
    Host: www.wrox.com
    User-Agent: Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.7.6)
    Gecko/20050225 Firefox/1.0.1
    Content-Type: application/x-www-form-urlencoded
    Content-Length: 40
    Connection: Keep-Alive
    name=Professional%20Ajax&publisher=Wiley
    
****3.3.3 `GET`和`POST`的区别****

    1、GET请求的数据会附在URL之后,以?分割URL和传输数据，多个参数用&连接;POST提交：把提交的数据放置在是HTTP包的包体中。所以GET提交的数据会在地址栏中显示出来，而POST提交，地址栏不会改变
	2、传输数据的大小：HTTP协议没有对传输的数据大小进行限制，HTTP协议规范也没有对URL长度进行限制。
	3、POST的安全性要比GET的安全性高。比如：通过GET提交数据,用户名和密码将明文出现在URL上,其他人查看浏览器的历史纪录,就可以拿到你的账号和密码了.除此之外，使用GET提交数据还可能会造成Cross-site request forgery攻击
	
**4.响应协议**

***4.1 响应内容***
 
响应协议的格式如下：

	响应首行； 
	响应头信息； 
	空行； 
	响应体。 
	
响应内容是由服务器发送给浏览器的内容，浏览器会根据响应内容来显示。

遇到`<img src=''>`会开一个新的线程加载，所以有时图片多的话，内容会先显示出来，然后图片才一张张加载出来。   
```
Request URL:http://127.0.0.1:8090/login/ 
Request Method:GET 
Status Code:200 OK 
Remote Address:127.0.0.1:8090 
Response Headers 
view source 
Content-Type:text/html; 
charset=utf-8 
Date:Wed, 26 Oct 2016 06:48:50 GMT 
Server:WSGIServer/0.2 CPython/3.5.2 
X-Frame-Options:SAMEORIGIN  
```
```
    <!DOCTYPE html> 
    <html lang="en"> 
    <head>     
        <meta charset="UTF-8">     
        <title>Title</title> 
    </head> 
    <body> 
    <form action="/login/" method="post">   
        用户名：<input type="text" name="username"/>   
        <input type="submit" value="提交"/> </form>     
    </body> 
    </html>  
```
    HTTP/1.1 200 OK：响应协议为HTTP1.1，状态码为200，表示请求成功，OK是对状态码的解释； 
    Server:WSGIServer/0.2 CPython/3.5.2：服务器的版本信息； 
    Content-Type: text/html;charset=UTF-8：响应体使用的编码为UTF-8； 
    Content-Length: 724：响应体为724字节； 
    Set-Cookie: JSESSIONID=C97E2B4C55553EAB46079A4F263435A4; Path=/hello：响应给客户端的Cookie； 
    Date: Wed, 25 Sep 2012 04:15:03 GMT：响应的时间，这可能会有8小时的时区差； 

***4.2 状态码*** 

响应头对浏览器来说很重要，它说明了响应的真正含义。

    200:请求成功，浏览器会把响应体内容（通常是html）显示在浏览器中； 
    404:请求的资源没有找到，说明客户端错误的请求了不存在的资源； 
    500:请求资源找到了，但服务器内部出现了错误； 
    302:重定向，当响应码为302时，表示服务器要求浏览器重新再发一个请求，服务器会发送一个响应头Location，它指定了新请求的URL地址； 
    304:用户第一次请求index.html时，服务器会添加一个名为Last-Modified响应头，这个头说明index.html的最后修改时间.
	
浏览器会把`index.html`内容，以及最后响应时间缓存下来。

当用户第二次请求`index.html`时，在请求中包含一个名为`If-Modified-Since`请求头，

它的值就是第一次请求时服务器通过`Last-Modified`响应头发送给浏览器的值，即`index.html`最后的修改时间，   

`If-Modified-Since`请求头就是在告诉服务器，浏览器缓存的`index.html`的最后修改时间,   

而如果第二次请求的`index.html`修改时间相同,服务器会发响应码304,浏览器就会显示自己的缓存页面,

如果比对不同，那么说明`index.html`已经做了修改，服务器会响应200。  
  
**5.HTTP工作原理**

`HTTP`协议定义Web客户端如何从Web服务器请求Web页面，以及服务器如何把Web页面传送给客户端。

`HTTP`协议采用了请求/响应模型。

客户端向服务器发送一个请求报文，请求报文包含请求的方法、`URL`、协议版本、请求头部和请求数据。

服务器以一个状态行作为响应，响应的内容包括协议的版本、成功或者错误代码、服务器信息、响应头部和响应数据。

以下是HTTP请求/响应的步骤：

	1、客户端连接到Web服务器,与Web服务器的HTTP端口（默认为80）建立一个TCP套接字连接。
	2、发送HTTP请求,通过TCP套接字，客户端向Web服务器发送一个文本的请求报文.
	3、Web服务器解析请求，定位请求资源。服务器将资源复本写到TCP套接字，由客户端读取。
	4、若connection 模式为close，则服务器主动关闭TCP连接，客户端被动关闭连接，释放TCP连接;若connection模式为keepalive，则该连接会保持一段时间，在该时间内可以继续接收请求;
	5、客户端浏览器解析HTML内容
	
客户端浏览器首先解析状态行，查看表明请求是否成功的状态代码。然后解析每一个响应头，响应头告知以下为若干字节的HTML文档和文档的字符集。

客户端浏览器读取响应数据`HTML`，根据HTML的语法对其进行格式化，并在浏览器窗口中显示。

在浏览器地址栏键入`URL`，按下回车之后会经历以下流程

	1、浏览器向 DNS 服务器请求解析该 URL 中的域名所对应的 IP 地址
	2、解析出 IP 地址后，根据该 IP 地址和默认端口 80，和服务器建立TCP连接
	3、浏览器发出读取文件(URL 中域名后面部分对应的文件)的HTTP 请求，该请求报文作为 TCP 三次握手的第三个报文的数据发送给服务器
	4、服务器对浏览器请求作出响应，并把对应的 html 文本发送给浏览器
	5、释放 TCP连接
	6、浏览器将该 html 文本并显示内容