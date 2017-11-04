**认证登陆**

在进行用户登陆验证的时候，如果是自己写代码，就必须要先查询数据库，看用户输入的用户名是否存在于数据库中；

如果用户存在于数据库中，然后再验证用户输入的密码，这样一来就要自己编写大量的代码。

事实上，Django已经提供了内置的用户认证功能。

在使用`"python manage.py makemigrationss"`和`"python manage.py migrate"`迁移完成数据库之后

根据配置文件`settings.py`中的数据库段生成的数据表中已经包含了6张进行认证的数据表，分别是

* auth_user
* auth_group
* auth_group_permissions
* auth_permission
* auth_user_groups
* auth_user_user_permissions

进行用户认证的数据表为`auth_user`

要使用Django自带的认证功能，首先要导入`auth`模块

	from django.contrib import auth         #导入auth模块
	
`django.contrib.auth`中提供了很多方法，我们常用的有三个方法：

***authenticate()***

提供了用户认证，即验证用户名以及密码是否正确，一般需要username和password两个关键字参数

如果通过认证，`authenticate()`函数会返回一个User对象。

`authenticate()`函数会在User对象上设置一个属性标识，这个属性标识经过数据库验证用户名及密码。

当我们试图登陆一个从数据库中直接取出来不经过`authenticate()`的User对象时会报错。

使用：

        user=authenticate(username="uaername",password="password")
        
        login(HttpResponse,user)

这个函数接受一个`HttpRequest`对象，以及一个通过`authenticate()`函数认证的User对象

***login(request)登陆用户***

这个函数使用`Django`的`session`框架给某个已认证的用户附加上`session_id`信息。

使用：

        from django.shortcuts import render,redirect,HttpResponse
        
        from django.contrib.auth import authenticate,login
        
        def auth_view(request):
            username=request.POST.GET("usernmae")       # 获取用户名
            password=request.POST.GET("password")       # 获取用户的密码
        
            user=authenticate(username=username,password=password)	# 验证用户名和密码，返回用户对象
        
            if user:                        # 如果用户对象存在
                login(request,user)         # 用户登陆
                return redirect("/index/")
        
            else:
                return HttpResponse("用户名或密码错误")

***logout(request)注销用户***

这个函数接受一个`HttpResponse`对象，无返回值。

当调用该函数时，当前请求的session信息全部被清除。

即使当前用户没有登陆，调用该函数也不会报错。

使用：

        from django.shortcuts import render,redirect,HttpResponse
        
        from django.contrib.auth import authenticate,login,logout
        
        def logout_view(request):
            
            logout(request)		# 注销用户
            
            return redirect("/index/")

***user对象的is_authenticated()***

要求：

* 用户登陆后才能访问某些页面
* 如果用户没有登陆就访问本应登陆才能访问的页面时会直接跳转到登陆页面
* 用户在登陆页面登陆后，又会自动跳转到之前访问的页面

方法一：

        def view1(request):
            
            if not request.user.is_authenticated():
                return redirect("/login/")
方法二：

使用Django的`login_requierd()`装饰器

使用：

        from django.contrib.auth.decorators import login_required
        
        @login_required
        def views(request):
            pass

如果用户没有登陆，则会跳转到Django默认的登陆URL的`"/accountss/login/"`


    login视图函数可以在settings.py文件中通过LOGIN_URL修改默认值

用户登陆成功后，会重定向到原来的路径。

**user对象**

User对象属性：username,password为必填项

    password用哈希算法保存到数据库中

* is_staff：判断用户是否拥有网站的管理权限
* is_active：判断是否允许用户登陆，设置为“False”时可以不用删除用户来禁止用户登陆

User对象的方法

***is_authenticated()***

如果是通过`auth`函数返回的真实的User对象，返回值则为True。这个方法检查用户是否已经通过了认证。

`is_authenticated()`函数的返回值为True时，表明用户成功的通过了认证。

***创建用户***

使用`create_user`辅助函数创建用户

	from django.contrib.auth.models import User
	user=User.objects.create_user(username="username",password="password")

***set_password(password)***

使用这个方法来修改密码

使用：

        from django.contrib.auth.models import User
        
        user=User.objects.get(username="username")		# 获取用户对象
        user.set_password(password="password")			# 设置对象的密码
        
        user.save()

***check_password(password)***

用户想修改密码的时候，首先要让用户输入原来的密码。

如果用户输入的旧密码通过密码验证，返回True。



例子一,使用`set_password()`方法来修改密码

        from django.shortcuts import render,redirect,HttpResponse
        from django.contrib.auth.models import User
        
        def create_user(request):
        
            msg=None
        
            if request.method=="POST":
                username=request.POST.get("username"," ")           # 获取用户名，默认为空字符串
                password=request.POST.get("password"," ")           # 获取密码，默认为空字符串
                confirm=request.POST.get("confirm_password"," ")    # 获取确认密码，默认为空字符串
        
                if password == "" or confirm=="" or username=="":   # 如果用户名，密码或确认密码为空
                    msg="用户名或密码不能为空"
                elif password !=confirm:                            # 如果密码与确认密码不一致
                    msg="两次输入的密码不一致"
                elif User.objects.filter(username=username):        # 如果数据库中已经存在这个用户名
                    msg="该用户名已存在"
                else:
                    new_user=User.objects.create_user(username=username,password=password)	#创建新用户 
                    new_user.save()
                
                    return redirect("/index/")
            
            return render(request,"login.html",{"msg":msg})

例子二,使用`login_required装饰器`来修改密码

        from django.shortcuts import render,redirect,HttpResponse
        from django.contrib.auth import authenticate,login,logout
        from django.contrib.auth.decorators import login_required
        from django.contrib.auth.models import User
        
        @login_required
        def change_passwd(request):
            user=request.user       # 获取用户名
            msg=None
        
            if request.method=='POST':
                old_password=request.POST.get("old_password","")    # 获取原来的密码，默认为空字符串
                new_password=request.POST.get("new_password","")    # 获取新密码，默认为空字符串
                confirm=request.POST.get("confirm_password","")     # 获取确认密码，默认为空字符串
        
                if user.check_password(old_password):               # 到数据库中验证旧密码通过
                    if new_password or confirm:                     # 新密码或确认密码为空
                        msg="新密码不能为空"   
                    elif new_password != confirm:                   # 新密码与确认密码不一样
                        msg="两次密码不一致"
        
                    else:
                        user.set_password(new_password)             # 修改密码
                        user.save()
        
                        return redirect("/index/")
                else:
                    msg="旧密码输入错误"
        
            return render(request,"change_passwd.html",{"msg":msg})