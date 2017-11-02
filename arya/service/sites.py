#!/usr/bin/env python
# -*- coding:utf-8 -*-
import copy
import json
from django.shortcuts import HttpResponse, render, redirect
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.http.request import QueryDict
from arya.utils.pagination import Page
from django.forms import ModelForm
from types import FunctionType
from django.db.models import ForeignKey, ManyToManyField
import functools
from django.db.models import Q


class FilterRow(object):
    """
    生成筛选a标签
    """
    def __init__(self, option, change_list, data_list, param_dict=None, is_choices=False):
        self.option = option

        self.data_list = data_list

        self.param_dict = copy.deepcopy(param_dict)

        self.param_dict._mutable = True

        self.change_list = change_list

        self.is_choices = is_choices

    def __iter__(self):

        base_url = self.change_list.model_config.changelist_url
        tpl = "<a href='{0}' class='{1}'>{2}</a>"
        # 全部
        if self.option.name in self.param_dict:
            pop_value = self.param_dict.pop(self.option.name)
            url = "{0}?{1}".format(base_url, self.param_dict.urlencode())
            val = tpl.format(url, '', '全部')
            self.param_dict.setlist(self.option.name, pop_value)
        else:
            url = "{0}?{1}".format(base_url, self.param_dict.urlencode())
            val = tpl.format(url, 'active', '全部')

        # self.param_dict

        yield mark_safe("<div class='whole'>")
        yield mark_safe(val)
        yield mark_safe("</div>")

        yield mark_safe("<div class='others'>")
        for obj in self.data_list:

            param_dict = copy.deepcopy(self.param_dict)

            if self.is_choices:
                pk = str(obj[0])
                text = obj[1]
            else:
                # url上要传递的值
                pk = self.option.val_func_name(obj) if self.option.val_func_name else obj.pk
                pk = str(pk)

                # a标签上显示的内容
                text = self.option.text_func_name(obj) if self.option.text_func_name else str(obj)

            exist = False
            if pk in param_dict.getlist(self.option.name):
                exist = True

            if self.option.is_multi:
                if exist:
                    values = param_dict.getlist(self.option.name)
                    values.remove(pk)
                    param_dict.setlist(self.option.name, values)
                else:
                    param_dict.appendlist(self.option.name, pk)
            else:
                param_dict[self.option.name] = pk
            url = "{0}?{1}".format(base_url, param_dict.urlencode())
            val = tpl.format(url, 'active' if exist else '', text)
            yield mark_safe(val)
        yield mark_safe("</div>")

class FilterOption(object):
    """
    组合搜索配置
    """

    def __init__(self, field_or_func, condition=None, is_multi=False, text_func_name=None, val_func_name=None):
        """
        :param field_or_func:在列表页面进行过滤的字段或自定义函数
        :param condition: 列表页面要进行过滤的条件
        :param is_multi: 是否支持多选
        :param text_func_name:在Model中定义函数，显示文本名称，默认使用 str(对象)
        :param val_func_name:在Model中定义函数，显示文本名称，默认使用 对象.pk

        list_filter = [
            sites.FilterOption('name',False,lambda x:x.name,lambda x:x.name),
            sites.FilterOption('consultant', condition=Q(depart_id=2)),
            sites.FilterOption('course',is_multi=True),
            sites.FilterOption('gender'),
        ]

        """
        self.field_or_func = field_or_func
        self.is_multi = is_multi
        self.text_func_name = text_func_name
        self.val_func_name = val_func_name
        self.condition = condition

    @property
    def is_func(self):
        if isinstance(self.field_or_func, FunctionType):
            return True

    @property
    def name(self):
        if self.is_func:
            return self.field_or_func.__name__      # 如果列表页面过滤条件为一个函数,则返回函数的名字
        else:
            return self.field_or_func       # 列表页面过滤条件为一个字段,返回字段的名字

    @property
    def get_condition(self):

        if self.condition:
            return self.condition
        con = Q()
        return con


