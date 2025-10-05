---
tags:
  - '#project'
---

## 基本运算

### 基本数据类型

| 整数  | 浮点数 | 字符串          | 布尔值  | 空值   |     |
| --- | --- | ------------ | ---- | ---- | --- |
| 1   | 1.1 | ‘1.1’或者“1.1” | true | None |     |
### 打印
```python
#转义字符
\
#换行
\n
#换到行首
\r
#常用函数
print()
input()
#格式化 

'Hello, %d' % 1  => Hello 1
这里%用来格式化字符串

%s是字符串占位符，%d整数占位符，%f浮点数占位符

#另外一种格式化

'Hello, {0}, 成绩提升了 {1:.1f}%'.format('小明', 17.125)
=> 'Hello, 小明, 成绩提升了 17.1%'


print(f'The area of a circle with radius {r} is {s:.2f}')
```


上述代码中，`{r}`被变量`r`的值替换，`{s:.2f}`被变量`s`的值替换，并且`:`后面的`.2f`指定了格式化参数（即保留两位小数），因此，`{s:.2f}`的替换结果是`19.62`。

### 变量

```python
#变量不固定，动态语言这是python的写法
a=1 
#变量固定，静态语言，不是python的写法
int a=1
```

### 常量

与变量相对应，用大写来表示这个变量不能变，也就是常量

### 运算

```python
#浮点数除法
9/3 => 3.0
#整数除法
10//3  =>3
#求余数
10%3 =>1
#变量加法
a=a+b or a+=b
#变量减法
a=a-b or a-=b
#乘法
a=a*b or a*=b
#指数
a=a**3

```


## 字符串以及编码

ASCII编码（一个字符占据一个字节的容量），最多表示255个字符
Unicode字符集编码（一个字符通常占据两个字节的容量），最多表示65535个字符，而一些偏僻的字符用4个字节表示

但是一些简单的字符用不到一个字节的容量来去表示，这样太浪费空间了，因此，UTF-8编码集就此诞生，UTF-8编码把一个Unicode字符根据不同的数字大小编码成1-6个字节，常用的英文字母被编码成1个字节，汉字通常是3个字节

ASCII、Unicode和UTF-8的关系：内存当中，计算机统一用Unicode编码集，存储或者传输的时候用UTF-8编码集

在最新的Python 3版本中，字符串是以Unicode编码的，

```python
ord()  #这个函数用来获取字符串的Unicode整数编码
chr()  #函数把编码转换为对应的字符
```

## 高级数据类型list、tuple

python里面的list就是一个数组，或者叫做有序集合，索引从0开始，最后一个元素的索引为len(变量)-1

常用API方法：
```python
classMates=['lee','jet']
classMates.append('Raga') #添加元素进去
classMates.insert(1,'Raga') #插入元素进去
classMates.pop() #删除队尾元素
classMates.pop(1) #删除指定索引位置元素
```

tuple(元组)

有序列表叫元组：tuple。tuple和list非常类似，但是tuple一旦初始化就不能修改
比如同样是列出同学的名字：

```python
>>> classmates = ('Michael', 'Bob', 'Tracy')
```
现在，classmates这个tuple不能变了，它也没有append()，insert()这样的方法。

当只定义一个数字的tuple时候，不要用
`t=(1)`，这个指的是数学符号上的小括号，为了避免歧义，`t=(1,)`要这样写

## 条件判断

如果`if`语句判断是`True`，就把缩进的两行print语句执行了
```python
age = 3
if age >= 18:
     print('adult')
elif age >= 6:
     print('teenager')
else:
     print('kid')
```
需要注意的是，if语句是从上到下执行的，也就是说如果第一个条件满足，直接走第一个条件的语句，不会盘进行判断下面的语句

`if`语句执行有个特点，它是从上往下判断，如果在某个判断上是`True`，把该判断对应的语句执行后，就忽略掉剩下的`elif`和`else`，所以，请测试并解释为什么下面的程序打印的是`teenager`：

```python
age = 20
if age >= 6:
    print('teenager')
elif age >= 18:
    print('adult')
else:
    print('kid')
```

如果需要在条件判断中有多个判断语句，可以用与或非来进行连接，在python中用关键字：`and or not`来进行
除了 `True` 和 `False` 这两个布尔类型之外，Python 的条件判断（比如 `if` 语句）还有个非常强大的概念，叫做**真值性**（truthiness）。


None，False，任何数值类型的0，所有的空序列，空字符串，空元组，空字典，空集合等等都是为False

除了上面这些，其他值都被视为True


## match语句

当我们用`if ... elif ... elif ... else ...`判断时，会写很长一串代码，可读性较差。

如果用`match`语句改写简单匹配，则改写如下：

```python
score = 'B'
match score:
    case 'A':
        print('score is A.')
    case 'B':
        print('score is B.')
    case 'C':
        print('score is C.')
    case _: # _表示匹配到其他任何情况
        print('score is ???.')
```

复杂匹配：
`match`语句除了可以匹配简单的单个值外，还可以匹配多个值、匹配一定范围，并且把匹配后的值绑定到变量：

```python
age = 15

match age:
    case x if x < 10:
        print(f'< 10 years old: {x}')
    case 10:
        print('10 years old.')
    case 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18:
        print('11~18 years old.')
    case 19:
        print('19 years old.')
    case _:
        print('not sure.')
```

## 循环

有两种循环方式，一种是for...in... 依次把list或者tuple遍历出来
```python
names = ['Michael', 'Bob', 'Tracy']
for name in names:
    print(name)
```
所以`for x in ...`循环就是把每个元素代入变量`x`，然后执行缩进块的语句

第二种是while循环，只要条件满足，就不断循环，条件不满足时退出循环
```python
sum = 0
n = 99
while n > 0:
    sum = sum + n
    n = n - 2
print(sum)

```

可以用break关键词来提前退出循环
如果要提前结束循环，可以用`break`语句：

```python
n = 1
while n <= 100:
    if n > 10: # 当n = 11时，条件满足，执行break语句
        break # break语句会结束当前循环
    print(n)
    n = n + 1
print('END')
```
在循环过程中，也可以通过`continue`语句，跳过当前的这次循环，直接开始下一次循环。

```python
n = 0
while n < 10:
    n = n + 1
    print(n)
```

上面的程序可以打印出1～10。但是，如果我们想只打印奇数，可以用`continue`语句跳过某些循环：

```python
n = 0
while n < 10:
    n = n + 1
    if n % 2 == 0: # 如果n是偶数，执行continue语句
        continue # continue语句会直接继续下一轮循环，后续的print()语句不会执行
    print(n)
```

## 使用dict和set

**dict全程dictionary**，其他语言被称为map，使用键值对来进行存储，具有极高的查找速度

初始化：
```python
>>> d = {'Michael': 95, 'Bob': 75, 'Tracy': 85}
>>> d['Michael']
95
```
把数据放入dict的方法，除了初始化时指定外，还可以通过key放入：

```python
>>> d['Adam'] = 67
>>> d['Adam']
67
```
如果key不存在，dict就会报错，要避免key不存在的错误，有两种办法，一是通过`in`判断key是否存在：
   
```python
>>> 'Thomas' in d
False
```
二是通过dict提供的`get()`方法，如果key不存在，可以返回`None`，或者自己指定的value：

