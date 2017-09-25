`configparser`模块用于生成与`windows.ini`文件类似格式的配置文件，可以包含一节或多节(`section`),每个节可以有一个或多个参数(键＝值)

在学习这个模块之前，先来看一个经常见到的配置文档：
```
    [DEFAULT]
    serveraliveinterval = 45
    compression = yes
    compressionlevel = 9
    forwardx11 = yes
    
    [bitbucket.org]
    user = admin
    
    [topsecret.server.com]
    port = 1000345
    forwardx11 = no
```
**1.创建配置文件**

现在来用python中的`configparser`模块生成一个与上面相同的配置文档
```
    #先导入configparser模块
    import configparser
    
    #为其中一个方法定义一个变量
    cfp=configparser.ConfigParser()
    
    #定义"DEFAULT"节及其子参数
    cfp["DEFAULT"]={"ServerAliveInterval":45,
                    "Compression":"yes",
                    "CompressionLevel":9,
                    "ForwardX11":"yes"
                    }
                    
    #定义“bitbucket.org”节
    cfp["bitbucke.ort"]={"USER":"admin"}
    
    #定义"topsecret.server.com"节及其参数
    cfp["topsecret.server.com"]={"Port":1000345,"ForwardX11":"no"}
    
    #把上面定义的节及其参数写入"cfp.ini"这个文件
    with open("cfp.ini","w") as f:
        cfp.write(f)
```       
运行程序后，生成的配置文件如下：
```
    [DEFAULT]
    serveraliveinterval = 45
    compression = yes
    compressionlevel = 9
    forwardx11 = yes
    
    [bitbucket.org]
    user = admin
    
    [topsecret.server.com]
    port = 1000345
    forwardx11 = no
```    
可以看到，跟文章开始处的配置文件格式一模一样的。

**2.读取配置文件中的变量**

目标配置文件就已经生成了，那现在想读取一个配置文件里的某个选项，该怎么做呢？
```
    import configparser
    
    cfp=configparser.ConfigParser()
    #读取目标配置文件
    cfp.read("cfp.ini")
    #打印目标配置文件的节
    print(cfp.sections())
```
理论上，读取配置文件的节，所得是一个列表，运行脚本，得到的字段为：

    ['bitbucket.org', 'topsecret.server.com']
    
这是因为第一节是“DEFAULT”字段，这个字段是默认对整个配置文件生效的，

所以"DEFAULT"默认是不会显示出来。

如果把配置文件中的“DEFAULT”改成“DEFAULTS”，如下：
```
    [DEFAULTS]
    serveraliveinterval = 45
    compression = yes
    compressionlevel = 9
    forwardx11 = yes
    
    [bitbucket.org]
    user = admin
    
    [topsecret.server.com]
    port = 1000345
    forwardx11 = no
```  
然后再用上面的代码来读取整个配置文件的节,结果如下：

    ['DEFAULTS', 'bitbucket.org', 'topsecret.server.com']
    
打印“`bitbucket.ort`”节下所有的键和值
```
    import configparser
    
    cfp=configparser.ConfigParser()
    #读取目标配置文件
    cfp.read("cfp.ini")
    print(cfp.items("bitbucket.org"))
``` 
从返回结果可以看到，把"DEFAULT"这个节下面的键和值也一起返回了，正如前面所说的，“DEFAULT”是默认全局生效的

    [('serveraliveinterval', '45'), ('compression', 'yes'), ('compressionlevel', '9'), ('forwardx11', 'yes'), ('user', 'admin')]
    
打印“`bitbucket.ort`”节下所有的键
```
    import configparser
    
    cfp=configparser.ConfigParser()
    #读取目标配置文件
    cfp.read("cfp.ini")
    print(cfp.options("bitbucket.org"))
```  
结果同上面一样，"DEFAULT"下面的键也被一起返回了

    ['user', 'serveraliveinterval', 'compression', 'compressionlevel', 'forwardx11']   
    
**3.测试配置文件中的键和值**

***1.测试某个选项是否在配置文件中***
```
    import configparser
    
    cfp=configparser.ConfigParser()
    #读取目标配置文件
    cfp.read("cfp.ini")
    print("topsecret.server.com" in cfp)
```   
得到的结果为：

    True
    
***2.测试某个节下面是否有某个键***
```
    import configparser
    
    cfp=configparser.ConfigParser()
    #读取目标配置文件
    cfp.read("cfp.ini")
    print(cfp.get("bitbucket.org","compression"))
```
返回如下：

    yes

**4.修改配置文件**

***1.向配置文件里添加一个键值对***

代码如下：
```
    import configparser
    
    cfp=configparser.ConfigParser()
    #打开目标配置文件
    cfp.read("cfp.ini")
    #添加节
    cfp.add_section("conf")
    #为添加的节设置键和值
    cfp["conf"]["group"]="group01"
    
    #把修改写入配置文件
    cfp.write(open("cfp.ini","w"))
```
添加后的文件如下：
```
    [DEFAULTS]
    serveraliveinterval = 45
    compression = yes
    compressionlevel = 9
    forwardx11 = yes
    
    [bitbucket.org]
    user = admin
    
    [topsecret.server.com]
    port = 1000345
    forwardx11 = no
    
    [conf]
    group = group01
```    
可以看到已经增加一个“conf”的节，“conf”节下面增加一个值为“group01”的键“group”

***2.删除配置文件的节及其对就的键和值***
```
    import configparser
    
    cfp=configparser.ConfigParser()
    #读取目标配置文件
    cfp.read("cfp.ini")
    
    #从“topsecret.server.com”节中删除
    cfp.remove_option("topsecret.server.com","forwardx11")
    cfp.write(open("cfp.ini","w"))
```
返回结果如下：
```
    [DEFAULT]
    serveraliveinterval = 45
    compression = yes
    compressionlevel = 9
    forwardx11 = yes
    
    [bitbucket.org]
    user = admin
    
    [topsecret.server.com]
    port = 1000345
```
可以看到"forwardx11"这个键值对已经从"topsecret.server.com"这个节中删除掉了。

***3.为某个键设置值***

代码如下：
```
    import configparser
    
    cfp=configparser.ConfigParser()
    #读取目标配置文件
    cfp.read("cfp.ini")
    
    #为"topsecret.server.com"节添加一个"k1"键，其值为“v1”
    cfp.set("topsecret.server.com","k1","v1")
    #为“conf”节添加一个"k100"键，其值为"v100"
    cfp.set("conf","k100","v100")
    
    cfp.write(open("cfp.ini","w"))
    print(cfp.sections())
```
返回结果为：
```
    [DEFAULT]
    serveraliveinterval = 45
    compression = yes
    compressionlevel = 9
    forwardx11 = yes
    
    [bitbucker.ort]
    user = admin
    
    [topsecret.server.com]
    port = 1000345
    forwardx11 = no
    k1 = v1
    
    [conf]
    group = group01
    k100 = v100
```