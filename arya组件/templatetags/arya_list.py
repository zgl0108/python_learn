#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.template import Library
from django.db.models import ForeignKey
from django.db.models import ManyToManyField
from types import FunctionType, MethodType

register = Library()        # simple_tag固定用法

def result_header_list(change_list):
    """
    处理表格头部
    :param modal_cls: 
    :param list_display: 
    :return: 
    """
    if not change_list.list_display:
        # 如果用户未自定义要显示的列,则返回数据表的名
        # model_name返回的是数据表的名字
        yield change_list.model_config.model_name
    else:
        for name in change_list.list_display:

            # 返回在列表页面显示的字段的verbose_name
            # isinstance(name,FunctionType)判断name是否是一个函数
            yield name(change_list.model_config,is_header=True) if isinstance(name,FunctionType) \
                else change_list.model_config.model_class._meta.get_field(name).verbose_name


def result_body_list(change_list):
    """
    处理表格内容
    :param queryset: 
    :param list_display: 
    :return: 
    """
    for row in change_list.result_list:
        if not change_list.list_display:
            yield [str(row), ]
        else:
            yield [name(change_list.model_config,obj=row) if isinstance(name, FunctionType) \
                       else getattr(row, name) for name in change_list.list_display]


@register.inclusion_tag('arya/change_list_results.html')
def show_result_list(change_list):
    """
    展示数据表格
    1. 表头
    2. 表体
    :param list_display: 
    :param queryset: 
    :return: 
    """
    return {
        'result': result_body_list(change_list),
        'headers': result_header_list(change_list)
    }


@register.inclusion_tag('arya/change_list_action.html')
def show_actions(change_list):
    return {'actions': ((item.__name__, item.short_description) for item in change_list.actions)}
