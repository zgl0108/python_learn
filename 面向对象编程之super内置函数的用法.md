先来看一段代码：

定义一个名叫People的父类，又定义了一个叫Teacher的老师类和一个叫Student的学生类
来继承People的类，并根据这两个子类实例化出两个对象s1和t1。

        class Date:
            def __init__(self,year,mon,day):
                self.year=year
                self.mon=mon
                self.day=day
        
            def birth_info(self):
                print("The birth is %s-%s-%s"%(self.year,self.mon,self.day))
        
        class People:
            def __init__(self,name,age):
                self.name=name
                self.age=age
        
        
            def walk(self):
                print("%s is walking"%self.name)
        
        class Teacher(People):
            def __init__(self,name,age,year,mon,day,course):
                People.__init__(self,name,age)
                self.course=course
                self.birth=Date(year,mon,day)
        
            def teach(self):
                print("%s is teaching"%self.name)
        
        class Student(People):
            def __init__(self,name,age,year,mon,day,group):
                People.__init__(self,name,age)
                self.birth = Date(year, mon, day)
                self.group=group
        
            def study(self):
                print("%s is studying"%self.name)
        t1=Teacher("alex",28,1989,9,2,"python")
        s1=Student("jack",22,1995,2,8,"group2")
        
现在问题来了，假如因为需要，我要修改老师类和学生类的父类People的名字。

这样一来，在老师类Teacher和学生类Student中继承的类People也要修改，以及它们

调用的`__init__`方法的那个父类也要修改名字，太麻烦了有没有？

这时候就可以使用`super()`这个内置函数来搞定了。

在python解释器中查看帮助信息：

    help(super)
    
得到如下信息：

    Help on class super in module builtins:
    
    class super(object)
     |  super() -> same as super(__class__, <first argument>)
     |  super(type) -> unbound super object
     |  super(type, obj) -> bound super object; requires isinstance(obj, type)
     |  super(type, type2) -> bound super object; requires issubclass(type2, type)
     
`super`是一个内置函数，加括号就得到一个对象，对象`super()`加`"."`可以直接调用父类的`__init__`方法。

这个对象在调用父类的`__init__`时，实际上就是在调用父类的绑定方法，所以就不需要在括号里加上`self`了。

修改后的代码如下：

        class Date:
            def __init__(self,year,mon,day):
                self.year=year
                self.mon=mon
                self.day=day
        
            def birth_info(self):
                print("The birth is %s-%s-%s"%(self.year,self.mon,self.day))
        
        class People:
            def __init__(self,name,age):
                self.name=name
                self.age=age
        
        
            def walk(self):
                print("%s is walking"%self.name)
        
        class Teacher(People):
            def __init__(self,name,age,year,mon,day,course):
                super().__init__(name,age)
                self.course=course
                self.birth=Date(year,mon,day)
        
            def teach(self):
                print("%s is teaching"%self.name)
        
        class Student(People):
            def __init__(self,name,age,year,mon,day,group):
                super().__init__(name,age)
                self.birth = Date(year, mon, day)
                self.group=group
        
            def study(self):
                print("%s is studying"%self.name)
        t1=Teacher("alex",28,1989,9,2,"python")
        s1=Student("jack",22,1995,2,8,"group2")    	

这样一来，父类的名字改变了，代码里面继承的父类的`"__init__"`方法的名字也不需要修改了。

    python2中，也可以使用super，其调用方法为：super(Teacher,self)

使用`super()`函数时，python会在mro列表中继续搜索下一个类。
```
只要每个重定义的方法统一使用super()并只调用它一次，那么控制流最终会遍历完整个mro列表。每个方法只会调用一次。
使用super调用的所有的属性，都是从mro列表当前的位置往后找，看mro列表的顺序就可以看到子类的继承关系
```
查看上面代码中Teacher这个子类的mro列表可以使用这个方法：

    Teacher.mro()	
    
使用`super`可以避免使用多重继承时，子类继承父类的顺序问题。

子类继承父类的数据属性和函数属性时，先执行的先生效，当后面的代码与前面的代码有冲突时，

后面的代码会把前面的代码覆盖掉，不使用`super`时需要自己解决继承的顺序问题，使用`super`就可以很好的解决这个问题了。		