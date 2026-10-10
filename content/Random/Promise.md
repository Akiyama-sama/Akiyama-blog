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

- **`Promise.all([p1, p2, ...])`**
    - **作用**：**全胜才胜，一败俱败**。并发执行多个任务，全部成功时返回结果数组（顺序与传入一致）；只要有一个失败就立即以该失败原因拒绝。
    - **典型示例**：页面初始化时，需要同时拉取“用户信息”、“系统配置”和“菜单列表”，全部到位后才渲染页面。
        
- **`Promise.allSettled([p1, p2, ...])`**
    - **作用**：**全完才完，绝不提前失败**。等待所有任务都有明确结果（无论成功或失败）后才触发，返回包含每个任务状态和结果的描述对象数组。
    - **典型示例**：批量发送多封邮件或批量上传图片，需要统计最终成功了多少张、失败了多少张，不能因某一张失败而打断全局。
        
- **`Promise.race([p1, p2, ...])`**
    - **作用**：**争先恐后，谁快听谁**。无论成功还是失败，只要有任意一个任务率先落定状态，就立即以该任务的结果作为最终输出。
    - **典型示例**：给网络请求设置超时机制（将真正的 API 请求与一个 `setTimeout` 包装的 reject Promise 进行 race）。
- **`Promise.any([p1, p2, ...])`**
    - **作用**：**一胜即胜，全败才败**。只要有一个任务成功就立即返回该成功结果；只有当所有任务都失败时，才抛出一个包含所有错误信息的 `AggregateError`。
    - **典型示例**：多 CDN 节点容灾备用加载，同时从多个镜像源请求同一个资源，谁先成功响应就用谁的。

# reference
https://wangdoc.com/javascript/async/promise
https://es6.ruanyifeng.com/#docs/promise