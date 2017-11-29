单例模式是一种常用的软件设计模式.

在单例模式的核心结构中,只包含一个被称为单例类的特殊类.

通过单例模式可以保证系统中一个类只有一个实例,而且这个实例可以轻易被外界访问,方便控制实例对象的个数以节约系统资源.

单例模式是解决一个系统中某个类的实例化对象有且只能有一个的最好解决方案.

单例模式的要点有三个:

* 某个类只能有一个实例
* 这个类必须自行创建其唯一实例
* 这个类必须自行向整个系统提供这个唯一实例.

在python中,单例模式有三种实现方式:

### 方法一,使用__new__方法 

先定义一个类,类中定义`__new__`方法,然后将类的一个实例类绑定到类变量中.

如果类的`_instance`值为None,则说明这个类还没有被实例化过,程序会自动实例化一个类的实例,然后返回.

如果类的`_instance`值不为None,则程序会直接返回`_instance`.

代码如下：

    class Singleton(object):
    
        _instance = None
    	
		def __init__(self):
			pass
        
        def __new__(cls, *args, **kwargs):
        
            if not cls._instance:
                cls._instance = super(Singleton, cls).__new__(cls, *args, **kwargs)  
            return cls._instance  
     
    class MyClass(Singleton):  
        a = 1

在上面的代码中，我们将类的实例和一个类变量 `_instance `关联起来.

如果 `cls._instance`为 None 则创建实例，否则直接返回` cls._instance`。

用上来定义的类实例化两个对象:

	cls1=MyClass()
	cls2=MyClass()

	print(id(cls1))
	print(id(cls2))

	print(cls1 == cls2)
	print(cls1 is cls2)
	
得到的结果

	43606480
	43606480
	True
	True
	
### 方法二,使用decorator装饰器

我们知道，装饰器（`decorator`）可以动态地修改一个类或函数的功能。

在这里使用装饰器来装饰某个类，使其只能生成一个实例，代码如下：

    def singleton(cls):
        instances={}
    
        def getinstance(*args,**kwargs):
            if cls not in instances:
                instances[cls]=cls(*args,**kwargs)
    
            return instances[cls]
        return getinstance
    
    @singleton
    class MyClass(object):
        a=1

在上面，我们定义了一个装饰器`singleton`，它返回了一个内部函数`getinstance`，该函数会判断某个类是否在字典`instances`中，

如果不存在，则会将cls作为`key，cls(*args, **kw)`作为`value`存到`instances`中，否则，直接返回`instances[cls]`。

使用上面定义的类实例化两个对象,比较两个对象

	cls1=MyClass()
	cls2=MyClass()

	print(id(cls1))
	print(id(cls2))

	print(cls1 == cls2)
	print(cls1 is cls2)

得到的结果为:

	43672016
	43672016
	True
	True
	
### 方法三,使用元类（metaclass）

元类（`metaclass`）可以控制类的创建过程，它主要做三件事：

    拦截类的创建
    修改类的定义
    返回修改后的类

用元类实现单例模式的代码如下：
```
    class Singleton(type):
        _inst = {}
    
        def __call__(self, *args, **kw):
            if self not in self._inst:
                self._inst[self] = super(Singleton, self).__call__(*args, **kw)
            return self._inst[self]
    
    class MyClass1(metaclass=Singleton):
        def __init__(self):
            self.xx = 0
    
        def getval(self):
            return self.xx
    
        def setval(self, val):
            self.xx = val

	cls1=MyClass()
	cls2=MyClass()

	print(id(cls1))
	print(id(cls2))

	print(cls1 == cls2)
	print(cls1 is cls2)

```
得到的结果为:

	43477984
	43477984
	True
	True

### 方法四,使用classmethod方法创建单例模式

	class Foo:
		_instance = None

		def __init__(self):
			pass

		@classmethod
		def get_instance(cls):
			if cls._instance:
				return cls._instance
			else:
				obj=cls()
				cls._instance=obj
				return obj

	cls1=Foo.get_instance()     # 实例化对象a1时,没有执行Foo这个类的__init__方法,直接执行Foo类的get_instance方法,在这里cls代指的是Foo类
								# 前面把_instance赋值为None,所以直接执行else中的语句,实例化一个obj对象,然后把obj对象中的_instance方法赋值为obj对象本身,然后返回obj对象
	cls2=Foo.get_instance()     # 实例化a1时,Foo类中的_instance已经被赋值为obj对象,所以再次执行Foo中的get_instance方法时,是执行if中的语句
								# 此时cls._instance就指的是obj对象,所以这里也返回obj这个对象
	print(id(cls1))
	print(id(cls2))

	print(cls1 == cls2)
	print(cls1 is cls2)

这种方法由于在实例化对象时要调用类中的`get_instance`方法,所以用的不多,知道即可.

### 特别声明

Python的模块是天然的单例模式

在一个py文件中,多次导入同一个模块,这个模块也只有在第一次的时候被导入,后续的该模块导入语句都不会再执行了