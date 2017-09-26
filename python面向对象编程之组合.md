前面讲了面向类与对象的继承，知道了继承是一种什么“是”什么的关系。

然而类与类之间还有另一种关系，这就是组合

先来看两个例子：

先定义两个类，一个老师类，老师类有名字，年龄，出生的年，月和日，所教的课程等特征以及走路，教书的技能。

        class Teacher:
            def __init__(self,name,age,year,mon,day):
                self.name=name
                self.age=age
                self.year=year
                self.mon=mon
                self.day=day
        
            def walk(self):
                print("%s is walking slowly"%self.name)
        
            def teach(self):
                print("%s is teaching"%self.name)
            
再定义一个学生类，学生类有名字，年龄，出生的年，月和日，学习的组名等特征以及走路，学习的技能

        class Student:
            def __init__(self,name,age,year,mon,day):
                self.name=name
                self.age=age
                self.year=year
                self.mon=mon
                self.day=day
        
            def walk(self):
                print("%s is walking slowly"%self.name)
        
            def study(self):
                print("%s is studying"%self.name)
                
根据类的继承这个特性，可以把代码缩减一下。

定义一个人类，然后再让老师类和学生类继承人类的特征和技能：

        class People:
            def __init__(self,name,age,year,mon,day):
                self.name=name
                self.age=age
                self.year=year
                self.mon=mon
                self.day=day
        
            def walk(self):
                print("%s is walking"%self.name)
        
        class Teacher(People):
            def __init__(self,name,age,year,mon,day,course):
                People.__init__(self,name,age,year,mon,day)
                self.course=course
        
            def teach(self):
                print("%s is teaching"%self.name)
        
        class Student(People):
            def __init__(self,name,age,year,mon,day,group):
                People.__init__(self,name,age,year,mon,day)
                self.group=group
        
            def study(self):
                print("%s is studying"%self.name)
            
再对老师和学生进行实例化，得到一个老师和一个学生。

    t1=Teacher("alex",28,1989,9,2,"python")
    s1=Student("jack",22,1995,2,8,"group2")
    
现在想知道t1和s1的名字，年龄，出生的年，月，日都很容易，但是想一次性打印出

t1或s1的生日就不那么容易了，这时就需要用字符串进行拼接了，有没有什么更好的办法呢？？

那就是组合。

    继承是一个子类是一个父类的关系，而组合则是一个类有另一个类的关系。
    
可以说每个人都有生日，而不能说人是生日，这样就要使用组合的功能 。

可以把出生的年月和日另外再定义一个日期的类，然后用老师或者是学生与这个日期的类

组合起来，就可以很容易得出老师t1或者学生s1的生日了，再也不用字符串拼接那么麻烦了。

来看下面的代码：

        class Date:
            def __init__(self,year,mon,day):
                self.year=year
                self.mon=mon
                self.day=day
        
            def birth_info(self):
                print("The birth is %s-%s-%s"%(self.year,self.mon,self.day))
        
        class People:
            def __init__(self,name,age,year,mon,day):
                self.name=name
                self.age=age
                self.birth=Date(year,mon,day)
        
            def walk(self):
                print("%s is walking"%self.name)
        
        class Teacher(People):
            def __init__(self,name,age,year,mon,day,course):
                People.__init__(self,name,age,year,mon,day)
                self.course=course
        
            def teach(self):
                print("%s is teaching"%self.name)
        
        class Student(People):
            def __init__(self,name,age,year,mon,day,group):
                People.__init__(self,name,age,year,mon,day)
                self.group=group
        
            def study(self):
                print("%s is studying"%self.name)
        t1=Teacher("alex",28,1989,9,2,"python")
        s1=Student("jack",22,1995,2,8,"group2")

这样一来，可以使用跟前面一样的方法来调用老师t1或学生s1的姓名，年龄等特征

以及走路，教书或者学习的技能。

    print(t1.name)
    t1.walk()
    t1.teach()
    
输出为：

    alex    
    alex is walking
    alex is teaching
    
那要怎么能够知道他们的生日呢:

    print(t1.birth)
    
输出为：

    <__main__.Date object at 0x0000000002969550>
    
这个birth是子类Teacher从父类People继承过来的，而父类People的birth又是与Date这个类组合在一起

所以，这个birth是一个对象。而在Date类下面有一个birth_info的技能，这样就可以通过调用Date下面的birth_info这个函数属性来知道老师t1的生日了。

    t1.birth.birth_info()
    
得到的结果为：

    The birth is 1989-9-2
    
同样的，想知道实例学生s1的生日也用同样的方法：

    s1.birth.birth_info()
    
得到的结果为：

    The birth is 1995-2-8

组合就是一个类中使用到另一个类，从而把几个类拼到一起。组合的功能也是为了减少重复代码。
