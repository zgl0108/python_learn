**1. 模板系统的介绍**

`Django`作为一个`Web`框架，其模板所需的`HTML`输出静态部分以及动态内容插入

模板由`HTML`代码和逻辑控制代码构成

`Django`框架的模板语言的语法格式：

    {{ var_name }}

例如:`HTML`被直接编码在`python`代码中:

    import datetime
	def current_datetie(request):
		time1 = datetime.datetime.now()
		html="<html><body>the time is $s.</body></html>"%time1
		
		return HttpResponse(html)
或者:

	>>> python manange.py shell             #进入该django项目的环境
	>>> from django.template import Context,Template
	>>> t1=Template("hello {{name}}.")
	>>> c1=Context({"name":"world"})
	>>> t1.render(c1)
	'hello world.'
同一个模板,可以有多个上下文,就可以通过创建模板对象来渲染多个上下文

创建一个模板就可以多次调用`render()`方法渲染上下文

**2. 模板支持的语法**

语法格式: 

	{{var_name}}
	
`Django`模板解析工作都是在后台通过对正则表达式一次性调用来完成

***2.1 深度的变量查找***

    #进入Django项目环境终端
	python manage.py shell  
	
***2.1.1 访问列表索引***

	>>> from django.template import Template, Context
	>>> t1 = Template('hello {{ items.2 }}.')
	>>> c1 = Context({'items': ['linux', 'javascript', 'python']})
	>>> t1.render(c1)
	'hello python.'
***2.1.2 访问字典索引***

	>>> from django.template import Template,Context
	>>> person = {"name":"Jack","age":22}
	>>> t1 = Template("{{person.name}} is {{person.age}} years old.")
	>>> c1 = Context({"person":person})
	>>> t1.render(c1)
	'Jack is 22 years old.'
***2.1.3 datetime示例***

	>>> from django.template import Template,Context
	>>> import datetime
	>>> day1=datetime.datetime.utcnow()
	>>> day1.year
	2017
	>>> day1.month
	8
	>>> day1.day
	20
	>>> t1=Template("the month is {{ date.month }} and the year is {{ date.year }}")
	>>> c1=Context({"date":day1})
	>>> t1.render(c1)
	'the month is 8 and the year is 2017'
***2.1.4 类的实例***

	>>> class Person(object):
	...     def __init__(self,first_name,second_name):
	...             self.first_name=first_name
	...             self.second_name=second_name
	...
	>>> t1=Template("hello,{{ person.first_name }}--{{ person.second_name }}.")
	>>> c1=Context({"person":Person("Jack","Bones")})
	>>> t1.render(c1)
	'hello,Jack--Bones.'	
***2.1.5 引用对象方法***

	>>> from django.template import Template,Context
	>>> t1 = Template("{{var}}--{{var.upper}}--{{var.isdigit}}")
	>>> t1.render(Context({"var":"Hello"}))
	'Hello--HELLO--False'
	>>> t.render(Context({"var":"666"}))
	'666--666--True'

注意点:

	调用方法时并没有使用圆括号,而且也无法给该方法传递参数
**2.2 变量的过滤器(filter的使用)**

格式:

	{{obj|filter:param}}
参数:

	add                 给变量加上相应的值
	addslashes          给变量中的引号前加上斜线
	capfirst            首字母大写
	cut                 从字符串中移除指定的字符
	date                格式化日期字符串
	default             如果值是False,就替换成设置的默认值，否则就是用本来的值
	default_if_none     如果值是None,就替换成设置的默认值，否则就使用本来的值
