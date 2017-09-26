前面我们定义了人的类，并用这个类实例化出两个人jack和lily,查看了它们的内存空间。

现在我们再来看看类中所存在的对向对象编程的三大特性之继承的一些特性。

前面定义了一个人的类，可是我们还知道，人都有属于自己的职业，比如说老师类，医生类，警察类等。

我们可以为每个职业都定义一个类，按照前面的定义，我们可以使用下面的代码来实现。

定义一个老师类：

        class Teacher:
            def __init__(self,name,age,sex,course):
                self.name=name
                self.age=age
                self.sex=sex
                self.course=course
        
            def walk(self):
                print("%s is walking slow"%self.name)
        
            def teach(self):
                print("%s is teaching"%self.name)
            
定义一个学生类：

        class Student:
            def __init__(self,name,age,sex,group):
                self.name=name
                self.age=age
                self.sex=sex
                self.group=group
                
            def walk(self):
                print("%s is walking slow"%self.name)
                
            def study(self):
                print("%s is studying hard"%self.name)
			
我们可以看到teacher和student类中，有很多重复的代码。

它们都有人类所共有的name,age,sex等特征，以及有人类有的walk这个技能，

那么我们就可以把人类共有的name,age,sex特征和walk技能抽离出来，生成一个人的类，

然后用老师和学生的类来继承人的类的这些特征和技能，这样可以避免写重复的代码。

    继承关系是子类继承父类，是类与类之间的关系

解决代码重用的问题，减少代码冗余，这就是我们说的类的三大特征之一的继承。

	把两个或多个类中的共同点抽离出来，生成一个新的类，也就是被继承的类，我们称之为父类
	把从父类中继承特征和技能的类称为子类或基类
	
具体实现代码如下：

**1.我们先把老师和学生中所重复的代码抽离出来，生成一个人类**

        class Person:
            def __init__(self,name,age,sex):
                self.name=name
                self.age=age
                self.sex=sex
                
            def walk(self):
                print("%s is walking slow"%self.name)	
**2.然后定义一个老师类，来继承人的类的一个特征和技能**

        class Teacher(Person):
            def __init__(self, name, age, sex, course):
                Person.__init__(self, name, age, sex)
                self.course = course
        
            def teach(self):
                print("%s is teaching" % self.name)
**3.最后，再定义一个学生类，来继承人的类的一些特征和技能**

        class Student(Person):
            def __init__(self, name, age, sex,group):
                Person.__init__(self, name, age, sex)
                self.group = group
        
            def study(self):
                print("%s is studying hard" % self.name)

类定义好了，在通过把类实例化生成一个学生和一个老师

    t1=Teacher("Jack",18,"male","python")
    s1=Student("Tom",28,"female","group1")

就可以调用s1或t1的特征和技能了。

比如，我想知道学生的姓名和老师的年龄，就可以这样做：
	
    print(t1.age,s1.name)
输出结果为：

    18 Tom						
调用老师t1的走路的技能：	
			
    t1.walk()
输出为：
    
    Jack is walking slow
调用老师t1的教书的技能：

    t1.teach()
输出为：

    Jack is teaching
调用学生s1的走路的技能：

    s1.walk()
输出为：

    Tom is walking slow
调用学生s1学习的技能：

    s1.study()
输出为：

    Tom is studying hard						
我们还可以使用下面的语句来查看子类Student所继承的父类的名称：

    print(Student.__bases__)
得到结果如下：

    (<class '__main__.Person'>,)
同样的，打印子类Teacher的父类也会得到同样的结果，显示其父类为Person.

在上面的输出中，可以看到输出结果是一个元组。这样的话，一个子类就可以继承多个父类了。

查看子类的父类得到的结果是前面定义的Person类，那我们查看Person的类的话，会得到什么样的结果呢？

    print(Person.__bases__)
输出为：
    
    (<class 'object'>,) 
           
其结果也是一个元组，但是这里出现了一个`object`，那么这个`object`又是什么东东？

事实上，在python3中，所有的类默认都继承`object`类。

    在python中:
    凡是继承了object类的子类，以及该子类的子类都被为新式类;
    没有继承object类的子类称为经典类.
    
所以python3中，所有的类都是新式类。

而在python2中，没有继承`object`的类，以及它的子类，通常称为经典类。

来看几个例子：
这几个例子，都是在python2的解释器中运行的：

    >>> class Foo:
    ...     pass
    ... 
    >>> Foo.__bases__
    ()
    >>> class Bar(object):
    ...     pass
    ... 
    >>> Bar.__bases__
    (<type 'object'>,)
可以看到，Foo这个类是一个经典类，而定义的第二个Bar类则是一个新式类

在定义老师和学生类的时候，在类的名字后面要加上被继承的类Person的名字,以告诉python解释器，这里调用了类的继承的特性。

