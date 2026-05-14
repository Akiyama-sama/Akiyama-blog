---
date: 2025-11-29
tags:
  - 前端实习挑战
  - 前端
  - 浏览器
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

变种：

有参数，无参数，函数先执行再防抖。

```js
/**
 * @param {Function} func - 需要防抖的目标函数
 * @param {number} wait - 等待时间（毫秒）
 * @param {boolean} immediate - 是否立即执行（true 为先执行，false 为后执行）
 */
function debounce(func, wait, immediate = false) {
  let timeout;

  return function(...args) {
    const context = this;

    // 清除之前的定时器
    if (timeout) clearTimeout(timeout);

    if (immediate) {
      // 如果已经执行过，timeout 就不为空，不再执行
      const callNow = !timeout;
      
      timeout = setTimeout(() => {
        timeout = null; // wait 时间后，释放锁，允许下次点击立即执行
      }, wait);

      if (callNow) func.apply(context, args);
    } else {
      // 常规防抖：设置定时器，最后一次触发后 wait 毫秒执行
      timeout = setTimeout(() => {
        func.apply(context, args);
      }, wait);
    }
  };
}
```