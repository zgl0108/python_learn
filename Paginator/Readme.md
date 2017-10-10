这是使用python开发的一个分页器.

使用方法:

从浏览器中取出当前的页码数

    current_page=int(request.GET.get("page",1))
从数据库中取出的总的记录数

    item_list=models.数据表.objects.all()
    total_item_count=item_list.count()

使用`Paginator`类实例化一个页码的对象:

    page_obj=Paginator(current_page,total_item_count,"/index/")
```
需要注意的是:

    实例化page_obj的时候,可以定义每页显示的记录个数per_page_count及显示在页面上的页码的个数show_page_count

    每页显示的记录数per_page_count默认值为10,
    页面显示的页码的个数show_page_count默认值为11
```
定义返回到客户端的每一页的数据记录列表

    per_page_list=models.数据表.objects.all()[page_obj.start:page_obj.end]

最后使用`render`或者`redirect`返回给客户端

    return render(request,"aaa.html",{"per_page_list":per_page_list,"page_html":page_obj.page_html()})
    
在前端的使用

使用for循环遍历`per_page_list`,然后渲染每个对象的属性

而`page_html`就要与`bootstrap`中的分页组件配合使用

代码如下:

		{% load staticfiles %}
		<!DOCTYPE html>
		<html lang="en">
		<head>
		    <meta charset="UTF-8">
		    <title>Title</title>
		    <link rel="stylesheet" href="{% static "bootstrap/css/bootstrap.css" %}">
		</head>
		<body>

		<div class="container">
		    <div class="row">
		        <div class="col-lg-12">
		            {#分页内容开始#}
		            <table class="table table-striped">
		                <tr>
		                    <td>td1</td>
		                    <td>td2</td>
		                    <td>td3</td>
		                    <td>td4</td>
		                    <td>td5</td>
		                    <td>td6</td>
		                    <td>td7</td>
		                    <td>td8</td>
		                </tr>
		                <ul>
		                    {% for item in per_page_list %}
		                        <tr>
		                            <td>{{ item.属性1 }}</td>
		                            <td>{{ item.属性2 }}</td>
		                            <td>{{ item.属性3 }}</td>
		                            <td>{{ item.属性4 }}</td>
		                            <td>{{ item.属性5 }}</td>
		                            <td>{{ item.属性6 }}</td>
		                            <td>{{ item.属性7 }}</td>
		                            <td>{{ item.属性8 }}</td>
		                        </tr>
		                    {% endfor %}
		                </ul>
		            </table>
		            {#分页内容结束#}
		            {#分页开始#}
		            <nav>
		                <ul class="pagination">
		                    {{ page_html }}
		                </ul>
		            </nav>
		            {#分页结束#}
		        </div>
		    </div>
		</div>
		<script src="{% static "bootstrap/js/bootstrap.js" %}"></script>
		<script src="{% static "jquery-3.2.1.js" %}"></script>
		</body>
		</html>