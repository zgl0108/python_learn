**1. Django的简介**

Django是一个由python写成的开放源代码的Web应用框架。

Django的目的是使常见的Web开发任务，快速和容易。

**2. Django框架的特点**

* 遵循MVC开发模式
* 内置进行快速web开发所需的各种组件
* 利用ORM(对象关系映射)机制来定义和数据库,使开发人员可以构建出独立于具体数据库引擎的web应用
* 内置后台管理web应用
* 内置web Server,开发人员无需安装任何web Server就可以进行各种web应用的开发和测试
* 具有灵活而强大的自定义url系统
* 内置多语种支持,可以方便地构建多国语言的web应用 

MVC设计模式

Django是一种遵循MVC开发模式的框架.

    models.py文件中定义各种类代表的数据模型(Model)和数据库引擎交互,执行数据库数据的存取操作.
    temolates文件夹中的各个模板文件代表视图(View),负责数据内容的显示
    urls.py中定义了各种url访问入口和views.py中定义的各种处理函数(也称为Django视图函数),可以根据用户输入的url请求,调用views.py中相应的函数,数据模型和视图交互,响应用户的请求.

基于Django的web应用开发活动由于主要集中在`models.py`,`templates`文件夹中的各模板文件以及`views.py`之内,因此Django的开发模式通常也称为MTV开发模式

**3. 安装**

方式一,`pip方式安装`

    pip install Django

方式二,`pycharm中在file菜单中安装`

    在pycharm中找开file-->settings-->Project-->Project Interpreter

方式三,到`github`克隆安装

	git clone https://github.com/django/django.git

**4. 基本配置**

***4.1 常用的命令***

在IDE中创建Django程序时,本质上都是自动执行上述命令
```
    #查看Django版本
    python -m django --version
    
    #创建一个名为mysite的项目
    django-admin startproject mysite
    
    #Django项目环境终端
    python manage.py shell
    
    #创建应用程序,确保和manage.py是同一个目录
    python manage.py startap polls
    
    #启动Django,端口使用Django默认的8000
    python manage.py runserver
    
    #启动Django,端口为8800
    python manage.py runserver 8800
    
    #启动Django,端口为8800,任意机器都可以访问
    python manage.py runserver 0.0.0.0:8800
    
    #进行创建模型变化迁移
    python manage.py makemigrations
    
    #运行应用模型变化到数据库
    python manage.py migrate
    
    #同步到数据库
    python manage.py syncdb
    
    #清空数据库(保留空表)
    python manage.py flush
    
    #admin创建管理员用户
    python manage.py createsuperuser
    
    #修改用户密码
    python manage.py changepassword username
```
Django会自动重新加载`runserver`,根据需要开发服务器自动加载python代码,这样开发人员不需要重新启动服务器代码更改生效

***4.2 Django程序基本目录及作用***
```
    mysite/                 #项目容器,名称根据需要自定义
        manage.py           #与该Django项目进行交互的命令行实用工具
        mysite/             #实际的python项目
            __init__.py     #空文件
            setting.py      #Django的项目配置文件
            urls.py         #路由分发，url中的path(路径)与视图函数的映射关系
            wsgi.py         #一个入口为WSGI兼容的WEB服务器
        appname
            models          #与数据库交互的文件
            views           #存放视图函数的	
```
`setting.py`配置文件的说明
```
    #导入OS模块
    import os
    
    #指定本项目的基本目录为这个项目所在的容器的路径
    # Build paths inside the project like this: os.path.join(BASE_DIR, ...)
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    
    # Quick-start development settings - unsuitable for production
    # SECURITY WARNING: keep the secret key used in production secret!
    SECRET_KEY = ')f9lt68ux%%98t872s8l#8i8w7(p8e&)m-yafln3%d%z2x!9st'
    
    # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG = True
    
    #白名单
    ALLOWED_HOSTS = []
    
    # 程序定义文件
    INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'blog',]
    
    # 中间件
    MIDDLEWARE = [
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',]
    
    ROOT_URLCONF = 'url_config.urls'
    
    #模板,用来存放html文件
    TEMPLATES = [
        {'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [os.path.join(BASE_DIR, 'templates')],
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    'django.template.context_processors.debug',
                    'django.template.context_processors.request',
                    'django.contrib.auth.context_processors.auth',
                    'django.contrib.messages.context_processors.messages',
                ],
            },
        },
    ]
    
    #网络服务网关接口
    WSGI_APPLICATION = 'url_config.wsgi.application'
    
    # Database
    # 配置数据库,Django默认使用sqlite数据库,默认自带sqlite数据库驱动,
    # 所使用的数据库的引擎为django.db.backends,sqlite3
    # 指定使用的数据库的路径
    DATABASES = {'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),}}
    
    # Password validation
    AUTH_PASSWORD_VALIDATORS = [
        {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
        {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
        {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
        {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},]
    
    # Internationalization
    #配置项目初始化时的一些参数
    LANGUAGE_CODE = 'en-us'
    TIME_ZONE = 'UTC'
    USE_I18N = True
    USE_L10N = True
    USE_TZ = True
    
    # Static files (CSS, JavaScript, Images)
    # 指定静态文件夹,用来存放css,javascript,image等文件
    STATIC_URL = '/static/'
```
***4.3 静态文件***

