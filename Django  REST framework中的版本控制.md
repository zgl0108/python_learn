## 1.REST framework版本控制的流程分析

### 1.1 determine_version方法的执行流程

首先,请求到达`REST framework`的CBV,执行CBV中的`dispatch`方法再次封装完成request后,执行`initial`方法.

在`REST framework`中的版本控制就是在`initial`函数中调用`determine_version`方法完成的

来看看源码

`initial`方法的源码:

    def initial(self, request, *args, **kwargs):
        """
        Runs anything that needs to occur prior to calling the method handler.
        """
        self.format_kwarg = self.get_format_suffix(**kwargs)

        # Perform content negotiation and store the accepted info on the request
        neg = self.perform_content_negotiation(request)
        request.accepted_renderer, request.accepted_media_type = neg

        # Determine the API version, if versioning is in use.
        version, scheme = self.determine_version(request, *args, **kwargs)
        request.version, request.versioning_scheme = version, scheme

        # Ensure that the incoming request is permitted
        self.perform_authentication(request)
        self.check_permissions(request)
        self.check_throttles(request)

`determine_version`方法的源码
        
    def determine_version(self, request, *args, **kwargs):

        if self.versioning_class is None:    # 如果versioning_class为空则返回一个None的元组
            return (None, None)	
        scheme = self.versioning_class()
        return (scheme.determine_version(request, *args, **kwargs), scheme)

`determine_version`方法中的`versioning_class`方法又是从哪里来的呢

### 1.2 versioning_class的由来

在UserView视图函数中没有定义versioning_class,那就要到UserView的父类APIView中去找

在APIView类中定义了versioning_class的信息

	class APIView(View):

		renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
		parser_classes = api_settings.DEFAULT_PARSER_CLASSES
		authentication_classes = api_settings.DEFAULT_AUTHENTICATION_CLASSES
		throttle_classes = api_settings.DEFAULT_THROTTLE_CLASSES
		permission_classes = api_settings.DEFAULT_PERMISSION_CLASSES
		content_negotiation_class = api_settings.DEFAULT_CONTENT_NEGOTIATION_CLASS
		metadata_class = api_settings.DEFAULT_METADATA_CLASS
		versioning_class = api_settings.DEFAULT_VERSIONING_CLASS

在视图函数中打印versioning_class

    None

可以看到默认设置的`versioning_class的值是None`,这说明我们`可以在视图函数中为versioning_class设置一个值`

在`detemine_version`函数的源码中,可以看到versioning_class后面加了一个括号,所以`versioning_class是一个函数或一个类`

    如果versioning_class是一个函数,那么执行versioning_class后会有一个返回值
    如果versioning_class是一个类,那么versioning_class加括号就实例化一个类

从rest_framework中导入versioning模块

    from rest_framework import versioning

然后进入versioning模块,可以看到这个versioning中定义了6个类

这6个类是`BaseVersioning`,`AcceptHeaderVersioning`,`URLPathVersioning`,`NamespaceVersioning`,`HostNameVersioning`,`QueryParameterVersioning`

而且还可以看到`BaseVersioning类`是其余5个类的父类.

并且这其余的5个类,每个类中都有一个`determine_version`方法

在项目的视图函数中导入其中任意一个类,打印`versioning_class`

	from django.shortcuts import render,HttpResponse
	from rest_framework.views import APIView
	from django.views import View
	from rest_framework.versioning import QueryParameterVersioning

	class UsersView(APIView):
		versioning_class=QueryParameterVersioning

		def get(self,request,*args,**kwargs):
			print(self.versioning_class)		#打印versioning_class

			return HttpResponse("aaaa")

打印结果

	<class 'rest_framework.versioning.QueryParameterVersioning'>

所以versioning_class是一个类,并且`versioning_class类中有一个determine_version方法`

### 1.3 REST framework版本控制的流程总结

在`initial`方法中,执行完`determine_version`后的返回值被赋值给version, scheme这两个变量

    def initial(self, request, *args, **kwargs):
	
        self.format_kwarg = self.get_format_suffix(**kwargs)

        neg = self.perform_content_negotiation(request)
        request.accepted_renderer, request.accepted_media_type = neg

        version, scheme = self.determine_version(request, *args, **kwargs)
        request.version, request.versioning_scheme = version, scheme

        self.perform_authentication(request)
        self.check_permissions(request)
        self.check_throttles(request)

