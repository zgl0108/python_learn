这是使用python开发的一个分页器.

使用方法:

从浏览器中取出当前的页码数

    current_page=int(request.GET.get("page",1))
从数据库中取出的总的记录数

    item_list=models.数据表.objects.all()
    total_item_count=item_list.count()

定义一个页码的对象

    page_obj=Paginator(current_page,total_item_count,"/index/")

定义返回到客户端的记录列表

    item_list=models.数据表.objects.all()[page_obj.start:page_obj.end]

最后使用render或者redirect返回给客户端

    return render(request,"aaa.html",{"item_list":item_list,"page_html":page_obj.page_html()})
    


