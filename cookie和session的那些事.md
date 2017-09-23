对于经常网购的朋友来说,经常会遇到一种情况:

打开淘宝或京东商城的首页,输入个人账号和密码进行登陆,然后进行购物,支付等操作都不需要用户再次输入用户名和密码

但是如果用户换一个浏览器或者等几个小时后再刷新这些网页进行购物操作,就必须要再次输入用户名和密码了.

这是为什么呢??这就用到了`cookie`和`session`的知识了.

**1. cookie的简介**

***1、http是无状态协议,cookie不属于http协议范围.***

在实际应用中，服务端与客户端需要保持连接状态，此时就需要使用到cookie.

`cookie`的工作原理是：由服务器产生客户端身份信息发送给客户端，客户端收到信息后保存在本地；

当客户端浏览器再次访问服务端时，会自动带上这段身份信息，服务器通过这段信息来判断客户端的身份。

***2、cookie在一定程度上解决了`"保持状态"`的需求***

由于cookie本身最大支持4096字节，并且cookie保存在客户端，可能被拦截或窃取,

因此需要有一种新的东西，它来弥补cookie的一些缺陷，并且保存在服务端，有较高的安全性,这就是session。

基于http协议的无状态特征，服务器不知道访问者的身份,此时cookie就起到桥接的作用。

服务端给每个客户端的cookie分配一个唯一的随机id，用户在访问服务端时，服务器通过cookie来判断客户端的身份。

服务端根据cookie的id的不同，在一定的期限内保存客户端传送过来的账号密码等关键信息.

***、cookie弥补了http无状态的不足，让服务器能够判断客户端的身份***

cookie以文本的形式保存在本地，自身安全性较差,因此服务端通过cookie识别不同的用户，对应的在session里保存私密的信息以及超过4096字节的文本。

***4、cookie和session其实是共通性的东西，不限于语言和框架***

**2. cookie和session的工作机制**

每当我们使用一款浏览器访问一个登陆页面的时候，一旦我们通过了认证,服务器端就会发送一组随机唯一的字符串（假设是123abc）到浏览器端.

这个被存储在浏览器端的东西就叫`cookie`。而服务器端也会存储一下用户当前的状态，比如`login=true`，`username="name"`之类的用户信息。

这种信息是以字典形式存储成为一个字符串，这串字符串以用户第一次请求时得到的cookie值为键,这就是session.

那么如果在服务器端查看session信息的话，理论上就会看到如下样子的类似的字典

    {'123abc':{'login':true,'username':'hahaha'}}
    
因为每个cookie都是唯一随机的，所以我们在同一台电脑上换个浏览器再登陆同一个网站也需要再次验证。

那么为什么说我们只是理论上看到这样子类似的字典呢？因为处于安全性的考虑，其键和值在服务器端都会被加密。

所以我们服务器上就算打开session信息看到的也是类似与以下样子的东西:

    {'123abc':dasdasdasd1231231da1231231}
    
**3.cookie和session的初步使用**

例子:制作一个登陆页面，服务端使用cookie和session验证了用户名和密码后才能跳转到后台的页面。

***3.1 首先创建一个Django的项目,配置好urls和settings,templates中创建一个login.html和index.html页面***

views中的代码:
```
def index(request):
    return render(request,"index.html")

def login(request):
    print("cookie:",request.COOKIES)        #打印cookie信息
    
    if request.method=="POST":              #如果浏览器使用post方式提交信息
        name=request.POST.get("username")
        pwd=request.POST.get("password")
        
        if name=="hello" and pwd=="123456":
            return redirect("/index/")

    return render(request,"login.html")
```        
login页面:
```
<form action="/login/" method="post">
    <p>姓名<input type="text" name="username"></p>
    <p>密码<input type="password" name="password"></p>
    <p><input type="submit"></p>
</form>
```    
index页面:

    <h3>welcome to index page</h3>
   
打开浏览器,输入`http://127.0.0.1:8000/login/`打开login页面,输入正确的用户名和密码,进入index页面

此时可以在后端看到如下的cookie信息

    cookie: {'csrftoken': 'AdkajMM65wOqa0NONe6dVwYqphGNDOgMbuzstmAy92HJ3GxRWUNpqXKJFXBv1Rn5', 
    'sessionid': '7jfj6uqbz6vylplfv429bhfdxh14iwfp'}
    
其中`sessionid`中的信息就是Django分配给浏览器的一段随机字符串.

***3.2 由用户自己设置cookie信息***

修改login视图函数:

```
def login(request):

    print("cookie:",request.COOKIES)
    
    if request.method=="POST":
        name=request.POST.get("username")
        pwd=request.POST.get("password")
        
        if name=="hello" and pwd=="123456":
            res=redirect("/index/")
            res.set_cookie("login_message","hello python")#设置cookie信息
            return res
            
    return render(request,"login.html")
```        
然后重启应用,重新输入用户名和密码,进入index页面,此时可以看到如下的cookie信息:

    cookie: {'csrftoken': 'AdkajMM65wOqa0NONe6dVwYqphGNDOgMbuzstmAy92HJ3GxRWUNpqXKJFXBv1Rn5', 
    'sessionid': '7jfj6uqbz6vylplfv429bhfdxh14iwfp', 'login_message': 'hello python'}   
    
可以看到在后端的login视图函数中设置的cookie的键值对,浏览器请求后又会被服务端接收.

