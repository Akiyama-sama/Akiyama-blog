---
tags:
  - #pernamant
  - 前端实习挑战
  - 前端
  - JavaScript
---
用对象扩展运算符...
```js
const obj1 = { a: 1, b: 2 };
const obj2 = { b: 3, c: 4 };
const mergedObj = { ...obj1, ...obj2 };

console.log(mergedObj); // { a: 1, b: 3, c: 4 }

```

使用Object.assign()
```js
const obj1 = { a: 1, b: 2 };
const obj2 = { b: 3, c: 4 };
const mergedObj = Object.assign(obj1, obj2);

console.log(mergedObj); // { a: 1, b: 3, c: 4 }

```


这两个都是浅拷贝，如果要用到深拷贝，就需要用到Lodash这样的工具库
```js
const _ = require('lodash');

const obj1 = { a: { x: 1, y: 2 }, b: 2 };
const obj2 = { a: { y: 3, z: 4 }, c: 3 };
const mergedObj = _.merge({}, obj1, obj2);

console.log(mergedObj); // { a: { x: 1, y: 3, z: 4 }, b: 2, c: 3 }

```


# reference