```python
>>> d.get('Thomas')
>>> d.get('Thomas', -1)
-1
```

要删除一个key，用`pop(key)`方法，对应的value也会从dict中删除：

```python
>>> d.pop('Bob')
75
>>> d
{'Michael': 95, 'Tracy': 85}
```

**而set是一个无序，不重复的集合**
要创建一个set，用`{x,y,z,...}`列出每个元素：

```python
>>> s = {1, 2, 3}
>>> s
{1, 2, 3}
```

或者提供一个list作为输入集合：

```python
>>> s = set([1, 2, 3])
>>> s
{1, 2, 3}
```
重复元素在set中自动被过滤

常用方法：
通过`add(key)`方法可以添加元素到set中，可以重复添加，但不会有效果
```python
>>> s.add(4)
>>> s
{1, 2, 3, 4}
>>> s.add(4)
>>> s
{1, 2, 3, 4}

```
通过`remove(key)`方法可以删除元素：
```python
>>> s.remove(4)
>>> s
{1, 2, 3}
```

## 不可变数据类型与可变数据类型

在上面讲的dict键值对集合这个数据类型中，key必须是不可变对象，因为python底层会拿这个不可变数据类型的变量来做一次hash运算，来找到key对应value的位置，所以如果这个变量是可变的，hash运算会得到不同的结果，也就指向了不同的value位置，这是不符合dict的定义的，因此，key必须为不可变对象

举例
对于可变对象，比如list，对list进行操作，list内部的内容是会变化的，比如：

```python
>>> a = ['c', 'b', 'a']
>>> a.sort()
>>> a
['a', 'b', 'c']
```
而对于不可变对象，比如str，对str进行操作呢：
```python
>>> a = 'abc'
>>> a.replace('a', 'A')
'Abc'
>>> a
'abc'
```

虽然字符串有个`replace()`方法，也确实变出了`'Abc'`，但变量`a`最后仍是`'abc'`，应该怎么理解呢？

我们先把代码改成下面这样：

```python
>>> a = 'abc'
>>> b = a.replace('a', 'A')
>>> b
'Abc'
>>> a
'abc'
```

要始终牢记的是，`a`是变量，而`'abc'`才是字符串对象！有些时候，我们经常说，对象`a`的内容是`'abc'`，但其实是指，`a`本身是一个变量，它指向的对象的内容才是`'abc'`：

```
┌───┐     ┌───────┐
│ a │────▶│ 'abc' │
└───┘     └───────┘
```

当我们调用`a.replace('a', 'A')`时，实际上调用方法`replace`是作用在字符串对象`'abc'`上的，而这个方法虽然名字叫`replace`，但却没有改变字符串`'abc'`的内容。相反，`replace`方法创建了一个新字符串`'Abc'`并返回，如果我们用变量`b`指向该新字符串，就容易理解了，变量`a`仍指向原有的字符串`'abc'`，但变量`b`却指向新字符串`'Abc'`了：

```
┌───┐     ┌───────┐
│ a │────▶│ 'abc' │
└───┘     └───────┘
┌───┐     ┌───────┐
│ b │────▶│ 'Abc' │
└───┘     └───────┘
```

所以，对于不变对象来说，调用对象自身的任意方法，也不会改变该对象自身的内容。相反，这些方法会创建新的对象并返回，这样，就保证了不可变对象本身永远是不可变的。

## 函数

**调用函数**
函数名(参数，参数。。。。)

### 定义函数
定义一个函数要使用`def`语句，依次写出函数名、括号、括号中的参数和冒号`:`，然后，在缩进块中编写函数体，函数的返回值用`return`语句返回。

我们以自定义一个求绝对值的`my_abs`函数为例：

```python
def my_abs(x):
    if x >= 0:
        return x
    else:
        return -x

print(my_abs(-99))
```

如果想定义一个什么事也不做的空函数，可以用`pass`语句：

```python
def nop():
    pass
```
`pass`语句什么都不做，那有什么用？实际上`pass`可以用来作为占位符，比如现在还没想好怎么写函数的代码，就可以先放一个`pass`，让代码能运行起来。

`pass`还可以用在其他语句里，比如：

```python
if age >= 18:
    pass
```

缺少了`pass`，代码运行就会有语法错误。

### 如果返回值有多个怎么办？
直接在return语句中每个返回值中间加逗号：
```python
import math

def move(x, y, step, angle=0):
    nx = x + step * math.cos(angle)
    ny = y - step * math.sin(angle)
    return nx, ny

```

调用这个函数，你可以同时或者返回值：
```python 
>>> x, y = move(100, 100, 60, math.pi / 6)
>>> print(x, y)
151.96152422706632 70.0

```
但其实这只是一种假象，Python函数返回的仍然是单一值：

```python
>>> r = move(100, 100, 60, math.pi / 6)
>>> print(r)
(151.96152422706632, 70.0)
```
原来返回值是一个tuple！但是，在语法上，返回一个tuple可以省略括号，而多个变量可以同时接收一个tuple，按位置赋给对应的值，所以，Python的函数返回多值其实就是返回一个tuple，但写起来更方便。


## 函数的参数

定义函数的时候，我们把参数的名字和位置确定下来，函数的接口定义就完成了。对于函数的调用者来说，只需要知道如何传递正确的参数，以及函数将返回什么样的值就够了，函数内部的复杂逻辑被封装起来，调用者无需了解。

```python
def power(x, n):
    s = 1
    while n > 0:
        n = n - 1
        s = s * x
    return s

```

`power(x, n)`函数有两个参数：`x`和`n`，这两个参数都是位置参数，调用函数时，传入的两个值按照位置顺序依次赋给参数`x`和`n`。

这里的参数n也可以直接写成n=2，即这个函数将n=2作为默认参数，当直接调用函数`power(5)`的时候，其实就是在调用`power(5,2)`

但是需要注意的是，默认参数必须为不可变对象
如果默认参数为可变对象，会发生什么？

先定义一个函数，传入一个list，添加一个`END`再返回：

```python
def add_end(L=[]):
    L.append('END')
    return L
```

当你正常调用时，结果似乎不错：

```python
>>> add_end([1, 2, 3])
[1, 2, 3, 'END']
>>> add_end(['x', 'y', 'z'])
['x', 'y', 'z', 'END']
```

当你使用默认参数调用时，一开始结果也是对的：

```python
>>> add_end()
['END']
```


但是，再次调用`add_end()`时，结果就不对了：

```python
>>> add_end()
['END', 'END']
>>> add_end()
['END', 'END', 'END']
```
很多初学者很疑惑，默认参数是`[]`，但是函数似乎每次都“记住了”上次添加了`'END'`后的list。

原因解释如下：

Python函数在定义的时候，默认参数`L`的值就被计算出来了，即`[]`，因为默认参数`L`也是一个变量，它指向对象`[]`，每次调用该函数，如果改变了`L`的内容，则下次调用时，默认参数的内容就变了，不再是函数定义时的`[]`了。

要修改上面的例子，我们可以用`None`这个不变对象来实现：

```python
def add_end(L=None):
    if L is None:
        L = []
    L.append('END')
    return L
```


现在，无论调用多少次，都不会有问题：

```python
>>> add_end()
['END']
>>> add_end()
['END']
```

