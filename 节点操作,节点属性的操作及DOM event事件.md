**1. 节点操作**

    createElement(标签名)                           创建一个指定名称的元素
    someone.appendChild(new_node)                  追加一个子节点(作为最后的子节点)
    someone.insertBefore(new_node,指定节点)         把增加的节点放到指定节点的前边
    removeChild()                                  获取要删除的元素,通过父元素调用删除
    someone.replaceChild(new_node,指定节点)         把指定节点替换成新节点
    
**2. 节点属性操作**

***2.1 获取文本节点的值***

    innerText               获取一个标签的文本内容
	innerHTML               获取一个标签的全部标签内容
	
例子:

    <div id="c1"><p>hello</p></div>
    <script>
        var ele=document.getElementById("c1");//通过id的方式获取元素
        console.log(ele.innerHTML);//打印元素的全部标签
        console.log(ele.innerText);//打印元素的字体
    </script>
	
***2.2 `attribute`操作***

	elementNode.setAttribute(name,value)       为一个元素设置属性及属性值
	elementNode.getAttribute(属性名)            获得一个元素的属性值
	elementNode.removeAttribute("属性名")       删除一个元素的指定属性
	
***2.3 `value`获取当前选中的`value`值***

	input
	select(selectedIndex)
	textarea
	
***2.4 `innerHTML`给节点添加html代码***

	tag.innerHTML="<p>添加的内容</p>"
	
***2.5 关于`class`的操作***

	elementNode.className               获取一个元素节点的类名
	elementNode.classList.add           为一个元素节点添加类属性
	elementNode.classList.remove		删除一个元素节点中的类属性
	
例子:

    <div class="item btn" id="d1">DIV</div>
    <script>
        var ele=document.getElementById("d1");//通过id号获取元素
        console.log(ele.className);//打印元素的类名
        ele.classList.add("div1");//为元素的类添加一个"div1"属性
        console.log(ele.className);//打印元素的类名
        ele.classList.remove("item");//删除元素的"item"属性
        console.log(ele.className);//打印元素的类名
    </script>
	
***2.6 改变`css`的样式***

	<p id="p2">hello world</p>
	document.getElementById("p2").style.color="red";//把p标签的颜色设置成红色
	document.getElementById("p2").style.fontsize=20px;//把p标签的字体大小设置为20像素
	
例子:

    <p>1111</p>
    <p>2222</p>
    <p>3333</p>
    <p>4444</p>
    <p>5555</p>
    <script>
        //通过标签名获取元素集合
        var p_eles=document.getElementsByTagName("p");
        //通过for循环遍历元素集合中的每一个元素
        for (var i=0;i <p_eles.length;i++){
            //为每一个元素绑定点击事件
            p_eles[i].onclick=function (){
                this.style.color="red";//使标签颜色为成红色
            }
        }
    </script>
	
浏览器页面的5个p标签,点击每个标签后,标签的字体颜色变成红色

**3. DOM event(事件)**

`event`对象: `event`对象代表事件的状态,比如事件在其中发生的元素,键盘按键的状态,鼠标的位置,鼠标按钮的状态

事件通常与函数结合使用,函数不会在事件发生前被执行,`event`对象在事件发生时系统已经创建好了,并且会在事件函数被调用时传给事件函数,开发者仅仅需要接收一下即可.

事件类型:
        
        onclick             当用户点击某个对象时调用的事件
        ondbclick           当用户双击某个对象时调用的事件
        
        onfocus             元素获得焦点,即鼠标移动到该元素时触发的事件
        onblur              元素失去焦点,即鼠标移出该元素时触发的事件
        
        onchange            文本域的内容被改变,使用在input文本输入框中
                
        onkeydown           键盘的某个键被按下
        
        onkeypress          键盘的某个键被按下并松开
        onkeyup             键盘的某个键被松开
        
        onload              只用于body元素,这个属性的触发标志着页面内容被加载完成
        
        onmousedown         鼠标按钮被按下
        onmousemove         鼠标被移动
        onmouseout          鼠标从某个元素移开
        onmouseover         鼠标移到某个元素之上
        onmouseleave        鼠标从元素离开
        
        onselect            文本被选中
        onsubmit            当表单在提交是触发,只能给form元素使用
    
例子一,绑定提交事件

    <form action="" id="form">
        <p>姓名<input type="text"></p>
        <p>密码<input type="password"></p>
        <input type="submit">
    </form>
    <script>
        //通过id号获取元素
        var ele=document.getElementById("form");
        //提交按钮被点击
        ele.onsubmit=function(e){
            alert("1234");//弹出对话框
        }
    </script>
	
例子二,绑定窗口加载完成事件 

    <script>
        //为窗口绑定加载完成函数
        window.onload=function(){
            //获取元素
            var ele=document.getElementById("c1");
            //把元素的字符颜色变成红色
            ele.style.color="red";
        }
    </script>
    <body>
    <div id="c1">div</div>
    </body>	
	
例子三,绑定键盘按下松开事件

    <input type="text" id="user">
    <script>
        var ele=document.getElementById("user");
        ele.onkeydown=function(e){
            e=e||window.event;
            //键盘输入的字符对应ASCII码中对应小写字母的ASCII码
            console.log(String.fromCharCode(e.keyCode));
            console.log(e.keyCode);//按下键盘上的某个键时,对应文本字符的ASCII码中的小写字母
        }
    </script>
	
例子四,悬浮下拉菜单

    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title></title>
        <style type="text/css">
            .container {
                width: 300px;
            }
            .title {
                background-color: gray;
                line-height: 44px;
                text-align: center;
            }
            .list {
                display: none;
            }
            .list div {
                line-height: 40px;
            }
            .item1 {
                background-color: green;
            }
            .item2 {
                background-color: goldenrod;
            }
            .item3 {
                background-color: rebeccapurple;
            }
            .item4 {
                background-color: pink;
            }
        </style>
    </head>
    <div class="container">
        <div class="title">text</div>
        <div class="list">
            <div class="item1">1111</div>
            <div class="item2">2222</div>
            <div class="item3">3333</div>
            <div class="item4">4444</div>
        </div>
    </div>
    <script>
        var ele = document.getElementsByClassName("title")[0];//获取class类集合的第一个元素
        var ele_list = document.getElementsByClassName("list")[0];//获取list类集合的第一个元素
        var ele_box = document.getElementsByClassName("container")[0];//获取container类集合的第一个元素
    
        //绑定鼠标悬浮事件
        ele.onmouseover = function () {
            ele_list.style.display = "block";
        };
    
        //绑定鼠标离开事件
        ele_box.onmouseleave = function () {
            ele_list.style.display = "none";
        }
    </script>
    <body>
    </body>
    </html>
	
**4. 事件的绑定方式**

***4.1 方式1***

代码:

    //在标签的属性中绑定点击事件
    <div id="div1" onclick="func()">div</div>
    <script>
        function func(self){
            alert("12345")
        }
    </script>
	
***4.2 方式2***

代码:

    <p id="div1">div1</p>
    <script>
        
        var ele1=document.getElementById("div1");//通过id名获取标签
        
        //为上面获取的标签绑定点击事件
        ele.onclick=function(){
            console.log("ok")
        };
    </script>