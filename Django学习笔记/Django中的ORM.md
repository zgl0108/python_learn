**1. 数据库的配置**

`Django`可以配置使用`sqlite3`,`mysql`,`oracle`,`postgresql`等数据库

在一个`Django`项目中，默认使用的是`sqlite3`数据库
```
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',#默认使用的数据库引擎是sqlite3，项目自动创建
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),#指定数据库所在的路径
        }
    }
```
如果想在一个`Django`项目中配置使用`mysql`数据库，可以使用如下配置：
```
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',#表示使用的是mysql数据库的引擎
            'NAME': 'db1',      #数据库的名字，可以在mysql的提示符下先创建好
            'USER':'root',      #数据库用户名
            'PASSWORD':'',      #数据库密码
            'HOST':'',          #数据库主机，留空默认为"localhost"
            'PORT':'3306',      #数据库使用的端口
        }
    }
```
配置好数据库的信息后还必须安装数据库的驱动程序

`Django`默认导入的`mysql`的驱动程序是`MySQLdb`，然而`MySQLdb`对于py3支持不全,所以这里使用`PyMySQL`

在项目名文件下的`__init__.py`文件中写入如下配置：

	import pymysql
	pymysql.install_as_MySQLdb()
	
**2. ORM表模型**

人的模型:每个人都有只属性自己的身份信息,包含生日,性别,身份证号等,每个人和他的信息是一对一的关系,

因此可以把一个人的所有身份信息汇总到一张数据表中,没必要拆分成两张表,这是一对一(`one-to-one`)的概念

书的模型:一本书有书名,出版日期,价格,所属的出版社等信息.一本书可以有多个作者来编写,一个作者也可以写作多本书,

书与作者是多对多的关联关系,这是多对多(`many-to-many`)的概念

同时,一本书只能由一个出版社出版,但是一个出版社可以出版多本书,所以出版社与书是一对多的关系,这是一对多(`one-to-many`)的概念

每个数据模型都是`Django.db.models.Model`的子类,它的父类`Model`包含了所有必要的和数据库交互的方法,并提供了一个简单的定义数据库字段的语法 

每个模型相当于单个数据库表(多对多关系例外,会多生成一张关系表),每个属性都是数据表中的字段.

属性名就是字段名,其类型(例如`CharField`)相当于数据库的字段类型(例如`varchar`).

因此,在Django的数据库中:

	表名对应为python中的类名
	字段对应python中的类属性
	表中的每一条记录对应python中的类实例对象
	
数据模型的三种关系:

	一对一模型:实质就是在主外键(foreign key)的关系基础上,给外键加了一个unique=True的属性
	一对多模型:就是主外键关系(foreign key)
	多对多模型:(ManyToManyField)自动创建第三张表,也可以手动创建第三张表:两个foreign key 
	
例子,创建一个包含一对一,一对多和多对多关系的数据表:
	
        #创建一个书的类,继承models类
        class Book(models.Model):
        
        #用models类创建书的名字,类型为字符串,CharField相当于mysql语句中的varchar,字段最长为32
        title = models.CharField(max_length=32)
        
        #创建书的价格,类型为浮点型,小数点前最长4位,小数点后最长2位
        price = models.DecimalField(max_digits=6, decimal_places=2)
        
        #创建书的出版社信息,其与出版社的外键关系为一对多,所以用外键
        publish = models.ForeignKey(Publish)
        
        #创建书的出版日期,类型为日期
        publication_date = models.DateField()
        
        #创建书的类型信息,为字符串类型,最长为20
        classification=models.CharField(max_length=20)
        
        #创建书的作者信息,书籍与作者的关系为多对多,所以使用many-to-many
        authors = models.ManyToManyField("Author")
		
**3. ORM之增(create,save)**

例如,为数据库中插入书的信息,有两种方式

***3.1 使用`create`方式***

方式一:

	Publish.objects.create("name"="人民出版社",city="北京"}
	
方式二:
	
	Publish.objects.create(**{"name":"文艺出版社","city":"上海"}}
	
***3.2 使用`save`方式***

方式一:

	book1=Book(title="python",price="88",publish_id="1",publication_date="2017-06-18")
    book1.save()
    
方式二:

    author1=Author(name="jerry")
    author1.save()
    
上面创建的都是一对一的信息

***3.3 一对多的信息的创建(`Foreignkey`)***

方式一:
	
        #获取出版社对象
        publish_obj=Publish.objects.get(id=4)   
        
        #将出版社的对象绑定到书籍的记录中
        Book.objects.create(
            title="python",
            price=48.00,
            publication_date="2017-07-12",
            publish=publish_obj,
        )	
    
