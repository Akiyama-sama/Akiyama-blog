---
date: 2026-04-29
tags:
  - 前端实习挑战
  - 前端
  - 手撕题
  - JavaScript
---
```js
Function.prototype.myCall = function(context,...args){
  //处理边界情况
  context = context || global
  const fnSymbol = Symbol('fn')
  context[fnSymbol] = this //这里的 this 指的当前实际 call 了的 function 对象 
  //调用这个函数
  const result = context[fnSymbol](...args)

  //call / apply的职责是执行函数，而不是修改 context 对象 
  // delete 关键字，删除对象中的属性 
  delete context[fnSymbol]
  return result
}

const student ={
  name: "mio"
}

function log(value) {
  console.log(`${this.name} call ${value}`) 
}

log.myCall(student,'yui')

```

跟[[Function_apply]]的区别是：call 传过来的是任意个参数，而 apply 传过来的第二个参数是一个数组

