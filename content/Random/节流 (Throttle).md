---
date: 2025-11-29
tags:
  - 前端实习挑战
  - 前端
  - 浏览器
---
无论触发多少次，按**固定频率**执行。本质是**“稀释冷却”**。

实现

```js
function thorttle(func,delay){
  let lastTime = 0

  return function(...args){
    const now = Date.now()
    if(now - lastTime>delay){
      func.apply(this,args)
      lastTime = now
    }
  }
}

```