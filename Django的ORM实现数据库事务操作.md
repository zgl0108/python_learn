在Django中实现数据库的事务操作

在学习MySQL数据库时,`MySQL数据库是支持原子操作`的.

什么是数据库的原子操作呢??打个比方,一个消费者在一个商户里刷信用卡消费.

交易正常时,银行在消费者的账户里减去相应的款项,在商户的帐户加上相应的款项.

但是如果银行从消费者的账户里扣完钱之后,还未在商户的帐户里加上相应的款项时.

由于某些原因,系统或者数据库出现异常了,那么此时钱已经从消费者的账户里扣除了,但是商户的账户里却没有加上相应的款项,让会让商户遭受损失.

这种情况下,最好的解决办法就是使用数据库的原子性操作.

如果数据库使用了事务操作,当出现上面的操作异常时,待数据库正常运行后,数据库系统会把先前执行了一半的操作退回到这个操作之前的状态,

这个通常称为数据库的回滚,也即数据库的原子性操作.

Django中,正常的数据库操作应该是原子性操作的.

在Django的`ORM`中,想使用事务操作时,要先导入一个Django的内置模块

    from django.db import transaction

首先创建一个项目test,项目中有一个应用app01.

项目的`model`为:

        from django.db import models
        
        class Userinfo(models.Model):
            username=models.CharField("用户名",max_length=32)
            email=models.EmailField("邮箱",max_length=32)
        
        class Group(models.Model):
            title=models.CharField("组名",max_length=32)

配置好url

    urlpatterns = [
        url(r'^admin/', admin.site.urls),
        url(r'^index/',views.index),
    ]

路由对应的视图函数为


        from django.shortcuts import render,HttpResponse
        from . import models
        
        def index(request):
        
            from django.db import transaction
        
            try:
                with transaction.atomic():
                    models.Userinfo.objects.create(username="python001",email="python001@qq.com")
                    models.Group.objects.create(title="python002")
        
            except Exception as e:
                return HttpResponse("出现错误....")
            return HttpResponse("ok")

首在先浏览器中打开`http://127.0.0.1:8000/index/`,浏览器的页面上出现

![](http://images2017.cnblogs.com/blog/1133627/201710/1133627-20171025225928598-1437795304.png)

打开对应的数据库可以看到,`UserInfo`数据表和`Group`数据表中已经添加一条记录

![](http://images2017.cnblogs.com/blog/1133627/201710/1133627-20171025225940379-1151157468.png)

![](http://images2017.cnblogs.com/blog/1133627/201710/1133627-20171025225948082-1841209455.png)

现在修改视图函数,使程序出现运行错误,

        from django.shortcuts import render,HttpResponse
        from . import models
        
        def index(request):
        
            from django.db import transaction
        
            try:
                with transaction.atomic():
                    models.Userinfo.objects.create(username="python001",email="python001@qq.com")
                    models.Group.objects.create(tile="python002")
        
            except Exception as e:
                return HttpResponse("出现错误....")
            return HttpResponse("ok")
	
再次刷新浏览器,可以看到

![](http://images2017.cnblogs.com/blog/1133627/201710/1133627-20171025230031676-1958103919.png)

而刷新两张数据表,可以看到两张数据库都没有添加数据记录.

![](http://images2017.cnblogs.com/blog/1133627/201710/1133627-20171025230043254-156500959.png)

![](http://images2017.cnblogs.com/blog/1133627/201710/1133627-20171025230052754-1661431835.png)

这就是Django的`ORM`所支持的事务操作.!