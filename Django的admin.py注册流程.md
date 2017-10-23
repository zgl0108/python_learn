通常创建一个Django项目的时候,在Django的配置文件settings.py中,都会有下面的这段配置:

    INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'app01.apps.App01Config',
    ]

这段配置文件是Django用来注册Django创建的应用的.

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
这个ready是程序在执行路由映射之前执行这个方法.那这个函数有什么用呢??

在admin.py文件中,可以注册数据库中数据表,这样方便在Django的后台管理所注册的数据库.

实际上,把想在Django后台管理的数据表写在admin.py文件中以后,Django会执行一个autodiscover_modules方法.
        
    def autodiscover():
        autodiscover_modules('admin', register_to=site)
            
Django执行autodiscover_modules后,admin.py文件也就会选择了.

只有admin.py文件执行过后,Django的路由中生成在Django的后台中对已注册的数据表进行增删查改的路由关系映射.

admin执行后,又会执行site函数.

site又会执行什么样的操作呢??进入site函数,在sites.py文件的最后一行,可以看到:

    site = AdminSite()

site是AdminSite这个类的一个实例对象,这样一来,执行site方法就相当于执行了AdminSite这个类中的__init__方法.

    def __init__(self, name='admin'):
        self._registry = {}
        self.name = name
        self._actions = {'delete_selected': actions.delete_selected}
        self._global_actions = self._actions.copy()
        all_sites.add(self)

在这里,AdminSite先定义了一个空的字典.然后会执行其register方法.

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

register方法的前两个参数都是一个类名.

可以看到register方法的最后会把其参数定义的类加入到__init__方法中_registry方法定义的那个空字典中.

同时对参数中的类进行实例化.类进行实例化的参数为这个类本身以及site本身.类似下面的情形,

        {
            models.UserInfo: UserInfoAdmin(models.UserInfo,site对象),
            models.UserGroup: ModelAdmin(models.UserGroup,site对象),
        }

同时,由于对AdminSite进行实例化的时候使用了单例模式,所以程序第一次执行完后,系统中会一直存在这个site对象.

这样一来,admin.py程序后,就相当于是把在admin.py中注册的类以及对应的配置文件实例化之后的对象全部封闭到AdminSite的register方法中了.

admin.py执行完成后,Django才开始执行urls.py中配置的路由关系映射.

    urlpatterns = [
        url(r'^admin/', admin.site.urls),
        url(r'^index/', index),
    ]

如上所示,在路由关系映射中,Django也会再执行一次admin.site.urls的方法.

进入urls方法中,可以看到

    @property
    def urls(self):
        return self.get_urls(), 'admin', self.name

urls方法是执行了一个get_urls方法.再次进入get_urls方法

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

在get_urls方法中,循环_registry这个字典,为字典中的每个类生成Django后台使用的增删查改等操作的url.

    urlpatterns += [
        url(r'^%s/%s/' % (model._meta.app_label, model._meta.model_name), include(model_admin.urls)),
    ]
            
在这里,

    * model._meta.app_label表示的是Django中添加的应用名
    * model._meta.model_name表示Django的数据库中的表名

把这两个字符串以"/"进行拼接后生成新的字符串

urlpatterns与这个字符串进行拼接,生成了新的urlpatterns.

在这一行的后边,model_admin又会调用这个对象中的url函数间接执行get_url方法来生成路由关系映射的后半部分.

这个生成的后半部分路由再与前面的新urlpatterns进行拼接,依次循环就生成在Django后台进行数据表操作的路由关系映射.

这就是在admin.py中注册数据表后Django的执行流程.








