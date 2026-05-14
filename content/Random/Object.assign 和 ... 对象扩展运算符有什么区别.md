---
tags:
  - #pernamant
  - 前端实习挑战
  - 前端
  - JavaScript
---
Object.assign和 [[对象扩展运算符]]都是[[浅拷贝]]，但是Object.assign会修改原对象并且返回原对象，而... 会创建一个新的对象并进行拷贝

```js
const obj1 = { a: 1, b: { c: 2 } };
const obj2 = { b: { d: 3 }, e: 4 };

const mergedObj = Object.assign({}, obj1, obj2);
console.log(mergedObj); // { a: 1, b: { d: 3 }, e: 4 }
console.log(obj2.b === mergedObj.b); // true，浅拷贝只复制了对象的引用

```

# reference
