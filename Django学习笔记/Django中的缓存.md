1.����ļ��

�ڶ�̬��վ��,�û����е�����,����������ȥ���ݿ��н�����Ӧ����,ɾ,��,��,��Ⱦģ��,ִ��ҵ���߼�,��������û�������ҳ��.

��һ����վ���û��������ܴ��ʱ��,ÿһ�εĵĺ�̨����,�������ĺܶ�ķ������Դ,���Ա���ʹ�û����������˷�������ѹ��.

�����ǽ�һЩ���õ����ݱ����ڴ����memcache��,��һ����ʱ����������������Щ����ʱ,����ȥִ�����ݿ⼰��Ⱦ�Ȳ���,����ֱ�Ӵ��ڴ��memcache�Ļ�����ȥȡ������,Ȼ�󷵻ظ��û�.

2.Django�ṩ��6�ֻ��淽ʽ

* �������Ի���
* �ڴ滺��
* �ļ�����
* ���ݿ⻺��
* Memcache����(ʹ��python-memcachedģ��)
* Memcache����(ʹ��pylibmcģ��)

����ʹ�õ����ļ������Mencache����

2.1 ���ֻ��淽ʽ�������ļ�˵�� 

2.1.1 ��������(��ģʽΪ��������ʹ��,ʵ���ϲ�ִ���κβ���)

settings.py�ļ�����
    
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.dummy.DummyCache',     # �����̨ʹ�õ�����
            'TIMEOUT': 300,                                               # ���泬ʱʱ�䣨Ĭ��300�룬None��ʾ�������ڣ�0��ʾ�������ڣ�
            'OPTIONS':{
                'MAX_ENTRIES': 300,                                       # ��󻺴��¼��������Ĭ��300��
                'CULL_FREQUENCY': 3,                                      # ���浽��������֮���޳���������ı���������1/CULL_FREQUENCY��Ĭ��3��
            },
        }
    }

2.1.2 �ڴ滺��(���������ݱ������ڴ�������)

settings.py�ļ�����

    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',     # ָ������ʹ�õ�����
            'LOCATION': 'unique-snowflake',                                 # д���ڴ��еı�����Ψһֵ 
            'TIMEOUT':300,                                                  # ���泬ʱʱ��(Ĭ��Ϊ300��,None��ʾ��������)
            'OPTIONS':{
                'MAX_ENTRIES': 300,                                         # ��󻺴��¼��������Ĭ��300��
                'CULL_FREQUENCY': 3,                                        # ���浽��������֮���޳���������ı���������1/CULL_FREQUENCY��Ĭ��3��
            }      
        }
    }
    
2.1.3 �ļ�����(�ѻ������ݴ洢���ļ���)

settings.py�ļ�����

    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',   #ָ������ʹ�õ�����
            'LOCATION': '/var/tmp/django_cache',                                #ָ�������·��
            'TIMEOUT':300,                                                      #���泬ʱʱ��(Ĭ��Ϊ300��,None��ʾ��������)
            'OPTIONS':{
                'MAX_ENTRIES': 300,                                             # ��󻺴��¼��������Ĭ��300��
                'CULL_FREQUENCY': 3,                                            # ���浽��������֮���޳���������ı���������1/CULL_FREQUENCY��Ĭ��3��
            }
        }           
    }

2.1.4 ���ݿ⻺��(�ѻ������ݴ洢�����ݿ���)

settings.py�ļ�����

    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.db.DatabaseCache',       # ָ������ʹ�õ�����
            'LOCATION': 'cache_table',                                      # ���ݿ��                
            'OPTIONS':{
                'MAX_ENTRIES': 300,                                         # ��󻺴��¼��������Ĭ��300��
                'CULL_FREQUENCY': 3,                                        # ���浽��������֮���޳���������ı���������1/CULL_FREQUENCY��Ĭ��3��
            }     
        }           
    }
ע��,������������ݿ��ʹ�õ����:
    
    python manage.py createcachetable

Memcached��Djangoԭ��֧�ֵĻ���ϵͳ.Ҫʹ��Memcached,��Ҫ����Memcached��֧�ֿ�`python-memcache`d��`pylibmc`.

2.1.5 Memcache����(ʹ��python-memcachedģ������memcache)

settings.py�ļ�����

    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',   # ָ������ʹ�õ�����
            'LOCATION': '192.168.10.100:11211',                                 # ָ��Memcache�����������IP��ַ�Ͷ˿�
            'OPTIONS':{
                'MAX_ENTRIES': 300,                                             # ��󻺴��¼��������Ĭ��300��
                'CULL_FREQUENCY': 3,                                            # ���浽��������֮���޳���������ı���������1/CULL_FREQUENCY��Ĭ��3��
            }
        }
    }

LOCATIONҲ�������ó�����:

    'LOCATION': 'unix:/tmp/memcached.sock',         # ָ���������ڵ���������socket�׽���ΪMemcache���������
    'LOCATION': [                                   # ָ��һ̨���̨��������ip��ַ�Ӷ˿�ΪMemcache���������
        '192.168.10.100:11211',
        '192.168.10.101:11211',
        '192.168.10.102:11211',
    ]

2.1.6 Memcache����(ʹ��pylibmcģ������memcache)

    settings.py�ļ�����
        CACHES = {
            'default': {
                'BACKEND': 'django.core.cache.backends.memcached.PyLibMCCache',     # ָ������ʹ�õ�����
                'LOCATION':'192.168.10.100:11211',                                  # ָ��������11211�˿�ΪMemcache���������
                'OPTIONS':{
                    'MAX_ENTRIES': 300,                                             # ��󻺴��¼��������Ĭ��300��
                    'CULL_FREQUENCY': 3,                                            # ���浽��������֮���޳���������ı���������1/CULL_FREQUENCY��Ĭ��3��
                },     
            }
        }

