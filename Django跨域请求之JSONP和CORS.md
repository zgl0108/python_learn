现在来新建一个Django项目`server01`,url配置为

    url(r'^getData.html$',views.get_data)
	
其对应的视图函数为`get_data`:

        from django.shortcuts import render,HttpResponse
        
        def get_data(request):
        
            return HttpResponse("server----001")

以Django的默认端口启动这个项目,在浏览器中输入网址`http://127.0.0.1:8000/getData.html`

![](http://images2017.cnblogs.com/blog/1133627/201710/1133627-20171019094107537-155623979.png)

现在所有的人就都可以来访问这个网站,浏览器上打印`"server----001"`这个目标字符串.

此时打开系统的命令提示符,调用`requests`这个模块

![](http://images2017.cnblogs.com/blog/1133627/201710/1133627-20171019094116646-1649121791.png)

通过上面的实验知道,可以使用`requests`这个模块获取这个字符串,也可以通过浏览器来获取到这个字符串 

现在再新建一个Django项目`server02`,url配置为

    url(r'^index.html/',views.index),

视图函数views配置为:

        from django.shortcuts import render
        
        def index(request):
        
            return render(request,"index.html")	

`index.html`页面引入静态文件jquery,然后把这个项目以`8100`端口启动

现在打开`http://127.0.0.1:8100/index.html/`的页面如下:

![](http://images2017.cnblogs.com/blog/1133627/201710/1133627-20171019094125412-132117006.png)

如果想把server01页面上的字符串`"server----001"`引入到这个index页面上,就要向server01这台服务器发送请求.

此时有两种方案

**第一种方案:使用`requests`模块获取字符串**

修改视图函数`index`

        from django.shortcuts import render
        import requests
        
        def index(request):
        
            response=requests.get("http://127.0.0.1:8000/getData.html")
            return render(request,"index.html",{"response":response})
            
在index.html页面上使用模板语言渲染

	<body>
	<h1>server----002</h1>
	{{ response.text }}
	<script src="/static/jquery-3.2.1.js"></script>
	</body>

刷新浏览器,可以看到如下所示:

![](http://images2017.cnblogs.com/blog/1133627/201710/1133627-20171019094135584-1515123043.png)

此时,已经获取到想要的数据了

获取这个字符串的步骤:

首先,请求到达server02,经过路由转发给视图函数,在视图函数中又调用了`requests`模块向server01发送请求,获取到目标字符串经过渲染 后在页面上显示出来.

这个方法获取到了数据,但是使用这种方法有一个缺点:显示到页面上的字符串经过了两次请求才获取到,这种方法比较麻烦.

第二种方法:不通过后台,发送Ajax请求来获取字符串

修改index.html:

	<!DOCTYPE html>
	<html lang="en">
	<head>
		<meta charset="UTF-8">
		<title>Title</title>
	</head>
	<body>
	<h1>server----002</h1>
	<script src="/static/jquery-3.2.1.js"></script>
	<script>
		$.ajax({
			url:'http://127.0.0.1:8000/getData.html',
			type:'GET',
			succedd:function(arg){
				console.log("arg")
			}
		})
	</script>
	</body>
	</html>

此时再次刷新浏览器,会发现页面上并没有发现想要的字符串

![](http://images2017.cnblogs.com/blog/1133627/201710/1133627-20171019094143756-1240938047.png)

打开chrome浏览器的查看功能,可以看到报错了

![](http://images2017.cnblogs.com/blog/1133627/201710/1133627-20171019094150834-1264067854.png)

为什么会出现这个错误呢??

在当前index.html网页中,请求的域名为`http://127.0.0.1:8100`,而在ajax中,请求的是另外一个域名`http://127.0.0.1:8000`

虽然看起来都是本机的地址,但是因为请求的端口不同,所以请求的不是同一个域名.

而Ajax请求都只能向当前的域名发起请求,所以当向另一个域名发送请求时,浏览器就会报错了.

那为什么不能通过ajax向别的域名发送请求呢??在这里,是因为浏览器做了同源策略的限制

那到底浏览器又是在哪一个导面做的限制呢??是限制发出请求,还是限制响应请求呢??做个测试就知道了.

重新启动server01项目,此时再次刷新`index.html`的页面,可以看到在server01中接收到了请求.

![](http://images2017.cnblogs.com/blog/1133627/201710/1133627-20171019094209287-1912193772.png)

可以看到在server01中已经接收到了请求.server01中接收到请求然后返回响应信息,但是在浏览器上却没有显示出来,所以浏览器是在接收层面上做出了限制.

在前面的例子里,调用`requests`发起请求时,`requests`模块接收到字符串,使用模板语言渲染后发送给`index.html`网页

因此可以知道,

    调用requests发起跨域请求时,浏览器无限制.
    使用ajax发起跨域请求时,浏览器会做出限制.

那么接下来,该怎么做才能解除浏览器的限制呢??

首先,尝试使用`JSONP`方法绕过浏览器同源策略的限制,

	JSONP(JSONP-JSON with Padding是JSON的一种“使用模式”)，利用script标签的src属性(浏览器允许script标签跨域)
	
首先来看一个实例,在index.html中引入博客园的图片

	<body>
	<h1>server----002</h1>
	<img src="https://www.cnblogs.com/images/logo_small.gif">
	<script src="/static/jquery-3.2.1.js"></script>
	<script>
		$.ajax({
			url: 'http://127.0.0.1:8000/getData.html',
			type: 'GET',
			success: function (arg) {
				alert(arg);
			}
		})
	</script>
	</body>
刷新浏览器,可以看到

![](http://images2017.cnblogs.com/blog/1133627/201710/1133627-20171019094218506-2143654179.png)

可以看到引入图片的地址不是当前的域名,但是图片依然被引入了.

请求发成功了,所以知道了img不受浏览器同源策略的限制.

使用过bootstrap的同学都知道,调用bootstrap的时候可以使用本地的bootstrap文件,也可以使用cdn来调用bootstrap.

例如,这个项目也可以使用cdn的jquery来显示页面.

	<body>
	<h1>server----002</h1>
	<img src="https://www.cnblogs.com/images/logo_small.gif">
	<script src="https://cdn.bootcss.com/jquery/3.2.1/core.js"></script>
	<script>
		$.ajax({
			url: 'http://127.0.0.1:8000/getData.html',
			type: 'GET',
			success: function (arg) {
				alert(arg);
			}
		})
	</script>
	</body>

刷新浏览器,显示的页面跟上次的页面是一样的.表示使用cdn引入jquery成功.

所以, 使用具有src属性的标签发送跨站请求都不受浏览器同源策略的限制.

    具有src属性的标签有img,script,iframe等.

修改`index.html`网页,把跨站请求的网址写在script标签里.

	<!DOCTYPE html>
	<html lang="en">
	<head>
		<meta charset="UTF-8">
		<title>Title</title>
		<script src="http://127.0.0.1:8000/getData.html"></script>
	</head>
	<body>
	<h1>server----002</h1>
	</body>
	</html>

再次刷新浏览器,可以看到想获取的字符串并没有显示在index.html网页上.

![](http://images2017.cnblogs.com/blog/1133627/201710/1133627-20171019094535865-389718832.png)

但是浏览器中出现了一个字符串没有定义的错,说明想获取的字符串已经获取到了,跨站的请求已经发送成功了.

![](http://images2017.cnblogs.com/blog/1133627/201710/1133627-20171019094230943-632049096.png)

这里"server----001没有定义"的错是怎么产生的呢??通常来说,没有定义针对的都是变量.

在这个网页里,只有编写的javascript里面有变量.

在上面的代码里,所发出的请求是写在sript标签里的,server01里返回的信息都会当做script语法来渲染.

但是这样一来,虽然绕过了同源策略的影响,也拿到了想要的字符串,但是获取到的目标字符串根本没法直接使用.

修改server01的视图函数,现在`func("server----001")`就是一个字符串了.

        from django.shortcuts import render,HttpResponse
        
        def get_data(request):
        
            return HttpResponse('func("server----001")')

server02网站请求的时候把`func("server----001")`这个字符串返回给server02,

再修改server02的`index.html`网页

        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>Title</title>
            
            <script>
                function func(arg){
                    console.log(arg)
                }
            </script>
            <script src="http://127.0.0.1:8000/getData.html"></script>
        </head>
        <body>
        <h1>server----002</h1>
        </body>
        </html>

再次刷新`http://127.0.0.1:8100/index.html/`这个网页,可以看到想要的字符串已经出现在`console`里了.

![](http://images2017.cnblogs.com/blog/1133627/201710/1133627-20171019094613990-1580080726.png)

由于浏览器的同源策略,ajax发的跨站请求不能获取跨站的返回数据,但是可以使用`src`属性和`script`代码来自己构造获取跨站请求的返回数据.

但是这样一来对请求的网页也有要求,那就是不能直接返回目标数据,而是要在目标数据的外层包装一个func函数名.

所以上面的方法对客户端和服务端都有限制.这种方法就叫做`JSONP`.

上面的方法是手动实现`JSONP`方法,可不可能看上去使用`JSONP`的方法来实现跨站请求呢??

修改server02的`index.html`

	<!DOCTYPE html>
	<html lang="en">
	<head>
		<meta charset="UTF-8">
		<title>Title</title>
	</head>
	<body>
	<h1>server----002</h1>
	<input type="button" onclick='jsonp("http://127.0.0.1:8000/getData.html")' value="发送JSONP请求"/>
	<script src="/static/jquery-3.2.1.js"></script>
	<script>
		function func(arg) {
			alert(arg);

			document.head.removeChild(tag);
		}
		function jsonp(url) {
			tag = document.createElement("script");
			tag.src = url;
			document.head.appendChild(tag);
		}
	</script>
	</body>
	</html>

刷新浏览器,

![](http://images2017.cnblogs.com/blog/1133627/201710/1133627-20171019094631037-1613913425.png)

点击"发送JSONP请求"按钮,网页会弹出一个对话框,显示目标字符串.

![](http://images2017.cnblogs.com/blog/1133627/201710/1133627-20171019094639052-526036988.png)

在这里每次发送跨站请求,页面都没有刷新,依然没有使用ajax发送请求.这样做的好处一样是,不受浏览器同源策略的限制.

但这种方法也有一个缺点,那就是server01的视图函数中目标字符串外面被包装的函数名被固定了.

正常情况下,这个函数名应该是会改变的.

由于server02服务器向server01请求数据时是使用`GET`方法发出的请求,所以可以在发送的请求网址上进行修改.

修改server01的视图函数

        from django.shortcuts import render,HttpResponse
        
        def get_data(request):
            func_name=request.GET.get("callback")
        
            return HttpResponse('%s("server----001")' % func_name)

然后修改server02的`index.html`网页,在请求的地址上加上一个`callback=func1`的字符串

        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>Title</title>
        </head>
        <body>
        <h1>server----002</h1>
        <input type="button" onclick='jsonp("http://127.0.0.1:8000/getData.html?callback=func1")' value="发送JSONP请求"/>
        <script src="/static/jquery-3.2.1.js"></script>
        <script>
            function func1(arg) {
                alert(arg);
        
                document.head.removeChild(tag);
            }
            function jsonp(url) {
                tag = document.createElement("script");
                tag.src = url;
                document.head.appendChild(tag);
            }
        </script>
        </body>
        </html>

刷新浏览器,点击`发送JSONP请求`按钮,可以看到目标字符串同样显示在页面上了.

![](http://images2017.cnblogs.com/blog/1133627/201710/1133627-20171019094651677-837073747.png)

这样一来,server01服务端上的函数名就由客户端网页文件来决定了.

上面的例子都是自己开发的代码来实现的`JSONP`的本质.

**自动实现JSONP方法**

在`jQuery`里默认就支持`JSONP`的方法

        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>Title</title>
        </head>
        <body>
        <h1>server----002</h1>
        <input type="button" onclick='jsonp2()' value="发送JSONP请求"/>
        <script src="/static/jquery-3.2.1.js"></script>
        <script>
        
            function jsonp2(){
                $.ajax({
                    url:'http://127.0.0.1:8000/getData.html',
                    type:'GET',
                    dataType:'JSONP',
                    success:function(data){
                        console.log(data)
                    }
                })
            }
        </script>
        </body>
        </html>

使用ajax向server01发送请求,原来没有声明`'dataType="JSONP"'`时会被浏览器的同源策略所阻止的.

但现在没有受到浏览器的阻止,已经获取到目标字符串了.

![](http://images2017.cnblogs.com/blog/1133627/201710/1133627-20171019094700521-310411953.png)

也可以把`index.html`修改成下面这样来实现同样的功能

        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>Title</title>
        </head>
        <body>
        <h1>server----002</h1>
        <input type="button" onclick='jsonp2()' value="发送JSONP请求"/>
        <script src="/static/jquery-3.2.1.js"></script>
        <script>
            function list(arg){
                console.log(arg)
            }
        
            function jsonp2(){
                $.ajax({
                    url:'http://127.0.0.1:8000/getData.html',
                    type:'GET',
                    dataType:'JSONP',
                    jsonp:'callback',
                    jsonpCallback:'list',	// list为请求中发送的函数名
                })
            }
        </script>
        </body>
        </html>

在使用`JSONP`方法时,有两种方法,手动实现与调用jQuery自动实现

编写跨域请求时,在本地使用jQuery的方式来向目标服务器发送跨域请求,

而在远程服务器上,接收客户端发送的`GET请求,获取接收到的数据中的函数中,包装目标数据就可以了.

应用场景:

	在调用外部的API时,如果使用JSONP的方式请求数据,则服务端和客户端都要做出相应的修改.
	如果服务端无法做出修改时,可以调用requests模块来获取数据
	
需要注意的是`JSONP无法发送POST请求`,在ajax中即使把发送请求的类型设置为`POST`,其`实质仍然发送的是GET请求`.

**Django跨域请求之CORS**

`跨域资源共享(CORS，Cross-Origin Resource Sharing)，`其本质是设置响应头，使得浏览器允许跨域请求

CORS实现跨域请求的实现思路与JSONP完全是不一样的.那么CORS是怎么实现的呢?

在前面通过实验,知道了使用ajax发送跨域请求时,请求实际上到达了服务端,而且服务端也做出了响应.

但是被浏览器的同源策略限制了而已.浏览器为什么会限制呢,就是因为服务端的响应数据里缺少了一个头.

在上面的例子里,使用ajax来请求数据的时候,浏览器出现了一个报错信息,如下图

![](http://images2017.cnblogs.com/blog/1133627/201710/1133627-20171019094713521-171540003.png)

根据报错信息,可以知道返回的信息里缺少一个头部信息,由于响应信息是由server01服务端返回来的,所以如果在从server01服务端返回的信息里加上缺少的响应头,会怎么样呢?

依旧拿上面的代码来做实验,修改server01的视图函数,在响应信息里加上缺少的响应头信息

        from django.shortcuts import render,HttpResponse
        
        def get_data(request):
            response=HttpResponse("server----001")		# 设定响应信息
            response["Access-Control-Allow-Origin"]="http://127.0.0.1:8100"		# 允许定义的域名可以向本机发送请求
        
            return HttpResponse(response)

打开浏览器,进入`http://127.0.0.1:8100/index.html/`网页,可以获取到相应的目标数据了

![](http://images2017.cnblogs.com/blog/1133627/201710/1133627-20171019094721349-193467579.png)

这种方法就是通过CORS方法设置响应头部信息来实现允许指定域名的主机向本机发送跨域请求.

如果想设定为允许所有的域名主机可以向本机发送请求,可以指头部信息设定为"*"

	response["Access-Control-Allow-Origin"]="*"		# 允许所有域名可以向本机发送请求

由上面的实验可以知道,所谓的CORS的本质就是为响应的数据信息设置响应头部,而本地主机不需要做特别的设置.