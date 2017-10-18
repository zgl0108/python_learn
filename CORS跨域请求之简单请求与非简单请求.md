先来看一个例子

定义`server01`的项目,在路由表中添加一条路由记录

    url(r'^getData.html$',views.get_data)

对应的视图函数

        from django.shortcuts import render,HttpResponse
        
        def get_data(request):
        
            response=HttpResponse("server----001")
            return response

定义`server02`项目,在路由表中添加一条路由记录

    url(r'^index.html/',views.index),

对应的视图函数

        from django.shortcuts import render
        
        def index(request):
        
            return render(request,"index.html")
		
对应的index.html文件

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
                success:function(data){
                    console.log(data);
                }
            })
        </script>
        </body>
        </html>
	
运行`server01`项目,使用`8100端口`打开server02的`index.html`网页,可以看到如下信息

![](http://images2017.cnblogs.com/blog/1133627/201710/1133627-20171018181537756-1874808628.png)

发送这个请求使用的是`GET`方法.如果把server02的index.html网页中设定为使用`PUT`方法发送请求,会看到什么情况呢?

把`index.html`中的请求方法修改为`PUT`,然后刷新浏览器

![](http://images2017.cnblogs.com/blog/1133627/201710/1133627-20171018181547537-63878354.png)

可以看到网页上显示的request method变成了`OPTIONS`,可是在网页中声明的请求方法是`PUT`呀

为什么会出现这样的情况呢???这就涉及到`简单请求`和`非简单请求`了.

    简单请求就是使用设定的请求方式请求数据
    而非简单请求则是在使用设定的请求方式请求数据之前,先发送一个OPTIONS请求,看服务端是否允许客户端发送非简单请求.
        只有"预检"通过后才会再发送一次请求用于数据传输

简单请求与非简单请求的区别

	* 请求方式:HEAD,GET,POST
	* 请求头信息:
        Accept
        Accept-Language
        Content-Language
        Last-Event-ID
        Content-Type 对应的值是以下三个中的任意一个
                            application/x-www-form-urlencoded
                            multipart/form-data
                            text/plain
	
只有同时满足以上两个条件时,才是简单请求,否则为非简单请求

如果在上面的例子中,在server01中设定响应头,

        from django.shortcuts import render,HttpResponse
        
        def get_data(request):
            if request.method=="OPTIONS":
            
                response=HttpResponse()
                response['Access-Control-Allow-Origin']="*"
                response['Access-Control-Allow-Methods']="PUT"
                return response
            elif request.method =="PUT":
            
                response=HttpResponse("server----001")
                response['Access-Control-Allow-Origin']="*"
                return response

再次刷新`http://127.0.0.1:8100/index.html/`网页,可以看到

![](http://images2017.cnblogs.com/blog/1133627/201710/1133627-20171018181600224-1965424594.png)

![](http://images2017.cnblogs.com/blog/1133627/201710/1133627-20171018181607849-50215134.png)

![](http://images2017.cnblogs.com/blog/1133627/201710/1133627-20171018181615740-1763658312.png)

先发送的是`OPTIONS请求`,第二次发送的是`PUT请求`,而且获取到目标字符串.

由此得知,对于非简单请求,客户端以`PUT`方式请求数据,服务端的"预检"里边一定要包含允许客户端使用非简单方式请求数据的响应头

	“预检”请求时，允许请求方式则需服务器设置响应头：Access-Control-Request-Method
	“预检”请求时，允许请求头则需服务器设置响应头：Access-Control-Request-Headers
	“预检”缓存时间，服务器设置响应头：Access-Control-Max-Age

虽然可以通过设置响应头和响应方式等支持非简单请求,但是不到万不得已的情况,不能允许客户端发送非简单请求.

因为非简单请求会使服务器比简单请求的多一倍的压力.

上次发表的Django的思维导图在一些地方折叠起来了,这次重新发一张关于Django的思维导图,方便以后自己查询.

![](http://images2017.cnblogs.com/blog/1133627/201710/1133627-20171018181646224-309707627.png)