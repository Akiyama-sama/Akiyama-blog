---
date: 2025-11-29
tags: 
---
无论触发多少次，只执行**最后一次**。本质是**“归零重置”**。

简约实现

```js
const debounce = function(action,wait){
    let timeout;
    
    return function(...arg){
        clearTimeout(timeout)
        let content = this
        timeout = setTimeout(()=>action.apply(content,arg),wait)
    }
}

const WAIT_TIME = 2000;

const debouncedAction = debounce(() => {
    console.log(`去抖动操作执行了，且在 ${WAIT_TIME}ms 内没有再次点击。`);
}, WAIT_TIME);

const handleClick = function() {
    // 2. 每次点击都调用这个已经去抖动过的函数
    debouncedAction(); 
    
    // 这条log会立即执行，因为它在 setTimeout 之外
    console.log("新的点击事件已被触发，正在等待去抖...");
```