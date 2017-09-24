**1. MySQL数据库的安装**

`CentOS6`上`mysql`服务端和客户端的安装和启动:
```
    #使用yum安装mysql数据库的服务端和客户端
    yum install -y mysql mysql-server
    
    #把mysql服务端加入开机自启动
    chkconfig msyqld on
    
    #立即启动mysql服务端
    service mysqld start 
```
`CentOS7`上`MariaDB`数据库的服务端和客户端的安装和启动:
```
    #yum安装MariaDB服务端和客户端
    yum install -y mariadb mariadb-server
    
    #把MariaDB的服务端加入开机自启动
    systemctl enable mariadb
    
    #立即启动MariaDB的服务端
    systemctl start mariadb
```
windows平台：

到官方网站下载操作系统对应的版本:

[安装版下载地址](https://dev.mysql.com/downloads/installer/)

[解压版下载地址](https://dev.mysql.com/downloads/mysql/)

window解压版的安装步骤：

***1.下载到电脑上***

`Windows (x86, 64-bit), ZIP Archive`

***2.解压***

解压到C盘的目录下：

`C:\mysql-5.7.16-winx64`

***3.初始化***

进入`C:\mysql-5.7.16-winx64\bin`目录下，执行命令初始化`mysql`:

    mysqld --initialize-insecure
    
***4.启动mysql服务端***

进入`C:\mysql-5.7.16-winx64\bin`目录下，执行

    mysqld
***5.启动mysql客户端并连接mysql服务端***

进入`C:\mysql-5.7.16-winx64\bin`目录下，执行

    mysql -u root -p
提示输入密码，这里初始化时没有设置密码,直接回车，进行mysql的提示符

这里显示的是在CentOS7上安装的MariaDB的提示符:
```
    [root@localhost ~]#mysql -u root -p
    Enter password: 
    Welcome to the MariaDB monitor.  Commands end with ; or \g.
    Your MariaDB connection id is 10
    Server version: 5.5.52-MariaDB MariaDB Server
    
    Copyright (c) 2000, 2016, Oracle, MariaDB Corporation Ab and others.
    
    Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.
    
    MariaDB [(none)]> 
```
***6.把mysql可执行文件添加到系统环境变量中，方便以后执行mysql***

具体步骤请点[这里](http://jingyan.baidu.com/article/e4d08ffdd5f6670fd2f60d2f.html)

**2.数据库的基本操作**

***1.显示服务端所有的数据库***
```
    #显示系统上的所有的数据库
    mysql> SHOW DATABASES;
    +--------------------+
    | Database           |
    +--------------------+
    | information_schema |
    | mysql              |
    | performance_schema |
    | sys                |
    +--------------------+
    4 rows in set (0.00 sec)
```
***2.创建数据库***
```
    #创建数据库db1
    mysql> CREATE DATABASE db1;
    Query OK, 1 row affected (0.00 sec)
    
    #创建数据库student
    mysql> CREATE DATABASE student;
    Query OK, 1 row affected (0.00 sec)
    
    #列出所有的数据库
    mysql> SHOW DATABASES;
    +--------------------+
    | Database           |
    +--------------------+
    | information_schema |
    | db1                |
    | mysql              |
    | performance_schema |
    | student            |
    | sys                |
    +--------------------+
    6 rows in set (0.00 sec)
```
创建数据库时可以使用参数来指定字符集有：

    DEFAULT CHARSET utf8        #指定数据表的字符集为"utf8"
    DEFAULT CHARSET gbk         #指定数据表的字符集为"gbk"
    
***3.使用数据库***
```
    #使用use语句指定要操作的数据库
    mysql> USE mysql;
    Reading table information for completion of table and column names
    You can turn off this feature to get a quicker startup with -A

    Database changed
```
***4.显示当前数据库中所有的表***
```
    #列出数据库mysql中的所有的数据表
    mysql> SHOW TABLES;
    +---------------------------+
    | Tables_in_mysql           |
    +---------------------------+
    | columns_priv              |
    | db                        |
    | engine_cost               |
    | event                     |
    | func                      |
    | general_log               |
    | gtid_executed             |
    | help_category             |
    | help_keyword              |
    | help_relation             |
    | help_topic                |
    | innodb_index_stats        |
    | innodb_table_stats        |
    | ndb_binlog_index          |
    | plugin                    |
    | proc                      |
    | procs_priv                |
    | proxies_priv              |
    | server_cost               |
    | servers                   |
    | slave_master_info         |
    | slave_relay_log_info      |
    | slave_worker_info         |
    | slow_log                  |
    | tables_priv               |
    | time_zone                 |
    | time_zone_leap_second     |
    | time_zone_name            |
    | time_zone_transition      |
    | time_zone_transition_type |
    | user                      |
    +---------------------------+
    31 rows in set (0.01 sec)
```
***5.用户管理***
```
    #创建一个指定密码,只允许在指定主机上登陆数据库的用户
    CREATE USER "用户名"@"IP地址" IDENTIFIED BY "密码";
    
    #删除用户
    DROP USER "用户名"@"IP地址";
    
    #修改用户的登陆名称
    RENAME USER "用户名""@"IP地址" TO "新用户名""@"IP地址";
    
    #设定用户使用指定主机登陆数据库的密码
    SET PASSWORD FOR "用户名"@"IP地址"="新密码";
```
IP地址的说明：

    192.168.1.100   表示192.168.1.100主机
    192.168.1.*     表示对192.168.1地址段
    192.168.*.*     表示192.168网段
    *               表示所有的主机
注意的是：

用户权限相关数据保存在mysql数据库中的user表中，可以直接对其进行操作,但是不建议这样操作

***6.授权管理***
```
    #显示某个用户在指定主机的权限
    SHOW GRANTS FOR "用户名"@"IP地址"
    
    #授权
    GRANT 权限 ON 数据库.表 TO "用户名"@"IP地址"
    
    #取消授权
    GRANT 权限 ON 数据库.表 FROM "用户名"@"IP地址"
```
可以设定的权限有：
```
all privileges              除授权之外的所有权限
select,insert               查看和插入数据的权限        
usage                       除了登陆之外,无任何权限
alter                       更改数据库权限
alter routine               用户可以修改或删除存储函数
create                      创建新的数据库或数据表     
create routine              用户可以更改或放弃存储过程和函数
create temporary tables     用户可以创建临时数据表
create user                 创建新的用户
create view                 创建新的视图
delete                      删除表的记录
drop                        删除数据库或数据表
execute                     用户可以执行存储过程
event                       用户可以创建,修改和删除触发器
file                        在数据库服务器上读写文件
grant option                用户是否可以将自己的权限再授予其他用户
index                       建立或删除索引
insert                      插入新的数据
lock tables                 锁定数据表,禁止别的用户对数据表的访问和修改
process                     显示或杀死属于其他用户的服务线程
select                      查找检索数据
show databases              显示数据库
show view                   显示视图
trigger                     用户可以创建和删除触发器
updata                      更新数据库或数据表
reload                      重载访问控制表
shutdown                    关闭mysql服务端
super                       用户可以执行的强大的管理功能,例如修改mysql的全局变量,执行关于复制和日志的各种命令
replication client          用户可以确定复制从服务器和主服务器的位置
replication slave           用户可以读取维护复制数据库环境的二进制日志文件
```
数据库可以使用的选项：

    数据库名.*                  数据库中所有的表
    数据库名.表                  指定数据库中的某张表
    数据库名.存储过程           指定数据库的存储过程
    .*.                         所有的数据库
例子:
```
    #授权用户对db1下的table1数据表拥有除了授权之外的所有权限
    GRANT all privileges on DB1.table1 to "用户名"@"IP"
    
    #授权用户对db1下的所有的数据表都仅有查找的权限
    grant select on db1.* to "用户名"@"IP"
    
    #授权用户对db1下的所有的数据表都有查找和插入数据的权限
    grant select,insert on db1.* to "用户名"@"IP"
    
    #移除用户对db1下的table1数据表的查找的权限 
    revoke select on db1.table1 from "用户名"@"IP"
```
特殊的:

    flush privileges		#将数据读取到内存中，从而立即生效
    
**3. mysql数据库中的基本数据类型**

    mysql的数据类型大致分为：数值，时间和字符串
    
***1.数值类型***
```
    bit[(m)]
    二进制位，m表示二进制的长度(1-64),默认m=1
    
    tinyint[(m)][unsigned][zerofill]
    小整数，数据类型用于保存一些范围内的整数数值范围
    有符号：-128~127
    无符号：0~255
    特别的：MySQL中无布尔值，使用tinyint(1)构造
    
    int[(m)][unsigned][zerofill]
    整数，数据类型用于保存一些范围的整数数值范围
    有符号：-2147483648~2147483647(2的31次方)
    无符号：0~4294967295(2的32次方)
    特别的：整数类型中的m仅用于显示，对存储范围无限制
    例如：int(5),表示插入数据时，数据的长度为５位
    
    bigint[(m)][unsigned][zerofill]
    大整数，数据类型用于保存一些范围的整数数值范围
    有符号：-2**63 ~ 2**63
    无符号：0~2**64
    
    decimal[(m[,d])][unsigned][zerofill]
    准确的小数值，m是数字的个数，d是小数点后个数，m最大值为65,d最大值为30.
    特别的：
    对于精确数值计算时需要用此类型
    decimal能够存储精确值的原因在于其内部按照字符串存储
    
    float[(m,d)][unsigned][zerofill]
    单精度浮点数(非准确小数值)，m是数字总个数，d是小数点后个数
    无符号：
    -3.402823466E+38 to -1.175494351E-38
    0
    1.175494351E-38 to 3.02823466E+38
    有符号：
    0
    1.175494351E-38 to 3.402823466E+38
    需要注意的是,数值越大，表示的数值越不准确
    
    double[(m,d)][unsigned][serofill]
    双精度浮点数(非准确小数值)，m是数字总个数，d是小数点后个数
    数值越大，越不准确
```
***2.字符串***
```
    char(m)
    char表示固定长度的字符串,可以包含最多达255个字符,其中m代表字符串的长度
    即使数据小于m长度，存储后也会占用m长度
    
    varchar(m)
    varchar用于变长的字符串,可以包含最多255个字符,其中m代表该数据类型所允许保存的字符串的最大长度
    只要长度小于该最大值的字符串都可以被保存在该数据类型中
    需要注意的是,虽然varchar使用起来较为灵活，但是从整个系统的性能角度来说，char数据类型的处理速度比varchar类型更快
    
    text
    text数据类型用于保存变长的大字符串，可以组到65535(2**16-1)个字符
    
    mediumtext
    mediumtext类型数据也是用来保存变长的大字符串，最长可以表示
    (2**24-1)个字符
    
    longtext
    longtext数据类型也是用来保存变长的大字符串，最长可以表示(2**32-1)个字符
```
***3. `enum`***

枚举类型,其最大可以包含65535个不重复的成员,但是实际被限制小于3000个成员

***4. `set`***

集合类型,其最大可以包含64个不重复的成员

***5.时间类型***
```
    date
    YYYY-MM-DD
    例如：2017-07-24
    
    time
    HH:MM:SS
    例如：14:35:33
    
    year
    YYYY
    例如：2017
    
    datetime
    YYYY-MM-DD HH:MM:SS
    例如：2017-07-25 15:55:22
    
    timestamp
    YYYYMMDD HHMMSS
    例如：20170725 15:55:20
```
**4.数据表的基本操作**

***1.创建表***

语法如下:
```
    CREATE TABLE table_name(
        列名　类型　　是否可以为空
        列名　类型　　是否可以为空
    )　ENGINE=Innodb DEFAULT CHARSET=utf8
```
创建数据表时，可以添加的选项有：

	not null        设定指定的字段不可以为空
	null            设定指定的字段可以为空
	DEFAULT n       设定默认值，创建列时可以指定默认值，当插入数据时这个字段未设置值,则自动添加默认值
	auto_increment  自增,如果某列设置为自增列，插入数据时无需设置此列,其值将在原来的基础上加1(表中只能有一个自增列)
	primary key     一种特殊的唯一索引,不允许有空值,如果主键使用单个列,则其值必须唯一，如果是多列，则其组合必须唯一
***2.创建外键***

一种特殊的索引，只能是指定内容

语法如下：
```
    #创建一张表，用来记录学生的ID，姓名
    mysql> CREATE TABLE stu_info(
        -> id INT PRIMARY KEY AUTO_INCREMENT,
        -> name VARCHAR(10)
        -> ) ENGINE=innodb CHARSET=utf8;
    Query OK, 0 rows affected (0.26 sec)
```
***3.删除表***
```
	#删除这张数据表中的所有数据,包括表中的字段
	drop table 表名
	
	#一行一行的删除数据表中的除字段处的所有的行,速度较慢
	delete from 表名
	
	#先把数据表删除，然后再创建一张跟被删除的数据表的字段一样的空表，速度较快
	truncate table 表名
```
***4.添加列***

	#为数据表添加一个指定类型的列
	alter table 表名 add  列名　类型
例子：
```
    #为学生信息表插入性别字段
    mysql> ALTER TABLE stu_info ADD(
        -> gender VARCHAR(6) DEFAULT "male");
    Query OK, 0 rows affected (0.37 sec)
    Records: 0  Duplicates: 0  Warnings: 0
    
    #为学生信息表插入年龄，语言分数，数学分数和英语分数
    mysql> ALTER TABLE stu_info ADD(
        -> age INT(2),
        -> chinese INT(2),
        -> math INT(2),
        -> english INT(2));
    Query OK, 0 rows affected (0.38 sec)
    Records: 0  Duplicates: 0  Warnings: 0
    
    #为学生信息表插入生日字段
    mysql> ALTER TABLE stu_info ADD(birthday DATE);
    Query OK, 0 rows affected (0.40 sec)
    Records: 0  Duplicates: 0  Warnings: 0
    
    #显示学生信息表的描述信息
    mysql> DESC stu_info;
    +----------+-------------+------+-----+---------+----------------+
    | Field    | Type        | Null | Key | Default | Extra          |
    +----------+-------------+------+-----+---------+----------------+
    | id       | int(11)     | NO   | PRI | NULL    | auto_increment |
    | name     | varchar(10) | YES  |     | NULL    |                |
    | age      | int(2)      | YES  |     | NULL    |                |
    | chinese  | int(2)      | YES  |     | NULL    |                |
    | math     | int(2)      | YES  |     | NULL    |                |
    | english  | int(2)      | YES  |     | NULL    |                |
    | gender   | varchar(6)  | YES  |     | male    |                |
    | birthday | date        | YES  |     | NULL    |                |
    +----------+-------------+------+-----+---------+----------------+
    8 rows in set (0.00 sec)
```
***5.删除列***

	#删除数据表中指定有列
	alter table 表名 drop column 列名
例子：
```
    #删除学生信息表中的生日字段
    mysql> ALTER TABLE stu_info DROP birthday;
    Query OK, 0 rows affected (0.37 sec)
    Records: 0  Duplicates: 0  Warnings: 0
    
    mysql> DESC stu_info;
    +---------+-------------+------+-----+---------+----------------+
    | Field   | Type        | Null | Key | Default | Extra          |
    +---------+-------------+------+-----+---------+----------------+
    | id      | int(11)     | NO   | PRI | NULL    | auto_increment |
    | name    | varchar(10) | YES  |     | NULL    |                |
    | age     | int(2)      | YES  |     | NULL    |                |
    | chinese | int(2)      | YES  |     | NULL    |                |
    | math    | int(2)      | YES  |     | NULL    |                |
    | english | int(2)      | YES  |     | NULL    |                |
    | gender  | varchar(6)  | YES  |     | male    |                |
    +---------+-------------+------+-----+---------+----------------+
    7 rows in set (0.00 sec)
```
***6.修改列***
```
	#更改数据表的字段的类型
	alter table 表名 modify 列名 类型
	
	#更改数据表的字段的名称以及类型
	alter table 表名 change 原列名 新列名 类型
```
例子:
```
    #修改学生信息表中的姓名字段，类型改为字符串的长度为6,且不能为空
    mysql> ALTER TABLE stu_info MODIFY name VARCHAR(6) NOT NULL;
    Query OK, 0 rows affected (0.85 sec)
    Records: 0  Duplicates: 0  Warnings: 0
    
    mysql> DESC stu_info;
    +---------+------------+------+-----+---------+----------------+
    | Field   | Type       | Null | Key | Default | Extra          |
    +---------+------------+------+-----+---------+----------------+
    | id      | int(11)    | NO   | PRI | NULL    | auto_increment |
    | name    | varchar(6) | NO   |     | NULL    |                |
    | age     | int(2)     | YES  |     | NULL    |                |
    | chinese | int(2)     | YES  |     | NULL    |                |
    | math    | int(2)     | YES  |     | NULL    |                |
    | english | int(2)     | YES  |     | NULL    |                |
    | gender  | varchar(6) | YES  |     | male    |                |
    +---------+------------+------+-----+---------+----------------+
    7 rows in set (0.01 sec)
    
    #把学生信息表中的chinese改为chinese_score,类型改为int(3)
    mysql> ALTER TABLE stu_info CHANGE chinese chinese_score INT(3);
    Query OK, 0 rows affected (0.11 sec)
    Records: 0  Duplicates: 0  Warnings: 0
    
    mysql> DESC stu_info;
    +---------------+------------+------+-----+---------+----------------+
    | Field         | Type       | Null | Key | Default | Extra          |
    +---------------+------------+------+-----+---------+----------------+
    | id            | int(11)    | NO   | PRI | NULL    | auto_increment |
    | name          | varchar(6) | NO   |     | NULL    |                |
    | age           | int(2)     | YES  |     | NULL    |                |
    | chinese_score | int(3)     | YES  |     | NULL    |                |
    | math          | int(2)     | YES  |     | NULL    |                |
    | english       | int(2)     | YES  |     | NULL    |                |
    | gender        | varchar(6) | YES  |     | male    |                |
    +---------------+------------+------+-----+---------+----------------+
    7 rows in set (0.01 sec)
```
***7.删除主键***

	#删除某张表中的主键
	ALTER TABLE 表名 drop primary key;
	ALTER TABLE 表名 modify 列名 ,drop primary key;
***8.添加主键***
	
	#把数据表中的指定列设为主键
	ALTER TABLE 表名 add primary key 列名;
***9.添加外键***
	
	#把主表的某个字段设为从表某个字段的外键
	ALTER TABLE 从表 ADD CONSTRAINT 外键名称 
	FOREIGN KEY 从表(外键字段) REFERENCES 主表(主键字段);
***10.删除外键***

	#删除数据表中的指定外键
	ALTER TABLE 表名 DROP FOREIGN KEY 外键名称
***11.修改默认值***

	#修改数据表的默认值
	ALTER TABLE 表名 ALTER 要修改的字段 DEFAULT 修改后的值
***12.删除默认值***

	#删除数据表的默认值
	ALTER TABLE ALTER DROP DEFAULT

**4.表内容操作**

***1.增***

	insert into 表名(列名，列名) values (值1，值2)
	insert into  表名(列名，列名) values(值值值),(值值值)
	insert into 表名(列名，列名) select (列名，列名)  from 表名
例子：
```
    #向学生信息表中插入四条数据
    mysql> INSERT INTO stu_info(name,gender,age,chinese,math,english) VALUES
        -> ("xiaoming","male",14,98,98,62),
        -> ("xiaohong","female",13,67,59,82),
        -> ("xiaoliang","male",12,59,89,67),
        -> ("xiaona","female",13,88,98,55);
    Query OK, 4 rows affected, 3 warnings (0.01 sec)
    Records: 4  Duplicates: 0  Warnings: 3

    #向学生信息表中插入单条数据
    mysql> INSERT INTO stu_info(name,gender,age,chinese,math,english) VALUES("xiaoqi","male",14,88,100,
    Query OK, 1 row affected (0.01 sec)
```
***2.删***

	#删除整张表
	delete from 表名
	#删除数据表中符合要求的条目
	delete from 表名 where id =n and name="name"
	
***3.查***

****1. `*`表示查找所有列，也可以指定一个列，`from指定从哪张表查找，distinct用来剔除重复行`****
```
    #查询表中所有的信息
    select * from 表名
    #查询表中id大于10的人的所有信息
    select * from 表名　where id > 10
    #查询表中id大于10的人的所有信息
    select id,name,gender as info from 表名　where id >10
    
    #检索表中所有人的所有信息
    mysql> SELECT * FROM stu_info;
    +----+--------+--------+------+---------+------+---------+
    | id | name   | gender | age  | chinese | math | english |
    +----+--------+--------+------+---------+------+---------+
    |  1 | xiaomi | male   |   14 |      98 |   98 |      62 |
    |  2 | xiaoho | female |   13 |      67 |   59 |      82 |
    |  3 | xiaoli | male   |   12 |      59 |   89 |      67 |
    |  4 | xiaona | female |   13 |      88 |   98 |      55 |
    |  5 | xiaoqi | male   |   14 |      88 |  100 |      67 |
    +----+--------+--------+------+---------+------+---------+
    5 rows in set (0.01 sec)
    
    #检索表中ID号大于4的学生的所有信息
    mysql> SELECT * FROM stu_info WHERE id >4;
    +----+--------+--------+------+---------+------+---------+
    | id | name   | gender | age  | chinese | math | english |
    +----+--------+--------+------+---------+------+---------+
    |  5 | xiaoqi | male   |   14 |      88 |  100 |      67 |
    +----+--------+--------+------+---------+------+---------+
    1 row in set (0.00 sec)
```
****2.`select`也可以使用表达式，并且可以使用：字段 as 别名或者：字段 别名****
```
    #检索所有的学生的姓名，年龄并且把英语成绩加５分
    mysql> SELECT name,age,english+5 as english FROM stu_info;
    +--------+------+-----------+
    | name   | age  |  english  |
    +--------+------+-----------+
    | xiaomi |   14 |        67 |
    | xiaoho |   13 |        87 |
    | xiaoli |   12 |        72 |
    | xiaona |   13 |        60 |
    | xiaoqi |   14 |        72 |
    +--------+------+-----------+
    5 rows in set (0.06 sec)
```
****3.使用`where`子句，进行过滤查询****

`where`字句可以使用：
```
    <   >   <=  >=  <>  !=          比较运算符
    between m and n                 在m和n范围中间(包括m和n)取值
    in(a,b,c)                       在括号中的值里面选择
    like "pattern%"                 查询以pattern开头,后接任意字符的所有的信息
    like "pattern_"                 查询以pattern开头后接一个字符的所有的信息
        _有几个表示可以接几个字符
    在多个条件的时候可以使用逻辑运算符and,or,not
```
例子:
```
	#查询表中id大于1且name不等于"xiaoming"的人的所有信息
	select * from table_name where id>1 and name != "xiaoming";
	
	#查询表中id号在2和5之间(包括2和5)的人的所有信息
	select * from table_name where id between 2 and 5;
	
	#查询表中name以"li"开头的人的所有信息
	select * from table_name where name like "li%";
	
	#查询表中name以"li"开头后面接两个字符的所有人的所有的信息
	select * from table_name where name like "li__"
	
	#查询表中id号为11或者22或者33的所有人的所有信息
	select * from table_name where id in (11,22,33);
	
	#查询表中id号不为11和22和33的人的所有信息
	select * from table_name where id not in (11,22,33);
	
	#查询表中id号在另外一张表中的人的所有信息
	select * from table_name where id in (select id from another_table);
```
****4.`order by`指定排序的列，排序的列可以是表中的列名，也可以是`select`后面指定的别名****

	SELECT *|field1,field2... from table_name where 语句 order by field [Asc|Desc]
排序参数:

	Asc         指定按升序进行排序，默认以Asc进行排序
	Desc        指定按降序进行排序
例子:

	#检索表中id号大于5的人的所有信息,且字段1按降序排列,字段2按升序排列
	select * from table_name where id > 5 order by field1 desc,field2 asc

	#检索出来的列按照从小到大排列
	select * from table_name order by 列 asc

	#检索出来的列按照从大到小排列
	select * from table_name order by 列 desc
	
****5.`group by `分组查询****

    当表中某一列中有很多相同的值时，可以进行分组查询，但是按分组条件进行分组后每一组只会显示第一条记录
    
    group by字句，其后可以接多个列名，也可以接having子句，对group by的结果进行筛选
    
    where与having两者都可以对查询结果进行进一步的过滤，但也有差别：   
    where语句只能用在分组之前筛选，having可以用在分组之后筛选
    使用where语句的地方都可以用having进行替换
    having中可以使用聚合函数，where中不可以使用聚合函数
	需要注意的是,group by语句必须在where之后,在order by之前
	
****6.聚合函数****

聚合函数一般和分组配合使用

	COUNT(列名)   统计行的个数
	SUM(列名) 统计满足条件的内容的和
	AVG(列名) 统计满足条件的内容的平均值       
	MAX         求最大值		
	MIN         求最小值
	
****7.`limit`取结果中的几条值****

	limit m     取检索结果的前m条
	limit m,n   检索的结果中跳过前n条，取接下来的m条记录
	
例子:
```
    #查询数据表中id大于5的结果中的前3条数据
    select * from table_name where id >5 limit 3
    
    #检索表的前5行
    select * from table_name limit 5
    
    #检索从表的第4行开始向下的5行
    select * from table_name limit 4,5
    
    #检索从表的第4行开始向下的5行
    select * from table_name limit 5 offset 4
```
****8.正则表达式查询****

语法:

	SELECT * FROM table_name WHERE 条件 REGEXP "pattern";
	
可以使用正则表达式的模式来进行匹配
```
    #查询表中id大于3且以"pattern"开头的人的所有信息
    select * from table_name where id >3 and REGEXP "^pattern";
    
    #查询表中id大于3且以"pattern"结尾的人的所有信息      
    select * from table_name where id >3 and REGEXP "pattern$";
```
****9. 连表查询****

	#从两个或两个以上的表中查询数据
	select A.field1,A.field2,B.field1,B.field2 from A,B where A.id=B.id
	
***4. 改***
```
	#把数据表中id大于1的name的值设定"new_name"
	update 表名 set name="new_name" where id >1
```