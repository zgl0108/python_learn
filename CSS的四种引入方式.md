**1.行内式**

行内式是在标记的`style`属性中设定CSS样式.

    <p style="color:red;background-color: yellow">hello world</p>
    
这种方式没有体现出CSS的优势.因此不推荐使用.

**2.嵌入式**

嵌入式是将`.CSS`样式集中写在网页的`<head></head>`下的`<style></style>`标签对里.

格式如下:

    <head>
        <meta charset="utf-8">
        <title>
            index
        </title>
        <style>
            s1 {
                color: red;
                background-color: yellow
            }
        </style>
    </head>
    <body>
    </body>
	
**3.链接式**

将一个`.css`文件引入HTML文件中

	<link rel="stylesheet" href="index.css" type="text/css"/>

**4.导入式**

将一个独立的CSS文件引入`HTML`文件中,导入式使用`CSS`规则引入外部`CSS`文件,`style`标记也是写在`<head>`标记中.

使用语法如下:

        <style type="text/css">
            <!--index.css指的是CSS文件的路径-->
            @import "index.css";
        </style>

注意:

导入式会在整个网页装载完成后再装载CSS文件,因此如果网页比较大则会出现先显示CSS无样式的页面,

闪烁一下之后,再出现网页的样式的问题.这是导入式固有的一个缺陷.

使用链接式则会在网页文件主体装载前装载CSS文件,因此显示出来的网页从一开始就是带CSS样式的效果的.

它不会像导入式那样先显示无样式的网页,然后再显示有样式的网页,这是链接式的优点.