方式二:
	
        #直接把出版社的id号插入到书籍的记录中
        Book.objects.create(
            title="python",
            price=48.00,
            publish_id=2,
            publication_date="2017-06-18",
        )
    
***3.4 多对多信息的创建(`ManyToManyField()`)***

****3.4.1 为一本书添加多个作者****

    author1=Author.objects.get(id=1)                #获取id号为1的作者对象
    author2=Author.objects.filter(name="tom")       #获取名字为"tom"的作者对象
    book1=Book.objects.get(id=2)                    #获取id号为2的书籍对象
    book1.authors.add(author1,author2)              #为书籍对象添加多个作者对象
    
也可以用这种方式:

    book1.authors.add(*[author1,author2])           #为书籍对象添加作者对象的列表
	book1.authors.remove(*[author1,author2])        #删除指定书籍的所有作者
	
****3.4.2 为一个作者添加多本书****

	author_obj = Author.objects.filter(name="jerry")#获取名字为"jerry"的作者对象
    book_obj=Book.objects.filter(id__gt=3)          #获取id大于3的书籍对象集合
    author_obj.book_set.add(*book_obj)              #为作者对象添加书籍对象集合
	author_obj.book_set.remove(*book_obj)           #删除指定作者对象所有的书籍
	
使用`models.ManyToManyField()`会自动创建第三张表

***3.5 手动创建多对多的作者与书籍信息表***

        class Book2Author(models.Models):
            author=models.ForeignKey("Author")      #为作者指定Author这张表做为外键
            book=models.ForeignKey("Book")          #为书籍指定Book这张表做为外键
        
        author_obj=models.Author.objects.filter(id=3)[0]#获取Author表中id为3的作者对象
        book_obj=models.Book.objects.filter(id=4)[0]#获取Book表中id为4的书籍对象
	
****3.5.1 方式一****
	
	obj1=Book2Author.objects.create(author=author_obj,book=book_obj)
	obj1.save()
	
****3.5.2 方式二****
	
	obj2=Book2Author(author=author_obj,book=book_obj)
	obj2.save()
	
**4. ORM之删(delete)**

语句格式:

	Book.objects.filter(id=1).delete()
	
这个操作不仅会删除Book表中的一条记录,同时也会删除书籍与作者表中与Book相关联的记录,这种删除方式是Django默认的级联删除

**5. ORM之查(filter,value)	**

***5.1 方法***

	filter(**kwargs)            包含了与所给筛选条件相匹配的对象
	all()                       查询所有结果
	get(**kwargs)               返回与所给筛选条件相匹配的对象,返回结果有且只有一个,如果符合筛选条件的对象超过一个或者没有都是报错
	values(*field)              返回一个ValueQuerySet,运行后得到的并不是一系列model的实例化对象,而是一个可迭代的字典序列
	exclude(**kwargs)           包含了与所给的筛选条件不匹配的对象
	order by(*field)            对查询结果排序
	reverse()                   对查询结果反向排序
	distinct()                  从返回结果中剔除重复记录
	values_list(*field)         与values()非常相似,返回一个元组序列,values返回一个字典序列
	count()                     返回数据库中匹配的记录的数量
	first()                     返回数据库中匹配的对象的第一个对象
	last()                      返回数据库中匹配的对象的最后一个对象
	exists()                    判断一个对象集合中是否包含指定对象,包含返回True,不包含返回False
	
***5.2 `QuerySet`与惰性机制***

所谓惰性机制,`Publisher.objects.all()`或者`.filter()`等都只是返回一个`QuerySet`(查询结果集合对象)

其不会立即执行sql查询,而是当调用`QuerySet`的时候才会执行sql语句

****5.2.1 QuerySet的特点****

	可迭代的
	可切片
	
例子:

        obj=Book.objects.all()      #得到一个对象集合
        
        for item in obj:            #对QuerySet进行迭代,每一个item就是一个行对象
            print("item":,item)
            print(obj[1])           #对QuerySet进行切片
            print(obj[1:4])
            print(obj[::-1])
		
****5.2.2 Django的`QuerySet`是惰性的****

Django的`QuerySet`对应于数据库的记录,通过设定的条件进行过滤.

一个简单的查询并不会运行任何的数据库查询.只有遍历`QuerySet`或者使用if语句的时候,才会执行sql语句

例子:

        book_obj=Book.objects.filter(id=3)
        for i in book_ojb:          #到这一步才会真正执行sql查询
            print(i)
            
        if book_obj:                #到这一步才会真正执行sql查询
            print("ok")
		
