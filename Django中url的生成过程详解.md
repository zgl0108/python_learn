在前面我们知道,Django启动之前会执行`admin.py`中的`autodiscover()`方法.

    def autodiscover():
        autodiscover_modules('admin', register_to=site)

在这个方法里,既然`autodiscover_modules`能执行`admin.py`文件,那当然也可以执行别的py文件.

如果想让`autodiscover_modules`执行自定义的py文件,该怎么做呢?

在app01的apps.py文件的App01Config类中,定义ready方法

然后导入`autodiscover_modules`模块,让`autodiscover_modules`来执行自定义的py文件

        from django.apps import AppConfig
        
        class App01Config(AppConfig):
            name = 'app01'
        
            def ready(self):
                from django.utils.module_loading import autodiscover_modules
                
                autodiscover_modules("aaaa")

这样,程序在启动的时候就会在项目所有的目录下查找并调用`autodiscover_modules`方法来执行aaaa.py文件

在app01目录下创建aaaa.py文件,在aaaa.py文件中打印"hello world!"

可以看到在项目启动之前就会在后台打印"hello world!"了.

![](http://images2017.cnblogs.com/blog/1133627/201710/1133627-20171027224553211-1480014887.png)

项目运行到这里,下一步就是要生成URL了,这里又是怎么实现的呢???

新建一个text_url项目,包含appo1的应用,在项目的urls.py中配置url

    urlpatterns = [
        url(r'^index/$',views.index),
    ]

在app01的views.py中定义相应的视图函数index

        from django.shortcuts import render,HttpResponse
        
        def index(request):
            
            return HttpResponse("ok")

以默认端口启动项目,打开浏览器输入地址`http://127.0.0.1:8000/index/`

![](http://images2017.cnblogs.com/blog/1133627/201710/1133627-20171027224605305-1239516891.png)

我们既然可以在views.py生定义视图函数,当然也可以直接在urls.py中定义视图函数index

        from django.shortcuts import render,HttpResponse
        
        def index(request):
        
            return HttpResponse("aaaaaa")
    
        urlpatterns = [
            url(r'^admin/', admin.site.urls),
            url(r'^index/$',index),
        ]
 
重启项目,刷新浏览器,可以看到

![](http://images2017.cnblogs.com/blog/1133627/201710/1133627-20171027224615164-2018810680.png)

这样也完成同样的路由匹配.

除了上面的两种路由定义方法,我们还可以使用`include`方法来实现路由转发功能.

        from django.conf.urls import url,include
        
        urlpatterns = [
            url(r'^index/$',index),
            url(r'^app01/',include("url_test1"))
        ]
        
在`include`方法中,其参数表面是一个字符串,其实际是一个文件路径.
        
按照上面定义的方式,在app01这个应用目录下创建url_test1文件   
   
url_test1文件内容如下

        from django.conf.urls import url,include
        
        urlpatterns = [
            url(r'^index/$',index),
        ]   
        
为什么使用`include`方法也可以生成url,使用路由转发的功能呢?

打开`include`方法,可以看到

        def include(arg, namespace=None, app_name=None):
            ...         # 此处省略
        
            if isinstance(urlconf_module, six.string_types):
                urlconf_module = import_module(urlconf_module)
            patterns = getattr(urlconf_module, 'urlpatterns', urlconf_module)
            app_name = getattr(urlconf_module, 'app_name', app_name)
            if namespace and not app_name:
                warnings.warn(
                    'Specifying a namespace in django.conf.urls.include() without '
                    'providing an app_name is deprecated. Set the app_name attribute '
                    'in the included module, or pass a 2-tuple containing the list of '
                    'patterns and app_name instead.',
                    RemovedInDjango20Warning, stacklevel=2
                )
        
            namespace = namespace or app_name
                ...     # 此处省略
            
                return (urlconf_module, app_name, namespace)
        
`include方法执行完成以后,返回的数据是一个元组类型.
        
既然`include`方法返回的数据类型是元组类型,那么在app01应用目录下的url_test1.py中,也可以直接以元组的方式取代include方法.

        from django.conf.urls import url
        from django.shortcuts import HttpResponse
        
        def index(request):
        
            return HttpResponse("bbbbbb")
        
        urlpatterns = [
            # url(r'^admin/', admin.site.urls),
            url(r'^index/$',index),
        ]

重启项目,浏览器地址更改为`http://127.0.0.1:8000/app01/index/`

![](http://images2017.cnblogs.com/blog/1133627/201710/1133627-20171027224633820-1047278545.png)

在`include`方法中,返回的元组有三个元素,第一个元素是`urlconf_module`

在`include`方法中,有一个判断方法
        
    if isinstance(urlconf_module, six.string_types):
        urlconf_module = import_module(urlconf_module)
    patterns = getattr(urlconf_module, 'urlpatterns', urlconf_module)
    app_name = getattr(urlconf_module, 'app_name', app_name)
        
由此可以知道如果`urlconf_module`是字符串类型,就以字符串方式导入了`urlconf_module`模块.

导入模块后,从模块中获取`urlpatterns`,如果没有`urlpatterns`就使用默认值`urlconf_module`

所以`include`方法返回的数据第一个元素就是urls.py中`include`方法的参数.
 
而使用`include`方法进行路由分发时,被分发的路由中也会有`urlpatterns`

所以进行路由分发时,urls.py文件也可以写成下面的样子

    urlpatterns = [
        url(r'^app01/',(url_test1,"test1","test2")),
    ]

在app01目录的url_test1文件内容如下

        from django.conf.urls import url
        from django.shortcuts import HttpResponse
        
        def index(request):
        
            return HttpResponse("cccccc")
        
        urlpatterns = [
            url(r'^index/$',index),
        ]
 
重启项目,刷新浏览器

![](http://images2017.cnblogs.com/blog/1133627/201710/1133627-20171027224644617-67388451.png)

在这里url_test1做为元组的一个元素,其可以是模块名,也可以是列表
 
可以用url_test1文件中的urlpatterns替换urls.py文件中的url_test1,这样一来项目的urls.py内容就跟下面的代码一样了

        from django.conf.urls import url,include
        from django.contrib import admin
        from app01 import views
        from app01 import url_test1
        from django.shortcuts import render,HttpResponse
        
        def index(request):
            return HttpResponse("aaaaaa")
        
        urlpatterns = [
            # url(r'^admin/', admin.site.urls),
            # url(r'^index/$',index),
            # url(r'^app01/',include("app01.url_test1")),
            url(r'^app01/',([
        
                        url(r'index/',index),
        
                            ],"test1","test2")),
        ]

重启项目,刷新浏览器,可以看到

![](http://images2017.cnblogs.com/blog/1133627/201710/1133627-20171027224655226-499347207.png)

可以看到,项目已经可以成功运行起来了

按照上面的步骤,一个项目的url可以再次进行分发

        urlpatterns = [
            url(r'^app01/',([
        
                        url(r'index1/',([
                                url(r'index2/',index),
                        ],"test3","test4")),
        
                            ],"test1","test2")),
        ]

重启项目,浏览器打开`http://127.0.0.1:8000/app01/index1/index2/index`

![](http://images2017.cnblogs.com/blog/1133627/201710/1133627-20171027224705164-985282292.png)

现在有了index视图函数,当然也可以有其他的视图函数

        urlpatterns = [
            url(r'^app01/',([
        
                        url(r'index1/',([
                                url(r'index2/',index),
                                url(r'index2/add',index),
                                url(r'index2/(\d+)/delete',index),
                                url(r'index2/(\d+)/change',index),
                        ],"test3","test4")),
        
                            ],"test1","test2")),
        ]

这就是在Django后台进行数据表管理时使用的增删查改的urlr的生成方式

    /userinfo/
    /userinfo/add
    /userinfo/(\d+)/delete
    /userinfo/(\d+)/change

再把上面urlpatterns中的url改变一下

        urlpatterns = [
            url(r'^admin/',([
        
                        url(r'app01/',([
                                url(r'userinfo/',index),
                                url(r'userinfo/add',index),
                                url(r'userinfo/(\d+)/delete',index),
                                url(r'userinfo/(\d+)/change',index),
                        ],"test3","test4")),
        
                            ],"test1","test2")),
        ]

把上面的url组合在一起,,就变成完完全全的Django后台进行数据表管理时使用的增删查改的url了.