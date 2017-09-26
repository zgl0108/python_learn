**1.HTML中表单元素的基本概念**

HTML表单是HTML元素中较为复杂的部分,表单往往和脚本,动态页面,数据处理等功能相结合,因此是制作动态网站很重要的内容.

表单一般用来收集用户的输入信息

**2.表单工作原理**

访问者在浏览有表单的网页时,可填写必需的信息,然后按某个按钮提交,这些信息通过网络传送到服务器上.

服务器上专门的程序对这些数据进行处理,如果有错误会返回错误信息,并要求纠正错误.当数据完整无误后,服务器反馈一个输入完成的信息

**3.表单的功能**

功能:表单用于向服务器传输数据,从而实现用户与WEB服务器的交互

表单能够包含`input`系统标签,比如文本字段,复选框,单选框,提交按钮等

表单还可以包含`textarea`,`select`,`fieldset`,`label`标签.

**4.表单的常用类型及说明**

***1.表单常用的类型有***

    text            文本输入框
    password        密码输入框
    radio           单选框     
    checkbox        多选框
    button          提交按钮
    file            提交文件,from表单需要加上属性enctype=multipart/form-data
    
***2.表单属性***

    name:   表单提交项的键,是和服务器通信时使用的名称   
    value:表单提交项的值,对于不同的输入类型,value属性的用法也不同   
    
***3.文本输入框(`text`)***

当用户要在表单中输入字母,数字内容时,就会用到文本域

代码如下:

    <form>
        <p>姓名:<input type="text" name="username" placeholder="用户名"></p>
        <p>密码:<input type="password" name="password" values="567"></p>
    </form>
    
注意,表单本身并不可见.同时,在大多浏览器中,文本域的缺省宽度是20个字符.

在密码域中输入的字符,浏览器将使用项目符号来代替这些字符.

***4.单选按钮(`radio`)***

当用户从若干给定的选择中选取一个选项时,就会用到单选框.

代码如下:

    <form>
        <p>性别:<input type="radio" name="sex" value="male">男
                <input type="radio" name="sex" value="female">女</p>
    </form>
    
用户只能从众多选择中选取一个选项.

当用户点击一个单选按钮时,该按钮会变为选中状态,其他所有按钮会变为非选中状态.

***5.复选框(`checkboxes`)***

当用户需要从若干给定的选择中选取一个或多个选项时,就会用到复选框

代码如下:

    <form>
    <p>爱好:<input type="checkbox" name="hobby" value="baskerball">basketball
            <input type="checkbox" name="hobby" value="football">football
            <input type="checkbox" name="hobby" value="table tennis">table tennis</p>
    </form>
    
用户一次可以选择多个选项. 
  
***6.重置按钮(`reset`)***

重置按钮会清除当前页面上的用户输入的所有数据,把当前页面恢复到打开时的样子.

代码如下:

    <form>
    <p><input type="reset"></p>
    </form> 
    
***7.提交按钮***

会在当前页面生成一个提交按钮,用户点击此按钮,浏览器就会把当前页面用户输入的数据传送到服务端

代码如下:

    <form>
    <p><input type="button" value="按钮"/></p>
    </form> 
    
***8.提交文件***

当需要把客户端的文件发送到服务端时,需要用到提交文件按钮

代码如下:

    <form action="/index/" method="post">
    <p><input type="file"/></p>
    </form>
    
上传文件注意两点:

    请求方式必须是post
    enctype="multipart/form-data"

***9.下拉菜单***

当需要用户从很多选项中选择一个或多个选项时,也可以使用下拉列表.

代码如下:

    <form>
        <p>籍贯<select name="籍贯">
            <option value="hebei">河北省</option>
            <option value="hubei">湖北省</option>
            <option value="henan">河南省</option>
            <option value="hunan">湖南省</option></select></p>
    </form> 
    
这样的下拉列表,用户只能从其中选择一个选项,当需要用户选择两个或以下时,可以添加参数来进行控制.

代码如下:

    <form>
        <p>籍贯<select name="籍贯" size="2" multiple="multiple">
            <option value="hebei">河北省</option>
            <option value="hubei">湖北省</option>
            <option value="henan">河南省</option>
            <option value="hunan">湖南省</option>
        </select></p>
    </form> 
    
还可以在`OPTION`中添加`selected="selected"`选项来设置默认值.
    
***10.表单属性***

    action:表单提交到哪,一般指向服务端一个程序,程序接收到表单提交过来的数据(即表单元素值)作相应处理
    method:表单的提交方式,post或者get,默认为get
    
****1.`action`属性的说明****

    action属性定义在提交表单时执行的动作
    向服务器提交表单的通常做法是使用提交按钮
    通常,表单会被提交到web服务器上的网页,
    表单的动作属性定义了目的文件的文件名,由动作属性定义的这个文件通常会对接收到的输入数据进行相关的处理

使用`action`选项来指定服务端的脚本来处理被提交的表单

    <form action="/index/" method="post">
    
如果省略`action`属性,则`action`会被设置为当前页面

****2.method属性的说明****

`method`属性规定在提交表单时所用的`http`方法(`POST`或`GET`)

    <form action="/index/" method="post">
或

    <form action="/index/" method="get">
    
****3.`get`方法或`post`方法的使用方式说明****

如果表单提交是被动的(比如搜索引擎查询),并且没有敏感信息.

当使用`get`方法时,表单的数据在页面地址栏中是可见的

因此,`get`最适合少量数据的提交,浏览器会设定容量限制
    
如果表单正在更新数据,或者包含敏感信息(比如密码)时应该使用`post`,`post`的安全性更好.

因为在页面地址栏中被提交的数据是不可见的.