****5.2.3 `QuerySet`是具有`cache`的****

当遍历`QuerySet`时,会从数据库中获取匹配的记录,然后转换成`Django`的`model`,此时执行sql语句
    
这些`model`会保存在`QuerySet`内置的cache中,这样如果你再次遍历整个`QuerySet`,就不会再次执行sql查询

例子:

        book_obj=Book.objects.filter(id=3)
        
        for i in book_obj:
            print(i)
            
        for i in book_obj:          #执行两次遍历,结果只会打印一次结果
            print(i)	
		
****5.2.4 简单的使用if语句进行判断也会完全执行整个`QuerySet`并且把数据放入cache,可以使用`exists()`方法来判断是否有数据****

例子:

        book_obj=Book.objects.filter(id=4)  #获取Book表中id为4的对象
        
        if book_obj.exists():               #exists()的检查可以避免数据放入QuerySet的cache中
            print("hello world")
		
****5.2.5 当处理的记录数量很大时,cache会占用很多内存****

巨大的`QuerySet`可能会锁住系统进程,使用程序崩溃.避免在遍历数据的同时产生`QuerySet`的`cache`,可以使用`iterator()`方法来获取数据,等到数据迭代并处理完就会被丢弃

例子:

        book_obj=Book.objects.all().iterator()      #iterator()每次只从数据库中取出少量数据,以节省内存
        
        for obj in book_obj:                        #第一次遍历,,打印每本书的名字
            print(obj.name)
            
        for obj in book_obj:                        #打印第二次,因为迭代器已经在第一次遍历到最后了,此次遍历不会打印
            print(obj.name)
		
使用`iterator()`方法来防止生成cache,意味着遍历同一个`QuerySet`时会重复执行查询.

所以使用`iterator()`时,要确保代码在操作一个大的`QuerySet`时没有执行重复的迭代

***5.2.6 `QuerySet`的`cache`是用于减少程序对数据库的查询,在通常情况下会保证在需要的时候才会查询数据库.***

使用`exists()`和`iterator()`方法可以优化程序对内存的使用,但是`exists()`和`iterator()`不会生成`cache`,可能会造成额外的数据库查询

***5.3 对象查询***

****5.3.1 正向查找****

	res1=Book.objects.first()
	print(res1.title)
	print(res1.price)
	print(res1.publish)
	print(res1.publisher.name)          #因为一对多的关系,所以res1.publisher是一个对象,不是一个QuerySet集合
	
****5.3.2 反向查找****

	res2=Publish.objects.last()
	print(res2.name)
	print(res2.city)
	print(res2.book_set.all())          #res2.book_set是一个QuerySet集合,所以会打印集合中的所有对象元素
	
***5.4 双下划线(__)查询***

****5.4.1 双下划线(__)之单表条件查询****

例子:

        table1.objects.filter(id__lt=10,id__gt=1)               #获取id小于10,且大于1的记录
        table1.objects.filter(id__in=[11,22,33,44])             #获取id在[11,22,33,44]中的记录
        table1.objects.exclude(id__in=[11,22,33,44])            #获取id不在[11,22,33,44]中的记录
        table1.objects.filter(name__contains="content1")        #获取name中包含有"contents"的记录(区分大小写)
        table1.objects.filter(name__icontains="content1")       #获取name中包含有"content1"的记录(不区分大小写)
        
        table1.objects.filter(id__range=[1,4])                  #获取id在1到4(不包含4)之间的的记录
	
可使用的条件:

        startswith			指定开头的匹配条件
        istartswith			指定开头的匹配条件(忽略大小写)
        endswith			指定结束的匹配条件
        iendswith			指定结束的匹配条件(忽略大小写)
	
****5.4.2 双下划线(__)之多表条件查询****

正向查找(条件)之一对一查询
    
        #查询书名为"python"的书的id号
        res3=Book.objects.filter(title="python").values("id")
        print(res3)
	
正向查找(条件)之一对多查询
	
        #查询书名为"python"的书对应的出版社的地址
        res4=Book.objects.filter(title="python").values("publisher__city")
        print(res4)
        
        #查询"aaa"作者所写的所有的书的名字
        res5=Book.objects.filter(author__name="aaa").values("title")
        print(res5)
        
        #查询"aaa"作者所写的所有的书的名字(与上面的用法没区别)
        res6=Book.objects.filter(author__name="aaa").values("title")
        print(res6)
	
反向查找之一对多查询

        #查询出版了书名为"python"这本书的出版社的名字
        res7=Publisher.objects.filter(book__title="python").values("name")
        print(res7)
        
        #查询写了书名为"python"的作者的名字
        res8=Publisher.objects.filter(book__title="python").values("book__authors")
        print(res8)
	
