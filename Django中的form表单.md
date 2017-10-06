我们在某个网站注册账号的时候，总会遇到下面的情况：

    限定用户名的长度最少8位
    用户输入的密码最短8位，最长28位
    还有用户输入的手机号或者邮箱验证等

这些情况都可以由Django的`form`来实现。

**Django中的form表单的定义** 

Django的表单系统中，所有的表单都继承自`django.forms.Form`类

基于Django的表单系统，主要分两类：

* 基于django.forms.Form：所有表单类的父类
* 基于django.forms.ModelForm：与模型类绑定的Form

**Django的form的使用**

先在`views.py`中自定义一个MyForm类

    class MyForm(forms.Form):
        user=forms.CharField()
        age=forms.IntegerField()
        email=forms.EmailField()

然后再定义一个reg的视图函数

        def reg(request):
            form_obj=MyForm()       # 实例化一个MyForm类
        
            return render(request,"reg.html",{"form_obj":form_obj})

再生成一个reg的网页，配置好路由表，`reg.html`的内容如下：

        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>Title</title>
        </head>
        <body>
        <h4>{{ error_message }}</h4>
        <form action="/reg/" method="post">
            {% csrf_token %}
            {{ form_obj.as_p }}
        </form>
        </body>
        </html>
    
启动程序，用浏览器打开`http://127.0.0.1:8000/reg/`后，可以看到浏览器上的页面如下：