### 可变参数

但传入的函数参数不固定的时候，可以用`*`来表示参数为可变参数
```python 
def calc(*numbers):
    sum = 0
    for n in numbers:
        sum = sum + n * n
    return sum


cal(1,2) #2
cal(1,2,3) #6
```

如果已经有一个list或者tuple，要调用一个可变参数怎么办？可以这样做：

```plain
>>> nums = [1, 2, 3]
>>> calc(nums[0], nums[1], nums[2])
14
```


这种写法当然是可行的，问题是太繁琐，所以Python允许你在list或tuple前面加一个`*`号，把list或tuple的元素变成可变参数传进去：

```plain
>>> nums = [1, 2, 3]
>>> calc(*nums)
14
```

`*nums`表示把`nums`这个list的所有元素作为可变参数传进去。这种写法相当有用，而且很常见。

### 关键字参数

可变参数允许你传入0个或任意个参数，这些可变参数在函数调用时自动组装为一个tuple。而关键字参数允许你传入0个或任意个含参数名的参数，这些关键字参数在函数内部自动组装为一个dict。请看示例：

```python
def person(name, age, **kw):
    print('name:', name, 'age:', age, 'other:', kw)
```

函数`person`除了必选参数`name`和`age`外，还接受关键字参数`kw`。在调用该函数时，可以只传入必选参数：

```plain
>>> person('Michael', 30)
name: Michael age: 30 other: {}
```

也可以传入任意个数的关键字参数：

```plain
>>> person('Bob', 35, city='Beijing')
name: Bob age: 35 other: {'city': 'Beijing'}
>>> person('Adam', 45, gender='M', job='Engineer')
name: Adam age: 45 other: {'gender': 'M', 'job': 'Engineer'}
```


关键字参数有什么用？它可以扩展函数的功能。比如，在`person`函数里，我们保证能接收到`name`和`age`这两个参数，但是，如果调用者愿意提供更多的参数，我们也能收到。试想你正在做一个用户注册的功能，除了用户名和年龄是必填项外，其他都是可选项，利用关键字参数来定义这个函数就能满足注册的需求。

和可变参数类似，也可以先组装出一个dict，然后，把该dict转换为关键字参数传进去：

```plain
>>> extra = {'city': 'Beijing', 'job': 'Engineer'}
>>> person('Jack', 24, city=extra['city'], job=extra['job'])
name: Jack age: 24 other: {'city': 'Beijing', 'job': 'Engineer'}
```

当然，上面复杂的调用可以用简化的写法：

```plain
>>> extra = {'city': 'Beijing', 'job': 'Engineer'}
>>> person('Jack', 24, **extra)
name: Jack age: 24 other: {'city': 'Beijing', 'job': 'Engineer'}
```



`**extra`表示把`extra`这个dict的所有key-value用关键字参数传入到函数的`**kw`参数，`kw`将获得一个dict，注意`kw`获得的dict是`extra`的一份拷贝，对`kw`的改动不会影响到函数外的`extra`。


## 递归函数

在一个函数内部可以调用其他函数，如果函数内部在调用自身，那么这个函数是递归函数

举个例子，我们来计算阶乘`n! = 1 x 2 x 3 x ... x n`，用函数`fact(n)`表示，可以看出：
fact(n)=n!=1×2×3×⋅⋅⋅×(n−1)×n=(n−1)!×n=fact(n−1)×n

所以，`fact(n)`可以表示为`n x fact(n-1)`，只有n=1时需要特殊处理。

于是，`fact(n)`用递归的方式写出来就是：

```python
def fact(n):
    if n==1:
        return 1
    return n * fact(n - 1)
```


## 类与对象

类是抽象的模板，比如Student类，而实例是根据类创建出来的一个个具体的“对象”，每个对象都拥有相同的方法，但各自的数据可能不同。

仍以Student类为例，在Python中，定义类是通过`class`关键字：

```python
class Student(object):
    pass
```


`class`后面紧接着是类名，即`Student`，类名通常是大写开头的单词，紧接着是`(object)`，表示该类是从哪个类继承下来的，继承的概念我们后面再讲，通常，如果没有合适的继承类，就使用`object`类，这是所有类最终都会继承的类。

定义好了`Student`类，就可以根据`Student`类创建出`Student`的实例，创建实例是通过类名+()实现的：

```plain
>>> bart = Student()
>>> bart
<__main__.Student object at 0x10a67a590>
>>> Student
<class '__main__.Student'>
```

可以看到，变量`bart`指向的就是一个`Student`的实例，后面的`0x10a67a590`是内存地址，每个object的地址都不一样，而`Student`本身则是一个类。


### 初始化

一个类在初始化的时候需要绑定一些特定的参数，这时候就需要初始化的构造函数了
通过定义一个特殊的`__init__`方法，在创建实例的时候，就把`name`，`score`等属性绑上去：

```python
class Student(object):
    def __init__(self, name, score):
        self.name = name
        self.score = score
```

注意到`__init__`方法的第一个参数永远是`self`，表示创建的实例本身，因此，在`__init__`方法内部，就可以把各种属性绑定到`self`，因为`self`就指向创建的实例本身。

有了`__init__`方法，在创建实例的时候，就不能传入空的参数了，必须传入与`__init__`方法匹配的参数，但`self`不需要传，Python解释器自己会把实例变量传进去：

```plain
>>> bart = Student('Bart Simpson', 59)
>>> bart.name
'Bart Simpson'
>>> bart.score
59
```


和普通的函数相比，在类中定义的函数只有一点不同，就是第一个参数永远是实例变量`self`，并且，调用时，不用传递该参数。除此之外，类的方法和普通函数没有什么区别，所以，你仍然可以用默认参数、可变参数、关键字参数和命名关键字参数。


### 数据封装

面向对象编程的一个重要特点就是数据封装。在上面的`Student`类中，每个实例就拥有各自的`name`和`score`这些数据。我们可以通过函数来访问这些数据，比如打印一个学生的成绩：

```python
>>> def print_score(std):
...     print('%s: %s' % (std.name, std.score))
...
>>> print_score(bart)
Bart Simpson: 59
```

但是，既然`Student`实例本身就拥有这些数据，要访问这些数据，就没有必要从外面的函数去访问，可以直接在`Student`类的内部定义访问数据的函数，这样，就把“数据”给封装起来了。这些封装数据的函数是和`Student`类本身是关联起来的，我们称之为类的方法：

```python
class Student(object):
    def __init__(self, name, score):
        self.name = name
        self.score = score

    def print_score(self):
        print('%s: %s' % (self.name, self.score))
```

要定义一个方法，除了第一个参数是`self`外，其他和普通函数一样。要调用一个方法，只需要在实例变量上直接调用，除了`self`不用传递，其他参数正常传入：

```plain
>>> bart.print_score()
Bart Simpson: 59
```

这样一来，我们从外部看`Student`类，就只需要知道，创建实例需要给出`name`和`score`，而如何打印，都是在`Student`类的内部定义的，这些数据和逻辑被“封装”起来了，调用很容易，但却不用知道内部实现的细节。


**为什么需要数据封装**

数据封装对于这里类的含义为：
将数据（属性）和操作这些数据的方法（函数）捆绑成一个独立的单元（即类），并对外部隐藏该单元的内部实现细节