class ChangeList(object):
    """
    封装列表页面需要字段或功能
    """
    def __init__(self, model_config, result_list):
        """
        :param model_config: 如果注册类时没有定义model_config.则model_config为AryaConfig
            sites.site.register(models.ClassList,ClassListConfig)       model_config== ClassListConfig
            sites.site.register(models.ClassList)                       model_config== AryaConfig
        :param result_list:
        """
        self.model_config = model_config

        self.show_add_btn = model_config.get_show_add_btn()
        self.list_display = model_config.get_show_list_display()
        self.actions = model_config.get_actions()
        self.list_filter = model_config.get_list_filter()
        self.search_list = model_config.get_search_list()

        # self.result_list = result_list
        all_count = result_list.count()
        query_params = copy.copy(model_config.request.GET)
        query_params._mutable = True

        self.pager = Page(model_config.request.GET.get('page'), all_count, base_url=model_config.changelist_url,
                          query_params=query_params)                # 实例化分页对象
        self.result_list = result_list[self.pager.start:self.pager.end]         # 在一个列表页面要显示的数据个数

    def add_html(self):
        """
        添加按钮
        :return: 
        """
        add_html = mark_safe('<a class="btn btn-primary" href="%s">添加</a>' % (self.model_config.add_url_params,))
        return add_html

    def gen_list_filter(self):

        for option in self.model_config.list_filter:

            if option.is_func:
                data_list = option.field_or_func(self.model_config, self, option)
            else:
                _field = self.model_config.model_class._meta.get_field(option.field_or_func)

                if isinstance(_field, ForeignKey):
                    data_list = FilterRow(option, self, _field.rel.model.objects.filter(option.get_condition),
                                          self.model_config.request.GET)
                elif isinstance(_field, ManyToManyField):
                    data_list = FilterRow(option, self, _field.rel.model.objects.filter(option.get_condition),
                                          self.model_config.request.GET)
                else:
                    print(_field.choices)  # [(),()]
                    data_list = FilterRow(option, self, _field.choices, self.model_config.request.GET, is_choices=True)
            yield data_list

    def search_attr(self):
        val = self.model_config.request.GET.get(self.model_config.q)
        return {"value": val, 'name': self.model_config.q}