这两个变量又把`determine_version`方法的返回值赋值给`request.version`, `request.versioning_scheme`这两个变量

在视图函数中打印这两个变量

	from django.shortcuts import render,HttpResponse
	from rest_framework.views import APIView
	from rest_framework.versioning import QueryParameterVersioning

	class UsersView(APIView):
		versioning_class=QueryParameterVersioning

		def get(self,request,*args,**kwargs):
			print(self.versioning_class)
			print("request.version:",request.version)
			print("request.versioning_scheme:",request.versioning_scheme)

			return HttpResponse("aaaa")

打印结果

	<class 'rest_framework.versioning.QueryParameterVersioning'>
	request.version: None
	request.versioning_scheme: <rest_framework.versioning.QueryParameterVersioning object at 0x00000000057722B0>

## 2. REST framework获取版本的方法

在上面的流程分析中,versioning模块中定义了6个类

这6个类是`BaseVersioning`,`AcceptHeaderVersioning`,`URLPathVersioning`,`NamespaceVersioning`,`HostNameVersioning`,`QueryParameterVersioning`

`BaseVersioning类`是其余5个类的父类,`REST framework`获取版本调用的就是这5个类

### 2.1 QueryParameterVersioning:基于url的get传参方式

在settings.py文件的`INSTALLED_APPS`配置项中引入rest-framework
    
    INSTALLED_APPS = [
        ...
        'rest_framework',
    ]

配置路由表

    from django.conf.urls import url
    from django.contrib import admin
    from app01 import views
    
    urlpatterns = [
        url(r'^admin/', admin.site.urls),
        url(r'^users/$',views.UsersView.as_view()),
    ]
    
视图函数配置获取版本方式为`QueryParameterVersioning`
   
    from django.shortcuts import render,HttpResponse
    from rest_framework.views import APIView
    from rest_framework.versioning import QueryParameterVersioning
    
    class UsersView(APIView):
        versioning_class=QueryParameterVersioning
    
        def get(self,request,*args,**kwargs):
            # print("request:",request.__dict__)
            print("request.version:",request.version)       # 打印版本
            # print(request.version.scheme)
            # print(request.versioning_scheme.reverse("test1",request=request))
            # print(request.versioning_scheme.reverse(viewname="test1",request=request))
    
            return HttpResponse("aaaa")    

在浏览器中输入`http://127.0.0.1:8000/users/?version=v1`地址,服务端打印结果

    request.version: v1

再把浏览器中的url地址更换为`http://127.0.0.1:8000/users/?version=v5`,刷新浏览器,服务端打印结果

    request.version: v5

### 2.2 URLPathVersioning:基于url的正则方式

配置url路由信息

    urlpatterns = [
        url(r'^admin/', admin.site.urls),
        url(r'^(?P<version>\w+)/users/$',views.UsersView.as_view()),
    ]

视图函数配置获取版本方式为`URLPathVersioning`

    from django.shortcuts import render,HttpResponse
    from rest_framework.views import APIView
    from rest_framework.versioning import URLPathVersioning
    
    class UsersView(APIView):
        versioning_class=URLPathVersioning
    
        def get(self,request,*args,**kwargs):
    
            print("request.version:",request.version)   # 打印版本
    
            return HttpResponse("aaaa")

在浏览器中输入`http://127.0.0.1:8000/v1/users/`地址,服务端打印结果

    request.version: v1

再把浏览器中的url地址更换为`http://127.0.0.1:8000/v10/users/`,刷新浏览器,服务端打印结果

    request.version: v10

### 2.3 AcceptHeaderVersioning:基于accept请求头方式获取版本信息

在settings.py文件中添加如下配置

	REST_FRAMEWORK = {
		'VERSION_PARAM': "version",     # 版本的参数,在url中可以体现
		'DEFAULT_VERSION': 'V1',        # 默认的版本
		'ALLOWED_VERSIONS': ['v1', 'v2','v3']  # 允许的版本
	}

