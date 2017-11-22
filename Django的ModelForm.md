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

需要注意的是,`ModelForm`在`sava`的时候有一个`commit`的参数,`commit的值默认为True`

	当commit等于True的时候,ModelForm就会把数据提交到数据库当中保存;
	当commit设定为False的时候,ModelForm并不会真正在数据库中保存数据.

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