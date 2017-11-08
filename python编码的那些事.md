字符串编码在python里是经常会遇到的问题,特别是写文件或是网络传输调用某些函数的时候.

现在来看看python中的unicode编码和utf-8编码

字符串编码的历史

1. 计算机只能处理数字,文本转换为数字才能处理. 计算机中8个bit作为一个字节,所以一个字节能表示最大的数字为255

2. 计算机是美国人发明的,一个字节就可以表示所有的英文字符了,所以ACSII(一个字节)编码就成为美国人的标准编码

3. 但是中文里远远不止255个汉字,这时用ASCII来处理中文是明显不够用的,所以我国制定了GB2312编码,用两个字节表示一个汉字.

GB2312还把ASCII包含进去.同理,别的国家为了解决自己国家的编码问题也都发展了一套字节的编码,这样标准就越来越多.

如果一篇文章出现多种语言混合显示就一定会出现乱码.

4. 这里unicode出现了,unicode把所有的语言统一到一套编码里.

5. 看一下ASCII编码和unicode编码:
	字母A用ASCII编码十进制是65,二进制是0100 00001
	汉字"中"已经超出了ASCII编码的范围,用unicode编码是20013,二进制是0100 1110 0010 1101
	A用unicode编码只需要前面补0,二进制是00000000 0100 0001

6. 乱码问题解决了,但是如果一段内容全是英文,unicode编码比ASCII需要多一倍的存储空间,浪费很多硬盘容量.同时传输时也需要多浪费很多带宽.

7. "utf-8"会把英文变成一个字节,汉字3个字节.特别生僻的变成4到6个字节.如果传输的英文,就把英文轮换成unicode编码格式.

python保存文件和读取文件时编码的关系

    保存文件时,把unicode编码转换成utf-8编码格式
    读取文件时,把utf-8编码转换成unicode编码格式
 
分别在windows系统和linux系统中测试python2和python3的编码区别

在`windows系统的python2版本`中

        Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:53:40) [MSC v.1500 64 bit (AMD64)] on win32
        >>> str1="hello"                # 因为str1和str2都是英文,所以atr1和str2不管是unicode编码还是ASCII格式
        >>> str2=u"hello"               # encode成utf-8编码时都不会出现错误
        >>> str1.encode("utf-8")
        'hello'
        >>> str2.encode("utf-8")
        'hello'
        
        >>> type(str1)
        <type 'str'>
        >>> type(str2)
        <type 'unicode'>
        
        >>> str3="我用python"             # python中的字符串在内存中是用unicode来编码的
        >>> str4=u"我用python"            # str3在windows系统中保存成GBK编码
        >>> str3.encode("utf-8")            # str3在调用encode方法之前必须转换为unicode编码
        Traceback (most recent call last):      # 此时str3应该先decode成为unicode编码,然后再encode成utf-8编码
          File "<input>", line 1, in <module>
        UnicodeDecodeError: 'ascii' codec can't decode byte 0xe6 in position 0: ordinal not in range(128)
        
        >>> str3.decode("utf-8")
        Traceback (most recent call last):
          File "<stdin>", line 1, in <module>
          File "D:\Python27\lib\encodings\utf_8.py", line 16, in decode
            return codecs.utf_8_decode(input, errors, True)
        UnicodeDecodeError: 'utf8' codec can't decode byte 0xce in position 0: invalid c
        ontinuation byte
        
        >>> str3.decode('gbk')
        u'\u6211\u7528python'	
        
        >>> str3.decode("utf-8").encode("utf-8")
        '\xe6\x88\x91\xe7\x94\xa8python'
        
        >>> str4.encode("utf-8")
        '\xe6\x88\x91\xe7\x94\xa8python'
        
        >>> type(str3)
        <type 'str'>
        >>> type(str4)
        <type 'unicode'>
        
        >>> import sys
        >>> sys.getdefaultencoding()
        'ascii'

在`windows系统的python3版本`中

        Python 3.6.1 (v3.6.1:69c0db5, Mar 21 2017, 18:41:36) [MSC v.1900 64 bit (AMD64)] on win32
        Type "help", "copyright", "credits" or "license" for more information.
        >>> str1="hello"                        # python3中所有的字符串都是unicode编码
        >>> str2=u"hello"
        >>> str1.encode("utf-8")
        b'hello'
        >>> str2.encode("utf-8")
        b'hello'
        >>> str3="我用python"
        >>> str3.encode("utf-8")
        b'\xe6\x88\x91\xe7\x94\xa8python'
        >>> str4=u"我用python"
        >>> str4.encode("utf-8")
        b'\xe6\x88\x91\xe7\x94\xa8python'
        
        >>> import sys
        >>> sys.getdefaultencoding()  
        'utf-8'

在`linux系统的python2版本`中

        Python 2.7.5 (default, Nov  6 2016, 00:28:07) 
        [GCC 4.8.5 20150623 (Red Hat 4.8.5-11)] on linux2
        Type "help", "copyright", "credits" or "license" for more information.
        >>> str1="我用python"				
        >>> str1.encode("utf-8")			
        Traceback (most recent call last):		
          File "<stdin>", line 1, in <module>
        UnicodeDecodeError: 'ascii' codec can't decode byte 0xe6 in position 0: ordinal not in range(128)
        
        >>> str1.decode("gbk")							
        u'\u93b4\u6220\u6564python'						
        >>> str1.decode('utf-8')                        # linux系统中python2会把字符串保存成utf-8编码,那为什么不能直接encode呢?
        u'\u6211\u7528python'                           # 字符串在encode之前应该保证是一个unicode编码格式,字符串在encode之前
                                                        # 会调用decode方法把字符串转换成unicode编码,然后才能encode
        >>> str1.decode("utf-8").encode("utf-8")        # str1字符串中含有中文,直接encode成utf-8编码会出现错误
        '\xe6\x88\x91\xe7\x94\xa8python'
        
        >>> str1.decode("gbk").encode("utf-8")
        '\xe9\x8e\xb4\xe6\x88\xa0\xe6\x95\xa4python'
        
        >>> str2=u"我用python"
        >>> str2.encode("utf-8")
        '\xe6\x88\x91\xe7\x94\xa8python'
        
        >>> type(str1)
        <type 'str'>
        >>> type(str2)
        <type 'unicode'>
        
        >>> import sys
        >>> sys.getdefaultencoding()
        'ascii'
	
在`linux系统的python3版本`中

        Python 3.6.3 (default, Nov  7 2017, 20:33:25) 
        [GCC 4.8.5 20150623 (Red Hat 4.8.5-11)] on linux
        Type "help", "copyright", "credits" or "license" for more information.
        >>> str1="我用python"                     # python3中所有的字符串都是unicode编码
        >>> str2=u"我用python"
        >>> str1.encode("utf-8")
        b'\xe6\x88\x91\xe7\x94\xa8python'
        >>> str2.encode("utf-8")
        b'\xe6\x88\x91\xe7\x94\xa8python'
        
        >>> import sys
        >>> sys.getdefaultencoding()  
        'utf-8'

不管是windows系统还是linux系统,`python2版本中默认使用ASCII编码`,`python3版本默认使用utf-8编码`