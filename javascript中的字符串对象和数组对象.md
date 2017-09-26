**1.javascript的对象的概念**

在`javascript`中,除了`null`和`undefined`以处,其他的数据类型都被定义成了对象

也可以用创建对象的方法定义变量,`string`,`math`,`array`,`data`都是`javascript`中重要的内置对象.

在javascript程序大多数功能都是基于对象实现的

    var aa=Number.MAX_VALUE;            //利用数字对象获取可表示最大数
	var bb=new String("hello world");   //创建字符串对象
	var cc=new Date();                  //创建日期对象
	var dd=new Array("monday","tuesday","thirsday","foutday"); //数组对象
	
**2.`javascript`内置对象的分类**

数据对象

	Number          数字对象
	String          字符串对象
	Boolean         布尔值对象
	
组合对象

	Array           数组对象
	Math            数学对象
	Date            日期对象
	
高级对象

	Object          自定义对象
	Error           错误对象
	Function        函数对象
	Regexp          正则表达式对象
	Global          全局对象
	
**3.`javascript`中的字符串(`String`)对象**

***1.字符串对象的创建***

字符串的创建有两种方式:

	* 变量="字符串"
	* 字符串对象名称=new String(字符串)
	
例子:

	var str1="hello world";
	var str1= new String("hello word");
	
***2.字符串对象的属性和函数***

***str.length***
				
获取字符串的长度

例子:

	var txt="Hello World!";
	document.write(txt.length);
	
返回:

	12
***str.toLowerCase()***
			
把字符串转换为小写

例子:

	var str="Hello World!";
	document.write(str.toLowerCase());
	
返回:

	hello world!

***str.toUpperCase()***
			
把字符串转换为大写

例子:

	var str="Hello World!";
	document.write(str.toUpperCase());
	
返回:

	HELLO WORLD!

***str.trim()***
		
去除字符串两边的空格

例子:

	var str1="    hello world   ";
	document.write(str1.length + "<br />");
	document.write(str1.trim() + "<br />");
	document.write(str1.trim().length);
返回值:

	18
	hello world
	11
	
***str.charAt(index)***	
			
返回指定索引的字符,字符串的第一个字符串的下标为0

例子:

	var str="Hello world!";
	document.write(str.charAt(1));
	
返回:

	e
	
***str.indexOf(findstr,index)***	
	
返回指定字符在字符串中首次出现的位置

从字符串str的index处开始,查找`findstr`,如果找到则返回`findstr`第一次出现的位置,如果没有指定index,则从头开始查找
如果没有找到要查找的字符串,返回`-1`,大小写敏感

例子:

	var str="Hello world!";
	document.write(str.indexOf("Hello") + "<br />");
	document.write(str.indexOf("World") + "<br />");
	document.write(str.indexOf("world") + "<br />");
	
返回值:

	0
	-1
	6
	
***str.lastIndexOf(findstr,index)***

在字符串str中的`index`处向前查找指定字符`findstr`,没有指定`index`时,则从后向前查找,如果找到`findstr`,则返回第一个`findstr`在字符串str的位置.

如果没找到指定指定字符串,则返回-1,大小写敏感

例子:

	var str="Hello world!";
	document.write(str.lastIndexOf("Hello") + "<br />");
	document.write(str.lastIndexOf("World") + "<br />");
	document.write(str.lastIndexOf("world"));
	
返回:
	
	0
	-1
	6
	
***str.match(findstr)***
		
在字符串中查找指定的字符,这个字符可以是正则表达式

若在字符串`str`中找到指定的字符串,则返回找到的字符串,没找到则返回null

例子:

	var str="Hello world!";
	document.write(str.match("world") + "<br />");
	document.write(str.match("World") + "<br />");
	document.write(str.match("worlld") + "<br />");
	document.write(str.match("world!"));
	
返回:

	world
	null
	null
	world!
	
***str.search(regexp)***

在字符串`str`中查找指定的子字符串或与正则表达式匹配的子字符串

返回指定子字符串在字符串`str`的起始位置,未匹配到子字符串则返回-1,大小写敏感

例子:

	var str="hello world!";
	document.write(str.search(/world/));
	document.write(str.search(/World/));
	
返回:

	6
	-1
	
***str.substr(start,length)***

从字符串str的起始索引处开始提取指定长度的字符串

如果没有指定长度,则提取从`start`处开始到结尾的全部字符

例子1:
	
	var str="Hello world!";
	document.write(str.substr(3));
	
返回:
	
	lo world!
	
例子2:

	var str="Hello world!";
	document.write(str.substr(3,7));
	
返回:
	
	lo worl

***str.substring(start,end)***

提取字符串str中两个索引之间的字符串,不包括end处的字符

如果`start`与`end`的值相等,则返回一个空的字符串

例子1:

	var str="Hello world!";
	document.write(str.substring(3));
	
返回:

	lo world!
	
例子2:

	var str="Hello world!";
	document.write(str.substring(3,7));
	
返回:
	
	lo w
	
***str.slice(start,end)***

对字符串进行切片操作,返回字符串str从`start`(包含`start`)开始,到`end`(不包括`end`)结尾的所有字符

例子1:

	var str="Hello happy world!";
	document.write(str.slice(6));
	
返回:

	happy world!
	
例子2:

	var str="Hello happy world!";
	document.write(str.slice(6,11));
	
返回:

	happy
	
***str.replace(oldstr,newstr)***

把字符串中str的`oldstr`替换成`newstr`

例子:

	var str="hello world!";
	document.write(str.replace(/world/, "javascript"));
	
返回:

	hello javascript!
	
