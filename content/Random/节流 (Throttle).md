---
date: 2025-11-29
tags: 
---
无论触发多少次，按**固定频率**执行。本质是**“稀释冷却”**。

实现

```js
const throttle = function (action,wait){
    let timeout
    return function(...arg){
        const content  = this
        //有计时器才会去执行，没有不执行
        if(!timeout){
            timeout = setTimeout(() => {
               action.apply(content,arg)
               //执行完毕过后清除计时器
               timeout = null
               
            }, wait);
        }
    }
}

const WAIT_TIME = 2000

const throttleAction = throttle(()=>{
    console.log(`正在节流执行当中...`)
},WAIT_TIME)

const handleClick = function (){
   throttleAction()
   console.log('同步代码正在执行，但节流代码不会执行') 
}
```