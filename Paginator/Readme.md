����ʹ��python������һ����ҳ��.

ʹ�÷���:

���������ȡ����ǰ��ҳ����

    current_page=int(request.GET.get("page",1))
�����ݿ���ȡ�����ܵļ�¼��

    item_list=models.���ݱ�.objects.all()
    total_item_count=item_list.count()

ʹ��`Paginator`��ʵ����һ��ҳ��Ķ���:

    page_obj=Paginator(current_page,total_item_count,"/index/")
```
��Ҫע�����:

    ʵ����page_obj��ʱ��,���Զ���ÿҳ��ʾ�ļ�¼����per_page_count����ʾ��ҳ���ϵ�ҳ��ĸ���show_page_count

    ÿҳ��ʾ�ļ�¼��per_page_countĬ��ֵΪ10,
    ҳ����ʾ��ҳ��ĸ���show_page_countĬ��ֵΪ11
```
���巵�ص��ͻ��˵�ÿһҳ�����ݼ�¼�б�

    per_page_list=models.���ݱ�.objects.all()[page_obj.start:page_obj.end]

���ʹ��`render`����`redirect`���ظ��ͻ���

    return render(request,"aaa.html",{"per_page_list":per_page_list,"page_html":page_obj.page_html()})
    
��ǰ�˵�ʹ��

ʹ��forѭ������`per_page_list`,Ȼ����Ⱦÿ�����������

��`page_html`��Ҫ��`bootstrap`�еķ�ҳ������ʹ��

��������:

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
		            {#��ҳ���ݿ�ʼ#}
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
		                            <td>{{ item.����1 }}</td>
		                            <td>{{ item.����2 }}</td>
		                            <td>{{ item.����3 }}</td>
		                            <td>{{ item.����4 }}</td>
		                            <td>{{ item.����5 }}</td>
		                            <td>{{ item.����6 }}</td>
		                            <td>{{ item.����7 }}</td>
		                            <td>{{ item.����8 }}</td>
		                        </tr>
		                    {% endfor %}
		                </ul>
		            </table>
		            {#��ҳ���ݽ���#}
		            {#��ҳ��ʼ#}
		            <nav>
		                <ul class="pagination">
		                    {{ page_html }}
		                </ul>
		            </nav>
		            {#��ҳ����#}
		        </div>
		    </div>
		</div>
		<script src="{% static "bootstrap/js/bootstrap.js" %}"></script>
		<script src="{% static "jquery-3.2.1.js" %}"></script>
		</body>
		</html>