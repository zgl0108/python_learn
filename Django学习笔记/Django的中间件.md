����Django����������,����֪�����е�http����Ҫ����Django���м��.

����������һ������,���е������˵�url������ϵͳ�м�¼һ����־,����ô����?

**Django���м���ļ��**

Django���м��������linux�еĹܵ���

Django���м��ʵ�ʾ���һ����,��֮����Django�Ѿ��������һЩ����.

ÿ��http���󶼻�ִ���м���е�һ����������

    ����Django�е����󶼻�ִ��process_request����;
    Django���ص���Ϣ����ִ��process_response����.;

Django�ڲ����м��ע����`settings.py`�ļ�

    MIDDLEWARE = [
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ]

����`from  django.middleware.csrf import CsrfViewMiddleware`ģ��,�鿴��Դ��

	class CsrfViewMiddleware(MiddlewareMixin)
	
���Կ���`CsrfViewMiddleware`�Ǽ̳�`MiddlewareMixin`����м����

�ٲ鿴`MiddlewareMixin`��Դ��
```
    class MiddlewareMixin(object):
        def __init__(self, get_response=None):
            self.get_response = get_response
            super(MiddlewareMixin, self).__init__()
    
        def __call__(self, request):
            response = None
            if hasattr(self, 'process_request'):
                response = self.process_request(request)
            if not response:
                response = self.get_response(request)
            if hasattr(self, 'process_response'):
                response = self.process_response(request, response)
            return response
```            
����֪��`MiddlewareMixin`�ǵ��������ڲ���`__call__`����,`__call__`�����Է���ķ�ʽִ��`process_request`��`process_response`����.

**�м����Ӧ��**

�½�һ��middleware��Ŀ,����Ŀ�ĸ�Ŀ¼���½�һ����Ϊ`middleware`�İ�,�����package��,�½�һ��`middleware.py`�ļ�.
```
    from django.utils.deprecation import MiddlewareMixin
    
    class middle_ware1(MiddlewareMixin):
    
        def process_request(self,request):
            print("middle_ware1.process_request")
    
        def process_response(self,request,response):
            print("middle_ware1.process_response")
            return response
```
��`settings.py`�����ļ��ĵ�һ��ע������м�� 
	
    MIDDLEWARE = [
        'middleware.middleware.middle_ware1'
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ]
    
���������http���󵽴�����,��ִ���м��`middle_ware1`��`process_request`����,��ִ�к�����м��,Ȼ�󵽴���ͼ����.

����һ����ͼ����index,���ú�·��ӳ���

    def index(request):
    
        print("index page")
        return HttpResponse("index")

��������,�������������`http://127.0.0.1:8000/index`,���ڷ���˵ĺ�̨��ӡ:

    middle_ware1.process_request
    index page
    middle_ware1.process_response
ǰ�˵�ҳ��Ϊ��ʾΪ:
	
	index
	
ͨ���������֪��,���е����󶼻ᾭ��`middle_ware1`����м��,��ִ��`process_request`����,��ִ����ͼ��������

���ִ��`process_response`����,Django���`process_response`�����ķ���ֵ���ظ��ͻ���.

�����ټ�һ������һ��`middle_ware2`���м��
```
    from django.utils.deprecation import MiddlewareMixin
    
    class middle_ware2(MiddlewareMixin):
    
        def process_request(self,request):
            print("middle_ware2.process_request")
    
        def process_response(self,request,response):
            print("middle_ware2.process_response")
            return response
```
��`settings.py`�����ļ���ע���м��
```
	MIDDLEWARE = [
		'middleware.middleware.middle_ware1',
		'middleware.middleware.middle_ware2',
		'django.middleware.security.SecurityMiddleware',
		'django.contrib.sessions.middleware.SessionMiddleware',
		'django.middleware.common.CommonMiddleware',
		'django.middleware.csrf.CsrfViewMiddleware',
		'django.contrib.auth.middleware.AuthenticationMiddleware',
		'django.contrib.messages.middleware.MessageMiddleware',
		'django.middleware.clickjacking.XFrameOptionsMiddleware',
	]
```
��������,�ٴ�ˢ����ҳ,����˴�ӡ��Ϣ

	middle_ware1.process_request
	middle_ware2.process_request
	index page
	middle_ware2.process_response
	middle_ware1.process_response
