---
tags:
  - '#pernamant'
---
## 一般情况
1. null和undefined仅相等于自身和对方
2. boolean类型和数字：true == 1 ，false == 0
3. 字符串和数字相比，需要字符串先转成数字，然后再和另一个数字比
4. 对象和原始类型：对象先用toPrimitive方法（valueOf或者toString）将对象变为原始类型，再和原始类型相比
5. Symbol：Symbol和其他类型相比都是false，只有和自己比才是true


## 特殊情况

1. 空字符“”先变为数字0，然后再进行比较




# reference
