zip函数接受任意多个可迭代对象作为参数,将对象中对应的元素打包成一个`tuple`,然后返回一个可迭代的zip对象.

这个可迭代对象可以使用循环的方式列出其元素

若多个可迭代对象的长度不一致,则所返回的列表与长度最短的可迭代对象相同.

## 用法1:用两个列表生成一个zip对象

**例1**

    >>> a1=[1,2,3]
    >>> a2=[4,5,6]
    >>> a3=[7,8,9]
    >>> a4=["a","b","c","d"]
    >>> zip1=zip(a1,a2,a3)
    >>> print(zip1)
    <zip object at 0x7f5a22651c08>
    >>> for i in zip1:
    ...     print(i)
    ... 
    (1, 4, 7)
    (2, 5, 8)
    (3, 6, 9)

**例2**

    >>> zip2=zip(a1,a2,a4)
    >>> print(zip2)
    <zip object at 0x7f5a22651d48>
    >>> for j in zip2:
    ...     print(j)
    ... 
    (1, 4, 'a')
    (2, 5, 'b')
    (3, 6, 'c')

**例3**

    >>> zip3=zip(a4)
    >>> print(zip3)
    <zip object at 0x7f5a22651d08>
    >>> for i in zip3:
    ...     print(i)
    ... 
    ('a',)
    ('b',)
    ('c',)
    ('d',)

**例4**

    >>> zip4=zip(*a4 *3)
    >>> 
    >>> print(zip4)
    <zip object at 0x7f5a22651f08>
    >>> for j in zip4:
    ...     print(j)
    ... 
    ('a', 'b', 'c', 'd', 'a', 'b', 'c', 'd', 'a', 'b', 'c', 'd')
    
## 用法2:二维矩阵变换(矩阵的行列互换)

    >>> l1=[[1,2,3],[4,5,6],[7,8,9]]
    >>> print([[j[i] for j in l1] for i in range(len(l1[0])) ])
    [[1, 4, 7], [2, 5, 8], [3, 6, 9]]
    >>> zip(*l1)
    <zip object at 0x7f5a22651f88>
    >>> for i in zip(*l1):
    ...     print(i)
    ... 
    (1, 4, 7)
    (2, 5, 8)
    (3, 6, 9)