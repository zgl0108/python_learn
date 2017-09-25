`pymysql`是python中操作mysql的模块。

**1.pymysql模块的安装**

    pip3 install pymysql
    
也可以使用`pycharm`这个IDE工具来安装`pymysql`这个模块。

**2.pymysql模块的使用**

***1.执行mysql语句，获取查询的结果***

代码如下:
```
    #!/usr/bin/env python
    #_*_coding:utf-8_*_
    
    import pymysql
    
    #创建连接
    conn=pymysql.connect(host="127.0.0.1",port=3306,user="root",passwd="",db="db1")
    #创建游标
    cursor=conn.cursor()
    #执行mysql语句，并返回执行的结果
    res=cursor.execute("select name from db1")
    #打印执行的结果
    print(res)
    #把要执行的语句提交，否则无法保存新建或者修改数据
    conn.commit()
    
    #关闭游标
    cursor.close()
    #关闭连接
    conn.close()
```
执行结果为：

    4    
因为从`db1.db1`这张表中检索到四条数据，所以返回的值为4

    需要注意的是，查询过程中存在中文的话，连接需要添加"charset='utf-8'",否则中文会显示乱码
    
***2.获取查询的数据***

代码如下:
```
    #!/usr/bin/env python
    #_*_coding:utf-8_*_
    
    import pymysql
    
    #创建连接
    conn=pymysql.connect(host="127.0.0.1",port=3306,user="root",passwd="",db="db1")
    #创建游标
    cursor=conn.cursor()
    #执行mysql语句
    cursor.execute("select name from db1")
    
    ＃获取所有的执行结果
    res=cursor.fetchall()
    ＃打印获取到的执行结果
    print(res)
    
    ＃提交要执行的mysql指令
    conn.commit()
    ＃关闭游标
    cursor.close()
    ＃关闭连接
    conn.close()
```
执行结果为：

    (('xiaoming',), ('xiaobing',), ('xiaoyong',), ('xiaojian',))
    
可以看到，返回的结果是一个元组类型的数据．

还可以在创建游标的时候，使用选项来指定返回的结果为哪种数据类型：

    cursor=conn.cursor(cursor=pymysql.cursors.DictCursor)
    
使用这个指令可以把返回的结果变成字典类型。

在获取执行的结果时，可以指定获取的结果的条数，可以使用的选项如下：

    fetchone()          取得检索结果的一条数据
    fetchmany(n)        取得检索结果的n条数据
    fetchall()          取得检索结果的所有数据
    
需要注意的是，与读取文件时的指针类似.如果在同一段代码中，先使用`fetchone()`获取检索结果的第一条数据，

然后再使用`fetchmany(2)`的话，指针会在检索结果的当前位置向后读取执行结果，而不会从头开始重新读取检索的结果．

代码如下：
```
    #!/usr/bin/env python
    #_*_coding:utf-8_*_
    
    import pymysql
    
    #创建连接
    conn=pymysql.connect(host="127.0.0.1",port=3306,user="root",passwd="",db="db1")
    #创建游标
    cursor=conn.cursor(cursor=pymysql.cursors.DictCursor)
    #执行mysql语句，并返回执行的结果
    cursor.execute("select name from db1")
    
    ＃取执行结果的第一条数据，并打印
    res1=cursor.fetchone()
    print("this is first result:",res1)
    ＃从剩下的执行结果中再取两条数据，并打印
    res2=cursor.fetchmany(2)
    print("this is second result:",res2)
    #再从剩下的数据中取所有的数据，并打印
    res3=cursor.getchall()
    print("this is third result:",res3)
    
    ＃提交要执行的命令
    conn.commit()
    ＃关闭游标
    cursor.close()
    ＃关闭连接
    conn.close()
```
执行结果如下：

    this is first result: {'name': 'xiaoming'}
    this is second result: [{'name': 'xiaobing'}, {'name': 'xiaoyong'}]
    this is third result: [{'name': 'xiaojian'}]
    
第一次取第一行的检索结果，第二次取两行的时候，第三次取剩下的所有的结果.因为数据表中只有四条记录，而第一次已经取走一行了，

第二次从第一次取得的结果又向后继续取两个值，所以最后取所有的值时，只剩下一个，所以第三次取得一个值。

在创建游标的时候,指定了返回的数据类型为字典类型,所以返回的结果是字典数据类型。

在使用`fetch`时，按照顺序进行取得数据，可以使用`cursor.scroll(num,mode)`来移动游标位置

    mode指定位置，是相对当前位置，还是绝对位置
    num指定移动的位数，正数向后移动，负数向前移动
    
例如：

    cursor.scroll(1,mode="relative")		#相对于当前的指针位置取一个值
    cursor.scroll(2,mode="absolute")		#在当前的绝对位置取一个值
    
`"relative"`与`"absolute"`的区别,看下面两段代码:

第一段代码:
```
    #!/usr/bin/env python
    #_*_coding:utf-8_*_
    
    import pymysql
    
    conn=pymysql.connect(host="127.0.0.1",port=3306,user="root",passwd="",db="db1")
    cursor=conn.cursor()
    
    cursor.execute("SELECT * FROM db1")
    cursor.fetchone()
    cursor.scroll(1,mode="relative")
    print(cursor.fetchone())
    
    conn.commit()
    cursor.close()
    conn.close()
```
执行结果如下:

    (3, 'xiaoyong', 'xiaoyong')
    
第二段代码:
```
    #!/usr/bin/env python
    #_*_coding:utf-8_*_
    
    import pymysql
    
    conn=pymysql.connect(host="127.0.0.1",port=3306,user="root",passwd="",db="db1")
    
    cursor=conn.cursor()
    
    cursor.execute("SELECT * FROM db1")
    cursor.fetchone()
    cursor.scroll(1,mode="absolute")
    print(cursor.fetchone())
    
    conn.commit()
    cursor.close()
    conn.close()
```
执行结果如下:

    (2, 'xiaobing', 'xiaobing')
    
***3.获取新创建数据的自增ID***

代码如下:
```
    #!/usr/bin/env python
    # _*_coding:utf-8_*_
    
    import pymysql
    
    conn=pymysql.connect(host="127.0.0.1",port=3306,user="root",passwd="",db="db1")
    
    cursor=conn.cursor()
    
    cursor.execute('INSERT INTO db1(name,password) VALUES("xiaofei","xiaofei")')
    
    conn.commit()
    cursor.close()
    conn.close()
    
    res=cursor.lastrowid
    print(res)
```
执行结果为:

    5
    
数据表db1中本来有四条数据,现在新增一条,其ID为自增类型,所以返回结果为5