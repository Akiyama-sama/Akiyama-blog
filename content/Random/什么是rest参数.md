---
tags:
  - #pernamant
  - 前端实习挑战
  - 前端
  - JavaScript
  - ES6
---
rest用于表示不确定数量的参数，将函数中传入的多个参数包装成一个数组，通过rest参数，可以方便的处理不确定数量的参数

```js
function sum(...numbers) {
    return numbers.reduce((acc, curr) => acc + curr, 0);
}

console.log(sum(1, 2, 3, 4)); // 输出: 10

```

其中，numbers就是rest参数


# reference
