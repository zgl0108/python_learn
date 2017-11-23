`Django REST framework`是一个基于`Django`的框架,`REST framework`又是怎么`反向生成url`的呢??

在前面的例子中,知道在`REST framework`中有6种版本控制的方式,进入任意一种版本控制的源码中,

	class QueryParameterVersioning(BaseVersioning):
		"""
		GET /something/?version=0.1 HTTP/1.1
		Host: example.com
		Accept: application/json
		"""
		invalid_version_message = _('Invalid version in query parameter.')

		def determine_version(self, request, *args, **kwargs):
			version = request.query_params.get(self.version_param, self.default_version)
			if not self.is_allowed_version(version):
				raise exceptions.NotFound(self.invalid_version_message)
			return version

		def reverse(self, viewname, args=None, kwargs=None, request=None, format=None, **extra):
			url = super(QueryParameterVersioning, self).reverse(
				viewname, args, kwargs, request, format, **extra
			)
			if request.version is not None:
				return replace_query_param(url, self.version_param, request.version)
			return url

可以看到每一个版本控制的类中也都有`reverse`方法,由此可以了`REST framework`也是使用`reverse`的方式来反向生成url

新建一个Django项目,在项目的app中导入`rest-framework`

在`settings.py`文件中做如下配置

	INSTALLED_APPS = [
		'django.contrib.admin',
		'django.contrib.auth',
		'django.contrib.contenttypes',
		'django.contrib.sessions',
		'django.contrib.messages',
		'django.contrib.staticfiles',
		'app01.apps.App01Config',
		'rest_framework',
	]

	REST_FRAMEWORK = {
		'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.URLPathVersioning',
		'VERSION_PARAM': "version",
		'DEFAULT_VERSION': 'V1',
		'ALLOWED_VERSIONS': ['v1', 'v2']
	}

在urls.py文件中添加路由信息

	from django.conf.urls import url
	from django.contrib import admin
	from app01 import views

	urlpatterns = [
		url(r'^admin/', admin.site.urls),
		url(r'^(?P<version>\w+)/users/$',views.UsersView.as_view(),name="test1"),
	]
	
在`views.py`文件中定义`UserView`的类

    from django.shortcuts import render,HttpResponse
    from rest_framework.views import APIView
    from rest_framework.versioning import URLPathVersioning
    
    class UsersView(APIView):
    
        def get(self,request,*args,**kwargs):
    		
    		# 打印版本信息
            print("request.version:",request.version)
    		
    		# reverse方法有一个viewname参数,在这里定义为urls.py中定义的name
            print(request.versioning_scheme.reverse("test1",request=request))
    
            return HttpResponse("aaaa")	
	
此时,在浏览器中输入`http://127.0.0.1:8000/v1/users/`,在服务端后台打印信息如下

	request.version: v1
	http://127.0.0.1:8000/v1/users/

再把浏览器中的url更换为`http://127.0.0.1:8000/v2/users/`,服务端后台的打印信息又变成了

	request.version: v2
	http://127.0.0.1:8000/v2/users/
	
可以看到打印出了正确的版本,并且反向生成url也已经成功了