�м��������ִ��Ϊ:

	��ִ��middle_ware1��process_request����,
	��ִ��middle_ware2�����process_request����,
	����ִ��Django����ͼ����.
	����ʱ,��ִ��middle_ware2�����е�process_response����,
	Ȼ����ִ��middle_ware1�����е�process_response����.

�����������,`process_response`����������returnֵ.����`process_response`û��returnֵ,����ô����??

��`middle_ware1`�м����`process_response`�����е�returnע�͵�,�ٴ�ˢ����ҳ,�����������ҳ����ʾ������Ϣ,����:

	A server error occurred.  Please contact the administrator.
	
http���󵽴�Django��,�Ⱦ����Զ�����м��`middle_ware1`��`middle_ware2`,�پ���Django�ڲ�������м��������ͼ����

��ͼ����ִ����ɺ�,һ���᷵��һ��`HttpResponse`����`render`.

ͨ���鿴`render`��Դ���֪,`render`����������Ҳ�ǵ�����`HttpResponse`
```
    def render(request, template_name, context=None, content_type=None, status=None, using=None):
    
        content = loader.render_to_string(template_name, context, request, using=using)
        return HttpResponse(content, content_type, status)
```
��ͼ�����ķ���ֵ`HttpResponse`�Ⱦ���Django�ڲ�������м��,�پ����û�������м��,��󷵻ظ�ǰ����ҳ.

�����û�������м����`process_response`���������趨����ֵ,�������ᱨ��.

ͬʱ,`process_response`�����е��β�`response`������ͼ�����ķ���ֵ.
��ô�����Ƿ�����Լ���������βεķ���ֵ��??

�û���������������Ϣ�ǹ̶���,��Ϊ���е�������Ϣ�ͷ�����Ϣ��Ҫ�����м��,�м���п��ܻ��޸ķ��ظ��û�����Ϣ
,�����п��ܻ�����û��յ��ķ���ֵ����ͼ�����ķ���ֵ��һ�������.

����,���ظ��û�����Ϣ������Ӧͷ����Ӧ��,���ǿ���������ͼ������û��������Ӧͷ,����Django���ڷ��ص���Ϣ���Զ�������Ӧͷ.

ǰ��,`process_response`���������˷���ֵ,`process_request`��û�����÷���ֵ,���Ϊ`process_response`����һ������ֵ,�������ô����??

Ϊ�м��`middle_ware1`��`process_request`�������÷���ֵ

	return HttpResponse("request message")
ˢ�������,����˴�ӡ��Ϣ:
	
	middle_ware1.process_request
	middle_ware1.process_response
�ͻ����������ʾ��ϢΪ:

	request message
	
��ִ��`process_request`����,��Ϊ`process_request`�����з���ֵ,���򲻻���ִ�к�����м��,����ֱ��ִ��`process_response`����,Ȼ�󷵻���Ϣ���û�.

��ʵ��Ӧ����,`process_request`��������ֱ���趨����ֵ.����������趨����ֵ,�����ڷ���ֵǰ���������ж����.

�������趨��վ�ĺ�������ʱ�����Ϊ`process_request`�������÷���ֵ.

**�����м��ʵ�ֵļ��û���¼��֤**

����,��һ������ϵͳ��,���еĺ�̨����ҳ�涼�������û���¼����ܴ�,���Ի����м����ʵ���û���¼��֤

�����м��
```
    from django.utils.deprecation import MiddlewareMixin
    from django.shortcuts import HttpResponse,redirect
    
    class middle_ware1(MiddlewareMixin):
    
        def process_request(self,request):
            if request.path_info == "/login/":
                return None
    
            if not request.session.get("user_info"):
                return redirect("/login/")
    
        def process_response(self,request,response):
            print("middle_ware1.process_response")
            return response
```
��`settings.py`�ļ���ע���м��
```
	MIDDLEWARE = [
		'django.middleware.security.SecurityMiddleware',
		'django.contrib.sessions.middleware.SessionMiddleware',
		'django.middleware.common.CommonMiddleware',
		'django.middleware.csrf.CsrfViewMiddleware',
		'django.contrib.auth.middleware.AuthenticationMiddleware',
		'django.contrib.messages.middleware.MessageMiddleware',
		'django.middleware.clickjacking.XFrameOptionsMiddleware',
		'middleware.middleware.middle_ware1',
	]
```
�û�����index��ҳ,����ִ�е�`process_request`,��ִ��if not���,Ȼ���ض���`login`ҳ��,ʹ�û������û����������¼�����̨����ҳ��.