class AryaConfig(object):
    """
    基础配置类,主要用于处理请求
    """

    """定制数据列表"""
    list_display = []       # 在这个列表中定义了table的哪些列,列表页面就显示哪些列

    def list_display_checkbox(self, obj=None, is_header=False):
        """
        生成列表表头和checkbox
        :param obj:传递过来的用户对象
        :param is_header:判断数据是否是表头
        :return:
        """
        if is_header:
            tpl = "<input type='checkbox' id='headCheckBox' />"
        else:
            tpl = "<input type='checkbox' name='pk' value='{0}' />".format(obj.pk)

        return mark_safe(tpl)

    def list_display_edit(self, obj=None, is_header=False):
        """
        如果是表头,则表头显示"操作",否则显示编辑和删除按钮
        :param obj:
        :param is_header:
        :return:
        """
        if is_header:
            return '操作'
        else:
            tpl = "<a href='{0}?{2}'>编辑</a> | <a href='{1}?{2}'>删除</a>".format(
                self.change_url(obj.pk),self.delete_url(obj.pk),self.back_url_param())
            return mark_safe(tpl)

    def get_show_list_display(self):
        list_display = []
        if self.list_display:
            list_display.extend(self.list_display)
            list_display.insert(0, AryaConfig.list_display_checkbox)
            list_display.append(AryaConfig.list_display_edit)

        return list_display

    """定制添加按钮数据列表"""
    show_add_btn = True

    def get_show_add_btn(self):
        return self.show_add_btn

    """定制Action"""
    actions = []

    def delete_action(self, request):
        """
        定制Action行为
        :param request: 
        :param queryset: 
        :return: 
        """
        pk_list = request.POST.getlist('pk')
        # self.model_class.filter(id__in=pk_list).delete()

    delete_action.short_description = "删除选择项"

    def get_actions(self):
        actions = []
        actions.extend(AryaConfig.actions)
        actions.append(AryaConfig.delete_action)

        return actions

    """ModelForm"""
    model_form = None

    def get_model_form_class(self):
        model_form_cls = self.model_form
        if not model_form_cls:
            _meta = type('Meta', (object,), {'model': self.model_class, "fields": "__all__"})
            model_form_cls = type('DynamicModelForm', (ModelForm,), {'Meta': _meta})
        return model_form_cls

    """定制查询组合条件"""
    list_filter = []

    def get_list_filter(self):
        return self.list_filter

    @property
    def get_list_filter_condition(self):
        # 字段，FK，choice
        # fields1 = [obj.name for obj in self.model_class._meta.fields]
        # print(fields1)

        # 获取多对多
        # fields2 = [obj.name for obj in self.model_class._meta.many_to_many]
        # print(fields2)

        # 包含反向关联字段
        fields3 = [obj.name for obj in self.model_class._meta._get_fields()]
        print(fields3)

        # fields = [obj.name for obj in self.model_class._meta.]
        # print(fields)


        # 去请求URL中获取参数
        # 根据参数生成条件
        con = {}
        params = self.request.GET
        for k in params:
            # 判断k是否在数据库字段支持
            if k not in fields3:
                continue
            v = params.getlist(k)
            k = "{0}__in".format(k)
            con[k] = v
        return con

    """模糊搜素"""
    search_list = []

    def get_search_list(self):
        search_list = []
        search_list.extend(self.search_list)
        return search_list

    @property
    def get_search_condition(self):
        con = Q()           # 定义Q对象
        con.connector = "OR"    # 定义Q查询的连接方法
        # asdfasdf
        val = self.request.GET.get(self.q)      # 获取网页中的要进行搜索的值
        if not val:
            return con
        # ['qq__contains','name]
        field_list = self.get_search_list()
        for field in field_list:
            field = "{0}__contains".format(field)
            con.children.append((field, val))

        return con

    def __init__(self, model_class, site):

        self.q = "q"
        self.change_filter_name = "_change_filter"
        self.popup_key = "_popup"

        self.model_class = model_class
        self.app_label = model_class._meta.app_label
        self.model_name = model_class._meta.model_name
        self.site = site
        self.request = None

    def changelist_view(self, request, *args, **kwargs):
        """
        显示列表页面
        :param request: 
        :param args: 
        :param kwargs: 
        :return: 列表页面arya/change_list_html
        """
        self.request = request
        if request.method == "POST":
            action_name = request.POST.get('action')
            action_func = getattr(self, action_name, None)
            if action_func:
                action_func(request)

        # data_list = self.model_class.objects.all()
        # 去请求中获取url参数,根据参数生成过滤条件
        # 因为一个用户可能符合多个条件,所以列出的用户可能有重复,去distinct()进行去重
        data_list = self.model_class.objects.filter(**self.get_list_filter_condition).filter(
            self.get_search_condition).distinct()

        cl = ChangeList(self, data_list)    # 执行ChangeList方法对data_list进行分页
        context = {
            'cl': cl,
        }
        return render(request, 'arya/change_list.html', context)

    def save(self, form, add_or_update=False):
        """
        保存
        :param form: 
        :param add_or_update: True表示添加,False表示更新 
        :return: 
        """
        return form.save()

    def add_view(self, request, *args, **kwargs):
        """
        添加页面
        :param request: 
        :param args: 
        :param kwargs: 
        :return: 
        """
        model_form_cls = self.get_model_form_class()
        popup_id = request.GET.get(self.popup_key)
        if request.method == 'GET':
            form = model_form_cls()
            return render(request, "arya/add_popup.html" if popup_id else "arya/add.html", {'form': form})
        elif request.method == "POST":
            form = model_form_cls(data=request.POST, files=request.FILES)
            if form.is_valid():
                obj = self.save(form, True)
                if obj:
                    if popup_id:
                        context = {'pk': obj.pk, 'value': str(obj), 'popup_id': popup_id}
                        return render(request, 'arya/popup_response.html', {"popup_response_data": json.dumps(context)})
                    else:
                        return redirect(self.changelist_url_params)
            return render(request, "arya/add_popup.html" if popup_id else "arya/add.html", {'form': form})

    def delete_view(self, request, pk, *args, **kwargs):
        self.model_class.objects.filter(pk=pk).delete()

        return redirect(self.changelist_url_params)

    def change_view(self, request, pk, *args, **kwargs):
        """
        修改页面
        :param request: 
        :param pk: 
        :param args: 
        :param kwargs: 
        :return: 
        """
        print(self.model_class, type(self.model_class))
        obj = self.model_class.objects.filter(pk=pk).first()
        if not obj:
            return redirect(self.changelist_url)
        model_form_class = self.get_model_form_class()
        if request.method == "GET":
            form = model_form_class(instance=obj)
            return render(request, 'arya/change.html', {'form': form})
        elif request.method == "POST":
            form = model_form_class(instance=obj, data=request.POST, files=request.FILES)
            if form.is_valid():
                if self.save(form, False):
                    return redirect(self.changelist_url_params)
            return render(request, 'arya/change.html', {'form': form})

    # 反向生成URL相关
    def back_url_param(self):
        query = QueryDict(mutable=True)
        if self.request.GET:
            query[self.change_filter_name] = self.request.GET.urlencode()
        return query.urlencode()

    def delete_url(self, pk):
        """
        reverse反向生成删除url
        :param pk: 被删除对象的id,作为一个参数传给list_display_edit方法
        :return:
        """
        base_url = reverse('{0}:{1}_{2}_delete'.format(self.site.namespace, self.app_label, self.model_name),
                           args=(pk,))

        return base_url

    def change_url(self, pk):
        """
        reverse反向生成编辑的url
        :param pk: 等于被编辑对象的id,作为一个参数传给反向生成url方法list_display_edit
        :return:
        """
        base_url = reverse('{0}:{1}_{2}_change'.format(self.site.namespace, self.app_label, self.model_name),
                           args=(pk,))
        return base_url

    @property
    def add_url(self):
        """
        reverse反向生成添加的url
        :return:
        """
        base_url = reverse("{0}:{1}_{2}_add".format(self.site.namespace, self.app_label, self.model_name))
        return base_url

    @property
    def add_url_params(self):
        base_url = self.add_url
        if self.request.GET:
            return base_url
        else:
            query = QueryDict(mutable=True)
            query[self.change_filter_name] = self.request.GET.urlencode()

            return "{0}?{1}".format(base_url, query.urlencode())

    @property
    def changelist_url(self):
        base_url = reverse("{0}:{1}_{2}_changelist".format(self.site.namespace, self.app_label, self.model_name))
        return base_url

    @property
    def changelist_url_params(self):
        base_url = self.changelist_url
        query = self.request.GET.get(self.change_filter_name)
        return "{0}?{1}".format(base_url, query if query else "")

    def wrapper(self, func):
        @functools.wraps(func)
        def inner(request, *args, **kwargs):
            self.request = request
            return func(request, *args, **kwargs)

        return inner

    def get_urls(self):
        """
        生成url
        self.model_class._mete.app_label        返回应用的名称
        self.model_class._mete.model_name       返回使用的表名
        :return:
        """
        from django.conf.urls import url

        app_model_name = self.model_class._meta.app_label, self.model_class._meta.model_name

        patterns = [
            url(r'^$', self.wrapper(self.changelist_view), name="%s_%s_changelist" % app_model_name),
            url(r'^add/$', self.wrapper(self.add_view), name="%s_%s_add" % app_model_name),
            url(r'^(.+)/delete/$', self.wrapper(self.delete_view), name="%s_%s_delete" % app_model_name),
            url(r'^(.+)/change/$', self.wrapper(self.change_view), name="%s_%s_change" % app_model_name),
        ]
        patterns += self.extra_urls()
        return patterns

    def extra_urls(self):
        """
        扩展URL预留的钩子函数
        :return:
        """
        return []

    @property
    def urls(self):
        return self.get_urls(), None, None