例子:
```
    #value1="aBcDe"
    {{ value1|upper }}                      #把所有的结果渲染为大写，输出为"ABCDE"
    
    #value2=5
    {{ value2|add:3 }}                      #把结果中的结果加上加上指定值输入为8
    
    #value3='he  llo wo r ld'
    {{ value3|cut:' ' }}                    #去除结果中的指定字符，输入为"helloworld"
    
    #value4="hello world"
    {{ value4|capfirst }}                   #查询结果首字母大写，输入为"Hello world"
    
    #import datetime
    #value5=datetime.datetime.now()
    {{ value5|date:'Y-m-d' }}               #设定前端页面的显示时间为"2017-08-20"格式
    
    #value6=[]
    {{ value6 }}                            #从数据库的查询结果为空是在前端页面显示为"[]"
    {{ value6|default:'空的' }}               #从数据库的查询结果为空是在前端页面显示为default的值 
    
    #value7='<a href="#">click</a>'
    {{ value7 }}                            #输入为"<a href="#">click</a>"
    {{ value7|safe }}<br>                   # 如果不想标签被渲染,加safe即可
    {{ value7|striptags }} 
    
    {% autoescape off %}                    #Django安全机制关闭,标签会被渲染
      {{ value7 }}
    {% endautoescape %}
    
    #value8='1234'
    {{ value8|filesizeformat }}
    {{ value8|first }}
    {{ value8|length }}
    {{ value8|slice:":-1" }}
    
    #value9='http://www.baidu.com/?a=1&b=3'
    {{ value9|urlencode }}
    value9='hello I am Tony'
    
    {{ value10|tuncatewords:3 }}            # 如果最后的结果是一个长字符串时，显示前3个单词，剩余的用点号(.)表示
    {{ value10|tuncatechars:20 }}            # 如果最后的结果是一个长字符串时，显示前20个字母，剩余的用点号(.)表示
```
标签`(tag)`的使用(使用大括号和百分比的组合来表示使用`tag`)

**2.3 模板语言的控制语句**

***2.3.1 {% if %} 的使用***

`{% if %}`标签计算一个变量值，如果是`“true”`，即它存在、不为空并且不是`false`的`boolean`值,

系统则会显示`{% if %}`和`{% endif %}`间的所有内容

例子:

    {% if num >= 100 and 8 %}
        {% if num > 200 %}
            <p>num大于200</p>
        {% else %}
            <p>num大于100小于200</p>
        {% endif %}
    {% elif num < 100%}
        <p>num小于100</p>
    {% else %}
        <p>num等于100</p>
    {% endif %}

`{% if %}`标签接受单个`and`，`or`或者`not`来测试多个变量值或者否定一个给定的变量

`{% if %}`标签不允许同一标签里同时出现`and`和`or`，否则会产生歧义

例如下面的标签是不合法的：

	{% if obj1 and obj2 or obj3 %}  
	
***2.3.2 {% for %}的使用***

`{% for %}`标签按顺序遍历一个序列中的各个元素,每次循环模板系统都会渲染`{% for %}`和`{% endfor %}`之间的所有内容

例子:

	<ul>
	{% for obj in list %}
		<li>{{ obj }}</li>
	{% endfor %}
	</ul>
可以在标签里添加`reversed`来反序循环列表：

	{% for obj in list reversed %}
	...
	{% endfor %}
	
`{% for %}`标签可以嵌套：

    {% for country in countries %}
        <h1>{{ country.name }}</h1>
        <ul>
         {% for city in country.city_list %}
            <li>{{ city }}</li>
         {% endfor %}
        </ul>
    {% endfor %}
    
`for`循环不支持中断循环，也不支持`continue`语句

`{% for %}`标签内置了一个`forloop`模板变量，这个变量含有关于循环的属性

	forloop.counter         表示循环的次数，它从1开始计数
	forloop.counter0        类似于forloop.counter，但它是从0开始计数
	forloop.revcounter      反向遍历整个列表,revcounter表示循环的次数,最后一次为1
	forloop.revcounter0     反向遍历整个列表,revcounter表示循环的次数,最后一次为0
	forloop.first           返回一个布尔值,当第一次循环时值为True,其余为False	
例子:
```
    {% for item in todo_list %}
        <p>{{ forloop.counter }}: {{ item }}</p>
    {% endfor %}
    
    {% for object in objects %}   
         {% if forloop.first %}
            <li class="first">
         {% else %}
            <li>
         {% endif %}   
            {{ object }}</li>  
    {% endfor %}
```
`forloop`变量只能在循环中得到，当模板解析器到达`{% endfor %}`时`forloop`变量就会消失

如果模板`context`已经包含一个叫`forloop`的变量，`Django`会用`{% for %}`标签替代它

`Django`会在`for`标签的块中覆盖由开发人员定义的`forloop`变量的值

在其他非循环的地方，你的`forloop`变量仍然可用

 ***2.3.3 {% empty %}***