**Django�м�����÷���**

���������Ѿ��ù���`process_request`������`porcess_response`����,Django���м���������¼��ַ���.

***process_view����***
	
���������м������
```
    from django.utils.deprecation import MiddlewareMixin
    from django.shortcuts import HttpResponse,redirect
    
    class middle_ware1(MiddlewareMixin):
    
        def process_request(self,request):
            print("middle_ware1.process_request")
    
        def process_view(selfs,request,view_func,view_func_args,view_func_kwargs):
            print("middle_ware1.process_view")
    
        def process_response(self,request,response):
            print("middle_ware1.process_response")
            return response
    
    class middle_ware2(MiddlewareMixin):
    
        def process_request(self,request):
            print("middle_ware2.process_request")
    
        def process_view(self,request,view_func,view_func_args,view_func_kwargs):
            print("middle_ware2.process_view")
    
        def process_response(self,request,response):
            print("middle_ware2.process_response")
            return response
```
��`settings.py`�е�ע���м��
```	
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'middleware.middleware.middle_ware1',
    'middleware.middleware.middle_ware2',
]
```
��ͼ����
```
    def index(request):
    
        print("index page")
        return HttpResponse("index")
```
�������������`http://127.0.0.1:8000/index`ҳ��,�ڷ���˴�ӡ��Ϣ

	middle_ware1.process_request
	middle_ware2.process_request
	middle_ware1.process_view
	middle_ware2.process_view
	index page
	middle_ware2.process_response
	middle_ware1.process_response
��ǰ��ҳ����ʾ��Ϣ: 

	index
����ִ������:

��ִ�������м���е�`process_request`����-->����·��ƥ��-->ִ���м���еĵ�`process_view`����

-->ִ�ж�Ӧ����ͼ����-->ִ���м���е�`process_response`����

�����������,`process_view`������û������returnֵ.Ϊ`process_view`�������趨returnֵ,�����ֻ���ôִ����??

Ϊ`process_view`�����趨����ֵ
```
    from django.utils.deprecation import MiddlewareMixin
    from django.shortcuts import HttpResponse,redirect
    
    class middle_ware1(MiddlewareMixin):
    
        def process_request(self,request):
            print("middle_ware1.process_request")
    
        def process_view(selfs,request,view_func,view_func_args,view_func_kwargs):
            return HttpResponse("middle_ware1.process_view")
    
        def process_response(self,request,response):
            print("middle_ware1.process_response")
            return response
    
    class middle_ware2(MiddlewareMixin):
    
        def process_request(self,request):
            print("middle_ware2.process_request")
    
        def process_view(self,request,view_func,view_func_args,view_func_kwargs):
            return HttpResponse("middle_ware2.process_view")
    
        def process_response(self,request,response):
            print("middle_ware2.process_response")
```
ˢ�������,�ڷ���˴�ӡ��Ϣ����:

	middle_ware1.process_request
	middle_ware2.process_request
	middle_ware2.process_response
	middle_ware1.process_response
�ڿͻ��˵������ҳ����ʾ��Ϣ����:

	iddle_ware1.process_view

���Կ�����ͼ����`index`��û��ִ��,����ִ�������м����`process_request`������,���ִ��`process_view`����.

����`process_view`����������returnֵ,���Գ����е���ͼ������û��ִ��,����ִ�����м���е�`process_response`����.

**process_exception����**

