---
date: 2026-04-29
tags:
---
```js
function myNew(Constructor,...args) {
  //先创建一个指向构造函数 prototype 的一个对象
  const obj = Object.create(Constructor.prototype) 
  //再将 obj 绑定到 Constructor的 this 对象当中
  //
  const result = Constructor.apply(obj,...args);

  //如果构造函数显示的返回对象，那么就丢弃 obj 这个我们创建的对象，只返回
  //构造函数当中的对象

  const isObj = typeof result === Object 
  const isFunction = typeof result === Function
  return isObj || isFunction ? result : obj
}

```