用户请求页面时,是带着标示自己的身份信息的,服务端对客户端的身份信息进行判断,只有身份正确,才能进入index页面.

但是如果在浏览器的地址中直接输入index的路由地址,也能进入index的页面的情况,这不符合我们的要求.

***3.3 实现客户端没有cookie,即使用户输入index路由信息,服务端发送登录页面给用户***

如果客户端没有cookie,说明用户名或密码没有验证成功,服务端就会把login页面发送给客户端浏览器,

只有用户输入正确的用户名和密码,服务端才会把index页面发送给客户端浏览器.

修改index视图函数:
```
    def index(request):
        if request.COOKIES.get("login_message")=="hello python":
            return render(request,"index.html",locals())
        else:
            return redirect("/login/")
```
这样用户在一个浏览器中经过验证进入index.html页面后,清除cookie或者更换一个浏览器再想进入index页面,就要再次验证用户名和密码了.

由于用户的cookie信息保存在客户端,每与服务端通信一次,客户端就要把cookie信息发送经服务端一次,而且保存在客户端也不够安全,所以又出现了session

session也保存客户端身份的信息,用户登录后服务端把表示用户身份的信息保存成以键值对形式存在的session中,然后服务端把这个字典发送给客户端的cookie,

这时客户端的cookie就以一个字符串的形式存在.

客户端使用cookie和session与服务端进行通信的步骤:

    用户经过用户名和密码验证登陆后,生成一个字典,将字典存入session,session的key是自动生成一段字符串标识,也就是前面说过的cookie.
    服务端返回给客户端session,session的value存储了用户的关键信息,如user和iflogin等.
    
在Django中用到session时,cookie由服务端随机生成,写到浏览器的cookie中,每个浏览器都有自己的cookie值,是session寻找用户信息的唯一标识

每个浏览器请求到后台接收的request,这时的session等价于标识用户身份信息的字典

***3.4 使用cookie加session来完成上面的例子***

修改views中的login视图函数
```
    def login(request):
        print("cookie:",request.COOKIES)
        print("session:",request.session)
    
        if request.method=="POST":
            name=request.POST.get("username")
            pwd=request.POST.get("password")
            if name=="hello" and pwd=="123456":
    
                res=redirect("/index/")
                res.set_cookie("login_message","hello python")
                return res
    
        return render(request,"login.html")
```
再次刷新浏览器,输入正确的用户名和密码后,打印cookie和session:

    cookie: {'csrftoken': 'AdkajMM65wOqa0NONe6dVwYqphGNDOgMbuzstmAy92HJ3GxRWUNpqXKJFXBv1Rn5', 
    'sessionid': '7jfj6uqbz6vylplfv429bhfdxh14iwfp', 'login_message': 'hello python'}
    
    session: <django.contrib.sessions.backends.db.SessionStore object at 0x00000000043D7D30>
    
可以看到的是此时的session是一个对象.

知道了`cookie`和`session`的情况后,那么该怎么使用cookie和session呢

修改视图函数
```
    def index(request):
        if request.session.get("is_login",None):#获取session中用户登录的信息
            name=request.session.get("user")#获取session中的用户名
            return render(request,"index.html",locals())
        else:
            return redirect("/login/")
    
    def login(request):
        print("cookie:",request.COOKIES)
        print("session:",request.session)
    
        if request.method=="POST":
            name=request.POST.get("username")
            pwd=request.POST.get("password")
            
            if name=="hello" and pwd=="123456":
                request.session["is_login"]=True
                request.session["user"]=name
                return redirect("/index/")
        return render(request,"login.html")
 ```       
先使用

    python manage.py makemigrations
    python manage.py migrate
    
命令初始化数据库,然后在浏览器中输入`http://127.0.0.1:8000/index/`后,进入登录页面,输入正确的用户名和密码,后端会打印如下信息:

    cookie: {}
    session: <django.contrib.sessions.backends.db.SessionStore object at 0x00000000043B46D8>
    
**4.  cookie和session的用法**

***4.1 操作cookie***

    获取cookie            request.COOKIE[key]
    设置cookie            response.set_cookie(key,value)
    
由于cookie保存在客户端的电脑上,所以jQuery也可以操作cookie

在上面的例子中,在html页面中就使用Django的语法可以渲染name变量.

设置cookie的失效时间:
```
    import datetime#导入datetime模块
    
    response.set_cookie("username",{"11":"22"},max_age=10,
        expires=datetime.datetime.utcnow()+datetime.timedelta(days=3))
```     
其中:

    datetime.datetime.utcnow()表示当前时间
    datetime.timedelta(days=3)表示3天
    
上面的代码表示设置cookie在当前时间的3天后失效

***4.2 操作session(session默认在服务端保存15天)***

    获取session       request.session[key]或者request.session.get(key)
    设置session       request.session[key]=value
    删除session       del request.session[key]
    
需要注意的是,删除服务端的`session`不会删除数据库中的`session_data`,而只是把session更新为一个其他的值

设置session的失效时间:

    request.session.set_expiry(value)是设置session的失效时间
    
参数说明:
   
    如果value是一个整数,session会在整数称后失效
    如果value是个datatime或者timedelta,session会在这个时间之后失效
    如果value是0,用户关闭浏览器后session就会失效
    如果value是None,session会依赖全局session的失效策略