例如：
```python
class BankAccount:
       def __init__(self, initial_balance):
           # 将余额设为私有属性，以防止外部直接访问和修改
           self._balance = initial_balance
   
       def get_balance(self):             
              """提供一个获取余额的公共方法"""
           return self._balance
   
       def deposit(self, amount):
           """存款方法：包含验证逻辑"""
           if amount > 0:
               self._balance += amount
               print(f"成功存入 {amount} 元。")
           else:
               print("存款金额必须大于0。")
   
       def withdraw(self, amount):
           """取款方法：包含验证逻辑"""
           if 0 < amount <= self._balance:
               self._balance -= amount
               print(f"成功取出 {amount} 元。")
           else:
               print("取款金额无效或余额不足。")
   
   # 创建一个账户实例
   my_account = BankAccount(100)
   
   print(f"初始余额: {my_account.get_balance()}")
   
   # 尝试正常操作 (必须通过方法)
   my_account.deposit(50)
   print(f"存款后余额: {my_account.get_balance()}")
   
   my_account.withdraw(20)
   print(f"取款后余额: {my_account.get_balance()}")
   
   # 尝试恶意或错误的直接操作 (会被方法阻止)
   my_account.withdraw(200)  # 余额不足，会被方法内的逻辑阻止
   my_account.deposit(-100)   # 存款金额无效，会被方法内的逻辑阻止
   
   # 尝试直接访问私有属性 (会报错或发出警告)
   # my_account._balance = -500  # 尽管在 Python 中技术上可行，但不推荐，也不符合封装原则。
```



这个例子充分展示了数据封装的以下核心价值：

1. **保证数据完整性：** 这是最重要的原因。通过 `deposit()` 和 `withdraw()` 方法，我们可以在修改数据前进行验证，确保 `_balance` 永远不会是负数，从而防止数据进入不合理的状态。
    
2. **提供清晰的接口：** `deposit()` 和 `withdraw()` 构成了 `BankAccount` 类的**公共接口**，明确告诉使用者如何安全、正确地与账户交互。使用者无需关心内部的 `_balance` 属性，只需调用这些方法即可。
    
3. **隐藏实现细节：** 如果未来我们决定改变账户余额的计算方式（例如，从一个单一变量变为记录每一笔交易的列表），我们只需要修改 `get_balance()`、`deposit()` 和 `withdraw()` 方法的内部实现，而**外部调用这些方法的代码完全不需要改变**。这使得代码更容易维护和迭代。




### 私有变量与get set方法

如果要让内部属性不被外部访问，可以把属性的名称前加上两个下划线`__`，在Python中，实例的变量名如果以`__`开头，就变成了一个私有变量（private），只有内部可以访问，外部不能访问，所以，我们把Student类改一改：

```python
class Student(object):
    def __init__(self, name, score):
        self.__name = name
        self.__score = score

    def print_score(self):
        print('%s: %s' % (self.__name, self.__score))
```

改完后，对于外部代码来说，没什么变动，但是已经无法从外部访问`实例变量.__name`和`实例变量.__score`了：

```plain
>>> bart = Student('Bart Simpson', 59)
>>> bart.__name
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AttributeError: 'Student' object has no attribute '__name'
```


这样就确保了外部代码不能随意修改对象内部的状态，这样通过访问限制的保护，代码更加健壮。

但是如果外部代码要获取name和score怎么办？可以给Student类增加`get_name`和`get_score`这样的方法：

```python
class Student(object):
    ...

    def get_name(self):
        return self.__name

    def get_score(self):
        return self.__score
```

如果又要允许外部代码修改score怎么办？可以再给Student类增加`set_score`方法：

```python
class Student(object):
    ...

    def set_score(self, score):
        self.__score = score
```

### 继承

继承的核心作用是**代码重用**和**建立类之间的逻辑关系**。

想象一下，我们要为各种动物编写程序。所有的动物都有一些共同的行为，比如“吃东西”和“睡觉”。

**如果不使用继承**，我们可能需要为每一种动物都重复编写这些代码：

```python 
class Dog:
    def eat(self):
        print("狗正在吃东西...")
    def sleep(self):
        print("狗正在睡觉...")
    def bark(self):
        print("汪汪汪！")

class Cat:
    def eat(self):
        print("猫正在吃东西...")
    def sleep(self):
        print("猫正在睡觉...")
    def meow(self):
        print("喵喵喵！")
```

可以看到，`eat()` 和 `sleep()` 方法被重复编写了，这不仅浪费精力，而且如果以后需要修改“吃东西”的逻辑，我们必须修改所有动物类。

**使用继承**，我们可以创建一个通用的 **父类 (Parent Class)** `Animal`，把所有动物的共同行为放在里面。然后，让 `Dog` 和 `Cat` **继承 (Inherit)** 这个父类


```python 
class Animal:
    def eat(self):
        print("动物正在吃东西...")
    def sleep(self):
        print("动物正在睡觉...")

class Dog(Animal):  # Dog 继承 Animal
    def bark(self):
        print("汪汪汪！")

class Cat(Animal):  # Cat 继承 Animal
    def meow(self):
        print("喵喵喵！")

# 实例化对象
my_dog = Dog()
my_cat = Cat()

# 调用继承来的方法
my_dog.eat()  # 输出: 动物正在吃东西...
my_cat.sleep() # 输出: 动物正在睡觉...

# 调用自身独有的方法
my_dog.bark()  # 输出: 汪汪汪！
```

**继承的重要性：**

- **代码重用**：`eat()` 和 `sleep()` 方法只需编写一次，所有子类都自动拥有。
    
- **代码维护性**：如果需要修改“吃东西”的逻辑，只需要修改 `Animal` 父类中的 `eat()` 方法，所有继承它的子类都会自动更新。
    
- **建立逻辑关系**：它清晰地表达了“**is-a**”关系（一只狗**是**一种动物），让程序结构更合理、更易于理解。


### 多态

**多态**的核心作用是**简化接口**，让不同的对象可以对同一个方法调用做出不同的响应。多态让代码变得更加通用和灵活。

我们接着上面的例子。所有动物都会发出声音，但发出的声音各不相同。我们可以给每个动物类添加一个 `make_sound()` 方法。

```Python
# 延续上面的例子
class Animal:
    def eat(self):
        print("动物正在吃东西...")
    def make_sound(self):
        # 通用方法，留待子类具体实现
        pass

class Dog(Animal):
    def make_sound(self):  # 重写 make_sound() 方法
        print("汪汪汪！")

class Cat(Animal):
    def make_sound(self):  # 重写 make_sound() 方法
        print("喵喵喵！")

class Cow(Animal):
    def make_sound(self):
        print("哞哞哞！")

# 创建不同类型的动物对象
dog = Dog()
cat = Cat()
cow = Cow()

# 将所有动物放入一个列表中
zoo = [dog, cat, cow]

# 遍历列表，对每个动物调用同一个方法
for animal in zoo:
    animal.make_sound()
```

**运行结果：**

```
汪汪汪！
喵喵喵！
哞哞哞！
```

**多态的重要性：**

- **简化编程接口**：我们通过一个统一的接口 `make_sound()` 来调用不同动物的叫声，而**不需要**使用 `if/elif/else` 语句来判断对象的具体类型。我们的代码更简洁，也更容易理解。
    