urls.py设定为

	from django.conf.urls import url
	from django.contrib import admin
	from app01 import views

	urlpatterns = [
		url(r'^admin/', admin.site.urls),
		url(r'^users/$',views.UsersView.as_view()),
	]

视图函数定义

	from django.shortcuts import render,HttpResponse
	from rest_framework.views import APIView
	from rest_framework.versioning import AcceptHeaderVersioning

	class UsersView(APIView):
		versioning_class=AcceptHeaderVersioning

		def get(self,request,*args,**kwargs):

			print("request.version:",request.version)	# 获取版本信息

			return HttpResponse("aaaa")

用浏览器打开`http://127.0.0.1:8000/users/`的url地址

	request.version: V1

    由于在settings.py文件中已经设定了默认的版本是v1,所以在服务端后台获取到的版本是v1

把settings.py中定义的默认版本更改变v2或者v3,再次刷新浏览器,后台打印的版本信息又会跟着改变

	request.version: V2

### 2.4 NamespaceVersioning:基于django路由系统的namespace

urls.py设定为

	from django.conf.urls import url
	from django.contrib import admin
	from app01 import views

	urlpatterns = [
		url(r'^admin/', admin.site.urls),
		url(r'^v1/users/',([url(r'test/',views.UsersView.as_view(),name='test1')],None,'v1')),
		url(r'^v2/users/',([url(r'test/',views.UsersView.as_view(),name='test2')],None,'v2')),
	]

视图函数定义

	from django.shortcuts import render,HttpResponse
	from rest_framework.views import APIView
	from rest_framework.versioning import NamespaceVersioning

	class UsersView(APIView):
		versioning_class=NamespaceVersioning

		def get(self,request,*args,**kwargs):
			print("request.version:",request.version)	# 获取版本信息

			return HttpResponse("aaaa")

用浏览器打开`http://127.0.0.1:8000/v1/users/test/`的url地址

	request.version: V1


把url的地址更换为`http://127.0.0.1:8000/v2/users/test/`,刷新浏览器,后台打印信息如下

	request.version: V2

### 2.5 HostNameVersioning由于要更换电脑的主机名称,所以这里不再进行测试

## 3. versioning_class的全局配置

在视图函数中定义`versioning_class`,只能作用于单个类,

如果想整个项目都使用同一种方法来进行版本控制,就可以在settings.py文件中定义全局的`versioning_class`

在`settings.py`中配置默认的`versioning_class`为`URLPathVersioning`

	REST_FRAMEWORK={
		'DEFAULT_VERSIONING_CLASS':'rest_framework.versioning.URLPathVersioning',
	}

在前面查看到`BaseVersioning`的源码时,可以看到还有几个参数可以在settings.py文件中定义的

	class BaseVersioning(object):
		default_version = api_settings.DEFAULT_VERSION
		allowed_versions = api_settings.ALLOWED_VERSIONS
		version_param = api_settings.VERSION_PARAM

再来看看这几个参数配置项的作用
		
	REST_FRAMEWORK={			# 默认使用URLPathVersioning类来获取版本信息
		'DEFAULT_VERSIONING_CLASS':'rest_framework.versioning.URLPathVersioning',
		'VERSION_PARAM':"version",			# 版本的参数,在url中可以体现
		'DEFAULT_VERSION':'V1',				# 默认的版本
		'ALLOWED_VERSIONS':['v1','v2']		# 允许的版本
	}

修改urls.py文件,使url可以匹配任意长度的字符url

	from django.conf.urls import url
	from django.contrib import admin
	from app01 import views

	urlpatterns = [
		url(r'^admin/', admin.site.urls),
		url(r'^(?P<version>\w+)/users/$',views.UsersView.as_view()),
	]

在浏览器中分别输入`http://127.0.0.1:8000/v1/users/`和`http://127.0.0.1:8000/v2/users/`

都可以获取到正确的响应信息

再在浏览器中输入`http://127.0.0.1:8000/v3/users/`时,浏览器中出现了报错

2

从这里可以知道,在settings.py文件中设定的url中允许的版本只能是v1或v2,在浏览器中输入的版本是v3,所以就会出现错误了