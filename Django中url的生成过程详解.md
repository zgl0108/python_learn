在前面我们知道,Django启动之前会执行admin.py中的autodiscover()方法.

    def autodiscover():
        autodiscover_modules('admin', register_to=site)

在这个方法里,既然autodiscover_modules能执行admin.py文件,那当然也可以执行别的py文件.

如果想让autodiscover_modules执行自定义的py文件,该怎么做呢?

在app01的apps.py文件的App01Config类中,定义ready方法

然后导入autodiscover_modules模块,让autodiscover_modules来执行自定义的py文件

    from django.apps import AppConfig
    
    class App01Config(AppConfig):
        name = 'app01'
    
        def ready(self):
            from django.utils.module_loading import autodiscover_modules
            
            autodiscover_modules("aaaa")

这样,程序在启动的时候就会在项目所有的目录下查找并调用autodiscover_modules方法来执行aaaa.py文件

在app01目录下创建aaaa.py文件,在aaaa.py文件中打印"hello world!"

可以看到在项目启动之前就会在后台打印"hello world!"了.

1

