现在有三处类

    class BookInfo(models.Model):
        title=models.CharField(verbose_name="书名",max_length=64)
        price=models.IntegerField(verbose_name="价格")
        publisher=models.ForeignKey(verbose_name="出版社",to="Publish")
        
    class Publish(models.Model):
        name=models.CharField(verbose_name="名字",max_length=64)
        
    class Author(models.Model):
        username=models.CharField(verbose_name="用户名",max_length=32)
        password=models.CharField(verbose_name="密码",max_length=64)
        books=models.ManyToManyField(verbose_name="书籍",to="BookInfo")
 
## all

models.BookInfo.objects.all(),返回的结果是一个包括书对象的列表

例如

    [book_obj1,book_obj2,book_obj3....]

## values

models.BookInfo.objects.values("id","title","price")返回一个由字段的及其值构成的字典组成的列表

例如

    [{"id":1,"title":"book1","price":39},{"id":2,"title":"book2","price":66},...]

## values_list

models.BookInfo.objects.values_list("id","title","price")返回一个由字段构成的元组组成的列表

    [(1,"book1",39),(2,"book2",45),(3,"book3",66),....]

ForeignKey相关操作
       
## 1. Publish数据表中有三个字段:id,name,fk_id

## 2. all()跨表操作

    book_list=models.BookInfo.objects.all()
    
publish_list是一个由publish对象组成的列表,循环遍历每一个对象,可以取出来的信息有

    for item in book_list:
        print(item.id)
        print(item.title)
        print(item.price)
        print(item.publisher.name)
        print(item.publisher.id)
## 3. values()跨表操作
        
    publish_list=models.Publish.objects.values("id","name","bookinfo_id","bookinfo__title")

    for item in publish_list:
        item["id"]
        item["name"]
        item["bookinfo_id"]
        item["bookinfo__name"]

## 4. values_list()跨表操作
        
    publish_list=models.Publish.objects.values("id","name","bookinfo_id","bookinfo__title")

    for item in publish_list:
        item[0]     
        item[1]     
        item[2]     
        item[3]     
            
## 5. 找出书数据表中"publish1"出版的书

    models.BookInfo.objects.filter(publish__name="publish1").all()
    models.Publish.objects.filter(bookinfo__title="book1").all()
        
ManyToMany相关操作
        
## 1. Author表中的字段有:id,username,password

## 2. 作者"user1"写了"book1","book2","book3"三本书,生成数据库

    user_obj=models.Author.objects.create(username="user1",password="password")
    user_obj.books.create(title="book1",price=39,publish="publish1")
    
    book_obj2=["book2",55,"publish2"]
    user_obj.books.create(*book_obj2)
    
    book_obj3={"title":"book3","price":88,"publisher":"publish3"}
    user_obj.books.create(**book_obj3)
        
## 3. 
        
        
        
        
        
        
        
        
        
        
        
        