- **提高代码扩展性**：如果以后你新增一个 `Cow`（牛）类，只要它继承了 `Animal` 并实现了 `make_sound()` 方法，你上面的 `for` 循环代码**无需做任何修改**，就能自动支持新的动物类型。这大大提高了程序的灵活性和可扩展性。

**总结来说**，**继承**帮助我们**复用**代码，建立类之间的逻辑关系；而**多态**则利用这种关系，让代码**更加通用和灵活**，从而简化接口并提高扩展性。





# 练习题
## **第一章：Python基础与数据类型**

**主要知识点：** 基本数据类型、变量、打印与格式化、`list`、`tuple`、`dict`、`set`，以及可变与不可变对象的概念。

### **练习题**

**1. （简单）自我介绍** 编写一个程序，要求用户输入你的名字、年龄、家乡以及一个你最喜欢的数字。然后，使用 **f-string 格式化**将这些信息组合成一个句子并打印出来。

**示例输出：**

```
你好，我叫[你的名字]，今年[你的年龄]岁，来自[你的家乡]，我最喜欢的数字是[你最喜欢的数字]。
```

**2. （中等）班级成绩统计** 假设有一个学生成绩列表和一本成绩字典，请完成以下任务：

- 给定一个列表 `scores = [88, 92, 75, 60, 95]`。
- 另给定一个字典 `student_grades = {'Alice': 88, 'Bob': 92, 'Charlie': 75, 'David': 60, 'Eve': 95}`。
- **任务1：** 使用 `list` 的方法向列表中添加一个新成绩 `98`。
- **任务2：** 计算列表中所有成绩的平均值，并使用 **f-string** 格式化打印结果，保留两位小数。
- **任务3：** 检查字典中是否存在名为 `Bob` 的学生。如果存在，打印出他的成绩；否则，打印“找不到该学生”。
    

**3. （挑战）字符串字符计数器** 编写一个程序，接受一个字符串作为输入。程序需要统计字符串中每个字符出现的次数，并以字典的形式返回结果。字典的键是字符，值是该字符出现的次数。

**示例：** 输入: `hello python` 输出: `{'h': 1, 'e': 1, 'l': 2, 'o': 2, ' ': 1, 'p': 1, 'y': 1, 't': 1, 'n': 1}`

---

## **第二章：流程控制与循环**

**主要知识点：** `if...elif...else` 条件判断、`match` 语句、`for` 循环、`while` 循环、`break` 和 `continue`。

### **练习题**

**1. （简单）数字范围判断** 编写一个程序，接受一个整数输入。如果该数字大于 `100`，打印“太大”；如果小于 `0`，打印“太小”；如果介于 `0` 和 `100` 之间（包括0和100），打印“刚刚好”。

**2. （中等）偶数求和** 编写一个程序，使用 `while` 循环计算 `1` 到 `100` 之间所有偶数的和。在循环中使用 **`continue`** 语句跳过所有奇数。

**3. （挑战）FizzBuzz游戏** 这是一个经典的编程面试题。编写一个程序，循环打印 `1` 到 `100` 的数字。但有以下规则：

- 如果数字是 `3` 的倍数，打印 `Fizz`。
- 如果数字是 `5` 的倍数，打印 `Buzz`。
- 如果数字同时是 `3` 和 `5` 的倍数，打印 `FizzBuzz`。
- 否则，打印数字本身。
    

**提示：** 你可以使用 `for` 循环和 **`if...elif...else`** 语句来解决此问题。

---

## **第三章：函数进阶与递归**

