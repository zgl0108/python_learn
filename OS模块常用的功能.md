
**OS模块常用的功能**

***目录相关***
```
chdir()             改变当前工作目录
chroot()            改变当前进程的根目录
listdir()           列出目录下的所有内容
makedirs()          创建多级目录
mkdir()             创建一个目录
getcwd()            返回当前工作的目录，即python脚本工作的目录路径
rmdir()             删除一个目录
removedirs()        删除多级目录
```
***文件相关***
```
mkfifo()            创建一个管道文件
mknod()             创建设备文件
remove()            删除一个文件或目录
unlink()            删除一个文件(跟remove功能一样)
rename()            重命名一个文件
stat()              显示一个文件的状态信息
symlink()           为指定的文件创建软链接
utime()             更新时间戳
tmpfile()           创建并打开(w+b)一个新的临时文件
walk()              生成一个目录树
curdir()            指当前目录
pardir()            上一级目录
sep()               输出系统特定的路径分隔符
linesep()           当前平台使用的行终止符
name()              指当前使用的操作系统
``` 
***访问权限***
```
access()            测试一个uid/gid是否对一个文件具有访问权限
chmod()             修改文件的权限
chown()             修改文件属主和属组
umask()             设置默认权限模式
```
***文件描述符***
```
open()
read()
write()
```
***设备文件***
```
makedev()           创建设备
major()			
minor()
```
	
**os.path路径管理**
```
abspath         获取路径的绝对路径
basename        取目录的基名
dirname         取目录的目录名
exists          测试指定文件是否存在
getatime        获取文件最后一次的访问时间	
getctime        获取文件最后一次修改(内容)的时间
getmtime        获取文件最后一次改变(文件名,属性)的时间
getsize         返回文件的大小
isabs           判断指定路径是否为绝对路径
isdir           判断是否为目录
isfile          判断是否为普通文件
islink          判断是否为符号链接
ismount         判断指定路径是否为挂载点
join            将多个离散的路径整合成一个目录名	
samefile        判断两个路径是否指向了同一个文件
split           返回dirname和basename组成的元组
splitext        返回文件的filename和extension组成的元组
```