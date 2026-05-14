---
tags:
  - #pernamant
  - 前端实习挑战
  - 前端
  - JavaScript
---
当我们想要对一个[[Js中的数据类型 | 原始类型]] 像是对象一样使用属性和方法的时候，会再后台自动帮我们创建一个包装类型，使得我们能使用属性和方法，一旦操作完成，这个临时创建的对象会被销毁

string,number,boolean分别对应String，Number，Boolean这三个包装类型

包装类型过后，就会将原始类型变为一个对象，本质是不同的

```js
let strPrimitive = "hello";
let strObject = new String("hello");

console.log(typeof strPrimitive); // "string"
console.log(typeof strObject);    // "object"

console.log(strPrimitive === strObject); // false
console.log(strPrimitive == strObject);  // tr

```



# reference
