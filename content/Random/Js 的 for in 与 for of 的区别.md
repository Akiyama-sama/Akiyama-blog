---
tags:
  - "#pernamant"
---

for in 用来

- 遍历一个对象的可枚举属性，包括原型链上的可枚举属性
- 返回的是键名（属性名）
- 可以遍历普通对象，也可以遍历数组（性能不如for of）
- ES3的语法

for of 用来

- 遍历可迭代对象（数组，字符串，Map，Set）
- 返回的是每次迭代的值
- 不能直接用于遍历普通对象
- ES6语法

1. 遍历顺序：for...in 不保证遍历顺序，而 for...of 会按照迭代器定义的顺序进行遍历。
2. 性能：通常来说，for...of 的性能比 for...in 更好，特别是在遍历数组时。所以遍历优先选 for...of
3. 继承属性：for...in 会遍历对象的原型链，而 for...of 不会。
4. 使用场景：for...in 更适合用于遍历对象的属性，而 for...of 更适合用于遍历数组或其他可迭代对象的值。

## 代码示例

### for...in 示例

```javascript
// 遍历对象（返回键名）
const person = { name: "Alice", age: 25, city: "Chongqing" }

for (const key in person) {
  console.log(key, person[key])
}
// 输出:
// name Alice
// age 25
// city Chongqing

// 遍历数组（返回索引）
const arr = ["a", "b", "c"]

for (const index in arr) {
  console.log(index, arr[index])
}
// 输出:
// 0 a
// 1 b
// 2 c

// 会遍历原型链上的属性
const parent = { type: "parent" }
const child = Object.create(parent)
child.name = "child"

for (const key in child) {
  console.log(key)
}
// 输出: name, type (包括继承属性)
```

### for...of 示例

```javascript
// 遍历数组（返回值）
const arr = ["a", "b", "c"]

for (const value of arr) {
  console.log(value)
}
// 输出: a, b, c

// 遍历字符串
const str = "hello"

for (const char of str) {
  console.log(char)
}
// 输出: h, e, l, l, o

// 遍历 Map
const map = new Map([
  ["a", 1],
  ["b", 2],
])

for (const [key, value] of map) {
  console.log(key, value)
}
// 输出: a 1, b 2

// 遍历 Set
const set = new Set([1, 2, 3])

for (const value of set) {
  console.log(value)
}
// 输出: 1, 2, 3

// for...of 不能直接遍历普通对象
const obj = { a: 1, b: 2 }

// for (const value of obj) {} // TypeError: obj is not iterable

// 需要先获取对象的迭代器或转成数组
for (const key of Object.keys(obj)) {
  console.log(key, obj[key])
}
// 输出: a 1, b 2
```

### 对比总结

```javascript
const arr = [10, 20, 30]

// for...in → 索引（字符串）
for (const i in arr) {
  console.log(typeof i) // string
}

// for...of → 值
for (const v of arr) {
  console.log(typeof v) // number
}
```

# reference