在`settings.py`里修改添加,用来存放`CSS,javascript,image`等文件

首先,创建`static`文件夹,然后修改`settings.py`配置文件
```
	STATIC_URL='/static/'		#相当于别名

	#指定静态文件的目录
	STATIC_ROOT={
	    os.path.join(BASE_DIR,"app_01/static"),
	}
```
想使用静态文件,必须在要创建的网页文件中写入引入语句

	{% load staticfiles $}      #写在引入静态文件的网页的第一行
	{% static '文件名' %}        #写在文件当中

引入静态文件的步骤：
```
    １.把所有的静态文件放到一个static文件夹中
    
    ２.将static文件夹放在应用文件夹下
    
    ３.在setting配置文件中配置别名
        STATIC_URL='/static/'
        STATIC_ROOT=(
            os.path.join(BASE_DIR,"应用名/static"),
        )
        
    4.在模板文件的首行加上"{% load staticfiles %}"
    
    5.在模板文件中引入静态文件：
        {% static static静态文件的路径 %}
```
例如,在一个项目中，使用`bootstrap`的样式，就必须这样写：
```
    {% load staticfiles %}
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Title</title>
        <link rel="stylesheet" href="{% static 'bootstrap/css/bootstrap.css' %}">
        <style type="text/css">
        </style>
    </head>
    <body>
    <div class="container">
        <div class="row">
        </div>
    </div>
    </body>
    </html>
```
***4.4 路由系统***

URL配置就像Django所支撑网站的目录,其本质是URL模式以及要为该URL模式调用的视图函数之间的映射表

在Django中,每一个请求的URL都要有一条路由映射,这样才能将请求交给对一个view中的函数去处理

格式:
```
    urlpatterns=[
        url(正则表达式,views视图函数,参数,别名)
    ]
```
****4.4.1 单一路由分配****
```
	#匹配名称为inex的视图
	url(r"^index$",views.index),
```
****4.4.2 基于正则的路由分配****
```
	#匹配以index/开头,后接任意个数字的视图
	url(r'^index/(\d*)',views.index),
	
	#匹配以index/开头,后接任意长度的字母的视图,并把正则表达式的分组匹配到的字段信息发送给客户端
	url(r"^index/(?P<name>\w*)/(?P<id>\d*)",views.index),
```
****4.4.3 添加额外的参数****
```
	#匹配以manage/开头,后接任意长度的字母的视图,并把值为333的id信息发送给客户端
	url(r'^manage/(?P<name>\w*)',views.manage,{'id':333}),
```
****4.4.4 路由映射设置名称****
```
    #匹配以home/开头的视图,并把别名设为h1
    url(r'^home',views.home,name='h1'),
    
    #匹配以index/开头,后接数字的视图,并把别名设置为h2
    url(r'^index/(\d*)',views.index,name='h2'),
```
****4.4.5 路由分发****

如果映射URL太多,都写在一个`URLpatterns`显得繁琐,可以使用路由分发功能

那就是在每个应用里面单独建立urls,即路由分发器.每个应用的视图都分别到各自的应用中找,避免因为一个应用的崩溃而影响整个项目.

	url(r'^blog/',include('blog.urls')),

需要注意的是:

URL多传一个参数,那`views`函数就必须要多接受一个参数

***4.5 视图层***

对逻辑负责处理用户的请求并返回响应,返回可以是HTML网页,或者重定向,或者404错误,或者一个XML文件,也可以是一个对象

在一个文件中称之为视图`views.py`,放在项目或应用程序目录