�޸��м��
```
    from django.utils.deprecation import MiddlewareMixin
    from django.shortcuts import HttpResponse,redirect
    
    class middle_ware1(MiddlewareMixin):
    
        def process_request(self,request):
            print("middle_ware1.process_request")
    
        def process_view(selfs,request,view_func,view_func_args,view_func_kwargs):
            print("middle_ware1.process_view")
    
        def process_exception(self,request,exvception):
            print("middleware1.process_exception")
    
        def process_response(self,request,response):
            print("middle_ware1.process_response")
            return response
    
    class middle_ware2(MiddlewareMixin):
    
        def process_request(self,request):
            print("middle_ware2.process_request")
    
        def process_view(self,request,view_func,view_func_args,view_func_kwargs):
            print("middle_ware2.process_view")
    
        def process_exception(self,request,exception):
            print("middleware2.process_exception")
    
        def process_response(self,request,response):
            print("middle_ware2.process_response")
            return response
```
ˢ�������,����˴�ӡ��Ϣ

	middle_ware1.process_request
	middle_ware2.process_request
	middle_ware1.process_view
	middle_ware2.process_view
	hello,index page
	middle_ware2.process_response
	middle_ware1.process_response

���ݷ���˵Ĵ�ӡ��Ϣ���Կ���,`process_exception`����û��ִ��,Ϊʲô��??

������Ϊ����Ĵ���û��bug.���������д���,���ֱ�����Ϣ��ʱ��,`process_exception`�Ż�ִ��

�����ھ�ģ���ó�����ִ���,�۲�`process_exception`������ִ�����

�޸���ͼ����
```
    def index(request):
    
        print("index page")
        int("aaaa")
        return HttpResponse("index")
```
ˢ�������,����˺�̨��ӡ��Ϣ

	middle_ware1.process_request
	middle_ware2.process_request
	middle_ware1.process_view
	middle_ware2.process_view
	index page
	middleware2.process_exception
	middleware1.process_exception
	Internal Server Error: /index
	Traceback (most recent call last):
	......
	ValueError: invalid literal for int() with base 10: 'aaaa'
	middle_ware2.process_response
	middle_ware1.process_response

�ɷ���˵ı�����Ϣ��֪,���`process_exception`������Ȼִ����.

�ɴ�����֪��,�������д���,�м���е�`process_exception`�����Ż�ִ��,�������������е�ʱ��,��������򲻻�ִ��

�ղŵĴ�����,`process_exception`����û�����÷���ֵ,���Ϊ`process_exception`�������÷���ֵ,�����ִ�����̻�����ô����???

�޸��м��,Ϊ�����м����`process_exception`���������÷���ֵ
```
    from django.utils.deprecation import MiddlewareMixin
    from django.shortcuts import HttpResponse,redirect
    
    class middle_ware1(MiddlewareMixin):
    
        def process_request(self,request):
            print("middle_ware1.process_request")
    
        def process_view(selfs,request,view_func,view_func_args,view_func_kwargs):
            print("middle_ware1.process_view")
    
        def process_exception(self,request,exvception):
            print("middleware1.process_exception")
            return HttpResponse("bug1")
    
        def process_response(self,request,response):
            print("middle_ware1.process_response")
            return response
    
    class middle_ware2(MiddlewareMixin):
    
        def process_request(self,request):
            print("middle_ware2.process_request")
    
        def process_view(self,request,view_func,view_func_args,view_func_kwargs):
            print("middle_ware2.process_view")
    
        def process_exception(self,request,exception):
            print("middleware2.process_exception")
            return HttpResponse("bug2")
    
        def process_response(self,request,response):
            print("middle_ware2.process_response")
            return response
```
��ͼ����
```
    def index(request):
    
        print("index page")
        int("aaaa")
        return HttpResponse("index")
```
ˢ��ҳ��,����˴�ӡ��Ϣ

middle_ware1.process_request
middle_ware2.process_request
middle_ware1.process_view
middle_ware2.process_view
index page
middleware2.process_exception
middle_ware2.process_response
middle_ware1.process_response

�����������ҳ��������Ϣ

	bug2
�����ִ������Ϊ:
	
�ͻ��˷�����http���󵽴��м��,ִ���м���е�`process_request`����,Ȼ����ִ��·��ƥ��,Ȼ��ִ��`process_view`����,

Ȼ��ִ����Ӧ����ͼ����,���ִ��`process_response`����,������Ϣ���ͻ��������.

