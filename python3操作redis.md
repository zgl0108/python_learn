redis也被称为缓存

    1.redis是一个key-value存储系统，没有ForeignKey和ManyToMany的字段.
    2.在redis中创建的数据彼此之间是没有关系的,所以也被称为是非关系型数据库
    3.它支持存储包括string(字符串)、list(链表)、set(集合)、zset(sorted set --有序集合)和hash（哈希类型）等数据类型。
    4.redis支持的数据类型都支持push/pop、add/remove及取交集并集和差集及更丰富的操作，而且这些操作都是原子性的。
	5.redis支持各种不同方式的排序。为了保证效率，数据都是缓存在内存中。
    6.redis会周期性的把更新的数据写入磁盘或者把修改操作写入追加的记录文件，并且在此基础上实现了master-slave(主从)同步。

在正常的服务器中,redis是运行在内存中的,而数据库是运行在服务器的硬盘上的

因为内存的运行速度远远快于硬盘的转速,所以redis查询速度远快于保存在硬盘的数据库

同样,因为redis是保存在内存中的,一台服务器可以配置非常大的硬盘,相对于硬盘来说,服务器内存的配置容量远小于配置的硬盘容量，

所以redis有一定的容量限制

同样因为redis是保存在内存中的,所以服务器一旦断电,redis中保存的数据很容易丢失

    redis中存放的是常用的,且不经常更新的数据

一台服务器刚上线的时候,用户访问服务器上的数据的时候,先去缓存中看看是否有要查询的数据.

    如果缓存中保存有用户需要的数据,则直接从缓存中获取需要的数据;
    如果缓存中没有用户需要的数据,则会从数据库中查询数据并返回给用户,同时会把这些数据在内存中保存一份;
    这样下一位用户再来访问同样的数据时,则会直接从缓存中读取需要的数据,而不用访问数据库,加快了用户的访问速度.

例如,我们在博客园发表一篇博客时,在博客园的首页不会立即出现刚才所发表的那篇博客,而是要等几分钟之后,在博客园的首页才会出现刚才发表的那篇博客文章,这就是因为缓存的原因.

### 1.准备工作

为CentOS系统配置好`epel`源

