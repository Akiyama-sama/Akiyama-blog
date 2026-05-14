---
tags:
  - #pernamant
  - 前端实习挑战
  - 前端
  - JavaScript
  - ES6
---
Promise是一个Javascript对象，是**异步操作与[[回调函数]]** 的中介，让异步操作具有同步操作的接口，解决异步处理的[[回调函数]]地狱问题，让写法更加清晰。

什么是回调地狱？可以看看[[回调地狱]]
Promise只有三种状态：
* pedding：初始状态，既没有成功也没失败
* fulfilled：按照函数预期执行成功，调用resolve() (即操作成功后要做的事情)
* rejected：没有按照预期执行（执行失败），调用reject() （即操作失败后要做的事情）

Promise的语法糖：[[async await]]
Promise的底层：[[Promise底层讲解]]
[[构建自己的Promise]]
## 基本结构

```js
const promise = new Promise((resolve, reject) => {
  // 模拟异步操作，比如请求数据
  setTimeout(() => {
    const success = true;
    if (success) { //如果按照预期成功
      resolve("成功啦！");
    } else {       //如果出错
      reject("出错了！");
    }
  }, 1000);
});

// 使用 Promise
promise
  .then(result => {
    console.log(" then接收到的:", result);  //  这就是 resolve() 传来的参数 result
  })
  .catch(error => {
    console.log("catch接收到的:", err);  //  这就是 reject() 传来的参数error
  });

```

## Promise 的最佳实践
* 总是返回Promise对象
* 封装异步操作时用Promise


# reference
https://wangdoc.com/javascript/async/promise
https://es6.ruanyifeng.com/#docs/promise