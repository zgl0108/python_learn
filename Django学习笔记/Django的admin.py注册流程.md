通常创建一个Django项目的时候,在Django的配置文件`settings.py`中,都会有下面的这段配置:

    INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'app01.apps.App01Config',
    ]

这段配置文件是Django用来注册所创建的应用的.

例如这里在创建Django项目时,添加了一个名为"app01"的应用.

在所创建的项目中,存在着一个名为"apps.py"的文件,这个文件的内容如下:

        from django.apps import AppConfig
        
        class App01Config(AppConfig):
            name = 'app01'

在这个文件中,以所注册的应用名加"Config"定义的类中,其实还有一个方法:

        from django.apps import AppConfig
        
        class App01Config(AppConfig):
            name = 'app01'
            
            def ready(self):
                pass
这个`ready是程序在执行路由映射之前执行这个方法`.那这个函数有什么用呢??

在`admin.py`文件中,可以注册数据库中数据表,这样方便在Django的后台管理所注册的数据库.

    admin.site.register(models.UserInfo)

把models.py中的类注册在这里后,就会生成在后台进行管理这个数据表的四个URL.

    /admin/app01/userinfo/
    /admin/app01/userinfo/add/
    /admin/app01/userinfo/1/change/
    /admin/app01/userinfo/2/delete/

实际上,把想在Django后台管理的数据表写在`admin.py`文件中以后,Django会执行一个`autodiscover_modules`方法.
        
    def autodiscover():
        autodiscover_modules('admin', register_to=site)
            
Django执行`autodiscover_modules`后,`admin.py`文件也就会执行了.

只有`admin.py`文件执行过后,Django的路由中生成在Django的后台中对已注册的数据表进行增删查改的路由关系映射.

admin执行后,又会执行`site`函数.

`site`又会执行什么样的操作呢??进入`site`函数,在`sites.py`文件的最后一行,可以看到:

    site = AdminSite()

site是`AdminSite`这个类的一个单例模式.这样一来,执行site方法就相当于执行了`AdminSite`这个类中的`__init__`方法.

    def __init__(self, name='admin'):
        self._registry = {}
        self.name = name
        self._actions = {'delete_selected': actions.delete_selected}
        self._global_actions = self._actions.copy()
        all_sites.add(self)

执行`admin.site`方法就相当于实例化一个`AdminSite`对象,然后这个对象会调用`AdminSite`这个类中的`register`方法.

        def register(self, model_or_iterable, admin_class=None, **options):
        
            if not admin_class:
                admin_class = ModelAdmin
        
            if isinstance(model_or_iterable, ModelBase):
                model_or_iterable = [model_or_iterable]
            for model in model_or_iterable:
                if model._meta.abstract:
                    raise ImproperlyConfigured(
                        'The model %s is abstract, so it cannot be registered with admin.' % model.__name__
                    )
        
                if model in self._registry:
                    raise AlreadyRegistered('The model %s is already registered' % model.__name__)
        
                if not model._meta.swapped:
           
                    if options:
             
                        options['__module__'] = __name__
                        admin_class = type("%sAdmin" % model.__name__, (admin_class,), options)
        
                    self._registry[model] = admin_class(model, self)

`register`方法的前两个参数都是一个类名.

可以看到`register`方法的最后会把其参数定义的类加入到`__init__`方法中`_registry`方法定义的那个空字典中.

同时对参数中的类进行实例化.

类进行实例化的参数为这个类本身以及site本身.类似下面的情形,

        {
            models.UserInfo: UserInfoAdmin(models.UserInfo,site对象),
            models.UserGroup: ModelAdmin(models.UserGroup,site对象),
        }

同时,由于对`AdminSite`进行实例化的时候使用了单例模式,所以程序第一次执行完后,系统中会一直存在这个site对象.

这样一来,`admin.py`程序后,就相当于是把在`admin.py`中注册的类以及对应的配置文件实例化之后的对象全部封装到`AdminSite`的`register`方法中了.

`admin.py`执行完成后,Django才开始执行`urls.py`中配置的路由关系映射.

    urlpatterns = [
        url(r'^admin/', admin.site.urls),
        url(r'^index/', index),
    ]

如上所示,在路由关系映射中,Django也会再执行一次`admin.site.urls`的方法.

进入urls方法中,可以看到

    @property
    def urls(self):
        return self.get_urls(), 'admin', self.name

urls方法是执行了一个`get_urls`方法.再次进入`get_urls`方法

        def get_urls(self):
            from django.conf.urls import url, include
            
            ...
        
            valid_app_labels = []
            for model, model_admin in self._registry.items():
                urlpatterns += [
                    url(r'^%s/%s/' % (model._meta.app_label, model._meta.model_name), include(model_admin.urls)),
                ]
                if model._meta.app_label not in valid_app_labels:
                    valid_app_labels.append(model._meta.app_label)
            ...
            
            return urlpatterns

在`get_urls`方法中,循环`_registry`这个字典,为字典中的每个类生成Django后台使用的增删查改等操作的`url`.

    urlpatterns += [
        url(r'^%s/%s/' % (model._meta.app_label, model._meta.model_name), include(model_admin.urls)),
    ]
            
在这里,

    * model._meta.app_label     表示的是Django中添加的应用名
    * model._meta.model_name    表示Django的数据库中的表名

把这两个字符串以`"/"`进行拼接后生成新的字符串

`urlpatterns`与这个字符串进行拼接,生成了新的`urlpatterns`.

在这一行的后边,`model_admin`又会调用这个对象中的url函数间接执行`get_url`方法来生成路由关系映射的后半部分.

这个生成的后半部分路由再与前面的新`urlpatterns`进行拼接,依次循环就生成在Django后台进行数据表操作的路由关系映射.

综上所述,在`admin.py`中注册`models.py`中的类的流程

    1. 先执行admin.py,使用单例模式创建一个admin.site的对象
    2. 在admin.site对象中,把admin.py中定义的类全部注册,并把类中所有的配置全部传递到admin.site对象的_registry生成的字典中
    3. 在生成url时,url会循环site中的类,为每一个类生成相应的url

这就是在`admin.py`中注册数据表后Django的执行流程.