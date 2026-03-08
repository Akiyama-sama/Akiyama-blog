---
tags:
  - "#pernamant"
---

## ||的返回值规则

如果第一个为true，返回第一个值，第一个为false返回第二个的值

```js
console.log(false || true) // true
console.log(0 || 42) // 42
console.log("" || "default") // "default"
console.log(null || "fallback") // "fallback"
console.log(undefined || "ok") // "ok"
console.log(false || 0 || "foo") // "foo"
console.log("" || 0 || NaN) // NaN
```

## && 的返回值

如果第一个值为 false 返回第一个操作数的值，如果第一个为true，返回第二个的值

```js
console.log(true && false) // false
console.log(42 && 0) // 0
console.log("foo" && "bar") // "bar"
console.log("hello" && 123) // 123
console.log(true && "ok") // "ok"
console.log(1 && 2 && 3) // 3
console.log("" && "fallback") // ""
console.log(null && "should not reach") // null
```

## 按位操作符 | 和 &

除了逻辑操作符 `||` 和 `&&`，JavaScript 还有**按位操作符**：

| 操作符  | 名称  | 说明             |
| ---- | --- | -------------- |
| `\|` | 按位或 | 二进制位有一个为1则结果为1 |
| `&`  | 按位与 | 二进制位两个都为1则结果为1 |

```js
// 按位或 |
console.log(5 | 1) // 5 (101 | 001 = 101)
console.log(1 | 4) // 5 (001 | 100 = 101)

// 按位与 &
console.log(5 & 1) // 1 (101 & 001 = 001)
console.log(6 & 3) // 2 (110 & 011 = 010)
```

> 注意：`|` 和 `&` 是**位运算**，不是逻辑运算。它们会对操作数进行二进制逐位计算。

# reference