LOCATIONҲ�������ó�����:

    'LOCATION': '/tmp/memcached.sock',      # ָ��ĳ��·��Ϊ����Ŀ¼
    'LOCATION': [                           # �ֲ�ʽ����,�ڶ�̨������������Memcached����,�����Ѷ�̨����������һ�������Ļ���,��������ÿ̨�������ϸ��ƻ���ֵ
        '192.168.10.100:11211',
        '192.168.10.101:11211',
        '192.168.10.102:11211',
    ]
    
`Memcached�ǻ����ڴ�Ļ���`,���ݴ洢���ڴ���.������������������Ļ�,���ݾͻᶪʧ,����`Memcached`һ���������������ʹ��

3.Django�еĻ���Ӧ��

Django�ṩ�˲�ͬ���ȵĻ���,���Ի���ĳ��ҳ��,����ֻ����һ��ҳ���ĳ������,�������Ի���������վ.

3.1 ������ͼ����

����,Ϊ������ͼ������ӻ���

·������:

    url(r'^index$',views.index),
���ݿ�

![](http://images2017.cnblogs.com/blog/1133627/201709/1133627-20170920195358415-856446810.png)

views����:

    from app01 import  models
    from django.views.decorators.cache import cache_page
    import time
    
    @cache_page(15)                                 #��ʱʱ��Ϊ15��
    def index(request):
        user_list=models.UserInfo.objects.all()     #�����ݿ���ȡ�����е��û�����
        ctime=time.time()                           #��ȡ��ǰʱ��
        return render(request,"index.html",{"user_list":user_list,"ctime":ctime})
index.html����:

    body>
    <h1>{{ ctime }}</h1>
    <ul>
        {% for user in user_list %}
            <li>{{ user.name }}</li>
        {% endfor %}
    </ul>
    </body>

��Ϊ�����ԭ��,��ͣ��ˢ�������ʱ�ᷢ��,ҳ������ʾ��ʱ��ÿ15���ӱ仯һ��.

������ˢ���������ʱ��,���������ݿ������һ���û�����,��ʱ����ˢ�������,ǰ��ҳ���ϲ�����ʾ�ղ���ӵ��û�

һֱˢ�������15���,����ӵ��û�������ǰ��ҳ������ʾ����.

����������ǻ����ڴ�Ļ�������,�����ļ��Ļ������ô������??

����settings.py������

    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',   # ָ������ʹ�õ�����
            'LOCATION': 'E:\django_cache',                                      # ָ�������·��
            'TIMEOUT': 300,                                                     # ���泬ʱʱ��(Ĭ��Ϊ300��,None��ʾ��������)
            'OPTIONS': {
                'MAX_ENTRIES': 300,                                             # ��󻺴��¼��������Ĭ��300��
                'CULL_FREQUENCY': 3,                                            # ���浽��������֮���޳���������ı���������1/CULL_FREQUENCY��Ĭ��3��
            }
        }
    }
Ȼ���ٴ�ˢ�������,���Կ����ڸղ����õ�Ŀ¼�����ɵĻ����ļ�

![](http://images2017.cnblogs.com/blog/1133627/201709/1133627-20170920195341509-956796075.png)

ͨ��ʵ�����֪��,Django�����Լ�����ʽ�ѻ����ļ������������ļ���ָ����Ŀ¼��.

3.2 ȫվʹ�û���

��Ȼ��ȫվ����,��ȻҪʹ��Django�е��м��.

�û�������ͨ���м��,����һϵ�е���֤�Ȳ���,�������������ڻ����д���,��ʹ��`FetchFromCacheMiddleware`��ȡ���ݲ����ظ��û�

�����ظ��û�֮ǰ,�жϻ������Ƿ��Ѿ�����,���������,��`UpdateCacheMiddleware`�Ὣ���汣����Django�Ļ���֮��,��ʵ��ȫվ����

�޸�settings.py�����ļ�

    MIDDLEWARE = [
        'django.middleware.cache.UpdateCacheMiddleware',            #��ӦHttpResponse�����ü���headers
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
        'django.middleware.cache.FetchFromCacheMiddleware',         #��������ͨ��GET��HEAD������ȡ��״̬��Ϊ200����Ӧ
    ]
    
    CACHE__MIDDLEWARE_SECONDS=15                                    # �趨��ʱʱ��Ϊ15��
    
views��ͼ����

    from django.shortcuts import render
    import time
    
    def index(request):
        ctime = time.time()
        return render(request,'index.html',{'ctime':ctime})
������벻��,ˢ���������15��,ҳ���ϵ�ʱ��仯һ��,������ʵ����ȫվ����. 

3.3 �ֲ���ͼ����

����,ˢ��ҳ��ʱ,������ҳ��һ����ʵ�ֻ���

views��ͼ����

    from django.shortcuts import render
    import time
    
    def index(request):
        # user_list = models.UserInfo.objects.all()
        ctime = time.time()
        return render(request,'index.html',{'ctime':ctime})     
ǰ����ҳ

    {% load cache %}                # ���ػ���
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Title</title>
    </head>
    <body>
    <h1>{{ ctime }}</h1>
    {% cache 15 'aaa' %}            # �趨��ʱʱ��Ϊ15��
        <h1>{{ ctime }}</h1>
    {% endcache %}
    </body>
    </html>
ˢ����������Կ���,��һ��ʱ��ʵʱ�仯,����һ��ʱ��ÿ15���ӱ仯һ��