反向查找之多对多查询
	
        #查询所写的书名为"python"的作者的名字
        res9=Author.objects.filter(bool__title="python").values("name")
        print(res9)
	
条件查询即与对象查询对应,是指`filter`,`values`等方法中的通过__来明确查询条件

***5.4 聚合查询和分组查询***

****5.4.1 aggregate(`*args,**kwargs`)****

通过到`QuerySet`进行计算,返回一个聚合值的字典,`aggregate()`中的每一个参数都指定一个包含在字典中的返回值,即在查询集合中生成聚合

例子:

        from django.db.models import Avg,Max,Min,Sum
        
        #计算所有书籍的平均价格,书籍最高的价格和最低价格
        res1=Book.objects.all().aggregate(Avg("price"),Max("price"),Min("price"))
        print(res1)#打印为"{'price__avg':xxx}"
    
`Django`的查询语句提供了一种方式描述所有图书的集合

	aggregate()子句的参数可以指定想要计算的聚合值.
	aggregate()是QuerySet的一个终止子句,返回一个包含一些键值对的字典.
		字典的键的名称是聚合值的标识符,是按照字段和聚合函数的名称自动生成出来的.
		字典的值是计算出来的聚合值.
		
可以为聚合值指定一个名称.

        #计算所有书籍的平均价格,并给书籍的平均价格起一个别名
        res2=Book.objects.all().aggregate(average__price=Avg("price"))
        print(res2)#打印为"{'average_price':xxx}"
    
****5.4.2 annotate(`*args,**kwargs`)****

可以通过计算查询结果中每一个对象所关联的对象集合,从而得出总计值(也可以是平均值或总和),即为查询集的每一项生成聚合

        #查询作者"aaa"所写的所有的书的名字
        res3=Book.objects.filter(authors__name="aaa").values("title")
        print(res3)
        
        #查询作者"bbb"所写的所有的书的总价格
        res4=Book.objects.filter(authors__name="bbb").aggregate(Sum("price"))
        print(res4)
    
查询各个作者所写的书的总价格,就要使用分组

        #查询每个作者所写的所有书籍的总价格
        res5=Book.objects.values("authors__name").annotate(Sum("price"))
        print(res5)
        
        #查询各个出版社所出版的书籍的总价格
        res6=Book.objects.values("Publish__name").annotate(Min("price"))
        print(res6)
    
***5.5 `F`查询和`Q`查询***

****5.5.1 `F`查询专门取对象中某列值的操作****

        #导入F
        from django.db.models import F
        #把table1表中的num列中的每一个值在的基础上加10
        table1.objects.all().update(num=F("num")+10)

****5.5.2 `Q`构建搜索条件****

        #导入Q
        from django.db.models import Q
        
        Q对象可以对关键字参数进行封装,从而更好的应用多个查询
        #查询table2表中以"aaa"开头的所有的title列
        q1=table2.objects.filter(Q(title__startswith="aaa")).all()
        print(q1)
	
`Q`对象可以组合使用`&`,`|`操作符,当一个操作符是用于两个`Q`对象时,会产生一个新的`Q`对象

	#查找以"aaa"开头,或者以"bbb"结尾的所有title
	Q(title__startswith="aaa") | Q(title__endswith="bbb")
	
`Q`对象可以用`"~"`操作符放在表达式前面表示否定,也可允许否定与不否定形式的组合

	#查找以"aaa"开头,且不以"bbb"结尾的所有title
	Q(title__startswith="aaa") & ~Q(title__endswith="bbb")
	
`Q`对象可以与关键字参数查询一起使用,`Q`对象放在关键字查询参数的前面

查询条件:

	#查找以"aaa"开头,以"bbb"结尾的title且书的id号大于4的记录
	Q(title__startswith="aaa") | Q(title__endswith="bbb"),book_id__gt=4
	
**6. ORM之改(update,save)**

***6.1 使用`save`方法将所有属性重新设定一遍,效率低***

	author1=Author.objects.get(id=3)#获取id为3的作者对象
	author1.name="jobs"#修改作者对象的名字
	author1.save()#把更改写入数据库
	
***6.2 使用`update`方法直接设置对就的属性***

	Publish.objects.filter(id=2).update(name="北京出版社")
	
***6.3 需要注意的点***

`update()`是`QuerySet`对象的一个方法,`get`返回的是一个`model`对象,其没有`update`方法.

`filter`返回的是一个`QuerySet`对象,`filter`里可以设定多个过滤条件