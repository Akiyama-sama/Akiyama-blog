---
date: 2026-04-29
tags:
  - 前端实习挑战
  - 前端
  - 手撕题
  - JavaScript
---
`Symbol` 是 ES6 新增的一种**原始类型**，表示独一无二的值。

## 基本特点

- 每次调用 `Symbol()` 都会生成一个全新的值
- 即使传入相同的描述，两个 `Symbol` 也不相等
- 常用来作为对象属性名，避免命名冲突

```js
const s1 = Symbol()
const s2 = Symbol()

console.log(s1 === s2) // false

const a = Symbol("id")
const b = Symbol("id")

console.log(a === b) // false
```

这里的 `"id"` 只是描述信息，方便调试，不会影响唯一性。

## 为什么要有 Symbol

对象的普通属性名通常是字符串，如果多人协作或者多个库同时往同一个对象上挂属性，就容易重名。

```js
const obj = {
  name: "mio"
}

obj.id = 1
obj.id = 2

console.log(obj.id) // 2
```

如果用 `Symbol` 作为 key，就不会轻易和别的属性冲突。

```js
const key1 = Symbol("id")
const key2 = Symbol("id")

const obj = {}
obj[key1] = 1
obj[key2] = 2

console.log(obj[key1]) // 1
console.log(obj[key2]) // 2
```

## 作为对象属性名

```js
const name = Symbol("name")
const user = {
  [name]: "mio"
}

console.log(user[name]) // "mio"
```

注意，定义 `Symbol` 属性时要用 `[]`。

## 遍历时的特点

`Symbol` 类型的属性默认不会出现在一些常见遍历里：

```js
const key = Symbol("secret")
const obj = {
  name: "mio",
  [key]: 123
}

console.log(Object.keys(obj)) // ["name"]
for (const k in obj) {
  console.log(k) // name
}
```

但它并不是“真正的私有属性”，只是普通遍历默认拿不到。

如果想拿到对象自身的 Symbol 属性，可以用：

```js
Object.getOwnPropertySymbols(obj)
Reflect.ownKeys(obj)
```

## Symbol.for()

`Symbol()` 每次都会创建新值，而 `Symbol.for()` 会去全局注册表里查找。

```js
const a = Symbol.for("token")
const b = Symbol.for("token")

console.log(a === b) // true
```

- `Symbol("x")`：每次都是新的
- `Symbol.for("x")`：相同 key 会复用同一个 Symbol

## 常见用途

### 1. 防止对象属性名冲突

这是最常见的用途。

### 2. 给对象挂“临时方法”或“内部标记”

例如手写 `call` / `apply` / `bind` 时，通常需要临时把函数挂到目标对象上执行，这时就可以用 `Symbol` 避免覆盖原有属性。

```js
const fnKey = Symbol("fn")
context[fnKey] = this
const result = context[fnKey](...args)
delete context[fnKey]
```

这也是 [[Function_apply]] 里使用 `Symbol` 的原因。

### 3. 定义内置行为

JavaScript 里还有一些内置 Symbol，比如：

- `Symbol.iterator`
- `Symbol.toStringTag`
- `Symbol.hasInstance`

它们可以影响对象的一些底层行为。

## 在 Function_apply 里怎么用

手写 `apply` 时，一般思路是：

1. 把当前函数临时挂到 `context` 对象上
2. 让 `context` 调用这个函数，这样函数里的 `this` 就指向 `context`
3. 调用结束后再删掉这个临时属性

问题在于：如果直接写成 `context.fn = this`，就可能覆盖掉对象原本的 `fn` 属性。

```js
context.fn = this
const result = context.fn(...args)
delete context.fn
```

这会有属性冲突风险。

所以更好的写法是：

```js
const fnSymbol = Symbol("fn")
context[fnSymbol] = this
const result = context[fnSymbol](...args)
delete context[fnSymbol]
```

因为 `fnSymbol` 是唯一的，几乎不可能和 `context` 上已有属性重名。

## 一句话总结

`Symbol` 的核心价值就是“制造一个不会撞名的唯一标识”，所以它特别适合做对象的隐藏键、内部标记和临时属性键。

## reference
[[Js中的数据类型]]
[[Function_apply]]
