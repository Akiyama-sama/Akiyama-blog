---
tags:
  - '#pernamant'
---
**`async/await` 是 [[Promise]] 的语法糖**，它能让你用 **同步的写法** 编写 **异步逻辑**，既直观又优雅。

本质上，`await` 后面就是一个 **Promise 对象**。  
`async` 声明的函数会自动返回一个 **Promise 对象**。
## 基本用法
```js
async function myFunction() {
  try {
    const result = await someAsyncFunction(); // 等待 Promise 返回结果
    console.log("结果是：", result);
  } catch (err) {
    console.error("出错了：", err); // 捕捉异常
  }
}

```


其本质上，就是将 await 下面的代码给包装到了.then()方法里面去。


# reference