用法:

      {%  for i in li %}        # 从数据库中查询结果有数据时正常显示<li></li>标签中的内容
          <li>{{ forloop.counter0 }}----{{ i }}</li>
      {% empty %}               # 从数据库中的查询结果为空时，显示的是empty中的内容
          <li>this is empty!</li>
      {% endfor %}
		  
 ***2.3.4 {% csrf_token %}csrf_token标签***

用于生成`csrf_token`的标签,用于防治跨站攻击验证

如果`view`的`index`里用的是`render_to_response`方法,则不会生效

其实这里是生成一个`input`标签,与其他表单标签一起提交给后台的

***2.3.5 {% url %}***			#引用路由配置的地址

在路由映射表中，为一个路由映射配置了别名的时候使用

***2.3.6 {% verbatim %}***	#禁止render
用法:

	{% verbatim %}	#hello标签不会被模板渲染
		{{ hello }}
	{% endverbatim %}
***2.3.7 {% load %}加载标签库***

加载静态文件或自定义filter时使用

***2.3.8 自定义filter和simply_tag***
 
* 1、在app中创建templatetags模块

* 2、创建任意 .py 文件，如：my_tags.py
```
    from django import template
    from django.utils.safestring import mark_safe
    
    register = template.Library()  # register的名字是固定的,不可改变
    
    @register.filter
    def custom_filter(x,y):
        return x*y
    
    @register.simple_tag
    def custom_simple(x,y,z):
        return x+y+z
```
* 3、在使用自定义simple_tag和filter的html文件中导入之前创建的 my_tags.py ：{% load my_tags %}

* 4、使用simple_tag和filter
```
    -------------------------------HTML文件
    {% load xxx %}         # 位于首行,xxx代表自定义的文件名
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Title</title>
    </head>
    <body>
        <h1>Hello {{ user.0 }}</h1>
        
        {{ user.3|custom_filter:8 }}
    
        {% custom_simple user.3 2 3 %}
    </body>
    </html>
```
* 5、在settings中的INSTALLED_APPS配置当前app，不然django无法找到自定义的simple_tag

* 6、filter可以用在if等语句后，simple_tag不可以

	{% if num|filter_multi:30 > 100 %}
		{{ num|filter_multi:30 }}
	{% endif %}
	
**2.4 模板继承**

***2.4.1 include(继承)模板标签***

{% include %}是一个内建模板标签,允许在模板中包含其它的模板内容.

标签的参数是所要包含的模板的名称,可以是一个变量,也可以是单/双引号硬编码的字符串.

每当在多个模板中出现相同的代码时,就应该考虑是否要使用{% include %}来减少代码重复


***2.4.2 extend(继承)模板标签***

在一个大型网站中，有一些区域的内容始终是不变的，

减少共用页面区域所引起的重复和冗余代码`Django`框架中使用的方法就是模板继承

本质上来说，模板继承是先构造一个基础框架模板，而后在其子模板中对公用部分和定义块进行重载

	母板：{% block title %}{% endblock %}    # 定义盒子
	子板：{% extends "base.html" %}          # 继承母板的内容，且必须放在模板第一行
	　　　{% block title %}{% endblock %}    # 可以对盒子的内容进行修改
		  {% csrf_token %}                   # 取消csrf安全保护
	　　　{% black.super %}
		 {% include '小组件路径' %}           # HTML出现相同块代码时，新建公用小组件HTML文件
		 
如果在模板中使用`{% extends %}`,必须保证其为模板中的第一个模板标记,否则模板不会起作用

一般来说,基础模板中的`{% block %}`标签越多越好,子模板不必定义父模板中所有的代码块,

因此,可以用合理的缺省值对一些代码块进行填充,然后只对子模板所需的代码块进行重定义.

如果多个模板之间的代码重用太多,可以考虑将重复代码段放放到父模板的某个`{% block %}`中.

当需要访问父模板中的块的内容,使用`{{ block.super }}`标签,这个魔法变量将会表现出父模板中的内容,

如果只想在上级代码块基础上添加内容,而不是全部重载,这个魔法变量就非常有用了.

不允许在同一个模板中定义多个同名的`{% block %}`.

因为`block`标签的工作方式是双向的,`block`标签定义了在父模板中`{% block %}`.

如果父模板中出现了两个相同名称的`{% block %}`标签,父模板将无法使用哪个块的内容