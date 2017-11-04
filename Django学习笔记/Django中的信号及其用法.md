Django���ṩ��"�źŵ���",�����ڿ��ִ�в���ʱ����.

һЩ����������ʱ��,ϵͳ������źŶ���ĺ���ִ����Ӧ�Ĳ���

**Django�����õ�signal**

***Model_signals***

    pre_init                        # Django�е�model����ִ���乹�췽��ǰ,�Զ�����
    post_init                       # Django�е�model����ִ���乹�췽����,�Զ�����
    pre_save                        # Django�е�model���󱣴�ǰ,�Զ�����
    post_save                       # Django�е�model���󱣴��,�Զ�����
    pre_delete                      # Django�е�model����ɾ��ǰ,�Զ�����
    post_delete                     # Django�е�model����ɾ����,�Զ�����
    m2m_changed                     # Django�е�model����ʹ��m2m�ֶβ������ݿ�ĵ����ű�(add,remove,clear,update),�Զ�����
    class_prepared                  # ��������ʱ,��⵽��ע���model��,����ÿһ����,�Զ�����
***Managemeng_signals***
    
    pre_migrate                     # ִ��migrate����ǰ,�Զ�����
    post_migrate                    # ִ��migrate�����,�Զ����� 
***Request/response_signals***

    request_started                 # ������ǰ,�Զ�����
    request_finished                # ���������,�Զ�����
    got_request_exception           # �����쳣ʱ,�Զ�����
***Test_signals***

    setting_changed                 # �����ļ��ı�ʱ,�Զ�����
    template_rendered               # ģ��ִ����Ⱦ����ʱ,�Զ�����
***Datebase_Wrapperd***
    
    connection_created              # �������ݿ�����ʱ,�Զ�����
����Django���õ��ź�,����ע��ָ���ź�,������ִ����Ӧ����ʱ,ϵͳ���Զ�����ע�ắ��

����,�������ݿ��¼,����`pre_save`��`post_save`�ź�

����һ��Django��Ŀ,���ú�·��ӳ��

`models.py`�еĴ���:

    from django.db import models
    
    class UserInfo(models.Model):
        name=models.CharField(max_length=32)
        pwd=models.CharField(max_length=64)
`views.py`�еĴ���:

    from django.shortcuts import render,HttpResponse
    from app01 import  models
    
    def index(request):
        models.UserInfo.objects.create(name="mysql",pwd="mysql123")
        return HttpResponse("ok")
��Ŀ��`__init__.py`�ļ��д���:
    
    from django.db.models.signals import pre_save,post_save
    
    def pre_save_func(sender,**kwargs):
    
        print("pre_save_func")
        print("pre_save_msg:",sender,kwargs)
    
    def post_save_func(sender,**kwargs):
        print("post_save_func")
        print("post_save_msg:",sender,kwargs)
    
    pre_save.connect(pre_save_func)             # models���󱣴�ǰ����callback����
    post_save.connect(post_save_func)           # models���󱣴�󴥷�����
����һ��`index.html`��ҳ,��������������Ŀ,�ڷ���˺�̨��ӡ��Ϣ����:

    pre_save_func
    pre_save_msg: <class 'app01.models.UserInfo'> {'signal': <django.db.models.signals.ModelSignal object at 0x0000000002E62588>, 
    'instance': <UserInfo: UserInfo object>, 'raw': False, 'using': 'default', 'update_fields': None}
    
    post_save_func
    post_save_msg: <class 'app01.models.UserInfo'> {'signal': <django.db.models.signals.ModelSignal object at 0x0000000002E62630>, 
    'instance': <UserInfo: UserInfo object>, 'created': True, 'update_fields': None, 'raw': False, 'using': 'default'}
�Ƚϴ�ӡ�Ľ��,���Կ���models���󱣴��,�ڴ�ӡ��Ϣ�����һ��`"create=True"`�ļ�ֵ��.

Ҳ����ʹ��װ�����������ź�,������`__init__.py`�еĴ����޸�:

    from django.core.signals import request_finished
    from django.dispatch import receiver
    
    @receiver(request_finished)
    def callback(sender, **kwargs):
        print("Request finished!")
���ڱ�������������Զ�����callback����,�ں�̨`"request finished"`��仰.

**�Զ����ź�**

1.�����ź�

�½�һ����Ŀ,���ú�·��,����Ŀ��Ŀ¼�´���һ��`singal_test.py`���ļ�,����Ϊ

    import django.dispatch
    
    action=django.dispatch.Signal(providing_args=["aaaa","bbbb"])
	
2. ע���ź� 

��ĿӦ�������`__init__.py`�ļ�����:

    from singal_test import action

    def pre_save_func(sender,**kwargs):
    
        print("pre_save_func")
        print("pre_save_msg:",sender,kwargs)
        
    action.connect(pre_save_func)
	
3. �����ź�

views��ͼ��������:

    from singal_test import action

    action.send(sender="python",aaa="111",bbb="222")
���������`index.html`��ҳ,��̨��ӡ��Ϣ����:

    pre_save_func 
    pre_save_msg: python {'signal': <django.dispatch.dispatcher.Signal object at 0x000000000391D710>, 'aaa': '111', 'bbb': '222'}
���������źŵĴ������Ѿ����ɵ�Django��,���Ի��Զ�����,�������Զ����ź���Ҫ������λ�ô���