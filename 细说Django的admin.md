 在`admin.py`中只需要将地`Model`中某个类注册,即可在Admin中进行增删查改的功能,例如:

	admin.site.register(models.UserInfo)
	
这种方式比较简单,如果想要进行更多的定制操作,就需要利用`ModelAdmin`进行操作

***方式一***

        from django.contrib import admin
        from . import models
        
        class BookAdmin(admin.ModelAdmin):
            list_display = ('title','price','publish')
            
        admin.site.register(models.Book,BookAdmin)

没有设置`BookAdmin`时,系统默认为`ModelAdmin`

`models.Book`实际上是一个列表,也可以写成

        from django.contrib import admin
        from . import models
        
        class BookAdmin(admin.ModelAdmin):
            list_display = ('title','price','publish')
            
        admin.site.register([models.Book,],BookAdmin)
	
这个参数里可以写多个表名,但要注意的是这里面添加的表名都必须要有`list_display`中声明要显示的字段

***方式二***

	from django.contrib import admin
	from . import models

	@admin.register(models.Book)
	class BookAdmin(admin.ModelAdmin):
		list_display = ('title','price','publish')

在`ModelAdmin`中提供了大量的可定制的功能

**定制admin**

**1.list_display:显示列表时,定制显示的列**

        from django.contrib import admin
        from . import models
        
        @admin.register(models.Book)
        class BookAdmin(admin.ModelAdmin):
            list_display = ('title','price','publish')

在后台管理页面中,显示书的名称,价格以及出版社等信息

