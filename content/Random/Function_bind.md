---
date: 2026-04-29
tags:
  - 前端实习挑战
  - 前端
  - JavaScript
  - ES6
---
```js
Function.prototype.myBind = function(context,...args1){
  const _this = this

  return function(...args2){
    return _this.apply(context,[...args1,...args2]);
  }
}

const student ={
  name: "mio"
}

function log(...values) {
  console.log(`${this.name} call ${values.join()}`) 
}

const log_bind = log.myBind(student,'yui','lzu')

log_bind('mio')

```

## 这里是如何利用剩余参数的

这段手写 `bind` 里，用到了两次剩余参数：

```js
Function.prototype.myBind = function(context, ...args1) {
  return function(...args2) {
    return _this.apply(context, [...args1, ...args2])
  }
}
```

### 第一次：`...args1`

```js
function(context, ...args1)
```

这里的 `args1` 用来接收**绑定时就提前传入的参数**。

比如：

```js
const log_bind = log.myBind(student, "yui", "lzu")
```

这时：

```js
args1 // ["yui", "lzu"]
```

也就是说，`bind` 在创建新函数的时候，就先把一部分参数保存起来了。

### 第二次：`...args2`

```js
return function(...args2)
```

这里的 `args2` 用来接收**真正调用新函数时传入的参数**。

比如：

```js
log_bind("mio")
```

这时：

```js
args2 // ["mio"]
```

### 最后再把两部分参数拼起来

```js
[...args1, ...args2]
```

这里不是剩余参数了，而是**扩展运算符**。它的作用是把两个数组展开后重新合并成一个新数组。

结果就是：

```js
["yui", "lzu", "mio"]
```

然后再交给：

```js
_this.apply(context, [...args1, ...args2])
```

这样原函数执行时，就同时拿到了：

- 绑定时预存的参数
- 调用时后来补上的参数

## 这其实就是“参数预置”

`bind` 除了固定 `this`，还会把一部分参数先记住，这就是常说的**偏函数**效果。

所以这段代码本质上做了两件事：

1. 固定 `this` 为 `context`
2. 通过 `...args1` 和 `...args2` 实现参数分两次传递，最后再合并

## 一句话理解

`...args1` 负责收集“绑定时的参数”，`...args2` 负责收集“调用时的参数”，最后用 `[...args1, ...args2]` 把它们拼起来交给原函数。

## reference
[[剩余参数]]
[[对象扩展运算符]]
