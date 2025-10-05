---
tags:
  - '#pernamant'
---
## 显式转换

### 转为Boolean

false有 false,0,"", null , undefinded, NaN
true 除了上面的值，其他都转为true，包括[],{} 和空函数

### 转为String

数字直接转为字符串形式的数字
boolean直接转为“true“或者”false“
null和undefined都会被转为对应的字符串
数组会用逗号，将各元素连接起来，转为一个字符串，例如：[1,2,3] -> "1,2,3"
对象默认情况下，转为”[object,Object]"


### 转为Number

字符串：
	只包含数字会被直接转化为对应的Number
	空字符或者只包含空格的字符串会被转化为0
	包含任何一个非数字的字符会被转为NaN
boolean：
	true为1
	false为0
Symbol：会被抛出错误

## 隐式转化

[[Js的 == 号强制转换规则]]，这里，用== 相比的时候会进行隐式的转化
还有+号的时候会被隐式转化




# reference
