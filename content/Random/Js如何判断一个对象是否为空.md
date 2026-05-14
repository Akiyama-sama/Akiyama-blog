---
tags:
  - #pernamant
  - 前端实习挑战
  - 前端
  - JavaScript
---
用Object.keys()，这个方法可以返回一个包含对象所有可枚举属性的数组，如果数组长度为0，那么就是个空对象

```js
function isEmptyObject(obj) {
  return obj && typeof obj === 'object' && Object.keys(obj).length === 0;
}

let emptyObj = {};
console.log(isEmptyObject(emptyObj)); // true

let nonEmptyObj = { key: 'value' };
console.log(isEmptyObject(nonEmptyObj)); // false

```

用Json.stringfy() 
```js
function isEmptyObject(obj) {
  return JSON.stringify(obj) === '{}';
}

```


# reference