**主要知识点：** 函数定义、返回值、默认参数、可变参数（`*args`）、关键字参数（`**kwargs``）、递归函数。

### **练习题**

**1. （简单）计算器函数** 编写一个名为 `calculate` 的函数，它接受两个数字作为参数，并返回它们的和与积。在函数外部接收这两个返回值，并分别打印出来。

**2. （中等）灵活的平均分计算器** 编写一个名为 `average_score` 的函数。该函数应该接受以下参数：

- 一个 **必选参数** `name`，代表学生姓名。
- 一个 **可变参数** `*scores`，代表该学生的所有科目成绩。 函数需要计算这些成绩的平均值，并返回一个包含学生姓名和平均分的元组。
    

**示例调用：** `average_score('小明', 90, 85, 95)` `average_score('小红', 100, 98)`

**3. （挑战）递归求幂** 编写一个名为 `power` 的**递归函数**，用于计算 `x` 的 `n` 次方。

- **提示：** 递归基准是 `n=0` 时，`x^0=1`。递归步骤是 `x^n = x * x^(n-1)`。不要使用 `**` 运算符或 `math.pow()` 函数。
    

---

## **第四章：类与面向对象编程**

**主要知识点：** 类与对象、`__init__` 初始化方法、数据封装、私有变量、`get` 和 `set` 方法。

### **练习题**

**1. （简单）矩形类** 定义一个 `Rectangle` 类。在 `__init__` 方法中，接收 `width`（宽）和 `height`（高）作为参数，并将其存储为类的属性。然后，定义一个名为 `get_area` 的方法，用于计算并返回矩形的面积。 

**2. （中等）学生信息管理** 定义一个 `Student` 类，用于表示学生信息。

- **任务1：** 在 `__init__` 方法中，将学生的姓名 `name` 和年龄 `age` 定义为 **私有变量**（`__name` 和 `__age`）。
- **任务2：** 为 `name` 和 `age` 属性添加 **`get_name()`**、**`get_age()`**、**`set_name()`** 和 **`set_age()`** 方法，以便在类外部安全地访问和修改这些私有属性。
    

**3. （挑战）银行账户** 定义一个 `Account` 类，用于模拟一个简单的银行账户。

- **任务1：** 在 `__init__` 方法中，将账户余额 `__balance` 初始化为 `0`，并设置为 **私有变量**。
- **任务2：** 定义一个 `deposit(amount)` 方法，用于向账户存入资金。
- **任务3：** 定义一个 `withdraw(amount)` 方法，用于从账户取款。在取款时，你需要检查取款金额是否小于或等于当前余额。如果余额不足，打印错误消息；否则，执行取款操作。
- **任务4：** 定义一个 `get_balance()` 方法，用于获取当前账户余额。

**4 . （中等）** 动物与狗——继承

- **任务1：** 定义一个名为 `Animal` 的父类。在 `__init__` 方法中，接收 `name` 参数并将其存储为属性。然后，定义一个名为 `eat` 的方法，打印出通用的信息，例如 `f"{self.name} 正在吃东西..."`。

- **任务2：** 定义一个名为 `Dog` 的子类，使其**继承**自 `Animal`。在 `Dog` 类中，定义一个独有的 `bark` 方法，打印 `f"{self.name} 在汪汪叫！"`。

- **任务3：** 创建 `Dog` 类的实例，并调用其继承自 `Animal` 的 `eat` 方法，以及其独有的 `bark` 方法。

5. **（挑战）** 车辆启动——多态

- **任务1：** 定义一个名为 `Vehicle` 的父类，其中包含一个名为 `start_engine` 的方法，打印一条通用信息，例如 `"车辆引擎启动了..."`。

- **任务2：** 定义两个子类 `Car` 和 `Motorcycle`，都继承自 `Vehicle`。分别**重写** `start_engine` 方法，使其打印各自特定的启动信息（例如：`"汽车引擎启动..."` 和 `"摩托车引擎启动..."`）。

- **任务3：** 定义一个**多态函数** `start_all_vehicles`，该函数接收一个车辆对象列表作为参数。函数内部遍历列表，并对列表中的每个车辆对象调用 `start_engine` 方法。

- **任务4：** 创建 `Car` 和 `Motorcycle` 的实例，并将它们放入一个列表中。然后调用 `start_all_vehicles` 函数，传入这个列表。观察程序如何根据对象类型自动调用正确的方法

## **综合练习**

### **训练一：简易图书管理系统**

场景描述：

你被分配到一个小型社区图书馆，任务是开发一个基础的图书管理程序。这个程序需要能够处理图书的增、删、查、借、还等基本操作。

**核心要求：**

6. **数据结构：** 使用一个 **`list`** 来存储所有图书的名字，同时使用一个 **`dict`** 来存储每本图书的详细信息（例如：`{'书名': {'作者': '...', '状态': '在馆'}}`）。
    
7. **主程序流程：**
    
    - 使用一个 **`while` 循环** 创建一个持续运行的菜单系统。
    - 菜单应提供以下选项：`1. 借书`、`2. 还书`、`3. 查询图书`、`4. 添加新书`、`5. 退出系统`。
    - 使用 **`input()`** 获取用户的选择，并用 **`if...elif...else`** 语句处理不同的用户操作。
        
8. **功能函数：**
    
    - 编写一个名为 `borrow_book(book_name)` 的函数，如果图书在馆，将其状态改为“已借出”，否则打印“图书已被借出或不存在”。
    - 编写一个名为 `return_book(book_name)` 的函数，如果图书已被借出，将其状态改为“在馆”，否则打印“图书状态有误”。
    - 编写一个名为 `add_book(book_name, author)` 的函数，将新书信息添加到数据结构中。
        
9. **额外要求：**
    
    - 在主循环中，每次完成一个操作后，打印出所有图书的当前状态，以便用户总能看到最新的信息。
    - 考虑用户可能输入不存在的图书名，在函数中进行处理，打印友好的提示信息。
        

---

### **训练二：在线购物模拟器**

场景描述：

你需要为一家在线商店开发一个购物车系统。用户可以添加商品，查看购物车内容，计算总价，并使用折扣码。这个系统将是面向对象编程（OOP）的完美实践。

**核心要求：**

10. **OOP核心：** 定义一个名为 **`ShoppingCart` 的类**。
    - 在 `__init__` 方法中，将一个 **私有字典** `__items` 作为实例属性，用于存储购物车中的商品。
    - 定义以下方法：
        - `add_item(item_name, price, quantity)`: 向购物车添加商品。如果商品已存在，则只增加数量。
        - `remove_item(item_name)`: 从购物车中移除某个商品。
        - `view_cart()`: 打印出购物车中所有商品及其数量和价格。
        - `calculate_total()`: 计算并返回购物车中所有商品的总价。

11. **主程序流程：**
    
    - 使用 **`while` 循环** 构建一个交互式菜单，让用户可以：`1. 添加商品`、`2. 移除商品`、`3. 查看购物车`、`4. 计算总价`、`5. 退出`。
    - 根据用户的输入，调用 `ShoppingCart` 实例对应的类方法。
        
12. **函数进阶：**
    
    - 定义一个独立的函数 `apply_discount(total, discount_code)`。
    - 这个函数接受总价和折扣码作为参数。使用 **`if...elif...else`** 语句来判断折扣码：
        - 如果折扣码是 `SAVE10`，返回 `total * 0.9`。
        - 如果折扣码是 `SAVE20`，返回 `total * 0.8`。
        - 如果折扣码无效，返回原始 `total` 并打印提示。
    - 在 `calculate_total` 方法执行后，询问用户是否使用折扣码，并调用此函数来计算最终价格。
        

---


# 练习答案
## 第一章答案

### **练习题1：自我介绍**

这个练习的重点是让你熟悉如何从用户那里获取输入，并使用 **f-string** 进行字符串格式化。f-string 是一种非常现代且方便的格式化方式。


```Python
# 获取用户输入
name = input("请输入你的名字：")
age = input("请输入你的年龄：")
hometown = input("请输入你的家乡：")
fav_number = input("请输入你最喜欢的数字：")

# 使用 f-string 格式化并打印输出
# f-string 会自动将花括号 {} 中的变量替换为它们的值
print(f"你好，我叫{name}，今年{age}岁，来自{hometown}，我最喜欢的数字是{fav_number}。")
```

### **练习题2：班级成绩统计**

这个练习帮助你实践 **list** 和 **dict** 的基本操作，包括如何添加元素、计算总和与平均值，以及在字典中查找元素。



```Python
# 1. 班级成绩统计

scores = [88, 92, 75, 60, 95]
student_grades = {'Alice': 88, 'Bob': 92, 'Charlie': 75, 'David': 60, 'Eve': 95}

# 任务1：向列表中添加一个新成绩
scores.append(98)
print(f"新成绩列表: {scores}")

# 任务2：计算平均值并格式化打印
total_score = sum(scores)  # 使用 sum() 函数计算总和
num_students = len(scores) # 使用 len() 函数获取元素个数
average = total_score / num_students
print(f"所有成绩的平均值为: {average:.2f}") # .2f 表示保留两位小数

# 任务3：在字典中查找学生
student_name = 'Bob'
if student_name in student_grades:
    print(f"{student_name} 的成绩是: {student_grades[student_name]}")
else:
    print(f"找不到学生 {student_name}。")
```

### **练习题3：字符串字符计数器**

这道题让你将字符串与 **dict** 结合起来解决实际问题。它的核心思想是：遍历字符串中的每个字符，然后用一个字典来记录每个字符出现的次数。


```Python
# 3. 字符串字符计数器

def count_characters(text):
    """
    统计字符串中每个字符出现的次数。
    """
    char_counts = {}  # 创建一个空字典来存储计数
    for char in text:
        if char in char_counts:
            # 如果字符已经在字典中，就将它的值加1
            char_counts[char] += 1
        else:
            # 如果是第一次出现，就将它作为新键，并设值为1
            char_counts[char] = 1
    return char_counts

# 测试函数
input_string = "hello python"
result = count_characters(input_string)
print(result)
```

---

## 第二章答案

### **练习题1：数字范围判断**

这道题考察你对 **`if...elif...else`** 语句的掌握。重要的是要理解 `if` 语句是从上到下依次判断的，一旦某个条件满足，后面的分支就会被忽略。



```Python
# 1. 数字范围判断

number = int(input("请输入一个整数："))

if number > 100:
    print("太大")
elif number < 0:
    print("太小")
else:
    # 这个分支会在 number >= 0 and number <= 100 的时候执行
    print("刚刚好")
```

### **练习题2：偶数求和**

这道题让你练习 **`while`** 循环以及 **`continue`** 语句。`continue` 会让程序跳过当前循环的剩余部分，直接开始下一次循环，这在处理特定条件时非常有用。



```Python
# 2. 偶数求和

total = 0
n = 1