***str.split(sep,num)***

把字符串`str`按`sep`分割成字符串数组,`num`为可分割的最大数

例子1:

	var str="How are you doing today?";
	document.write(str.split(" ") + "<br />");
	document.write(str.split("") + "<br />");
	document.write(str.split(" ",3));
	
返回:

	How,are,you,doing,today?
	H,o,w, ,a,r,e, ,y,o,u, ,d,o,i,n,g, ,t,o,d,a,y,?
	How,are,you
	
例子2:

	"2:3:4:5".split(":");	//将返回["2", "3", "4", "5"]
	"|a|b|c".split("|");	//将返回["", "a", "b", "c"]
	"hello".split("");	//可返回 ["h", "e", "l", "l", "o"]
	"hello".split("", 3);	//可返回 ["h", "e", "l"]
	
***str.concat(str1,str2...)***

连接两个或多个字符串

例子:

	var str1="Hello ";
	var str2="world!";
	document.write(str1.concat(str2));
	
返回:

	Hello world!
	
**4.javascript中的数组对象(Array)**

***4.1 创建数组的三种方式***

***4.1.1 var 数组名=[元素1,元素2,元素3...];***

例如:

	var arr1=[1,2,3,4];
	
***4.1.2 var 数组名=new Array(元素1,元素2,元素3...)***

例如:

	var arr2=new Array(5,6,7,8);
	
***4.1.3 var 数组名=new Array(数组长度);***

		var 数组名[0]="数组第一个元素的值";
		var 数组名[1]="数组第二个元素的值";
		var 数组名[2]="数组第三个元素的值";

***4.2 数组对象的属性和方法***

***arr.join(sep)***

把数组中的所有元素使用sep拼接成一个字符串,如果没指定分割符,则使用逗号做为分割符

例子1:

	var arr = new Array(3);
	arr[0] = "hello";
	arr[1] = "python";
	arr[2] = "javascript";
	document.write(arr.join());
	
返回:

	hello,python,javascript
	
例子2:

	var arr = new Array(3);
	arr[0] = "hello";
	arr[1] = "python";
	arr[2] = "javascript";
	document.write(arr.join("."));
	
返回:

	hello.python.javascript
	
***arr.concat(array1,array2...)***

`array1`可以是一个值,也可以是一个数组对象,该方法返回自身和参数连接在一起的新的数组

例子1:

	var a = [1,2,3];
	document.write(a.concat(4,5));
	
返回:

	1,2,3,4,5
	
例子2:

    var arr = new Array(2);
    arr[0] = "hello";
    arr[1] = "python";
    
    var arr2 = new Array(2);
    arr2[0] = "hello";
    arr2[1] = "javascript";
    
    document.write(arr.concat(arr2));
    
返回:

	hello,python,hello,javascript
	
***arr.reverse()***

把数组arr进行倒序处理,原来的数组会被改变

例子:

	var arr = new Array(3);
	arr[0] = "hello";
	arr[1] = "python";
	arr[2] = "javascript";

	document.write(arr + "<br />");
	document.write(arr.reverse());
	
返回:

	hello,python,javascript
	javascript,python,hello
	
***arr.sort()***

对数组的元素进行排序,原来的数组会被改变

例子:

	var arr = [11,33,55,77,66,44,22];
	document.write(arr.sort());
	
返回:

	11,22,33,44,55,66,77
	
***arr.slice(start,end)***

返回一个由数组`arr`从`start`(包括`start`)到`end`(不包括`end`)的元素组成的新数组

`end`不指定时,则返回从`start`到结尾的所有元素组成的数组

例子1:

	var arr = [11,33,55,77,66,44,22];
	document.write(arr.slice(2,6));
	
返回:
	
	55,77,66,44
	
例子2:

	var arr = [11,33,55,77,66,44,22];
	document.write(arr.slice(2));
	
返回:

	55,77,66,44,22
	
***arr.splice(start,deleteCount,value1,value2)***

从数组arr的`start`索引处开始删除长度为`deleteCount`的元素,并向数组被删除的元素的位置添加`value1,value2`,然后返回被删除的元素,原来的数组会被改变

例子:

	var arr = [11,33,55,77,66,44,22];
	document.write(arr.splice(2,3,88,99)+"<br>");
	document.write(arr);
	
返回:

	55,77,66
	11,33,88,99,44,22
	
***arr.push(value1,value2,value3)***

向数组的末尾添加一个或多个元素,并返回新数组的长度

例子:

    var arr = [11,33,55,77,66,44,22];
    document.write(arr.push(88,99)+"<br>");//返回数组的长度
    document.write(arr);	//返回新的数组
    
返回:

	9
	11,33,55,77,66,44,22,88,99
	
***arr.pop()***

删除并返回数组的最后一个元素

例子:

    var arr = [11,33,55,77,66,44,22];
    document.write(arr.pop()+"<br>");//删除并返回数组arr的最后一个元素
    document.write(arr);	//打印数组
    
返回:

	22
	11,33,55,77,66,44
	
***arr.unshift(value1,value2,value3)***

向数组的开头添加一个或多个元素,并返回新数组的长度

例子:

    var arr = [11,33,55,77,66,44,22];
    document.write(arr.unshift("aa","bb","cc")+"<br>");
    document.write(arr);
    
返回:

	10
	aa,bb,cc,11,33,55,77,66,44,22
	
***arr.shift()***

删除并返回数组的第一个元素

例子:

    var arr = [11,33,55,77,66,44,22];
    document.write(arr.shift()+"<br>");
    document.write(arr);
    
返回:

	11
	33,55,77,66,44,22