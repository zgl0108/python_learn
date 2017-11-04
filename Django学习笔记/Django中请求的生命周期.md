**1. ����**

��������֪��HTTP���󼰷������Ӧ�д�����������ݶ����ַ���.

��Django��,�����Ƿ���һ����urlʱ,��ͨ��·��ƥ�������Ӧ��html��ҳ��.

Django����������������ָ���û��������������url���û�������ҳ�����ʱ�����,Django��̨������������

��Django�����������ڵ��׷�����ʲô��??

    1. ���û��������������urlʱ,���������������ͷ�������巢�������
    ����ͷ���������л����������Ķ���(action),�������ͨ��Ϊget����post,������url֮��.

    2. Django��������url��ת����·��ӳ���,��·����һ��һ������ƥ��,
    һ������һ��ƥ��ɹ���ִ�ж�Ӧ����ͼ����,�����·�ɾͲ��ټ���ƥ����.
    3. ��ͼ�������ݿͻ��˵������ѯ��Ӧ������.���ظ�Django,Ȼ��Django�ѿͻ�����Ҫ��������Ϊһ���ַ������ظ��ͻ���.
    4. �ͻ�����������յ����ص�����,������Ⱦ����ʾ���û�.
    
��ͼ�������ݿͻ��˵������ѯ��Ӧ�����ݺ�.���ͬʱ�ж���ͻ���ͬʱ���Ͳ�ͬ��url���������������

����˲�ѯ�����ݺ�,��ô֪��Ҫ����Щ���ݷ��ظ��ĸ��ͻ�����??

��˿ͻ��˷�������˵�url�л�����Ҫ������Ҫ�����������Ϣ������.

����,`http://www.aaa.com/index/?nid=user`���url��,
�ͻ���ͨ��get���������˷��͵�`nid=user`������,����˿���ͨ��`request.GET.get("nid")`�ķ�ʽȡ��nid����

�ͻ��˻�����ͨ��post�ķ�ʽ��������������.

���ͻ�����post�ķ�ʽ�������������ݵ�ʱ��,��������ݰ�������������,��ʱ����˾�ʹ��request.POST�ķ�ʽȡ�ÿͻ�����Ҫȡ�õ�����

    ��Ҫע�����,request.POST�ǰ������������ת��һ���ֵ�,�������е�����Ĭ�������ַ�������ʽ���ڵ�.
    
**2. FBVģʽ��CBVģʽ**

һ��url��Ӧһ����ͼ����,���ģʽ����FBV(`Function Base Views`)

����FBV֮��,Django�л�������һ��ģʽ����CBV(`Class Base views`),��һ��url��Ӧһ����

����:ʹ��cbvģʽ��������ҳ
 
·����Ϣ:
```
    urlpatterns = [
        url(r'^fbv/',views.fbv),
        url(r'^cbv/',views.CBV.as_view()),
    ]
```
��ͼ��������:
```
    from django.views import View
    
    class CBV(View):
        def get(self,request):
            return render(request, "cbv.html")
    
        def post(self,request):
            return HttpResponse("cbv.get")
```
cbv.html��ҳ������:
```
    <body>
    <form method="post" action="/cbv/">
        {% csrf_token %}
        <input type="text">
        <input type="submit">
    </form>
    </body>
```
������Ŀ,�������������`http://127.0.0.1:8000/cbv/`,�س�,�õ�����ҳ����:


��input��������"hello",��س�

ʹ��fbv��ģʽ,��urlƥ��ɹ�֮��,��ֱ��ִ�ж�Ӧ����ͼ����.

�����ʹ��cbvģʽ,��urlƥ��ɹ�֮��,���ҵ���ͼ�����ж�Ӧ����,Ȼ�������ص�����ͷ���ҵ���Ӧ��`Request Method`.

    ����ǿͻ�����post�ķ�ʽ�ύ����,��ִ�����е�post����;
    ����ǿͻ�����get�ķ�ʽ�ύ����,��ִ�����е�get����
    