while n <= 100:
    if n % 2 != 0:  # 如果 n 是奇数
        n += 1      # 别忘了递增 n，否则会陷入死循环
        continue    # 跳过当前循环，直接进入下一次
    
    # 如果 n 是偶数，才会执行到这里
    total += n
    n += 1

print(f"1到100之间所有偶数的和是: {total}")
```

### **练习题3：FizzBuzz游戏**

这是一道非常经典的练习题，它综合考察了 **`for`** 循环和 **`if...elif...else`** 的逻辑。需要注意的是，判断 `3` 和 `5` 的倍数的条件 **`if (i % 3 == 0) and (i % 5 == 0)`** 必须放在最前面，否则程序将永远无法进入这个分支。


```Python
# 3. FizzBuzz游戏

for i in range(1, 101):  # range(1, 101) 生成 1 到 100 的数字
    if (i % 3 == 0) and (i % 5 == 0):
        # 必须先判断 3 和 5 的倍数
        print("FizzBuzz")
    elif i % 3 == 0:
        print("Fizz")
    elif i % 5 == 0:
        print("Buzz")
    else:
        print(i)
```

---

## 第三章答案

### **练习题1：计算器函数**

这个练习旨在让你掌握函数的基本定义和返回值。Python 的函数可以返回多个值，但实际上，它会将这些值封装成一个 **`tuple`**（元组）返回。



```Python
# 1. 计算器函数

def calculate(num1, num2):
    """
    接收两个数字，并返回它们的和与积。
    """
    sum_result = num1 + num2
    product_result = num1 * num2
    return sum_result, product_result

# 调用函数并接收返回值
sum_res, product_res = calculate(10, 5)
print(f"两个数的和是: {sum_res}")
print(f"两个数的积是: {product_res}")
```

### **练习题2：灵活的平均分计算器**

这道题考察你对 **可变参数（`*args`）** 的理解。`*scores` 会将所有传入的多余参数收集到一个 **`tuple`** 中，让你能对它们进行统一处理，这在参数个数不确定的情况下非常有用。



```Python
# 2. 灵活的平均分计算器

def average_score(name, *scores):
    """
    计算学生的平均分。
    name: 学生姓名
    *scores: 科目成绩（可变参数）
    """
    if not scores:  # 如果没有传入成绩，返回0
        return name, 0
    
    total_score = sum(scores)
    average = total_score / len(scores)
    
    return name, average

# 示例调用
student_name, avg_score = average_score('小明', 90, 85, 95)
print(f"学生 {student_name} 的平均分是: {avg_score:.2f}")

student_name, avg_score = average_score('小红', 100, 98)
print(f"学生 {student_name} 的平均分是: {avg_score:.2f}")

student_name, avg_score = average_score('小李')
print(f"学生 {student_name} 没有成绩，平均分是: {avg_score:.2f}")
```

### **练习题3：递归求幂**

这道题让你掌握 **递归函数** 的核心思想。递归的关键在于定义一个明确的 **基准情况（base case）** 和一个能够向基准情况靠近的 **递归步骤（recursive step）**。



```Python
# 3. 递归求幂

def power(x, n):
    """
    使用递归计算 x 的 n 次方。
    """
    # 递归基准情况：当 n 为 0 时，任何数的 0 次方都是 1
    if n == 0:
        return 1
    
    # 递归步骤：x^n = x * x^(n-1)
    return x * power(x, n - 1)

# 测试函数
print(f"2 的 3 次方是: {power(2, 3)}")
print(f"5 的 0 次方是: {power(5, 0)}")
print(f"4 的 4 次方是: {power(4, 4)}")
```

---

## 第四章答案

### **练习题1：矩形类**

这是面向对象编程最基础的练习。类（`class`）就像一个蓝图，`__init__` 方法则是建造房子的第一步，用于初始化它的基本属性。`self` 则代表正在被创建的那个具体实例。



```Python
# 1. 矩形类

class Rectangle:
    def __init__(self, width, height):
        # 初始化实例的 width 和 height 属性
        self.width = width
        self.height = height

    def get_area(self):
        # 计算并返回矩形面积
        return self.width * self.height

# 创建一个 Rectangle 实例（对象）
my_rectangle = Rectangle(10, 5)

# 调用实例的方法
area = my_rectangle.get_area()
print(f"这个矩形的面积是: {area}")
```

### **练习题2：学生信息管理**

这道题介绍了 **私有变量** 的概念，它通过在变量前加 `__` 来实现，从而避免外部代码随意修改。通常，我们会通过 **`get` 和 `set` 方法** 来提供一个受控的访问接口，这是一种良好的封装实践。



```Python
# 2. 学生信息管理

class Student:
    def __init__(self, name, age):
        # 定义私有变量，只能在类内部访问
        self.__name = name
        self.__age = age

    # getter 方法：获取私有变量的值
    def get_name(self):
        return self.__name

    def get_age(self):
        return self.__age

    # setter 方法：设置私有变量的值，可以加入验证逻辑
    def set_name(self, name):
        if isinstance(name, str) and len(name) > 0:
            self.__name = name
        else:
            print("错误：姓名必须是非空字符串。")

    def set_age(self, age):
        if isinstance(age, int) and age > 0:
            self.__age = age
        else:
            print("错误：年龄必须是正整数。")

# 创建学生实例
student1 = Student("张三", 18)
print(f"学生姓名: {student1.get_name()}, 年龄: {student1.get_age()}")

# 尝试通过 setter 方法修改值
student1.set_age(19)
print(f"修改后年龄: {student1.get_age()}")
student1.set_age(-5) # 尝试传入无效值，会被阻止
```

### **练习题3：银行账户**

这道题是面向对象编程 **数据封装** 的一个非常实用的例子。通过将 `__balance` 设为私有变量，并只提供 `deposit`（存钱）和 `withdraw`（取钱）两个公共方法，我们确保了账户余额只能通过我们设定的规则（例如取钱时检查余额）进行操作，大大提高了代码的健壮性。



```Python
# 3. 银行账户

class Account:
    def __init__(self):
        # 账户余额设为私有变量，初始化为0
        self.__balance = 0

    def deposit(self, amount):
        """存钱方法"""
        if amount > 0:
            self.__balance += amount
            print(f"存入成功。当前余额: {self.__balance}")
        else:
            print("存款金额必须大于0。")

    def withdraw(self, amount):
        """取钱方法，包含余额检查"""
        if amount > 0 and self.__balance >= amount:
            self.__balance -= amount
            print(f"取款成功。当前余额: {self.__balance}")
        elif amount <= 0:
            print("取款金额必须大于0。")
        else:
            print("余额不足。")

    def get_balance(self):
        """获取余额方法"""
        return self.__balance

# 创建一个账户实例
my_account = Account()
print(f"账户初始余额: {my_account.get_balance()}")

# 进行操作
my_account.deposit(1000)
my_account.withdraw(500)
my_account.withdraw(600)  # 尝试取款，余额不足
```

### 练习四：继承

```python
class Animal:
    def __init__(self, name):
        # 任务1：定义父类Animal
        self.name = name

    def eat(self):
        # 通用的“吃”方法，子类可以直接继承
        print(f"{self.name} 正在吃东西...")

class Dog(Animal):
    def __init__(self, name):
        # 任务2：Dog 继承自 Animal
        # 调用父类的__init__方法来初始化 name 属性
        super().__init__(name)
    
    def bark(self):
        # Dog 独有的“叫”方法
        print(f"{self.name} 在汪汪叫！")

