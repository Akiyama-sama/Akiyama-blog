---
date: 2026-04-28
tags:
  - 前端实习挑战
  - 前端
  - 手撕题
  - JavaScript
---
```js
Function.prototype.myApply = function(context,args){
  //处理边界情况
  context = context == null ? globalThis : Object(context)
  const fnSymbol = Symbol('fn')
  context[fnSymbol] = this //这里的 this 指的当前实际 call 了的 function 对象 
  //调用这个函数
  const result = context[fnSymbol](...(args || []))

  //call / apply的职责是执行函数，而不是修改 context 对象 
  // delete 关键字，删除对象中的属性 
  delete context[fnSymbol]
  return result
}
const student ={
  name: "mio"
}

function log(...values) {
  console.log(`${this.name} call ${values.join()}`) 
}

log.myApply(student,['yui','lzu'])

```

## 为什么这里要用 Symbol

手写 `apply` 的核心思路，是先把当前函数临时挂到 `context` 对象上，再通过“对象调用函数”的方式，让函数内部的 `this` 指向这个对象。

如果直接这样写：

```js
context.fn = this
const result = context.fn(...args)
delete context.fn
```

会有一个问题：`context` 本身可能已经有 `fn` 这个属性了，这样就会把原来的值覆盖掉。

```js
const obj = {
  fn: "原来的属性"
}
```

所以这里更好的做法是用：

```js
const fnSymbol = Symbol("fn")
```

因为 `Symbol` 生成的是唯一值，把它作为属性名时，几乎不可能和对象原有属性冲突：

```js
context[fnSymbol] = this
const result = context[fnSymbol](...args)
delete context[fnSymbol]
```

这样做的好处是：

- 不会覆盖对象已有属性
- 这个属性只是临时使用，调用完就删掉
- 语义上也更清楚，它是一个内部临时键

## 这一段代码实际做了什么

```js
const fnSymbol = Symbol('fn')
context[fnSymbol] = this
const result = context[fnSymbol](...(args || []))
delete context[fnSymbol]
```

可以理解成：

1. 创建一个唯一的属性名
2. 把当前函数挂到 `context` 上
3. 通过 `context[fnSymbol](...)` 调用，让 `this` 指向 `context`
4. 删除这个临时属性，恢复现场

## reference
[[Symbol]]
[[prototype原型对象]]
