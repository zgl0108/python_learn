我们家里都有电视机，从开机，浏览节目，换台到关机，我们不需要知道电视机里面的具体细节，只需要在用的时候按下遥控器就可以完成操作，这就是功能的封装。

在用支付宝进行付款的时候，只需要在用的时候把二唯码给收款方或是扫一下收款方提供的二唯码就可以完成支付，不需要知道支付宝的支付接口，以及后台的处理数据的能力，这就是方法的封装。

    生活中处处都是封装的概念。
    封装不是单纯意义的隐藏
    封装数据的主要原因是保护隐私
    封装方法的主要有因是隔离复杂度

在编程语言里，对外提供接口，表示这个接口的函数，通常称为接口函数。

封装分为两个层面：

    第一层面的封装：创建类和对象时，分别创建两者的名称空间。只能通过类名加“.”或者obj.的方式访问里面的名字
    
    第二层面的封装，类中把某些属性和方法隐藏起来，或者定义为私有，只在类的内部使用，在类的外部无法访问，或者留下少量的接口(函数)供外部访问

但无论是哪种层面的封装，都要对外提供好访问内部隐藏内容的接口。

在python中，使用双下划线的方式实现隐藏属性(设置成私有属性)。

在python中，隐藏类的属性用什么办法呢？？

来看下面的例子：

    class Teacher:
        def __init__(self,name,age,course):
            self.name=name
            self.age=age
            self.course=course
    
        def teach(self):
            print("%s is teaching"%self.name)
    
    class Student:
        def __init__(self,name,age,group):
            self.name=name
            self.age=age
            self.group=group
    
        def study(self):
            print("%s is studying"%self.name)
            
用所定义的类创建一个老师s1和一个学生s1。

    t1=Teacher("alex",28,"python")
    s1=Student("jack",22,"group2")
    
分别调用老师和学生的姓名，年龄等特征：

    print(t1.name,t1.age,t1.course)
    print(s1.name,s1.age,s1.group)
    
返回如下的信息：

    alex 28 python
    jack 22 group2
    
调用老师的教书技能和学生的学习技能：

    t1.teach()
    s1.study()
    
返回信息如下：

    alex is teaching
    jack is studying

把这两类中的一些属性隐藏起来后，代码如下：

        class Teacher:
            def __init__(self,name,age,course):
                self.__name=name
                self.__age=age
                self.__course=course
        
            def teach(self):
                print("%s is teaching"%self.__name)
        
        class Student:
            def __init__(self,name,age,group):
                self.__name=name
                self.__age=age
                self.__group=group
        
            def study(self):
                print("%s is studying"%self.__name)
                
创建老师和学生的实例：
    
    t1=Teacher("alex",28,"python")
    s1=Student("jack",22,"group2")
    
再用前面一样的方法调用老师和学生的特征：

    print(t1.name,t1.age,t1.course)
    print(s1.name,s1.age,s1.group)
    
此时这样调用就会报错，输出信息如下所示：

    Traceback (most recent call last):
      File "E:/py_code/oob.py", line 114, in <module>
        print(t1.name,t1.age,t1.course)
    AttributeError: 'Teacher' object has no attribute 'name
    
再调用老师的教书技能和学生的学习技能：

    t1.teach()
    s1.study()
    
返回信息如下：

    alex is teaching
    jack is studying


可以看到隐藏属性后，再像以前那样访问对象内部的属性，就会返回属性错误，那现在要怎么才能访问其内部属性呢？

现在来查看t1和s1的名称空间

    print(t1.__dict__)
    {'_Teacher__name': 'alex', '_Teacher__age': 28, '_Teacher__course': 'python'}
    print(s1.__dict__)
    {'_Student__name': 'jack', '_Student__age': 22, '_Student__group': 'group2'}

可以看到t1和s1的名称空间完全改变了，现在访问t1名称空间里的key，可以看到什么呢？？

    print(t1._Teacher__name)
    print(t1._Teacher__age)
    print(t1._Teacher__course)
    
返回如下：

    alex
    28
    python
    
这次没有报错了，看来隐藏属性之后可以通过"_类名__属性"的方式来访问其内部的属性值，

来得到和隐藏属性之前，直接查看其内部属性一样的值。

    python对于这样的隐藏，有一些特点：
    1.类中定义的_X吸能在内部使用，如self._X,引用的就是变形之后的结果。
    2.这种变形其实正是对外部的改变，在外部是无法通过_X这个名字访问到的。

事实上，python对于这一层面的封装，需要在类中定义一个函数。

这样在类的内部访问被隐藏的属性，在外部就可以使用了，而且这种形式的隐藏并没有

真正意义上的限制从外部直接访问属性，知道了类名和属性名一样可以调用类的隐藏属性。

python并不会真的阻止开发人员访问类的私有属性，模块也是遵循这种约定。

很多模块都有以单下划线开头的方法，此时使用

    from module import *
    
时，这些方法是不会被导入的，此时必须要通过 

    from module import _private_module
    
来导入这种类型的模块。

