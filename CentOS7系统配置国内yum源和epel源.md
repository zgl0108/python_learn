### 1.首先进入`/etc/yum.repos.d/`目录下，新建一个repo_bak目录，用于保存系统中原来的repo文件

    [root@bogon ~]# cd /etc/yum.repos.d/
    [root@bogon yum.repos.d]# mkdir repo_bak
    [root@bogon yum.repos.d]# mv *.repo repo_bak/

### 2.在CentOS中配置使用网易和阿里的开源镜像

到网易和阿里开源镜像站点下载系统对应版本的repo文件

    [root@bogon yum.repos.d]# wget http://mirrors.aliyun.com/repo/Centos-7.repo
    [root@bogon yum.repos.d]# wget http://mirrors.163.com/.help/CentOS7-Base-163.repo
    [root@bogon yum.repos.d]# ls
    Centos-7.repo  CentOS-Base-163.repo  repo.bak

或者手动下载repo文件并上传到`/etc/yum.repos.d/`目录

[网易开源镜像站](http://mirrors.163.com/.help/centos.html)

[阿里开源镜像站](http://mirrors.aliyun.com/help/centos)

### 3.清除系统yum缓存并生成新的yum缓存

    [root@bogon yum.repos.d]# ls    	# 列出/etc/yum.repos.d/目录下的文件
    Centos-7.repo  CentOS-Base-163.repo  repo.bak
	[root@bogon yum.repos.d]# yum clean all		# 清除系统所有的yum缓存
	Loaded plugins: fastestmirror, langpacks
	Repository base is listed more than once in the configuration
	Repository updates is listed more than once in the configuration
	Repository extras is listed more than once in the configuration
	Repository centosplus is listed more than once in the configuration
	Cleaning repos: base extras updates
	Cleaning up everything
	Cleaning up list of fastest mirrors
	[root@bogon yum.repos.d]# yum makecache		# 生成yum缓存
	Loaded plugins: fastestmirror, langpacks
	Repository base is listed more than once in the configuration
	Repository updates is listed more than once in the configuration
	Repository extras is listed more than once in the configuration
	Repository centosplus is listed more than once in the configuration
	base                                                                                  | 3.6 kB  00:00:00     
	extras                                                                                | 3.4 kB  00:00:00     
	updates                                                                               | 3.4 kB  00:00:00     
	(1/12): base/7/x86_64/filelists_db                                                    | 6.7 MB  00:00:02     
	(2/12): base/7/x86_64/group_gz                                                        | 156 kB  00:00:02     
	(3/12): base/7/x86_64/other_db                                                        | 2.5 MB  00:00:01     
	(4/12): base/7/x86_64/primary_db                                                      | 5.7 MB  00:00:02     
	(5/12): extras/7/x86_64/prestodelta                                                   |  51 kB  00:00:01     
	(6/12): extras/7/x86_64/filelists_db                                                  | 494 kB  00:00:02     
	(7/12): extras/7/x86_64/other_db                                                      |  86 kB  00:00:00     
	(8/12): extras/7/x86_64/primary_db                                                    | 130 kB  00:00:01     
	(9/12): updates/7/x86_64/prestodelta                                                  | 406 kB  00:00:01     
	(10/12): updates/7/x86_64/filelists_db                                                | 2.1 MB  00:00:01     
	(11/12): updates/7/x86_64/other_db                                                    | 354 kB  00:00:00     
	(12/12): updates/7/x86_64/primary_db                                                  | 3.6 MB  00:00:01     
	Determining fastest mirrors
	Metadata Cache Created

### 4.安装epel源

	[root@bogon yum.repos.d]# yum list | grep epel-release
	Repository base is listed more than once in the configuration
	Repository updates is listed more than once in the configuration
	Repository extras is listed more than once in the configuration
	Repository centosplus is listed more than once in the configuration
	epel-release.noarch                         7-9                        extras   

	[root@bogon yum.repos.d]# yum install -y epel-release
	Loaded plugins: fastestmirror, langpacks
	Repository base is listed more than once in the configuration
	Repository updates is listed more than once in the configuration
	Repository extras is listed more than once in the configuration
	Repository centosplus is listed more than once in the configuration
	Loading mirror speeds from cached hostfile
	Resolving Dependencies
	--> Running transaction check
	---> Package epel-release.noarch 0:7-9 will be installed
	--> Finished Dependency Resolution

	Dependencies Resolved

	=============================================================================================================
	 Package                       Arch                    Version                 Repository               Size
	=============================================================================================================
	Installing:
	 epel-release                  noarch                  7-9                     extras                   14 k

	Transaction Summary
	=============================================================================================================
	Install  1 Package

	Total download size: 14 k
	Installed size: 24 k
	Downloading packages:
	epel-release-7-9.noarch.rpm                                                           |  14 kB  00:00:00     
	Running transaction check
	Running transaction test
	Transaction test succeeded
	Running transaction
	  Installing : epel-release-7-9.noarch                                                                   1/1 
	  Verifying  : epel-release-7-9.noarch                                                                   1/1 

	Installed:
	  epel-release.noarch 0:7-9                                                                                  

	Complete!
	[root@bogon yum.repos.d]# ls			# epel源安装成功，比原来多了一个epel.repo和epel-testing.repo文件
	Centos-7.repo  CentOS-Base-163.repo  epel.repo  epel-testing.repo  repo.bak

### 5.再次清除系统yum缓存，并重新生成新的yum缓存	
	
	[root@bogon yum.repos.d]# yum clean all
	Loaded plugins: fastestmirror, langpacks
	Repository base is listed more than once in the configuration
	Repository updates is listed more than once in the configuration
	Repository extras is listed more than once in the configuration
	Repository centosplus is listed more than once in the configuration
	Cleaning repos: base epel extras updates
	Cleaning up everything
	Cleaning up list of fastest mirrors
	[root@bogon yum.repos.d]# yum makecache
	Loaded plugins: fastestmirror, langpacks
	Repository base is listed more than once in the configuration
	Repository updates is listed more than once in the configuration
	Repository extras is listed more than once in the configuration
	Repository centosplus is listed more than once in the configuration
	base                                                                                  | 3.6 kB  00:00:00     
	epel/x86_64/metalink                                                                  | 6.0 kB  00:00:00     
	epel                                                                                  | 4.7 kB  00:00:00     
	extras                                                                                | 3.4 kB  00:00:00     
	updates                                                                               | 3.4 kB  00:00:00     
	(1/18): base/7/x86_64/filelists_db                                                    | 6.7 MB  00:00:02     
	(2/18): base/7/x86_64/primary_db                                                      | 5.7 MB  00:00:01     
	(3/18): base/7/x86_64/other_db                                                        | 2.5 MB  00:00:00     
	(4/18): base/7/x86_64/group_gz                                                        | 156 kB  00:00:03     
	(5/18): epel/x86_64/group_gz                                                          | 261 kB  00:00:02     
	(6/18): epel/x86_64/updateinfo                                                        | 848 kB  00:00:05     
	(7/18): extras/7/x86_64/filelists_db                                                  | 494 kB  00:00:01     
	(8/18): extras/7/x86_64/prestodelta                                                   |  51 kB  00:00:00     
	(9/18): extras/7/x86_64/primary_db                                                    | 130 kB  00:00:00     
	(10/18): extras/7/x86_64/other_db                                                     |  86 kB  00:00:00     
	(11/18): updates/7/x86_64/filelists_db                                                | 2.1 MB  00:00:01     
	(12/18): updates/7/x86_64/prestodelta                                                 | 406 kB  00:00:00     
	(13/18): updates/7/x86_64/primary_db                                                  | 3.6 MB  00:00:01     
	(14/18): updates/7/x86_64/other_db                                                    | 354 kB  00:00:00     
	(15/18): epel/x86_64/primary_db                                                       | 6.1 MB  00:00:11     
	(16/18): epel/x86_64/filelists_db                                                     | 9.8 MB  00:00:14     
	(17/18): epel/x86_64/prestodelta                                                      |  884 B  00:00:00     
	(18/18): epel/x86_64/other_db                                                         | 2.9 MB  00:01:15     
	Determining fastest mirrors
	 * epel: mirrors.ustc.edu.cn
	Metadata Cache Created

### 6.查看系统可用的yum源和所有的yum源

	[root@bogon yum.repos.d]# yum repolist enabled		# 查看系统可用的yum源
	Loaded plugins: fastestmirror, langpacks
	Repository base is listed more than once in the configuration
	Repository updates is listed more than once in the configuration
	Repository extras is listed more than once in the configuration
	Repository centosplus is listed more than once in the configuration
	Loading mirror speeds from cached hostfile
	 * epel: mirrors.ustc.edu.cn
	repo id                             repo name                                                          status
	base/7/x86_64                       CentOS-7 - Base - 163.com                                           9,591
	epel/x86_64                         Extra Packages for Enterprise Linux 7 - x86_64                     12,071
	extras/7/x86_64                     CentOS-7 - Extras - 163.com                                           282
	updates/7/x86_64                    CentOS-7 - Updates - 163.com                                        1,084
	repolist: 23,028

	[root@bogon yum.repos.d]# yum repolist all		# 查看系统所有的yum源
	Loaded plugins: fastestmirror, langpacks
	Repository base is listed more than once in the configuration
	Repository updates is listed more than once in the configuration
	Repository extras is listed more than once in the configuration
	Repository centosplus is listed more than once in the configuration
	Loading mirror speeds from cached hostfile
	 * epel: mirrors.ustc.edu.cn
	repo id                       repo name                                                       status
	base/7/x86_64                 CentOS-7 - Base - 163.com                                       enabled:  9,591
	centosplus/7/x86_64           CentOS-7 - Plus - 163.com                                       disabled
	contrib/7/x86_64              CentOS-7 - Contrib - mirrors.aliyun.com                         disabled
	epel/x86_64                   Extra Packages for Enterprise Linux 7 - x86_64                  enabled: 12,071
	epel-debuginfo/x86_64         Extra Packages for Enterprise Linux 7 - x86_64 - Debug          disabled
	epel-source/x86_64            Extra Packages for Enterprise Linux 7 - x86_64 - Source         disabled
	epel-testing/x86_64           Extra Packages for Enterprise Linux 7 - Testing - x86_64        disabled
	epel-testing-debuginfo/x86_64 Extra Packages for Enterprise Linux 7 - Testing - x86_64 - Debu disabled
	epel-testing-source/x86_64    Extra Packages for Enterprise Linux 7 - Testing - x86_64 - Sour disabled
	extras/7/x86_64               CentOS-7 - Extras - 163.com                                     enabled:    282
	updates/7/x86_64              CentOS-7 - Updates - 163.com                                    enabled:  1,084
	repolist: 23,028