![](http://images2017.cnblogs.com/blog/1133627/201710/1133627-20171018233356521-354221807.png)

在class类中还有如下用法:

        from django.contrib import admin
        from . import models
        
        @admin.register(models.Book)
        class BookAdmin(admin.ModelAdmin):
            list_display = ('title','price','aaa')
        
            def aaa(self,obj):
                return obj.title+"--aaaa"
显示如下

![](http://images2017.cnblogs.com/blog/1133627/201710/1133627-20171018233406896-1666794332.png)

**2.list_display_links:列表时,定制列可以点击跳转**
        
        from django.contrib import admin
        from . import models
        
        @admin.register(models.Book)
        class BookAdmin(admin.ModelAdmin):
            list_display = ('title','price','publish')
            list_display_links = ('title','price','publish')

在后台页面显示的时候,所显示的列为可以点击跳转

![](http://images2017.cnblogs.com/blog/1133627/201710/1133627-20171018233417615-823834933.png)

**3.list_filter:列表时，定制右侧快速筛选**

例子一:

        from django.contrib import admin
        from . import models
        
        @admin.register(models.Book)
        class BookAdmin(admin.ModelAdmin):
        
            list_display = ('title','price','publish')
            list_filter = ('classification','publish')

效果如下:

![](http://images2017.cnblogs.com/blog/1133627/201710/1133627-20171018233431631-1217512736.png)

例子二:

        from django.contrib import admin
        from . import models
        
        @admin.register(models.Book)
        class BookAdmin(admin.ModelAdmin):
            list_display = ('title','price','publish')
        
            class Ugg(admin.SimpleListFilter):
        
                title=uget('类型')
        
                parameter_name = "book"
        
                def lookups(self, request, model_admin):
                    """
                    显示筛选选项,列出价格大于100的书箱的类型
                    :param request:
                    :param model_admin:
                    :return:
                    """
                    return models.Book.objects.filter(price__gt=100).values_list("publish","classification")
        
                def queryset(self, request, queryset):
                    """
                    点击查询时,进行筛选
                    :param request:
                    :param queryset:
                    :return:
                    """
                    v1=self.value()
                    return queryset
        
            list_filter = ["publish",Ugg,]
        
效果如下:

![](http://images2017.cnblogs.com/blog/1133627/201710/1133627-20171018233505287-452928624.png)

**4.list_select_related:列表时，连表查询是否自动select_related**

使用联表查询可以提高数据库的查询性能

        from django.contrib import admin
        from . import models
        
        @admin.register(models.Book)
        class BookAdmin(admin.ModelAdmin):
            list_display = ('title','price','publish')
        
            list_select_related = ["publish"]   # 联表查询出版社的信息
        
**5. 分页相关**

    list_per_page=10            # 分页,每页显示的数据条数
    list_max_show_all=100       # 分页,显示全部数据时,最多显示的数据条数
    paginator=Paginator         # 分布插件

例如:
    
        from django.contrib import admin
        from . import models
        
        @admin.register(models.Book)
        class BookAdmin(admin.ModelAdmin):
        
            list_display = ('title','price','publish')
            list_per_page = 2
效果如下:

![](http://images2017.cnblogs.com/blog/1133627/201710/1133627-20171018233524224-990675956.png)

**6. list_editable:列表时，可以编辑的列**

        from django.contrib import admin
        from . import models
        
        @admin.register(models.Book)
        class BookAdmin(admin.ModelAdmin):
            list_display = ('title','price','publish')
        
            list_editable = ('price','publish')
        
效果如下:

![](http://images2017.cnblogs.com/blog/1133627/201710/1133627-20171018233533740-2132929711.png)

**7. search_fields:列表时，模糊搜索的功能**

        from django.contrib import admin
        from . import models
        
        @admin.register(models.Book)
        class BookAdmin(admin.ModelAdmin):
            list_display = ('title','price','publish')
        
            list_select_related = ["publish"]
        
            search_fields = ['title','classification']

效果如下:

![](http://images2017.cnblogs.com/blog/1133627/201710/1133627-20171018233543365-894715266.png)

**8. date_hierarchy:列表时，对Date和DateTime类型进行搜索**

        from django.contrib import admin
        from . import models
        
        @admin.register(models.Book)
        class BookAdmin(admin.ModelAdmin):
            list_display = ('title','price','publish','publication_date')
        
            list_select_related = ["publish"]
        
            date_hierarchy="publication_date"

效果如下:
        
![](http://images2017.cnblogs.com/blog/1133627/201710/1133627-20171018233554349-41777080.png)

![](http://images2017.cnblogs.com/blog/1133627/201710/1133627-20171018233603177-1339358413.png)

**9. preserve_filters:详细页面，删除、修改，更新后跳转回列表后，是否保留原搜索条件**

        from django.contrib import admin
        from . import models
        
        @admin.register(models.Book)
        class BookAdmin(admin.ModelAdmin):
            list_display = ('title','price','publish','publication_date')
        
            list_select_related = ["publish"]
        
            search_fields = ['title', 'classification']
        
            preserve_filters=True

效果如下:

![](http://images2017.cnblogs.com/blog/1133627/201710/1133627-20171018233615584-707328858.png)

**10. save_as = False:详细页面，按钮为“Save as new” 或 “Save and add another”**

        from django.contrib import admin
        from . import models
        
        @admin.register(models.Book)
        class BookAdmin(admin.ModelAdmin):
            list_display = ('title','price','publish','publication_date')
        
            list_select_related = ["publish"]
        
            save_as = True

效果如下:

![](http://images2017.cnblogs.com/blog/1133627/201710/1133627-20171018233726349-1190205405.png)

        from django.contrib import admin
        from . import models
        
        @admin.register(models.Book)
        class BookAdmin(admin.ModelAdmin):
            list_display = ('title','price','publish','publication_date')
        
            list_select_related = ["publish"]
        
            save_as = False

效果如下:

![](http://images2017.cnblogs.com/blog/1133627/201710/1133627-20171018233738099-738730140.png)

**11. save_as_continue = True:点击保存并继续编辑**

用法与上一个用法相同

**12. save_on_top = False:详细页面，在页面上方是否也显示保存删除等按钮**

        from django.contrib import admin
        from . import models
        
        @admin.register(models.Book)
        class BookAdmin(admin.ModelAdmin):
            list_display = ('title','price','publish','publication_date')
        
            list_select_related = ["publish"]
        
            save_on_top = False

效果如下:

![](http://images2017.cnblogs.com/blog/1133627/201710/1133627-20171018233750771-1118728659.png)

        from django.contrib import admin
        from . import models
        
        @admin.register(models.Book)
        class BookAdmin(admin.ModelAdmin):
            list_display = ('title','price','publish','publication_date')
        
            list_select_related = ["publish"]
        
            save_on_top = True
            
效果如下:
   
![](http://images2017.cnblogs.com/blog/1133627/201710/1133627-20171018233802349-2113123655.png)

**13. inlines:详细页面，如果有其他表和当前表做FK，那么详细页面可以进行动态增加和删除**

        from django.contrib import admin
        from . import models
        
        @admin.register(models.Book)
        class BookAdmin(admin.ModelAdmin):
            list_display = ('title','price')
        
        
        class BookInline(admin.StackedInline):
            extra=0
            model=models.Book
        
        class PublishAdmin(admin.ModelAdmin):
            inlines = [BookInline,]
            list_display = ['name','addr']
        
        admin.site.register(models.Publish,PublishAdmin)
        
效果如下:

![](http://images2017.cnblogs.com/blog/1133627/201710/1133627-20171018233814506-1252934379.png)

在编辑或添加出版社的时候可以同时添加多本书箱数据,添加书籍信息的时候是纵向添加书籍信息的

在这里`BookInline`这个类还可以继承`TabularInline`这个类实现横向添加书籍信息

        from django.contrib import admin
        from . import models
        
        @admin.register(models.Book)
        class BookAdmin(admin.ModelAdmin):
            list_display = ('title','price')
        
        
        class BookInline(admin.TabularInline):
            extra=0
            model=models.Book
        
        class PublishAdmin(admin.ModelAdmin):
            inlines = [BookInline,]
            list_display = ['name','addr']
        
        admin.site.register(models.Publish,PublishAdmin)
        
效果如下:

![](http://images2017.cnblogs.com/blog/1133627/201710/1133627-20171018233834927-112006974.png)

**14. action:列表时，定制action中的操作**

        from django.contrib import admin
        from . import models
        
        @admin.register(models.Book)
        class BookAdmin(admin.ModelAdmin):
            list_display = ('title','price')
        
            def func1(self,request,queryset):       # 定义具体的action的方法
                pass
        
            func1.short_description = "自定义操作"   # 在页面上显示方法的名称
        
            actions_on_top = True                   # action在页面上方显示
        
            actions_on_bottom = False               # action在页面下方显示
        
            actions_selection_counter = True        # 显示页面上选择数据的条数
        
            actions=[func1,]                        # 添加定制的action的操作
        
在action列表中,添加一个func1的功能

![](http://images2017.cnblogs.com/blog/1133627/201710/1133627-20171018233845084-138491475.png)

**15. 定制HTML模板**

Django后台管理页面默认使用的模板是`change_list.html`

![](http://images2017.cnblogs.com/blog/1133627/201710/1133627-20171018233856787-1473818998.png)

打开change_list.html页面,添加一行

        <h3>hello python</h3>
  
刷新浏览器,可以看到

![](http://images2017.cnblogs.com/blog/1133627/201710/1133627-20171018233907802-614114793.png)

可以设置的选项有:

    add_form_template = None                        # 添加数据的模板 
    change_form_template = None                     # 修改数据的模板
    change_list_template = None                     # 显示数据的模板
    delete_confirmation_template = None             # 删除数据时确认页面的模板
    delete_selected_confirmation_template = None    # 选中之后删除的确认页面
    object_history_template = None                  # 有ForeignKey时关联数据进行处理的模板

例子:

        from django.contrib import admin
        from . import models
        
        @admin.register(models.Book)
        class BookAdmin(admin.ModelAdmin):
            list_display = ('title','price')
        
            change_list_template = ['change_list1.html']
            
效果如下:
        
![](http://images2017.cnblogs.com/blog/1133627/201710/1133627-20171018233923334-1230567627.png)

**16. raw_id_fields:详细页面，针对FK和M2M字段变成以Input框形式**

正常显示的时候,`FK`和`M2M`字段是通过下拉框来进行操作的

添加`raw_id_fields`配置后,针对`FK`和`M2M`字段变成以`Input`框形式

        from django.contrib import admin
        from . import models
        
        @admin.register(models.Book)
        class BookAdmin(admin.ModelAdmin):
            list_display = ('title','price','classification')
        
            raw_id_fields = ('publish','authors')

效果如下:

![](http://images2017.cnblogs.com/blog/1133627/201710/1133627-20171018233936162-618172965.png)

![](http://images2017.cnblogs.com/blog/1133627/201710/1133627-20171018233945427-1176858539.png)

**17. fields:详细页面时，显示的字段**

        from django.contrib import admin
        from . import models
        
        @admin.register(models.Book)
        class BookAdmin(admin.ModelAdmin):
            
            fields = ('title','price')
            
效果如下:

![](http://images2017.cnblogs.com/blog/1133627/201710/1133627-20171018234008052-195240581.png)

**18. exclude:详细页面时，排除的字段**
     
        from django.contrib import admin
        from . import models
        
        @admin.register(models.Book)
        class BookAdmin(admin.ModelAdmin):
        
            exclude = ('classification',)

效果如下:

![](http://images2017.cnblogs.com/blog/1133627/201710/1133627-20171018234020115-2112114572.png)

**19. readonly_fields:详细页面时，只读字段**

        from django.contrib import admin
        from . import models
        
        @admin.register(models.Book)
        class BookAdmin(admin.ModelAdmin):
            
            readonly_fields = ('classification',)
            
效果如下:
          
![](http://images2017.cnblogs.com/blog/1133627/201710/1133627-20171018234034052-1088297272.png)

**20. fieldsets:详细页面时，使用fieldsets标签对数据进行分割显示**


        from django.contrib import admin
        from . import models
        
        @admin.register(models.Book)
        class BookAdmin(admin.ModelAdmin):
        
            fieldsets = (
                ("基本信息",{
                    "fields":("title","price","publish",)
                }),
                ("出版信息",{
                "classes":("collapse","wide","extrapretty"),
                "fields":("classification","authors","publication_date",)
            }),
            )
            
效果如下:

![](http://images2017.cnblogs.com/blog/1133627/201710/1133627-20171018234049506-46891728.png)

![](http://images2017.cnblogs.com/blog/1133627/201710/1133627-20171018234059740-1934391323.png)

**21. 详细页面时，M2M显示时，数据移动选择(方向:上下和左右)**

    from django.contrib import admin
    from . import models
    
    @admin.register(models.Book)
    class BookAdmin(admin.ModelAdmin):
    
        filter_vertical = ("authors",)
        
效果如下:

![](http://images2017.cnblogs.com/blog/1133627/201710/1133627-20171018234110646-1407696772.png)

    from django.contrib import admin
    from . import models
    
    @admin.register(models.Book)
    class BookAdmin(admin.ModelAdmin):
    
        filter_horizontal = ("authors",)
        
效果如下:

![](http://images2017.cnblogs.com/blog/1133627/201710/1133627-20171018234123896-1971203009.png)

**22. ordering:列表时，数据排序规则**

        from django.contrib import admin
        from . import models
        
        @admin.register(models.Book)
        class BookAdmin(admin.ModelAdmin):
            list_display = ("title","price","classification","publish")
        
            ordering=("-price",)

效果如下:

![](http://images2017.cnblogs.com/blog/1133627/201710/1133627-20171018234137412-1038777537.png)

    from django.contrib import admin
    from . import models
    
    @admin.register(models.Book)
    class BookAdmin(admin.ModelAdmin):
        list_display = ("title","price","classification","publish")
    
        ordering=("price",)

效果如下:

![](http://images2017.cnblogs.com/blog/1133627/201710/1133627-20171018234150693-263640245.png)

**23. view_on_site:编辑时，是否在页面上显示view on set**

        from django.contrib import admin
        from . import models
        
        @admin.register(models.Book)
        class BookAdmin(admin.ModelAdmin):
            list_display = ("title","price","classification","publish")
        
            def view_on_site(self,obj):
        
                return "http://www.baidu.com"

点击`view on set`按钮,浏览器会指向`"http://www.baidu.com"`

![](http://images2017.cnblogs.com/blog/1133627/201710/1133627-20171018234202490-505946460.png)

**24. radio_fields:详细页面时，使用radio显示选项（FK默认使用select）**

        from django.contrib import admin
        from . import models
        
        @admin.register(models.Book)
        class BookAdmin(admin.ModelAdmin):
            list_display = ("title","price","classification","publish")
        
            radio_fields = {"publish":admin.VERTICAL}

效果如下:

![](http://images2017.cnblogs.com/blog/1133627/201710/1133627-20171018234213412-841697658.png)

**25. show_full_result_count = True:列表时，模糊搜索后面显示的数据个数样式**

        from django.contrib import admin
        from . import models
        
        @admin.register(models.Book)
        class BookAdmin(admin.ModelAdmin):
            list_display = ("title","price","classification","publish")
        
            search_fields = ('title','classification')
        
            show_full_result_count = True

效果如下:
    
![](http://images2017.cnblogs.com/blog/1133627/201710/1133627-20171018234225521-1977172751.png)

**26. formfield_overrides = {}:详细页面时，指定现实插件**

**27. prepopulated_fields = {}:添加页面，当在某字段填入值后，自动会将值填充到指定字段**

        from django.contrib import admin
        from . import models
        
        @admin.register(models.Book)
        class BookAdmin(admin.ModelAdmin):
            list_display = ("title","price","classification","publish")
        
            search_fields = ('title','classification')
        
            prepopulated_fields = {"title":("classification",)}

效果如下:
    
![](http://images2017.cnblogs.com/blog/1133627/201710/1133627-20171018234238146-879970499.png)

**28. form = ModelForm:用于定制用户请求时候表单验证**

未进行配置之前:

![](http://images2017.cnblogs.com/blog/1133627/201710/1133627-20171018234249787-1200549569.png)

修改配置文件:

        from django.contrib import admin
        from . import models
        from django.forms import ModelForm
        
        class MyForm(ModelForm):
            class Meta:
                model=models.Book
                fields="__all__"
                error_messages = {
                    "title": {'required': "书名不能为空"},
                    "price": {'required': "价格不能为空"}
                }  # 自定义错误信息，用户输入错误时显示
        
        @admin.register(models.Book)
        class BookAdmin(admin.ModelAdmin):
            list_display = ("title","price","classification","publish")
        
            search_fields = ('title','classification')
        
            form=MyForm

效果如下:

![](http://images2017.cnblogs.com/blog/1133627/201710/1133627-20171018234302552-763716274.png)

**29. empty_value_display = "列数据为空时，显示默认值"**

        from django.contrib import admin
        from . import models
        
        @admin.register(models.Book)
        class BookAdmin(admin.ModelAdmin):
            list_display = ("title","price","classification","publish")
        
            search_fields = ('title','classification')
        
            empty_value_display="列数据为空时,默认显示"

总结:

* 在定制admin的所有的操作的时候都是在配置文件中完成的.
* 在配置文件中,可以进行配置的有数据表的字段,函数和类
* 在某个页面中,可以配置使用自定义的模板.
* 同样的,请求到达Django的时候,也可以配置使其执行自定义的函数
    
`ModelAdmin`是放置在`options.py`文件中的.

打开`options.py`文件,可以看到`ModelAdmin`里有一个叫做`changelist_view `的方法 


        from django.contrib import admin
        from . import models
        
        @admin.register(models.Book)
        class BookAdmin(admin.ModelAdmin):
            list_display = ("title","price","classification","publish")
        
            search_fields = ('title','classification')
        
            empty_value_display="列数据为空时,默认显示"

可以看到,`BookAdmin`是继承自`ModelAdmin`这个类的,`ModelAdmin`里有一个`changelist_view` 的方法 

所以在`BookAdmin`中也可以自定义一个`changelist_view`的视图函数.

自定义了`changelist_view`后,`changelist_view`这个方法只能对`BookAdmin`类生效,对别的类不起作用