Ȼ������û���������url,Ȼ��������ִ�ж�Ӧ�ķ�����ѯ�����û���Ҫ������.

***2.1 fbv��ʽ����Ĺ���***

�û�����url����,Django�����α���·��ӳ����е����м�¼,һ��·��ӳ������е�һ��ƥ��ɹ���,

��ִ����ͼ�����ж�Ӧ�ĺ�����,����fbv��ִ������

***2.2 cbv��ʽ����Ĺ���***

�������ʹ��cbvģʽ��ʱ��,�û���������˵��������url��method,��������Ϣ�����ַ�������

�����ͨ��·��ӳ���ƥ��ɹ�����Զ�ȥ��dispatch����,Ȼ��Django��ͨ��dispatch����ķ�ʽ�ҵ����ж�Ӧ�ķ�����ִ��

���еķ���ִ�����֮��,��ѿͻ�����Ҫ�����ݷ��ظ�dispatch����,��dispatch���������ݷ��ؾ��ͻ���

����,������������е���ͼ�����޸ĳ�����:
```
    from django.views import View
    
    class CBV(View):
        def dispatch(self, request, *args, **kwargs):
            print("dispatch......")
            res=super(CBV,self).dispatch(request,*args,**kwargs)
            return res
    
        def get(self,request):
            return render(request, "cbv.html")
    
        def post(self,request):
            return HttpResponse("cbv.get")
```
��ӡ���:

	<HttpResponse status_code=200, "text/html; charset=utf-8">
	dispatch......
	<HttpResponse status_code=200, "text/html; charset=utf-8">

��Ҫע�����:

    ��get��ʽ��������ʱ,����ͷ������Ϣ,��������û������
    ��post��������ʱ,����ͷ���������ﶼ������.	
    
**3. Django������������֮��Ӧ����**

http�ύ���ݵķ�ʽ��`"post"`,`"get"`,`"put"`,`"patch"`,`"delete"`,`"head"`,`"options"`,`"trace"`.

�ύ���ݵ�ʱ��,���������method�Ĳ�ͬ�ᴥ����ͬ����ͼ����.
    
    ����from����˵,�ύ����ֻ��get��post���ַ���
    
����ķ�������ͨ��Ajax�������ύ 

����˸��ݸ���������Ϣ�Ĳ�ͬ���������ݿ�,����ʹ��ԭ����SQL���,Ҳ����ʹ��Django��ORM���.

Django�����ݿ��в�ѯ�������û���Ҫ������,��������ظ��û�.

��Django�з��ص���Ӧ���ݰ�����Ӧͷ����Ӧ��

��Django��,�е�ʱ��һ����ͼ����,ִ����ɺ��ʹ��HttpResponse������һ���ַ������ͻ���.

����ַ���ֻ����Ӧ��Ĳ���,���ظ��ͻ��˵���Ӧͷ�Ĳ���Ӧ����ô������???

Ϊ���ظ��ͻ��˵���Ϣ��һ����Ӧͷ:

�޸��������ӵ���ͼ����Ϊ����:
```
	from django.views import View

	class CBV(View):
		def dispatch(self, request, *args, **kwargs):
			print("dispatch......")
			res=super(CBV,self).dispatch(request,*args,**kwargs)
			print(res)

			return res

		def get(self,request):
			return render(request, "cbv.html")

		def post(self,request):

			res=HttpResponse("cbv.post")
			res.set_cookie("k2","v2")
			res.set_cookie("k4","v4")

			print("res:",res)
			print("request.cookie:",request.COOKIES)
			return res
```
��ӡ����Ϣ:
```
    res: <HttpResponse status_code=200, "text/html; charset=utf-8">
    request.cookie: {'csrftoken': 'jmX9H1455MYzDRQs8cQLrA23K0aCGoHpINL50GnMVxhUjamI8wgmOP7D2wXcpjHb', 'k2': 'v2', 'k4': 'v4'}
```