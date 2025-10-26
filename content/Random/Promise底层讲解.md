---
tags:
  - '#pernamant'
---
#  一、Promise 是什么？

在 JavaScript 中，`Promise` 是一个构造函数（类），用来创建表示**异步操作的状态机**的对象。

它的本质是：

> **一种状态管理工具** + **回调收集执行机制**

---

#  二、Promise 的核心特性

### Promise 三种状态（状态机）：

- `pending`：初始状态
  
- `fulfilled`：调用了 `resolve()`
  
- `rejected`：调用了 `reject()`
  

一旦 `fulfilled` 或 `rejected`，就不可变了（**不可逆状态**）。

---

##  三、手写实现一个简化版 Promise（核心源码讲解）

为了讲解原理，我们一步步造一个轮子：

---

### 第一步：定义类、构造器、状态和回调池

```javascript
class MyPromise {
  constructor(executor) {
    this.state = 'pending';      // 初始状态
    this.value = undefined;      // 成功值 or 错误信息
    this.successCallbacks = [];  // 成功回调列表
    this.failureCallbacks = [];  // 失败回调列表

    const resolve = (value) => {
      if (this.state === 'pending') {
        this.state = 'fulfilled';
        this.value = value;
        this.successCallbacks.forEach(cb => cb(value));
      }
    };

    const reject = (reason) => {
      if (this.state === 'pending') {
        this.state = 'rejected';
        this.value = reason;
        this.failureCallbacks.forEach(cb => cb(reason));
      }
    };

    try {
      executor(resolve, reject); // 立即执行传入函数
    } catch (err) {
      reject(err); // executor 报错也要捕获
    }
  }
```

---

### 第二步：实现 `.then()` 方法（核心）

```javascript
  then(onFulfilled, onRejected) {
    return new MyPromise((resolve, reject) => {
      // 包装一下回调函数，加入错误处理
      const fulfilledWrapper = (value) => {
        try {
          const result = onFulfilled ? onFulfilled(value) : value;
          resolve(result); // 让返回的 Promise resolve
        } catch (e) {
          reject(e); // 出错就 reject
        }
      };

      const rejectedWrapper = (reason) => {
        try {
          const result = onRejected ? onRejected(reason) : reason;
          reject(result);
        } catch (e) {
          reject(e);
        }
      };

      if (this.state === 'fulfilled') {
        fulfilledWrapper(this.value);
      } else if (this.state === 'rejected') {
        rejectedWrapper(this.value);
      } else {
        this.successCallbacks.push(fulfilledWrapper);
        this.failureCallbacks.push(rejectedWrapper);
      }
    });
  }
```

---

### 第三步：实现 `.catch()` 方法（只是 then 的语法糖）

```javascript
  catch(onRejected) {
    return this.then(null, onRejected);
  }
}
```

---

###  最小使用示例

```javascript
const p = new MyPromise((resolve, reject) => {
  setTimeout(() => {
    resolve("成功了");
  }, 1000);
});

p.then(res => {
  console.log("then拿到：", res);
}).catch(err => {
  console.log("出错：", err);
});
```

---

#  四、重点剖析：then 是怎么串联起来的？

```javascript
p.then(fn1).then(fn2).then(fn3)
```

> 每一次 `.then()` **都会返回一个新的 Promise**，这样就能实现“链式调用”。

### 链式调用的本质是：

- 当前的回调执行完（返回值或新 Promise），
  
- 传给下一个 `.then()` 中，
  
- 保证一个接一个执行（**基于状态转移** + **回调触发**）
  

---

#  五、原理总结图解

```
new Promise((resolve, reject) => {...})
      ↓
  resolve(value) 或 reject(err)
      ↓
状态变为 fulfilled / rejected
      ↓
触发已注册的 then/catch 中对应的回调
      ↓
回调返回新值 => 包装进下一个 Promise
      ↓
链式流转
```

---

#  六、真实 Promise 还有哪些我们没实现？

为了简单，我们没实现的还有：

|功能名|描述说明|
|---|---|
|`Promise.resolve()`|快速生成已完成的 Promise|
|`Promise.reject()`|快速生成已失败的 Promise|
|`Promise.all()`|并发多个 Promise，全部成功才算成功|
|`Promise.race()`|谁先完成就返回谁|
|微任务队列处理|真正的 Promise 回调是通过微任务（微任务队列）执行的|

---







# reference