class AryaSite(object):
    """
    生成路由
    """
    def __init__(self, name='arya'):
        self.name = name
        self.namespace = name
        self._registry = {}         # _registry是一个空字典

    def register(self, model, model_config=None):
        if not model_config:    # 如果注册类时没有定义model_config.则model_config为AryaConfig
            model_config = AryaConfig
        self._registry[model] = model_config(model, self)

    def get_urls(self):
        patterns = []

        from django.conf.urls import url, include
        patterns += [
            # url(r'^login/', self.login),
            # url(r'^logout/', self.logout),
        ]

        for model_class, model_nb_obj in self._registry.items():
            """
            self._registry.items():(<class 'rbac.models.User'>, <rbac.arya.UserConfig object at 0x00000000041804E0>),
                                   (<class 'rbac.models.Role'>, <rbac.arya.RoleConfig object at 0x0000000004180518>)
            model_class:在admin.py中注册了的类,如  User,Group
            model_nb_obj:在admin.py中注册的类的配置类,如 UserConfig,GroupConfig
            """
            patterns += [
                url(r'^%s/%s/' % (model_class._meta.app_label, model_class._meta.model_name,), model_nb_obj.urls)
            ]

        return patterns

    @property
    def urls(self):
        return self.get_urls(), self.name, self.namespace


site = AryaSite()
