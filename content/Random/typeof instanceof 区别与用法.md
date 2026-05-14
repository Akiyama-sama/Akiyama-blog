---
date: 2026-04-28
tags:
---
`typeof` 和 `instanceof` 都可以做类型判断，但判断的维度不一样。

## typeof

`typeof` 主要用来判断一个值的**基本类型**，返回结果是一个字符串。

```js
typeof 1 // "number"
typeof "abc" // "string"
typeof true // "boolean"
typeof undefined // "undefined"
typeof Symbol() // "symbol"
typeof 10n // "bigint"
typeof function () {} // "function"
```

对于大多数原始类型，`typeof` 很方便，写法也最简单。

### typeof 的特点

- 适合判断原始类型
- 返回值是字符串
- 可以判断函数，结果是 `"function"`
- 对对象、数组、`null` 都比较粗糙

```js
typeof {} // "object"
typeof [] // "object"
typeof null // "object"
```

> `typeof null === "object"` 是 JavaScript 的历史遗留问题，所以不能用 `typeof` 精确判断 `null`。

如果要判断 `null`，通常直接写：

```js
value === null
```

## instanceof

`instanceof` 主要用来判断一个对象是否出现在另一个构造函数的原型链上。

```js
[] instanceof Array // true
[] instanceof Object // true
new Date() instanceof Date // true
new Date() instanceof Object // true
```

它本质上判断的是：

> 某个构造函数的 `prototype` 是否存在于这个对象的原型链上。

比如：

```js
function Person() {}
const p = new Person()

p instanceof Person // true
p instanceof Object // true
```

### instanceof 的特点

- 适合判断引用类型
- 依赖原型链
- 左边一般是对象
- 右边必须是构造函数

```js
1 instanceof Number // false
"abc" instanceof String // false
true instanceof Boolean // false
```

因为 `1`、`"abc"`、`true` 都是原始值，不是通过 `new Number()`、`new String()`、`new Boolean()` 创建出来的对象。

## typeof 和 instanceof 的区别

| 对比点 | `typeof` | `instanceof` |
| --- | --- | --- |
| 判断依据 | 值的底层类型标签 | 原型链 |
| 常用场景 | 判断基本类型 | 判断引用类型 |
| 返回值 | 字符串 | 布尔值 |
| 是否能判断继承关系 | 不能 | 能 |
| 对数组的判断 | `object`，不精确 | `arr instanceof Array` |

## 常见用法

### 1. 判断一个变量是不是未定义

```js
if (typeof value === "undefined") {
  console.log("value 没有定义")
}
```

这个场景更适合用 `typeof`。

### 2. 判断一个值是不是数组

```js
arr instanceof Array
```

不过现代 JavaScript 更推荐：

```js
Array.isArray(arr)
```

### 3. 判断一个对象是不是某个类的实例

```js
class Animal {}
class Dog extends Animal {}

const d = new Dog()

d instanceof Dog // true
d instanceof Animal // true
```

这个场景更适合用 `instanceof`，因为它能体现继承关系。

## 常见坑

### 1. `typeof null`

```js
typeof null // "object"
```

这是经典坑点，不要拿它判断 `null`。

### 2. `instanceof` 不能很好判断原始类型

```js
"abc" instanceof String // false
123 instanceof Number // false
```

因为它们是原始值，不是包装对象。

### 3. 跨 iframe 或跨 window 时 `instanceof` 可能不准

不同执行上下文有不同的全局对象和构造函数：

```js
arr instanceof Array // 可能是 false
```

即使它看起来是数组，也可能因为不是当前窗口下的 `Array` 构造出来的而判断失败。

## 怎么选

- 判断 `string`、`number`、`boolean`、`undefined`、`symbol`、`bigint`：用 `typeof`
- 判断 `null`：直接 `=== null`
- 判断数组：优先 `Array.isArray()`
- 判断某个对象是不是某个类的实例：用 `instanceof`

## 一句话总结

`typeof` 看的是“这个值是什么基础类型”，`instanceof` 看的是“这个对象是谁构造出来的，原型链上有没有它”。

## reference
[[Js中的数据类型]]