可以参考我的博客[CentOS7系统配置国内yum源和epel源](http://www.cnblogs.com/renpingsheng/p/7845096.html)

### 2.安装Redis

    [root@bogon yum.repos.d]# yum list | grep redis
    Repository base is listed more than once in the configuration
    Repository updates is listed more than once in the configuration
    Repository extras is listed more than once in the configuration
    Repository centosplus is listed more than once in the configuration
    redis.x86_64                            3.2.10-2.el7                   @epel    
    collectd-redis.x86_64                   5.7.1-2.el7                    epel     
    collectd-write_redis.x86_64             5.7.1-2.el7                    epel     
    hiredis.x86_64                          0.12.1-1.el7                   epel     
    hiredis-devel.x86_64                    0.12.1-1.el7                   epel     
    opensips-redis.x86_64                   1.10.5-3.el7                   epel     
    pcp-pmda-redis.x86_64                   3.11.8-7.el7                   base     
    php-nrk-Predis.noarch                   1.0.4-1.el7                    epel     
    php-pecl-redis.x86_64                   2.2.8-1.el7                    epel     
    php-phpiredis.x86_64                    1.0.0-2.el7                    epel     
    python-redis.noarch                     2.10.3-1.el7                   epel     
    python-trollius-redis.noarch            0.1.4-2.el7                    epel     
    python2-django-redis.noarch             4.3.0-1.el7                    epel     
    redis-trib.noarch                       3.2.10-2.el7                   epel     
    rubygem-redis.noarch                    3.2.1-2.el7                    epel     
    rubygem-redis-doc.noarch                3.2.1-2.el7                    epel     
    syslog-ng-redis.x86_64                  3.5.6-3.el7                    epel     
    uwsgi-logger-redis.x86_64               2.0.15-1.el7                   epel     
    uwsgi-router-redis.x86_64               2.0.15-1.el7                   epel     
    [root@bogon yum.repos.d]# yum install -y redis
    Loaded plugins: fastestmirror, langpacks
    Repository base is listed more than once in the configuration
    Repository updates is listed more than once in the configuration
    Repository extras is listed more than once in the configuration
    Repository centosplus is listed more than once in the configuration
    Loading mirror speeds from cached hostfile
     * epel: ftp.cuhk.edu.hk
    Package redis-3.2.10-2.el7.x86_64 already installed and latest version
    Nothing to do
  
### 3.redis的文件目录结构  

使用`rpm -ql`命令查看redis安装之后在系统中生成的文件

    [root@bogon ~]# rpm -ql redis
    /etc/logrotate.d/redis
    /etc/redis-sentinel.conf  # redis的守护配置文件
    /etc/redis.conf       # redis的配置文件
    /etc/systemd/system/redis-sentinel.service.d
    /etc/systemd/system/redis-sentinel.service.d/limit.conf
    /etc/systemd/system/redis.service.d
    /etc/systemd/system/redis.service.d/limit.conf
    /usr/bin/redis-benchmark
    /usr/bin/redis-check-aof
    /usr/bin/redis-check-rdb
    /usr/bin/redis-cli      # redis的交互式命令行界面
    /usr/bin/redis-sentinel   # redis的守护文件
    /usr/bin/redis-server   # redis的服务端启动文件
    /usr/lib/systemd/system/redis-sentinel.service  # redis的守护程序的函数库文件
    /usr/lib/systemd/system/redis.service # redis的函数库文件
    /usr/libexec/redis-shutdown   # 停止redis的执行文件
    /usr/share/doc/redis-3.2.10   # redis的帮助文件
    /usr/share/doc/redis-3.2.10/00-RELEASENOTES
    /usr/share/doc/redis-3.2.10/BUGS
    /usr/share/doc/redis-3.2.10/CONTRIBUTING
    /usr/share/doc/redis-3.2.10/MANIFESTO
    /usr/share/doc/redis-3.2.10/README.md
    /usr/share/licenses/redis-3.2.10  # redis的licenses说明
    /usr/share/licenses/redis-3.2.10/COPYING
    /usr/share/man/man1/redis-benchmark.1.gz  # redis的man文件
    /usr/share/man/man1/redis-check-aof.1.gz
    /usr/share/man/man1/redis-check-rdb.1.gz
    /usr/share/man/man1/redis-cli.1.gz
    /usr/share/man/man1/redis-sentinel.1.gz
    /usr/share/man/man1/redis-server.1.gz
    /usr/share/man/man5/redis-sentinel.conf.5.gz
    /usr/share/man/man5/redis.conf.5.gz
    /var/lib/redis      # redis的
    /var/log/redis      # redis的日志文件
    /var/run/redis      # redis的进程PID文件

### 4.redis的启动停止与状态查看

    [root@bogon ~]# systemctl status redis.service      # 查看redis的状态，可以看到是活动状态
    ● redis.service - Redis persistent key-value database
     Loaded: loaded (/usr/lib/systemd/system/redis.service; disabled; vendor preset: disabled)
    Drop-In: /etc/systemd/system/redis.service.d
         └─limit.conf
     Active: active (running) since Thu 2017-11-16 17:29:39 CST; 1min 44s ago
    Process: 6272 ExecStop=/usr/libexec/redis-shutdown (code=exited, status=0/SUCCESS)
    Main PID: 6286 (redis-server)
     CGroup: /system.slice/redis.service
         └─6286 /usr/bin/redis-server 0.0.0.0:6379
    
    Nov 16 17:29:39 bogon systemd[1]: Started Redis persistent key-value database.
    Nov 16 17:29:39 bogon systemd[1]: Starting Redis persistent key-value database...
    [root@bogon ~]# systemctl stop redis.service      # 停止redis
    [root@bogon ~]# systemctl status redis.service      # redis牌非活动状态
    ● redis.service - Redis persistent key-value database
     Loaded: loaded (/usr/lib/systemd/system/redis.service; disabled; vendor preset: disabled)
    Drop-In: /etc/systemd/system/redis.service.d
         └─limit.conf
     Active: inactive (dead)
    
    Nov 16 17:21:56 bogon systemd[1]: redis.service: control process exited, code=exited status=1
    Nov 16 17:21:56 bogon systemd[1]: Unit redis.service entered failed state.
    Nov 16 17:21:56 bogon systemd[1]: redis.service failed.
    Nov 16 17:22:04 bogon systemd[1]: Started Redis persistent key-value database.
    Nov 16 17:22:04 bogon systemd[1]: Starting Redis persistent key-value database...
    Nov 16 17:29:39 bogon systemd[1]: Stopping Redis persistent key-value database...
    Nov 16 17:29:39 bogon systemd[1]: Started Redis persistent key-value database.
    Nov 16 17:29:39 bogon systemd[1]: Starting Redis persistent key-value database...
    Nov 16 17:31:38 bogon systemd[1]: Stopping Redis persistent key-value database...
    Nov 16 17:31:38 bogon systemd[1]: Stopped Redis persistent key-value database.
    [root@bogon yum.repos.d]# redis-server        # 启动redis程序
    5587:C 16 Nov 15:42:56.010 # Warning: no config file specified, using the default config. In order to specify a config file use redis-server /path/to/redis.conf
    5587:M 16 Nov 15:42:56.018 * Increased maximum number of open files to 10032 (it was originally set to 1024).
                    _._                                                  
               _.-``__ ''-._                                             
          _.-``    `.  `_.  ''-._           Redis 3.2.10 (00000000/0) 64 bit
      .-`` .-```.  ```\/    _.,_ ''-._                                   
     (    '      ,       .-`  | `,    )     Running in standalone mode
     |`-._`-...-` __...-.``-._|'` _.-'|     Port: 6379
     |    `-._   `._    /     _.-'    |     PID: 6519
      `-._    `-._  `-./  _.-'    _.-'                                   
     |`-._`-._    `-.__.-'    _.-'_.-'|                                  
     |    `-._`-._        _.-'_.-'    |           http://redis.io        
      `-._    `-._`-.__.-'_.-'    _.-'                                   
     |`-._`-._    `-.__.-'    _.-'_.-'|                                  
     |    `-._`-._        _.-'_.-'    |                                  
      `-._    `-._`-.__.-'_.-'    _.-'                                   
          `-._    `-.__.-'    _.-'                                       
              `-._        _.-'                                           
                  `-.__.-'                                        
    
    5587:M 16 Nov 15:42:56.022 # WARNING: The TCP backlog setting of 511 cannot be enforced because /proc/sys/net/core/somaxconn is set to the lower value of 128.
    5587:M 16 Nov 15:42:56.022 # Server started, Redis version 3.2.10
    5587:M 16 Nov 15:42:56.022 # WARNING overcommit_memory is set to 0! Background save may fail under low memory condition. To fix this issue add 'vm.overcommit_memory = 1' to /etc/sysctl.conf and then reboot or run the command 'sysctl vm.overcommit_memory=1' for this to take effect.
    5587:M 16 Nov 15:42:56.025 # WARNING you have Transparent Huge Pages (THP) support enabled in your kernel. This will create latency and memory usage issues with Redis. To fix this issue run the command 'echo never > /sys/kernel/mm/transparent_hugepage/enabled' as root, and add it to your /etc/rc.local in order to retain the setting after a reboot. Redis must be restarted after THP is disabled.
    5587:M 16 Nov 15:42:56.026 * The server is now ready to accept connections on port 6379
    [root@bogon ~]# systemctl status redis.service
    ● redis.service - Redis persistent key-value database
     Loaded: loaded (/usr/lib/systemd/system/redis.service; disabled; vendor preset: disabled)
    Drop-In: /etc/systemd/system/redis.service.d
         └─limit.conf
     Active: active (running) since Thu 2017-11-16 17:31:47 CST; 2s ago
    Main PID: 6325 (redis-server)
     CGroup: /system.slice/redis.service
         └─6325 /usr/bin/redis-server 0.0.0.0:6379

    Nov 16 17:31:47 bogon systemd[1]: Started Redis persistent key-value database.
    Nov 16 17:31:47 bogon systemd[1]: Starting Redis persistent key-value database...

redis的启动方式有两种：

    [root@bogon ~]# systemctl start redis.service   # 后台启动，无欢迎界面
    [root@bogon ~]# redis-server            # 前台启动，可以看到欢迎界面

redis的停止方式有两种：

    [root@bogon ~]# systemctl stop redis.service
    [root@bogon ~]# /usr/libexec/redis-shutdown

### 5.redis的主配置文件说明

    bind 127.0.0.1                          # redis绑定的主机地址，这里默认仅支持本地连接
    protected-mode yes                      # 是否以保护模式运行redis
    port 6379                               # 指定redis监听的端口
    tcp-backlog 511
    timeout 0                               # 客户端闲置多长时间后关闭连接，为0时关闭该功能
    tcp-keepalive 300                       # tcp方式最大允许的连接数
    daemonize no                            # 是否以守护进程方式运行
    supervised no                           # 不使用监控树
    pidfile /var/run/redis_6379.pid         # redis运行时保存pid的文件
    loglevel verbose                        # 日志文件的记录方式，默认为标准输出
    logfile /var/log/redis/redis.log        # redis日志文件的保存路径
    databases 16                            # 系统中保存redis数据库的数量
    save 900 1                              # redis中900秒之内有1次更新操作时，把数据同步到文件中保存
    save 300 10                             # redis在300秒内有10次更新操作时，把数据同步到文件中保存
    save 60 10000                           # redis在60秒内有10000次更新操作时，把数据同步到文件中保存
    stop-writes-on-bgsave-error yes
    rdbcompression yes                      # redis中的数据保存到本地数据库时是否启动压缩，默认为yes
    rdbchecksum yes
    dbfilename dump.rdb                     # 本地数据库的文件名
    dir /var/lib/redis                      # 本地数据库的路径
    slave-serve-stale-data yes
    slave-read-only yes
    repl-diskless-sync no
    repl-diskless-sync-delay 5
    repl-disable-tcp-nodelay no
    slave-priority 100
    appendonly no                           # 是否在每次更新操作时进行日志记录
    appendfilename "appendonly.aof"         # 指定更新日志的文件名
    appendfsync everysec                    # 每秒钟把redis中的数据同步到本地文件一次
    no-appendfsync-on-rewrite no
    auto-aof-rewrite-percentage 100
    auto-aof-rewrite-min-size 64mb
    aof-load-truncated yes
    lua-time-limit 5000
    slowlog-log-slower-than 10000
    slowlog-max-len 128
    latency-monitor-threshold 0
    notify-keyspace-events ""
    hash-max-ziplist-entries 512
    hash-max-ziplist-value 64
    list-max-ziplist-size -2
    list-compress-depth 0
    set-max-intset-entries 512
    zset-max-ziplist-entries 128
    zset-max-ziplist-value 64
    hll-sparse-max-bytes 3000
    activerehashing yes
    client-output-buffer-limit normal 0 0 0
    client-output-buffer-limit slave 256mb 64mb 60    #
    client-output-buffer-limit pubsub 32mb 8mb 60
    hz 10
    aof-rewrite-incremental-fsync yes
  
### 6.redis的交互式界面

    [root@bogon ~]# redis-cli   # 进入redis的交互式界面
    127.0.0.1:6379> 

可以看到，已经进入到redis的交互环境了

    127.0.0.1:6379> set k1 v1   # 设定k1这个键的值为v1
    OK
    127.0.0.1:6379> get k1      # 获取k1的值
    "v1"    
    127.0.0.1:6379> set k2 v2   # 设定k2的值为v2
    OK
    127.0.0.1:6379> get k2      # 获取k2的值
    "v2"

### 7.python3操作redis

在linux系统中打开redis的配置文件`/etc/redis.conf`

把第`61`行修改为

    bind 0.0.0.0

表示所有的主机都可以连接

然后重启redis，使配置文件生效

    [root@bogon ~]# systemctl restart redis.service

在windows系统中，安装redis模块

    pip3 install redis

新建`redis_test.py`文件,文件内容为

    import redis
    
    r1=redis.Redis(host="192.168.16.220",port=6379)
    
    print("第一次读取的k1值:",r1.get("k1"))
    print("第一次读取的k2值:",r1.get("k2"))
    r1.set("k3","v3")
    
    r1.delete("k1")
    r1.delete("k2")
    
    print("第二次获取k1的值",r1.get("k1"))
    print("第二次获取k2的值",r1.get("k2"))
    print(r1.get("k3"))


运行结果：

    第一次读取的k1值: b'v1'
    第一次读取的k2值: b'v2'
    第二次获取k1的值 None
    第二次获取k2的值 None
    b'v3'

再次在linux的命令提示符下获取k1和k2的值

    127.0.0.1:6379> get k1
    (nil)
    127.0.0.1:6379> get k2
    (nil) 

因为k1和k2的值已经在redis_test.py中被删除了，所以获取到的值为None.  
  
### 8.使用Redis的好处

    (1) 速度快，因为数据存在内存中，类似于HashMap，HashMap的优势就是查找和操作的时间复杂度都是O(1)
    (2) 支持丰富数据类型，支持string，list，set，sorted set，hash
    (3) 支持事务，操作都是原子性，所谓的原子性就是对数据的更改要么全部执行，要么全部不执行
    (4) 丰富的特性：可用于缓存，消息，按key设置过期时间，过期后将会自动删除 