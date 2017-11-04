##排序low B三人组

列表排序:将无序列表变成有充列表

应用场景:各种榜单,各种表格,给二分法排序使用,给其他算法使用

    输入无序列表,输出有序列表(升序或降序)
	
排序low B三人组

## 冒泡排序

首先,列表每两个相邻的数做比较,如果前边的数比后边的数大,那么交换这两个数
```
def bubble_sort(l1):
    for i in range(len(l1)-1):
        for j in range(len(l1)-i-1):
            if l1[j] > l1[j+1]:
                l1[j],l1[j+1]=l1[j+1],l1[j]
                
    return l1
```
**冒泡排序的优化**

如果冒泡排序中执行一趟而没有交换,则列表已经是有序状态,可以直接结束排序
```
def bubble_sort_1(l1):
    for i in range(len(l1)-1):
        flag=False
        
        for j in range(len(l1)-i-1):
            if l1[j] > l1[j+1]:
                l1[j],l1[j+1]=l1[j+1],l1[j]
                flag=True
        
        if not flag:
            return l1
```
## 选择排序

一趟遍历记录中最小的数,放到第一个位置
再一趟遍历记录剩余列表中最小的数,继续放置				
```
    def select_sort(l1):
        for i in range(len(l1)-1):
            mid=i
    
            for j in range(i+1,len(l1)):
                if l1[j] <l1[mid]:
                    mid=j
    
            l1[mid],l1[i]=l1[i],l1[mid]
    
        return l1
```
## 插入排序

列表被分有有序区和无序区两个部分.最初有序区只有一个元素

每次从无序区选择一个元素,插入到有序区的位置,直到无序区变空
```
def insert_sort(li):
    for i in range(1, len(li)):
        tmp = li[i]
        j = i - 1       #手里最后一张
        while j>=0 and li[j]>tmp:
            li[j+1]=li[j]
            j = j-1
        li[j+1] = tmp
        
    return li	
```