HTTP请求中产生两个核心对象

	HTTP请求:HttpRequest
	HTTP响应:HttpResponse对象

****4.5.1 HttpResponst对象****
```
    #从django.http模块中导入HttpResponse
    from django.http import HttpResponse
    
    #导入datetime模块
    import datetime
    
    def current_datetime(request):
        now=datetime.datetime.now()#获取系统当前时间
        html="<html><body>现在时刻：%s.</body></html>" %now
        return HttpResponse(html)
```
在这个(`views.py`)视图中每一个函数称作视图函数，视图函数都以一个`HttpRequest`对象为第一个参数，该参数通常命名为`request`

在上面的代码中，得到的第一个参数是一个`HttpRequest`对象,通过`request.*`的方式
```
    path                        #使用GET方法时,只会得到路径
    get_full_path()             #使用GET方法时,会得到包括路径和?,=等信息的全路径
    method                      #得到客户端请求网页的HTTP方法，POST或者GET
    GET                         #包含所有的HTTP的GET方法的类字典对象
    POST                        #包含所有的HTTP的POST方法的类字典对象
    COOKIES                     #包含cookies的字典对象，其键和值都是字符串
    FILES                       #通过表单上传的文件的类字典对象,其每个key都是input标签中name属性的值,其每一个value的值是一个标准的python字典对象
        filename                #表示上传文件的文件名
        content-type            #表示上传文件的内容原型
        content                 #表示上传文件的原始内容
    META                        #一个包含所有有效的HTTP头信息的字典
        content_length          #所接收的数据的长度
        content_type            #所接收的数据的类型
        query_string            #接收的原始请求字符串		
        remote_addr             #客户端的IP地址
        remote_host             #客户端的主机名称
        server_name             #服务端的主机名
        server_port             #服务端的端口号
        http_accept_encoding		
        http_accept_language
        http_host               #客户端发送的HOST头信息
        http_referer            #被指向的页面
        http_user_agent         #客户端使用的浏览器的信息
        http_x_bender           #X_bender头信息
    session                     #唯一可读写的类字典对象，表示与服务端的当前会话信息
    body                        #POST原始数据，用于对数据的复杂处理
    has_key()                   #布尔值，标识request.GET或request.POST是否包含指定的键
    is_secure()                 #客户端发出的请求是否安全
    is_ajax()
    user                        #是一个django.contrib.auth.models.User对象,代表当前登陆的用户,如果当前访问用户没有登陆,其值将被初始化为django.contrib.auth.models.
    
    AnonymousUser的实例,只有激活Django中的AuthenticationMideleware时,该属性才可用
```
****4.5.2 HttpRequest对象****

`HttpRequest`对象由Django自动创建

`HttpResponse`由开发人员创建，每个view请求处理方法必须返回一个`HttpResponse`对象

在`HttpResponse`对象上扩展的常用方法

****4.5.2.1 render()****

格式:

	render(request,template_name,context=None,content_type=None,status=None,using=None)

参数说明:
```
	template_name为模板的名字，是必要的参数
	可选的参数：
	context             开发人员可以添加一个字典信息到模板中，用来提示用户，默认是一个空字典
	content_type        MIME类型用于生成文档
	status              为响应状态代码，默认值为200
	using	
```
也可以使用`render_to_response`("网页文件")

结合给定的模板与一个给定的上下文，返回一个字典`HttpResponse`的渲染文本对象

例子：
```
    from django.shortcuts import render
    
    def index(request):
    
        return render(request,'index.html',{'msg':'hello world'})
```
****4.5.2.2 rdirect("路径")****

格式:

	redirect(to,args,kwargs)

重定向方法，可以在符合某个条件的时候跳转到另一个页面，

例子:
```
    from django.shortcuts import render, HttpResponse,redirect
    
    def register(request_info):
    
        if request_info.method == 'POST':
            user = request_info.POST.get('user')
            pwd = request_info.POST.get('pwd')
            if user == 'hello' and pwd == 'world':
                return redirect('/login/')
            return HttpResponse('账号或密码错误')
        return render(request_info,'register.html')
    
    
    def login(request_info):
        return render(request_info,'login.html')
```
****4.5.2.3 locals()把视图函数中所有的变量传给模板****

例子:
```
    def register(request):
    
        a1="aaa"
        a2="bbb"
        a3="ccc"
        a4="ddd"
    
        return render(request,"index.html",locals())#一次性把a1,a2,a3,a4四个变量传给模板
```