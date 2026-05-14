---
date: 2026-03-11
tags:
  - 前端实习挑战
  - 前端
  - 手撕题
  - JavaScript
---
map
```js
Array.prototype.myMap = function(callback, thisArg) {
  const res = [];
  // this 指向调用 myMap 的数组
  for (let i = 0; i < this.length; i++) {
    // 自动跳过稀疏数组的空位
    if (!this.hasOwnProperty(i)) continue;
    // 传入: 当前值, 索引, 原数组
    res[i] = callback.call(thisArg, this[i], i, this);
  }
  return res;
};
```

filter
```js
Array.prototype.myFilter = function(callback, thisArg) {
  const res = [];
  for (let i = 0; i < this.length; i++) {
    if (!this.hasOwnProperty(i)) continue;
    // 回调返回布尔值，决定是否 push
    if (callback.call(thisArg, this[i], i, this)) {
      res.push(this[i]);
    }
  }
  return res;
};
```

reduce

```js
Array.prototype.myReduce = function(callback, initialValue) {
  let accumulator = initialValue;
  let startIndex = 0;

  // 如果没有初始值，取第一个有效元素
  if (accumulator === undefined) {
    while (startIndex < this.length && !this.hasOwnProperty(startIndex)) {
      startIndex++;
    }
    if (startIndex >= this.length) throw new TypeError('Reduce of empty array with no initial value');
    accumulator = this[startIndex++]; //++写后面是先执行++在赋值
  }

  for (let i = startIndex; i < this.length; i++) {
    if (!this.hasOwnProperty(i)) continue;
    // 累加器 = 回调(旧累加器, 当前值, 索引, 原数组)
    accumulator = callback(accumulator, this[i], i, this);
  }
  return accumulator;
};
```