![](http://images2017.cnblogs.com/blog/1133627/201710/1133627-20171006180120927-1119554114.png)

在MyForm类中定义了用户名user,年龄age和邮箱email三个注册项，而在前端页面上就显示了三个标签。

所以可以知道这三个标签是由`form_obj`这个对象创建出来的。

***在前端页面提示用户输入信息时都是英文格式，想变成汉语格式的应该怎么办呢？？？***

把上面定义的`MyForm`类修改

    class MyForm(forms.Form):
        user=forms.CharField(label="用户")
        age=forms.IntegerField(label="年龄")
        email=forms.EmailField(label="邮箱")

刷新网页，显示页面如下

![](http://images2017.cnblogs.com/blog/1133627/201710/1133627-20171006180203646-575572104.png)

查看网页的源码，每个标签由一个`label`标签和`input`标签组成，而且每个标签都被一个p标签包围，

![](http://images2017.cnblogs.com/blog/1133627/201710/1133627-20171006180215161-887620643.png)

在前端页面上只写了`form_obj.as_p`,所以所有标签都是由Django的模板语言按照form表单的语法渲染出来的。

这种方式生成的代码封装性很好，但是可拓展性太差了。

***如果我想在`p`标签里面再添加一些别的装饰呢，这又怎么办呢？？？***

修改前端页面的代码

        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>Title</title>
        </head>
        <body>
        <h4>{{ error_message }}</h4>
        <form action="/reg/" method="post">
            {% csrf_token %}
            <p>姓名:{{ form_obj.user }}</p>
            <p>年龄:{{ form_obj.age }}</p>
            <p>邮箱:{{ form_obj.email }}</p>
            <input type="submit">
        </form>
        </body>
        </html>
        
在这里，我们就生成一个姓名，年龄和邮箱的文本，其余的交由`form`来渲染，渲染结果如下：

![](http://images2017.cnblogs.com/blog/1133627/201710/1133627-20171006180232005-2025464132.png)

再来看网页的源码

![](http://images2017.cnblogs.com/blog/1133627/201710/1133627-20171006180244021-1768863560.png)

原来的label标签已经没有了，取而代之的是自定义的文本，而且只剩下一个input标签了。

而且可以看到每个标签的`type`属性不一样，跟MyForm类里定义的字段类型是一样的。

    在MyForm类中定义的用户名user字段的类型是CharField类型，渲染后变成了text类型
    在MyForm类中定义的用户名age字段的类型是IntegerField类型，渲染后变成了number类型
    在MyForm类中定义的用户名email字的类型是EmailField类型，渲染后变成了email类型

而且其name属性和id属性的值都跟MyForm类中定义的字段是一样的。

看完了源码，现在什么信息都不输入就点击提交按钮会发生什么呢？？

![](http://images2017.cnblogs.com/blog/1133627/201710/1133627-20171006180327630-189433987.png)

浏览器提示信息告诉我们用户信息这一栏不能为空。

在用户信息栏里输入信息，再次点击提交按钮，又会在年龄栏中提示不能为空。

在这里如果我们向年龄信息栏中输入的是字母或特殊符号，也会输入不上，而只能输入数字。

因为在MyForm类中定义字段时使用了`Integer`类型。

同样的，在邮箱字段里也有同样的输入要求。

***对用户输入的用户名和密码的长度进行设定***

修改`MyForm`类

    class MyForm(forms.Form):
        user = forms.CharField(label="用户",min_length=5,max_length=12)
        age = forms.IntegerField(label="年龄")
        email = forms.EmailField(label="邮箱")

刷新浏览器，看会发生什么情况？？

![](http://images2017.cnblogs.com/blog/1133627/201710/1133627-20171006180337865-1256477507.png)

提示必须输入的信息的长度不能小于5。

修改reg视图函数

    def reg(request):
        if request.method=='POST':
            form_post=MyForm(request.POST)
    
            print(form_post.is_valid())
        form_obj=MyForm()
    
        return render(request,"reg.html",{"form_obj":form_obj})

打开IE浏览器，填写如下信息，然后提交

![](http://images2017.cnblogs.com/blog/1133627/201710/1133627-20171006180348240-1329668392.png)

在服务端后台打印的信息如下

    False

可以看到`is.valid()`方法返回的是一个布尔值。

按照正确的要求填写并提交信息后，后台才会打印`True`。

可以知道，Django的form到底有多少层校验取决于`views.py`的类中每个字段的类型及参数的个数.

如果用户输入的信息符合设定的要求，那么接下来就必须把用户填写的注册信息添加到数据库中。

先修改视图函数，看Django的form把用户输入的数据转换成什么样子的了。

        def reg(request):
            if request.method=='POST':
                form_post=MyForm(request.POST)
        
                if form_post.is_valid():
                    print("data:",form_post.cleaned_data)
        
            form_obj=MyForm()
        
            return render(request,"reg.html",{"form_obj":form_obj})

刷新浏览器，重新输入注册信息，打印如下

    data: {'user': 'aaaaaa', 'age': 100, 'email': 'bbbb@qq.com'}

可以看到Django的form把用户输入的信息封装成一个字典了。

此时添加数据库就可以使用关键字参数了。

        def reg(request):
            if request.method=='POST':
                form_post=MyForm(request.POST)
        
                if form_post.is_valid():
                    print("data:",form_post.cleaned_data)
        
                    models.UserInfo.objects.create_ue(**form_post)
        
            form_obj=MyForm()
        
            return render(request,"reg.html",{"form_obj":form_obj})

进行校验的时候，如果出现错误，就应该把错误信息返回，该怎么做呢？？

先打印下错误信息及错误信息的类型

        def reg(request):
            if request.method=='POST':
                form_post=MyForm(request.POST)
        
                if form_post.is_valid():
                    print("data:",form_post.cleaned_data)
        
                    models.UserInfo.objects.create_ue(**form_post)
                else:
                    print(form_post.errors)
                    
                    print(type(form_post.errors))
            form_obj=MyForm()
        
            return render(request,"reg.html",{"form_obj":form_obj})
打印信息如下：

        <ul class="errorlist">
        <li>user<ul class="errorlist"><li>This field is required.</li></ul></li>
        <li>age<ul class="errorlist"><li>This field is required.</li></ul></li>
        <li>email<ul class="errorlist"><li>This field is required.</li></ul></li></ul>
        
        <class 'django.forms.utils.ErrorDict'>

可以看到，返回的错误信息是一个字典。

既然是一个字典类型，那么就可以取出其中的值。

        def reg(request):
            if request.method=='POST':
                form_post=MyForm(request.POST)
        
                if form_post.is_valid():
                    print("data:",form_post.cleaned_data)
        
                    models.UserInfo.objects.create_ue(**form_post)
                else:
                    print("user_errors:",form_post.errors["user"])
                    print("age_errors:",form_post.errors["age"])
                    print("email_errors:",form_post.errors["email"])
                    
            form_obj=MyForm()
        
            return render(request,"reg.html",{"form_obj":form_obj})

打印结果如下：

    user_errors: <ul class="errorlist"><li>This field is required.</li></ul>
    age_errors: <ul class="errorlist"><li>This field is required.</li></ul>
    email_errors: <ul class="errorlist"><li>This field is required.</li></ul>

返回的信息是一个`<ul><li>`标签，其错误信息的内容为`"This field is required."`。

修改`views.py`文件

        def reg(request):
            if request.method=='POST':
                form_post=MyForm(request.POST)
        
                if form_post.is_valid():
                    print("data:",form_post.cleaned_data)
        
                    models.UserInfo.objects.create_user(**form_post)
                else:
                    errors_obj=form_post.errors
                    print("user_errors:",errors_obj["user"])
                    print("age_errors:",errors_obj["age"])
                    print("email_errors:",errors_obj["email"])
        
            form_obj=MyForm()
        
        return render(request,"reg.html",{"form_obj":form_obj,"errors_obj":errors_obj})

修改前端网页reg.html

        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>Title</title>
        </head>
        <body>
        <h4>{{ error_message }}</h4>
        <form action="/reg/" method="post">
            {% csrf_token %}
            <p>姓名:{{ form_obj.user }}<span>{{ errors_obj.user.0 }}</span></p>
            <p>年龄:{{ form_obj.age }}<span>{{ errors_obj.age.0 }}</span></p>
            <p>邮箱:{{ form_obj.email }}<span>{{ errors_obj.email.0 }}</span></p>
            <input type="submit">
        </form>
        </body>
        </html>

这样就可以把错误信息渲染到前端网页了，如下所示,正常打开网页时，不会显示错误信息

![](http://images2017.cnblogs.com/blog/1133627/201710/1133627-20171006180405302-1681076183.png)

当输入的信息不符合定义的要求时，就显在网页上显示错误信息了

![](http://images2017.cnblogs.com/blog/1133627/201710/1133627-20171006180414521-1544595378.png)

如果想自定义在前端网页上显示的错误信息，该怎么办呢？

修改MyForm类，如下

    class MyForm(forms.Form):
        user = forms.CharField(label="用户",min_length=5,max_length=12,error_messages={"required":"用户名必填"})
        age = forms.IntegerField(label="年龄",error_messages={"required":"年龄必填"})
        email = forms.EmailField(label="邮箱",error_messages={"required":"邮箱必填"})

此时，再次刷新浏览器，点击提交按钮，显示如下

![](http://images2017.cnblogs.com/blog/1133627/201710/1133627-20171006180424708-162487671.png)

**基于django.forms.ModelForm：与模型类绑定的Form**

先定义一个ModelForm类,继承ModelForm类

    from django.forms import ModelForm
    
    class MyModelForm(ModelForm):
        class Meta:
            model=models.UserInfo
    
            fields="__all__"
            
修改视图函数reg

        def reg(request):
            if request.method=="POST":
                model_form=MyModelForm()
        
                return render(request,"reg.html",{"model_fom":model_form})

修改reg.html网页

        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>Title</title>
        </head>
        <body>
        <h4>{{ error_message }}</h4>
        <form action="/reg/" method="post">
            {% csrf_token %}
            {{ model_fom.as_p }}
            <input type="submit">
        </form>
        </body>
        </html>

打开注册页面，可以看到，在定义数据库的用户信息表中定义的字段信息都显示在注册网页上了。

而且这里也支持使用万能的句点号，以及验证用户输入的信息是否与数据库中定义的类型符合

用户输入信息，验证通过后，就要保存到数据库中。

    def reg(request):
        if request.method=="GET":
            model_form=MyModelForm()
    
            return render(request,"reg.html",{"model_form":model_form})
        else: 
    
            model_form=MyModelForm(request.POST) # 实例化MyModelForm类
            if model_form.is_valid(): # 如果用户输入的信息合法
    
                model_form.save()       # 用户输入的信息保存到数据库中
                return redirect("/index/")
    
            return render(request,"reg.html",{"model_form":model_form})

***使用ModelForm编辑用户***

编辑用户的视图函数如下

        from django.forms import ModelForm
        
        class MyModelForm(ModelForm):
            class Meta:
                model=models.UserInfo
        
                fields="__all__"
        
        def edituser(request,uid):
            user_obj = models.UserInfo.objects.filter(id=uid).first()
        
            if not user_obj:
                return redirect("/index/")
        
            if request.method=="GET":
        
                model_form=MyModelForm(instance=user_obj)
        
            else:
                model_form=MyModelForm(request.POST,instance=user_obj)
        
                if model_form.is_valid():
                    model_form.save()
                    return redirect("/index/")
        
            return render(request,"edit.html",{"model_form":model_form})

***Django的ModelForm的其他的参数和功能***

可以在class Meta中设定的功能：

        model=models.Userinfo           # 显示对应Model的字段,这里显示用户信息表
        
        fields="__all__"                # 显示数据表中所有的字段
        
        fields=["username","age"]       # 显示数据表中指定的字段
        
        exclude=["email"]               # 不显示数据表中某些字段
        
        labels={
            "username":"用户名",
            "age":"年龄",
            "email":"邮箱"
        }                               # 自定义页面的标签
        
        help_texts={
            "username":"请输入正确的用户名",
            "email":"请输入正确的邮箱格式"
        }                               # 自定义在标签后面显示的提示帮助信息
        
        error_messages={
            "username":{'required':"用户名不能为空"}
            "email":{'invalid':"邮箱不能为空"}
        }                               # 自定义错误信息，用户输入错误时显示
        
        from django import fields as field_widget
        field_classes={
            "email":field_widget.EmailField
        }                               # 定义标签的类型，在这里把email这个输入框的类型更改为email类型
        
        from django.forms import widgets as formwidget
        widgets={
            "username":formwidget.Textarea(atts={"class":"c1"})
        }                               # 自定义插件(attrs为插件的属性)