**ceil**
```
#取大于等于x的最小的整数值，如果x是一个整数，则返回x
ceil(x)
Return the ceiling of x as an int.
This is the smallest integral value >= x.
```
    >>> math.ceil(4.01)
	5
	>>> math.ceil(4.99)
	5
	>>> math.ceil(-3.99)
	-3
	>>> math.ceil(-3.01)
	-3

**copysign**
```
#把y的正负号加到x前面，可以使用0
copysign(x, y)
Return a float with the magnitude (absolute value) of x but the sign 
of y. On platforms that support signed zeros, copysign(1.0, -0.0) 
returns -1.0.
```
	>>> math.copysign(2,3)
	2.0
	>>> math.copysign(2,-3)
	-2.0
	>>> math.copysign(3,8)
	3.0
	>>> math.copysign(3,-8)
	-3.0

**cos**
```
#求x的余弦，x必须是弧度
cos(x)
Return the cosine of x (measured in radians).
```
	#math.pi/4表示弧度，转换成角度为45度
	>>> math.cos(math.pi/4)
	0.7071067811865476
	math.pi/3表示弧度，转换成角度为60度
	>>> math.cos(math.pi/3)
	0.5000000000000001
	math.pi/6表示弧度，转换成角度为30度
	>>> math.cos(math.pi/6)
	0.8660254037844387

**degrees**
```
#把x从弧度转换成角度
degrees(x)
Convert angle x from radians to degrees.
```
	>>> math.degrees(math.pi/4)
	45.0
	>>> math.degrees(math.pi)
	180.0
	>>> math.degrees(math.pi/6)
	29.999999999999996
	>>> math.degrees(math.pi/3)
	59.99999999999999

**e**
```
#表示一个常量
```
	>>> math.e
	2.718281828459045

**exp**
```
#返回math.e,也就是2.71828的x次方
exp(x)
Return e raised to the power of x.
```
	>>> math.exp(1)
	2.718281828459045
	>>> math.exp(2)
	7.38905609893065
	>>> math.exp(3)
	20.085536923187668

**expm1**
```
#返回math.e的x(其值为2.71828)次方的值减１
expm1(x)
Return exp(x)-1.
This function avoids the loss of precision involved in the direct evaluation of exp(x)-1 for small x.
```
	>>> math.expm1(1)
	1.718281828459045
	>>> math.expm1(2)
	6.38905609893065
	>>> math.expm1(3)
	19.085536923187668

**fabs**
```
#返回x的绝对值
fabs(x)
Return the absolute value of the float x.
```
	>>> math.fabs(-0.003)
	0.003
	>>> math.fabs(-110)
	110.0
	>>> math.fabs(100)
	100.0

**factorial**
```
#取x的阶乘的值
factorial(x) -> Integral
Find x!. Raise a ValueError if x is negative or non-integral.
```
	>>> math.factorial(1)
	1
	>>> math.factorial(2)
	2
	>>> math.factorial(3)
	6
	>>> math.factorial(5)
	120
	>>> math.factorial(10)
	3628800

**floor**
```
#取小于等于x的最大的整数值，如果x是一个整数，则返回自身
floor(x)
Return the floor of x as an int.
This is the largest integral value <= x.
```
	>>> math.floor(4.1)
	4
	>>> math.floor(4.999)
	4
	>>> math.floor(-4.999)
	-5
	>>> math.floor(-4.01)
	-5

**fmod**
```
#得到x/y的余数，其值是一个浮点数
fmod(x, y)
Return fmod(x, y), according to platform C.  x % y may differ.
```
	>>> math.fmod(20,3)
	2.0
	>>> math.fmod(20,7)
	6.0

**frexp**
```
#返回一个元组(m,e),其计算方式为：x分别除0.5和1,得到一个值的范围，
#2**e的值在这个范围内，e取符合要求的最大整数值,然后x/(2**e),得到m的值
#如果x等于0,则m和e的值都为0,m的绝对值的范围为(0.5,1)之间，不包括0.5和1
frexp(x)
Return the mantissa and exponent of x, as pair (m, e).
m is a float and e is an int, such that x = m * 2.**e.
If x is 0, m and e are both 0.  Else 0.5 <= abs(m) < 1.0.
```
	>>> math.frexp(10)
	(0.625, 4)
	>>> math.frexp(75)
	(0.5859375, 7)
	>>> math.frexp(-40)
	(-0.625, 6)
	>>> math.frexp(-100)
	(-0.78125, 7)
	>>> math.frexp(100)
	(0.78125, 7)

**fsum**
```
#对迭代器里的每个元素进行求和操作
fsum(iterable)
Return an accurate floating point sum of values in the iterable.
Assumes IEEE-754 floating point arithmetic.
```
	>>> math.fsum([1,2,3,4])
	10.0
	>>> math.fsum((1,2,3,4))
	10.0
	>>> math.fsum((-1,-2,-3,-4))
	-10.0
	>>> math.fsum([-1,-2,-3,-4])
	-10.0