# 任务3：创建并调用
my_dog = Dog("旺财")

# 调用从 Animal 父类继承来的方法
my_dog.eat()

# 调用 Dog 子类独有的方法
my_dog.bark()
```

### 练习五：多态

```python
class Vehicle:
    # 任务1：定义父类 Vehicle
    def start_engine(self):
        print("车辆引擎启动了...")

class Car(Vehicle):
    # 任务2：Car 子类重写 start_engine 方法
    def start_engine(self):
        print("汽车引擎启动...")

class Motorcycle(Vehicle):
    # 任务2：Motorcycle 子类重写 start_engine 方法
    def start_engine(self):
        print("摩托车引擎启动...")

# 任务3：多态函数
def start_all_vehicles(vehicles):
    """
    接收一个车辆对象列表，并启动每辆车的引擎。
    这个函数不需要知道每辆车的具体类型。
    """
    for vehicle in vehicles:
        vehicle.start_engine() # 同一个方法调用，不同对象做出不同响应

# 任务4：创建并调用
my_car = Car()
my_motorcycle = Motorcycle()

# 将不同类型的对象放入同一个列表
fleet = [my_car, my_motorcycle]

# 调用多态函数，传入列表
print("--- 启动车队 ---")
start_all_vehicles(fleet)
```

## 综合训练答案

### 训练一
```python
# 存储所有图书信息的列表，每个元素都是一个字典
books = [
    {'title': 'Python编程入门', 'author': '小明', 'status': '在馆'},
    {'title': '数据结构基础', 'author': '小红', 'status': '在馆'},
    {'title': '人工智能原理', 'author': '老王', 'status': '已借出'}
]

def display_books():
    """打印出所有图书的当前状态"""
    print("\n--- 图书馆藏列表 ---")
    for book in books:
        print(f"书名：《{book['title']}》，作者：{book['author']}，状态：{book['status']}")
    print("-------------------\n")

def find_book(title):
    """根据书名查找图书，如果找到则返回图书字典，否则返回None"""
    for book in books:
        if book['title'] == title:
            return book
    return None

def borrow_book(title):
    """借书功能"""
    book = find_book(title)
    if book:
        if book['status'] == '在馆':
            book['status'] = '已借出'
            print(f"《{title}》借阅成功！")
        else:
            print(f"《{title}》已被借出。")
    else:
        print(f"图书馆中没有找到《{title}》这本书。")

def return_book(title):
    """还书功能"""
    book = find_book(title)
    if book:
        if book['status'] == '已借出':
            book['status'] = '在馆'
            print(f"《{title}》归还成功！")
        else:
            print(f"《{title}》的状态有误，无法归还。")
    else:
        print(f"图书馆中没有找到《{title}》这本书。")

def add_new_book(title, author):
    """添加新书功能"""
    if find_book(title):
        print(f"《{title}》这本书已存在，无法重复添加。")
    else:
        new_book = {'title': title, 'author': author, 'status': '在馆'}
        books.append(new_book)
        print(f"成功添加新书：《{title}》")

def main():
    """主程序入口"""
    while True:
        print("请选择操作：")
        print("1. 借书")
        print("2. 还书")
        print("3. 查询图书")
        print("4. 添加新书")
        print("5. 退出系统")

        choice = input("请输入你的选择 (1-5)：")

        if choice == '1':
            title = input("请输入要借阅的书名：")
            borrow_book(title)
        elif choice == '2':
            title = input("请输入要归还的书名：")
            return_book(title)
        elif choice == '3':
            title = input("请输入要查询的书名：")
            book = find_book(title)
            if book:
                print(f"查询结果：书名：《{book['title']}》，作者：{book['author']}，状态：{book['status']}")
            else:
                print(f"没有找到《{title}》这本书。")
        elif choice == '4':
            title = input("请输入新书名：")
            author = input("请输入作者：")
            add_new_book(title, author)
        elif choice == '5':
            print("感谢使用，再见！")
            break
        else:
            print("无效的选择，请重新输入。")
        
        display_books()

# 运行主程序
if __name__ == '__main__':
    main()
```

### 训练二

```python 
# 导入 math 模块以在需要时使用，例如进行数学运算，但此题中未直接使用
import math

class ShoppingCart:
    """代表一个在线购物车的类"""
    def __init__(self):
        # 私有属性，存储购物车中的商品，键为商品名，值为包含价格和数量的字典
        self.__items = {}

    def add_item(self, item_name, price, quantity=1):
        """向购物车添加商品"""
        if item_name in self.__items:
            # 如果商品已存在，则只增加数量
            self.__items[item_name]['quantity'] += quantity
            print(f"已增加 {quantity} 件 {item_name} 到购物车。")
        else:
            # 如果是新商品，则创建新的条目
            self.__items[item_name] = {'price': price, 'quantity': quantity}
            print(f"{item_name} 已添加到购物车。")

    def remove_item(self, item_name):
        """从购物车中移除商品"""
        if item_name in self.__items:
            del self.__items[item_name]
            print(f"{item_name} 已从购物车中移除。")
        else:
            print(f"购物车中没有找到 {item_name}。")

    def view_cart(self):
        """打印购物车中的所有商品"""
        if not self.__items:
            print("\n购物车为空。")
            return

        print("\n--- 你的购物车 ---")
        for item, details in self.__items.items():
            print(f"商品：{item}，单价：{details['price']:.2f}，数量：{details['quantity']}")
        print("--------------------\n")

    def calculate_total(self):
        """计算购物车中所有商品的总价"""
        total = 0
        for item, details in self.__items.items():
            total += details['price'] * details['quantity']
        return total

def apply_discount(total, discount_code):
    """根据折扣码计算最终价格"""
    if discount_code == 'SAVE10':
        print("折扣码 'SAVE10' 生效！")
        return total * 0.9
    elif discount_code == 'SAVE20':
        print("折扣码 'SAVE20' 生效！")
        return total * 0.8
    else:
        print("折扣码无效或未使用。")
        return total

def main():
    """主程序入口"""
    my_cart = ShoppingCart()
    
    while True:
        print("请选择操作：")
        print("1. 添加商品")
        print("2. 移除商品")
        print("3. 查看购物车")
        print("4. 计算总价")
        print("5. 退出")
        choice = input("请输入你的选择 (1-5)：")

        if choice == '1':
            item = input("商品名称：")
            try:
                price = float(input("单价："))
                quantity = int(input("数量："))
                my_cart.add_item(item, price, quantity)
            except ValueError:
                print("无效的输入，请确保单价和数量是数字。")
        elif choice == '2':
            item = input("要移除的商品名称：")
            my_cart.remove_item(item)
        elif choice == '3':
            my_cart.view_cart()
        elif choice == '4':
            total = my_cart.calculate_total()
            print(f"总价为: {total:.2f}")
            discount_code = input("如果有折扣码，请输入：")
            final_total = apply_discount(total, discount_code)
            print(f"最终价格为: {final_total:.2f}")
        elif choice == '5':
            print("谢谢惠顾，再见！")
            break
        else:
            print("无效的选择，请重新输入。")

# 运行主程序
if __name__ == '__main__':
    main()
```
