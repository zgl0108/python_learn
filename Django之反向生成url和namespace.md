首先新建一个项目test_url,项目包含一个名为app01的应用

在`urls.py`文件中生成如下内容

        from django.conf.urls import url
        from django.shortcuts import HttpResponse
        
        def index(request):
        
            return HttpResponse("index")
        
        def test(request):
        
            return HttpResponse("test")
        
        urlpatterns = [
            url(r'^index',index),
            url(r'^test',test),
        ]

启动项目,用浏览器打开`http://127.0.0.1:8000/test`和`http://127.0.0.1:8000/index/`

页面如下

![](http://images2017.cnblogs.com/blog/1133627/201711/1133627-20171101082746888-1558009882.png)

![](http://images2017.cnblogs.com/blog/1133627/201711/1133627-20171101082754029-1267280829.png)

上面的例子是正向生成url,既然Django可以正向生成url,当然也可以反向生成url

## 无参数反向生成url

修改`urls.py`文件

        from django.conf.urls import url
        from django.shortcuts import HttpResponse,redirect
        
        def index(request):
        
            from django.urls import reverse         # 导入reverse
        
            reverse_url=reverse("test_url")         # 用reverse把别名为test_url的路由反向生成url	
            print("reverse_url:",reverse_url)       # 打印反向生成的url
        
            return redirect(reverse_url)            # 重定向到反向生成的url
        
        def test(request):
        
            return HttpResponse("test")
        
        urlpatterns = [
            url(r'^index',index),
            url(r'^test1/test2/test3/test',test,name="test_url"),   # 为test路由设置一个test_url别名
        ]

用浏览器打开`http://127.0.0.1:8000/index`,然后回车

![](http://images2017.cnblogs.com/blog/1133627/201711/1133627-20171101082805998-1519643709.png)

而服务端打印的反向生成的utl如下

![](http://images2017.cnblogs.com/blog/1133627/201711/1133627-20171101082815638-1406102649.png)

可以看到,浏览器的地址栏里显示的url跟我们输入的地址不一样,而是跟Django的路由表中设置了路由别名的url是一样的.

从上面的例子可以看出,反向生成url已经成功了.

## 有参数的反向生成url

**使用正则表达式通过args传入参数反向生成url**

修改`urls.py`文件

        from django.conf.urls import url
        from django.shortcuts import HttpResponse,redirect
        
        def index(request):
        
            from django.urls import reverse
        
            reverse_url=reverse("test_url",args=(2,8))
            print("reverse_url:",reverse_url)
        
            return redirect(reverse_url)
        
        def test(request,*args,**kwargs):
        
            return HttpResponse("test")
        
        urlpatterns = [
            url(r'^index',index),
            url(r'^test1/(\d+)/test2/test3/(\d+)/test',test,name="test_url"),
        ]

浏览器打开`http://127.0.0.1:8000/index`这个地址

浏览器的地址变成了

![](http://images2017.cnblogs.com/blog/1133627/201711/1133627-20171101082824420-1840969984.png)

而在服务端后台打印反向生成的url为

![](http://images2017.cnblogs.com/blog/1133627/201711/1133627-20171101082832435-1401647618.png)

**使用正则表达式通过kwargs传入参数反向生成url**

修改`urls.py`文件

        from django.conf.urls import url
        from django.shortcuts import HttpResponse,redirect
        
        def index(request):
        
            from django.urls import reverse
        
            reverse_url=reverse("test_url",kwargs={"a1":23,"a2":37})
            print("reverse_url:",reverse_url)
        
            return redirect(reverse_url)
        
        def test(request,*args,**kwargs):
        
            return HttpResponse("test")
        
        urlpatterns = [
            url(r'^index',index),
            url(r'^test1/(?P<a1>\d+)/test2/test3/(?P<a2>\d+)/test',test,name="test_url"),
        ]
	
浏览器打开`http://127.0.0.1:8000/index`这个地址

![](http://images2017.cnblogs.com/blog/1133627/201711/1133627-20171101082851201-1362242213.png)

后台打印反向生成的url

![](http://images2017.cnblogs.com/blog/1133627/201711/1133627-20171101082859607-1240811013.png)

## 反向生成url之namespace

在上面的例子里,反向生成url使用的是一个视图函数和一个url别名

再来看反向生成url时,`namespace`的用法

修改`urls.py`文件

        from django.conf.urls import url
        from django.shortcuts import HttpResponse,redirect
        
        def index(request):
        
            return HttpResponse("index")
        
        def test(request,*args,**kwargs):
        
            return HttpResponse("test")
        
        urlpatterns = [
            url(r'^app01/',([
                url(r'^index/', index, name="index1"),
                url(r'^test/', test, name="test1"),
            ],"url1","url1")),
        ]

浏览器打开`http://127.0.0.1:8000/app01/index`这个地址

![](http://images2017.cnblogs.com/blog/1133627/201711/1133627-20171101082909982-546682270.png)

再来反向生成url

		from django.conf.urls import url
		from django.shortcuts import HttpResponse, redirect

		def index(request):
			from django.urls import reverse

			reverse_url=reverse("test1")
			print("reverse_url:",reverse_url)

			return HttpResponse("index")

		def test(request, *args, **kwargs):
			return HttpResponse("test")

		urlpatterns = [
			url(r'^app01/', ([
								url(r'^index/', index, name="index1"),
								url(r'^test/', test, name="test1"),
							], "url1", "url1")),
		]

浏览器打开`http://127.0.0.1:8000/app01/index`这个地址

![](http://images2017.cnblogs.com/blog/1133627/201711/1133627-20171101082921170-1512953665.png)

Django的报错信息提示:test1不是一个有效的视图函数或模式的名称

修改`urls.py`文件

        from django.conf.urls import url
        from django.shortcuts import HttpResponse, redirect
        
        
        def index(request):
            from django.urls import reverse
        
            reverse_url=reverse("test1")
            print("reverse_url:",reverse_url)
        
            return HttpResponse("index")
        
        def test(request, *args, **kwargs):
            return HttpResponse("test")
        
        urlpatterns = [
            url(r'^app01/', ([
                                url(r'^index/', index, name="index1"),
                                url(r'^test/', test, name="test1"),
                            ], None, None)),
        ]

浏览器再次打开`http://127.0.0.1:8000/app01/index`这个地址

![](http://images2017.cnblogs.com/blog/1133627/201711/1133627-20171101082931498-308278353.png)

如果url中出现了`namespace`,必须在`reverse`方法中加入`namespace`

把`urls.py`修改,在`reverse`中加入`namespace`

        from django.conf.urls import url
        from django.shortcuts import HttpResponse, redirect
        
        def index(request):
            from django.urls import reverse
        
            reverse_url=reverse("url1:test1")
            print("reverse_url:",reverse_url)
        
            return HttpResponse("index")
        
        def test(request, *args, **kwargs):
            return HttpResponse("test")
        
        urlpatterns = [
            url(r'^app01/', ([
                                url(r'^index/', index, name="index1"),
                                url(r'^test/', test, name="test1"),
                            ], "url1", "url1")),
        ]

浏览器再次打开`http://127.0.0.1:8000/app01/index`这个地址

![](http://images2017.cnblogs.com/blog/1133627/201711/1133627-20171101082940670-470846833.png)

在后台打印加入`namespace`的反向生成的url

![](http://images2017.cnblogs.com/blog/1133627/201711/1133627-20171101082950576-1676200716.png)

通过博客[Django中url的生成过程详解](http://www.cnblogs.com/renpingsheng/p/7745544.html)
知道一个项目的url是可以嵌套多层的,那么多层嵌套url的`namespace`应该怎么设定呢??

修改`urls.py`文件的`urlpatterns`如下

		urlpatterns=[
			url(r'^app01/',([
				url(r'^userinfo/',([
					url(r'^index/',index,name="index1"),
					url(r'^test/',test,name="test1"),
				],None,None))
			],"url1","url1"))
		]

这个url嵌套了3层,最里面一层的url设定了别名,最里面一层的url向外找,应该用谁的`namespace`呢??

最里面一层的url向外找,中间一层的url的`namespace`为None,即没有设定`namespace`,应该继续向最外面一层寻找`namespace`

修改`urls.py`文件,在`reverse`方法中添加`namespace`

        from django.conf.urls import url
        from django.shortcuts import HttpResponse, redirect
        
        def index(request):
            from django.urls import reverse
        
            reverse_url=reverse("url1:test1")
            print("reverse_url:",reverse_url)
        
            return HttpResponse("index")
        
        def test(request, *args, **kwargs):
            return HttpResponse("test")
        
        urlpatterns=[
            url(r'^app01/',([
                url(r'^userinfo/',([
                    url(r'^index/',index,name="index1"),
                    url(r'^test/',test,name="test1"),
                ],"url2","url2"))
            ],"url1","url1"))
        ]

浏览器打开`http://127.0.0.1:8000/app01/userinfo/index/`地址

![](http://images2017.cnblogs.com/blog/1133627/201711/1133627-20171101083004373-765773855.png)

![](http://images2017.cnblogs.com/blog/1133627/201711/1133627-20171101083011841-1503281307.png)

如果中间一层也有`namespace`,这时就有两个`namespace`,此时应该用哪个`namespace`呢??

        from django.conf.urls import url
        from django.shortcuts import HttpResponse, redirect
        
        def index(request):
            from django.urls import reverse
        
            reverse_url=reverse("url2:test1")
            print("reverse_url:",reverse_url)
        
            return HttpResponse("index")
        
        def test(request, *args, **kwargs):
            return HttpResponse("test")
        
        urlpatterns=[
            url(r'^app01/',([
                url(r'^userinfo/',([
                    url(r'^index/',index,name="index1"),
                    url(r'^test/',test,name="test1"),
                ],"url2","url2"))
            ],"url1","url1"))
        ]
		
只添加url2这个namespace,刷新浏览器页面

![](http://images2017.cnblogs.com/blog/1133627/201711/1133627-20171101083024451-983440883.png)

在上面的例子基础上添加url1这个`namespace`

        from django.conf.urls import url
        from django.shortcuts import HttpResponse, redirect
        
        def index(request):
            from django.urls import reverse
        
            reverse_url=reverse("url1:url2:test1")
            print("reverse_url:",reverse_url)
        
            return HttpResponse("index")
        
        def test(request, *args, **kwargs):
            return HttpResponse("test")
        
        urlpatterns=[
            url(r'^app01/',([
                url(r'^userinfo/',([
                    url(r'^index/',index,name="index1"),
                    url(r'^test/',test,name="test1"),
                ],"url2","url2"))
            ],"url1","url1"))
        ]
		
再次刷新浏览器

![](http://images2017.cnblogs.com/blog/1133627/201711/1133627-20171101083034123-576785819.png)

所以,如果url使用了多层嵌套,且每一层嵌套都有各自的`namespace`,在使用`reverse`进行反向生成url的时候

必须要把所有的`namespace`从最外层向里层使用`":"`连接起来.

`namespace(名称空间)`的作用是什么呢??

* 当一个项目中有多个应用,每个应用的url都嵌套了多层且里层的url和name别名相同的时候,这时就可以根据namespace来区分不同应用的相同url.