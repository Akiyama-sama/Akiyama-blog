---
tags:
  - #pernamant
  - 前端实习挑战
  - 前端
  - JavaScript
---

闭包是指一个函数能够记住并访问其创建时所在的词法环境（外部作用域）中的变量，即使这个函数在原始作用域之外被调用

这是一个简单示例

```js
function createCounter() {
  let count = 0
  return function () {
    count++
    console.log(count)
  }
}
const counter = createCounter()
counter() //1
counter() //2
counter() //3
```

- `createCounter()` 在执行时，创建了一个局部变量 `count`，然后返回了一个匿名函数。
- 由于这个返回的匿名函数可以“访问并修改” `count`（它在 `createCounter()` 的作用域里被定义），这就形成了闭包。
- 这样，每次调用 `counter()` 时，都会在原有的 `count` 基础上进行自增，而不是从头开始。

## 闭包的显著特征

判断闭包的核心特征：

1. **函数嵌套** — 一个函数内部定义了另一个函数（不一定是匿名函数）
2. **访问外层变量** — 内层函数能访问外层函数的变量
3. **记住变量** — 外层函数执行完后，内层函数仍能访问那些变量
4. **返回内部函数** — 外层函数返回内层函数

```js
// 特征1: 函数嵌套
function outer() {
  let x = 10 // 特征2: 外层变量

  function inner() {
    // 可以是命名函数，不一定是匿名函数
    return x * 2
  }

  return inner // 特征4: 返回内部函数
}

const fn = outer()
fn() // 20 — 特征3: outer()执行完后仍能访问x
```

> 注意：闭包**不只是修改**外部变量，**读取**外部变量也是闭包

# reference