���ִ����ͼ����ʱ�������д���,�м���е�`process_exception`������׽���쳣�ͻ�ִ��,������`process_exception`�����Ͳ�����ִ����.

`process_exception`����ִ�����,�����ִ�����е�`process_response`����.

**process_template_response����**

process_template_response����Ĭ��Ҳ���ᱻִ��,
	
�޸��м��
```
    from django.utils.deprecation import MiddlewareMixin
    from django.shortcuts import HttpResponse,redirect
    
    class middle_ware1(MiddlewareMixin):
    
        def process_request(self,request):
            print("middle_ware1.process_request")
    
        def process_view(selfs,request,view_func,view_func_args,view_func_kwargs):
            print("middle_ware1.process_view")
    
        def process_exception(self,request,exvception):
            print("middle_ware1.process_exception")
            return HttpResponse("bug1")
    
        def process_response(self,request,response):
            print("middle_ware1.process_response")
            return response
    
        def process_template_response(self,request,response):
            print("middle_ware1.process_template_response")
            return response
    
    class middle_ware2(MiddlewareMixin):
    
        def process_request(self,request):
            print("middle_ware2.process_request")
    
        def process_view(self,request,view_func,view_func_args,view_func_kwargs):
            print("middle_ware2.process_view")
    
        def process_exception(self,request,exception):
            print("middleware2.process_exception")
            return HttpResponse("bug2")
    
        def process_response(self,request,response):
            print("middle_ware2.process_response")
            return response
    
        def process_template_response(self,request,response):
            print("middle_ware2.process_template_response")
            return response
```
�޸���ͼ����,ʹ��ͼ��������ִ��
```

    def index(request):
    
        print("index page")
        return HttpResponse("index")
```
ˢ�������,����˺�̨��ӡ��Ϣ����:
	
	middle_ware1.process_request
	middle_ware2.process_request
	middle_ware1.process_view
	middle_ware2.process_view
	index page
	middle_ware2.process_response
	middle_ware1.process_response
���Կ���,������������,`process_template_response`����û��ִ��.
	
��ʵ��,`process_template_response`������ִ��ȡ������ͼ�����ķ��ص���Ϣ,

��ͼ�������ʹ��render����������Ϣ,�м�����`process_template_response`�����ͻᱻִ��.

�޸���ͼ����,����һ����,���������response
```
    class MyResponse(object):
        def __init__(self,response):
            self.response=response
    
        def render(self):
            return self.response
    
    def index(request):
    
        response=HttpResponse("index page")
        return MyResponse(response)
```
MyResponse�෵�ص����Զ���Ķ���,���������ߵ�����`render`����.

index��ͼ������,�ȵ�����`HttpResponse`����������Ϣ,��ʹ��`MyResponse`���е�`render`����������`HttpResponse`.

ִ�г���,����˺�̨��ӡ��Ϣ����:

	middle_ware1.process_request
	middle_ware2.process_request
	middle_ware1.process_view
	middle_ware2.process_view
	middle_ware2.process_template_response
	middle_ware1.process_template_response
	middle_ware2.process_response
	middle_ware1.process_response

���Կ���,`process_template_response`�����Ѿ�ִ��.

`process_template_response`���ô�	

    ���Ҫ�Է��ص�HttpResponse���ݽ��д���,���԰�Ҫ�������Ϣ��װ��һ������
    ֻҪ���ﶨ����render����,process_template_response�����Ż�ִ��.
    	
**�ܽ�**

* �м���ﱾ���Ͼ���һ����,
* ��ȫ�ֵ�http�����������ʱ�����ʹ���м��
* �м���еķ�����һ��Ҫȫ��ʹ��,��Ҫ�ĸ����ĸ�	
* process_request����������return,һ��Ҫʹ��return��ʱ��,Ҫ��������ж����ִ��
* process_response����һ��Ҫ��return,�����������д���
* process_view����������return,������ͼ��������ִ��
* process_exception����ֻ���ڳ���������д����ʱ��Ż�ִ��
* process_exception�����趨returnʱ,���򲻻���ִ�к����м���е�process_exception
* process_template_response����ֻ������ͼ������ʹ��render����������Ϣ��ʱ��Ż�ִ��