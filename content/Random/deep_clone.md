---
date: 2026-04-29
tags:
---
为什么这里用 weakmap 而不是 map：

因为 weakmap 可以对 target 对象实现弱引用，即如果内存当中，除了这个 weakmap 引用 target 的话，那么 V8 引擎就会回收这个对象，但如果是 map 存储 target 的话，这个就属于强引用


```js
function deepClone(target,map = new WeakMap) {
  if(typeof target !== 'object' | typeof target == null) return target 
  if(map.has(target)) return map.get(target)

  const clonedTarget  = Array.isArray(target) ? [] : {}
  map.set(target,clonedTarget) //先占位，后续在遍历的时候会直接通过索引填值 
  
  for (const key in target) {
    if (target.hasOwnProperty(key)) {
      // 递归调用
      clonedTarget[key] = deepClone(target[key],map)
    }
  }
  return clonedTarget 
}

const obj = {
    a:1,
    b:{
        c:2
    }
}

const clonedObj = deepClone(obj)

console.log(obj.b === clonedObj.b)

```