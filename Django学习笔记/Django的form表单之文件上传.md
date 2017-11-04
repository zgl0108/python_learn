在生成input标签的时候可以指定input标签的类型为file类型

    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Title</title>
    </head>
    <body>
    <h4>{{ error_message }}</h4>
    <form action="/index/" method="post">
        {% csrf_token %}
        <p><input type="file" name="up_file"></p>
        <input type="submit">
    </form>
    </body>
    </html>

此时，在网页上页示如下

![](http://images2017.cnblogs.com/blog/1133627/201710/1133627-20171006200828740-1741589799.png)

如果网页上提交的是用户名和密码等，通过键值对发送到服务端。

一组键值代表一个标签及标签对应的值。

在网页上选择一张图片，并使用`post`方式提交，在服务端打印`request.POST`

        def index(request):
            if request.method=="POST":
                print(request.POST)
        
            return render(request,"index.html",locals())
        
打印的信息如下：

    <QueryDict: {'csrfmiddlewaretoken': ['opmSmENIrgdGJJN'], 'up_file': ['1.png']}>

提交的文件名也在这个字典中，取出这个文件名

        def index(request):
            if request.method=="POST":
                print(request.POST.get("up_file"))
                print(type(request.POST.get("up_file")))
        
            return render(request,"index.html",locals())
        
打印结果如下：

    1.png
    <class 'str'>
    
想取出的是上传的文件，然而取出来的却是上传的文件的文件名

由此可知，上传的文件没有跟form表单提交的数据在一起

因为上传的文件通常大小比较大，所以Django默认会把上传的文件放在一个具体的文件夹中

打印`request.FILES`的信息

        def index(request):
            if request.method=="POST":
                print(request.POST.get("up_file"))
                print(type(request.POST.get("up_file")))
                print("files:",request.FILES)
        
            return render(request,"index.html",locals())

打印结果如下

    1.png
    <class 'str'>
    files: <MultiValueDict: {}>

`request.FILES`打印的结果是一个空的字典，问题出在上传文件的方式上

由于上传文件时在客户端与服务端传输的是二进制数据，与字符串数据不一样。

传输二进制数据，不管是在form表单，还是在Ajax中，都有自己的传输方式。

在form表单中，上传文件时要使用分片传输的方式。

修改index.html文件

    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Title</title>
    </head>
    <body>
    <h4>{{ error_message }}</h4>
    <form action="/index/" method="post" enctype="multipart/form-data">
        {% csrf_token %}
        <p><input type="file" name="up_file"></p>
        <input type="submit">
    </form>
    </body>
    </html>
    
重新上传文件，在服务端打印信息如下

    None
    <class 'NoneType'>
    files: <MultiValueDict: {'up_file': [<InMemoryUploadedFile: 1.png (image/png)>]}>
    
根据打印结果，`request.FILES`中可以看到上传的文件

打印结果是一个字典类型，字典的键是form表单中定义的标签的name属性值，而其值是所上传的文件的对象

打印上传文件的对象

    def index(request):
        if request.method=="POST":
    
            print("files:",request.FILES.get("up_file"))
            print(type(request.FILES.get("up_file")))
    
        return render(request,"index.html",locals())
打印结果

    files: 1.png
    <class 'django.core.files.uploadedfile.InMemoryUploadedFile'>

结果显示所取得的文件的类型是一个在内存中的上传文件

获取上传文件在内存中的名字

    def index(request):
        if request.method=="POST":
    
            print(type(request.FILES.get("up_file")))
    
            file_obj=request.FILES.get("up_file")
    
            print(file_obj.name)
    
    
        return render(request,"index.html",locals())

打印结果如下

    <class 'django.core.files.uploadedfile.InMemoryUploadedFile'>
    1.png

既然知道了文件在内存中的名字，就可以在服务端写入这个文件

    def index(request):
        if request.method=="POST":
            file_obj=request.FILES.get("up_file")
    
            f1=open(file_obj.name,"wb")
    
            for i in file_obj.chunks():
                f1.write(i)
    
            f1.close()
    
        return render(request,"index.html",locals())
再次选择上传文件，提交后，就可以在服务端后台看到所上传的文件

可以在settings.py文件中设定上传文件的路径，或者在打开文件句柄的时候进行路径拼接来把上传的文件保存在指定的目录下