**gcd**
```
#返回x和y的最大公约数
gcd(x, y) -> int
greatest common divisor of x and y
```
	>>> math.gcd(8,6)
	2
	>>> math.gcd(40,20)
	20
	>>> math.gcd(8,12)
	4

**hypot**
```
#得到(x**2+y**2),平方的值
hypot(x, y)
Return the Euclidean distance, sqrt(x*x + y*y).
```
	>>> math.hypot(3,4)
	5.0
	>>> math.hypot(6,8)
	10.0

**isfinite**
```
#如果x是不是无穷大的数字,则返回True,否则返回False
isfinite(x) -> bool
Return True if x is neither an infinity nor a NaN, and False otherwise.
```
	>>> math.isfinite(100)
	True
	>>> math.isfinite(0)
	True
	>>> math.isfinite(0.1)
	True
	>>> math.isfinite("a")
	>>> math.isfinite(0.0001)
	True

**isinf**
```
#如果x是正无穷大或负无穷大，则返回True,否则返回False
isinf(x) -> bool
Return True if x is a positive or negative infinity, and False otherwise.
```
	>>> math.isinf(234)
	False
	>>> math.isinf(0.1)
	False

**isnan**
```
#如果x不是数字True,否则返回False
isnan(x) -> bool
Return True if x is a NaN (not a number), and False otherwise.
```
	>>> math.isnan(23)
	False
	>>> math.isnan(0.01)
	False

**ldexp**
```
#返回x*(2**i)的值
ldexp(x, i)
Return x * (2**i).
```
	>>> math.ldexp(5,5)
	160.0
	>>> math.ldexp(3,5)
	96.0

**log**
```
#返回x的自然对数，默认以e为基数，base参数给定时，将x的对数返回给定的base,计算式为：log(x)/log(base)
log(x[, base])
Return the logarithm of x to the given base.
If the base not specified, returns the natural logarithm (base e) of x.
```
	>>> math.log(10)
	2.302585092994046
	>>> math.log(11)
	2.3978952727983707
	>>> math.log(20)
	2.995732273553991

**log10**
```
#返回x的以10为底的对数
log10(x)
Return the base 10 logarithm of x.
```
	>>> math.log10(10)
	1.0
	>>> math.log10(100)
	2.0
	#即10的1.3次方的结果为20
	>>> math.log10(20)
	1.3010299956639813

**log1p**
```
#返回x+1的自然对数(基数为e)的值
log1p(x)
Return the natural logarithm of 1+x (base e).
The result is computed in a way which is accurate for x near zero.
```
	>>> math.log(10)
	2.302585092994046
	>>> math.log1p(10)
	2.3978952727983707
	>>> math.log(11)
	2.3978952727983707

**log2**
```
#返回x的基2对数
log2(x)
Return the base 2 logarithm of x.
```
	>>> math.log2(32)
	5.0
	>>> math.log2(20)
	4.321928094887363
	>>> math.log2(16)
	4.0

**modf**
```
#返回由x的小数部分和整数部分组成的元组
modf(x)
Return the fractional and integer parts of x.  Both results carry the sign
of x and are floats.
```
	>>> math.modf(math.pi)
	(0.14159265358979312, 3.0)
	>>> math.modf(12.34)
	(0.33999999999999986, 12.0)

**pi**
```
#数字常量，圆周率
```
	>>> print(math.pi)
	3.141592653589793

**pow**
```
#返回x的y次方，即x**y
pow(x, y)
Return x**y (x to the power of y).
```
	>>> math.pow(3,4)
	81.0
	>>> 
	>>> math.pow(2,7)
	128.0

**radians**
```
#把角度x转换成弧度
radians(x)
Convert angle x from degrees to radians.
```
	>>> math.radians(45)
	0.7853981633974483
	>>> math.radians(60)
	1.0471975511965976

**sin**
```
#求x(x为弧度)的正弦值
sin(x)
Return the sine of x (measured in radians).
```
	>>> math.sin(math.pi/4)
	0.7071067811865475
	>>> math.sin(math.pi/2)
	1.0
	>>> math.sin(math.pi/3)
	0.8660254037844386

**sqrt**
```
#求x的平方根
sqrt(x)
Return the square root of x.
```
	>>> math.sqrt(100)
	10.0
	>>> math.sqrt(16)
	4.0
	>>> math.sqrt(20)
	4.47213595499958


**tan**
```
#返回x(x为弧度)的正切值
tan(x)
Return the tangent of x (measured in radians).
```
	>>> math.tan(math.pi/4)
	0.9999999999999999
	>>> math.tan(math.pi/6)
	0.5773502691896257
	>>> math.tan(math.pi/3)
	1.7320508075688767

**trunc**
```
#返回x的整数部分
trunc(x:Real) -> Integral
Truncates x to the nearest Integral toward 0. Uses the __trunc__ magic method.
```
	>>> math.trunc(6.789)
	6
	>>> math.trunc(math.pi)
	3
	>>> math.trunc(2.567)
	2