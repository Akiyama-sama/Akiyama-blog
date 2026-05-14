---
tags:
  - #pernamant
  - 前端实习挑战
  - 前端
  - JavaScript
  - ES6
---

# 一、Promise 是什么？

在 JavaScript 中，`Promise` 是一个构造函数（类），用来创建表示**异步操作的状态机**的对象。

它的本质是：

> **一种状态管理工具** + **回调收集执行机制**

---

# 二、Promise 的核心特性

### Promise 三种状态（状态机）：

- `pending`：初始状态
- `fulfilled`：调用了 `resolve()`
- `rejected`：调用了 `reject()`

一旦 `fulfilled` 或 `rejected`，就不可变了（**不可逆状态**）。

---

## 三、手写实现一个简化版 Promise（核心源码讲解）

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

### 最小使用示例

```javascript
const p = new MyPromise((resolve, reject) => {
  setTimeout(() => {
    resolve("成功了")
  }, 1000)
})

p.then((res) => {
  console.log("then拿到：", res)
}).catch((err) => {
  console.log("出错：", err)
})
```

---

# 四、重点剖析：then 是怎么串联起来的？

```javascript
p.then(fn1).then(fn2).then(fn3)
```

> 每一次 `.then()` **都会返回一个新的 Promise**，这样就能实现“链式调用”。

### 链式调用的本质是：

- 当前的回调执行完（返回值或新 Promise），
- 传给下一个 `.then()` 中，
- 保证一个接一个执行（**基于状态转移** + **回调触发**）

---

# 五、原理总结图解

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

# 六、真实 Promise 还有哪些我们没实现？

为了简单，简化版跳过了以下内容（第七节已全部补全）：

| 功能名                 | 描述说明                                            | 实现状态  |
| ---------------------- | --------------------------------------------------- | --------- |
| `Promise.resolve()`    | 快速生成已完成的 Promise                            | ✅ 已补全 |
| `Promise.reject()`     | 快速生成已失败的 Promise                            | ✅ 已补全 |
| `Promise.all()`        | 并发多个 Promise，全部成功才算成功                  | ✅ 已补全 |
| `Promise.race()`       | 谁先完成就返回谁                                    | ✅ 已补全 |
| `Promise.allSettled()` | 全部落定后返回每个结果（不短路）                    | ✅ 已补全 |
| `Promise.any()`        | 任意一个成功即返回，全失败抛 AggregateError         | ✅ 已补全 |
| `.finally()`           | 无论成败都执行的回调                                | ✅ 已补全 |
| 微任务队列处理         | 真正的 Promise 回调是通过微任务（微任务队列）执行的 | ⏳ 未实现 |

---

# 七、补全静态方法实现

## Promise.resolve() 和 Promise.reject()

最简单的工厂方法，快速创建一个已经确定状态的 Promise：

```javascript
static resolve(value) {
  return new MyPromise((resolve) => resolve(value));
}

static reject(reason) {
  return new MyPromise((_, reject) => reject(reason));
}
```

**使用示例：**

```javascript
MyPromise.resolve(42).then((val) => console.log(val)) // 42
MyPromise.reject("出错了").catch((err) => console.log(err)) // 出错了
```

---

## Promise.all() —— 全部成功才算成功

### 核心逻辑

- 接收一个 Promise 数组
- **全部 resolve** → 返回所有结果组成的数组（顺序与传入一致）
- **任意一个 reject** → 立即以该错误 reject

```javascript
static all(promises) {
  return new MyPromise((resolve, reject) => {
    const results = [];       // 收集成功结果
    let count = 0;            // 成功计数

    if (promises.length === 0) {
      resolve(results);       // 空数组直接成功
      return;
    }

    promises.forEach((promise, index) => {
      // 用 MyPromise.resolve 包一下，支持传入非 Promise 值
      MyPromise.resolve(promise).then(
        (value) => {
          results[index] = value;    // 按原始下标存（保证顺序）
          count++;
          if (count === promises.length) {
            resolve(results);        // 全部完成，统一 resolve
          }
        },
        (reason) => {
          reject(reason);            // 一个失败，立即 reject
        }
      );
    });
  });
}
```

**使用示例：**

```javascript
const p1 = MyPromise.resolve(1)
const p2 = MyPromise.resolve(2)
const p3 = MyPromise.resolve(3)

MyPromise.all([p1, p2, p3]).then((values) => {
  console.log(values) // [1, 2, 3]，顺序保证！
})

// 有一个失败的情况
const pFail = MyPromise.reject("网络错误")
MyPromise.all([p1, pFail, p3]).catch((err) => {
  console.log(err) // '网络错误'
})
```

> [!tip] 注意顺序保证
> 用 `results[index] = value` 而不是 `results.push(value)`，这样即使异步完成顺序不同，结果数组的下标也和传入顺序一致。

---

## Promise.race() —— 谁先完成返回谁

### 核心逻辑

- 接收一个 Promise 数组
- **第一个**完成的（无论成功或失败）决定最终结果
- 其余的继续执行，但结果被忽略（状态已锁定，后续 resolve/reject 被 `pending` 检查拦截）

```javascript
static race(promises) {
  return new MyPromise((resolve, reject) => {
    promises.forEach((promise) => {
      MyPromise.resolve(promise).then(
        (value) => resolve(value),   // 第一个 resolve 的赢了
        (reason) => reject(reason)   // 第一个 reject 的也会触发
      );
    });
  });
}
```

**使用示例：**

```javascript
const slow = new MyPromise((resolve) => setTimeout(() => resolve("慢"), 1000))
const fast = new MyPromise((resolve) => setTimeout(() => resolve("快"), 200))

MyPromise.race([slow, fast]).then((winner) => {
  console.log(winner) // '快'
})

// 常见用途：给请求加超时限制
const timeout = new MyPromise((_, reject) => setTimeout(() => reject("请求超时"), 3000))

MyPromise.race([fetch("/api/data"), timeout])
  .then((res) => console.log("成功", res))
  .catch((err) => console.log("失败", err)) // 超过3秒 → '请求超时'
```

---

## Promise.allSettled() —— 全部落定，不管成败

> ES2020 新增，等所有 Promise 都「落定」（无论成功或失败），再返回每个的结果。

```javascript
static allSettled(promises) {
  return new MyPromise((resolve) => {
    const results = [];
    let count = 0;

    if (promises.length === 0) {
      resolve(results);
      return;
    }

    promises.forEach((promise, index) => {
      MyPromise.resolve(promise).then(
        (value) => {
          results[index] = { status: 'fulfilled', value };
          if (++count === promises.length) resolve(results);
        },
        (reason) => {
          results[index] = { status: 'rejected', reason };
          if (++count === promises.length) resolve(results);
        }
      );
    });
  });
}
```

**使用示例：**

```javascript
const p1 = MyPromise.resolve("成功")
const p2 = MyPromise.reject("失败")
const p3 = MyPromise.resolve("也成功")

MyPromise.allSettled([p1, p2, p3]).then((results) => {
  console.log(results)
  // [
  //   { status: 'fulfilled', value: '成功' },
  //   { status: 'rejected', reason: '失败' },
  //   { status: 'fulfilled', value: '也成功' }
  // ]
})
```

> [!info] 和 all() 的区别
>
> - `all()` 遇到失败立刻短路，只要有一个挂了就完了
> - `allSettled()` 等所有都跑完，结果里记录每一个的成败

---

## Promise.any() —— 第一个成功的

> ES2021 新增，和 `race()` 类似，但只关心「成功」。

- 有一个 resolve → 立即以该值 resolve
- 全部 reject → 抛出 `AggregateError`

```javascript
static any(promises) {
  return new MyPromise((resolve, reject) => {
    const errors = [];
    let count = 0;

    if (promises.length === 0) {
      reject(new AggregateError([], '所有Promise都失败了'));
      return;
    }

    promises.forEach((promise, index) => {
      MyPromise.resolve(promise).then(
        (value) => {
          resolve(value);     // 第一个成功就赢，忽略后续
        },
        (reason) => {
          errors[index] = reason;
          if (++count === promises.length) {
            reject(new AggregateError(errors, '所有Promise都失败了'));
          }
        }
      );
    });
  });
}
```

---

## .finally() —— 无论如何都执行

> 不管成功还是失败，都会执行，常用于关闭 loading、释放资源等。

```javascript
finally(onFinally) {
  return this.then(
    value  => MyPromise.resolve(onFinally()).then(() => value),
    reason => MyPromise.resolve(onFinally()).then(() => { throw reason; })
  );
}
```

**使用示例：**

```javascript
MyPromise.resolve("数据")
  .then((data) => {
    console.log("获取到：", data)
  })
  .finally(() => {
    console.log("关闭 loading...") // 一定会执行
  })
```

---

# 八、四大并发方法对比

| 方法           | 成功条件                 | 失败条件             | 返回值                        |
| -------------- | ------------------------ | -------------------- | ----------------------------- |
| `all()`        | **全部**成功             | 任意一个失败（短路） | 成功值数组 / 第一个错误       |
| `race()`       | 第一个完成（成功或失败） | 第一个完成是失败     | 第一个结果                    |
| `allSettled()` | 全部落定（**不会失败**） | 不存在失败情况       | 每个结果的状态对象数组        |
| `any()`        | **任意一个**成功         | 全部失败             | 第一个成功值 / AggregateError |

```
场景选择：
  需要所有请求都成功    → all()
  哪个快用哪个         → race()
  只关心有没有一个成功  → any()
  需要知道每个结果      → allSettled()
```

---

# 九、完整版 MyPromise（汇总）

```javascript
class MyPromise {
  constructor(executor) {
    this.state = "pending"
    this.value = undefined
    this.successCallbacks = []
    this.failureCallbacks = []

    const resolve = (value) => {
      if (this.state === "pending") {
        this.state = "fulfilled"
        this.value = value
        this.successCallbacks.forEach((cb) => cb(value))
      }
    }

    const reject = (reason) => {
      if (this.state === "pending") {
        this.state = "rejected"
        this.value = reason
        this.failureCallbacks.forEach((cb) => cb(reason))
      }
    }

    try {
      executor(resolve, reject)
    } catch (err) {
      reject(err)
    }
  }

  then(onFulfilled, onRejected) {
    return new MyPromise((resolve, reject) => {
      const fulfilledWrapper = (value) => {
        try {
          const result = onFulfilled ? onFulfilled(value) : value
          resolve(result)
        } catch (e) {
          reject(e)
        }
      }
      const rejectedWrapper = (reason) => {
        try {
          const result = onRejected ? onRejected(reason) : reason
          reject(result)
        } catch (e) {
          reject(e)
        }
      }
      if (this.state === "fulfilled") fulfilledWrapper(this.value)
      else if (this.state === "rejected") rejectedWrapper(this.value)
      else {
        this.successCallbacks.push(fulfilledWrapper)
        this.failureCallbacks.push(rejectedWrapper)
      }
    })
  }

  catch(onRejected) {
    return this.then(null, onRejected)
  }

  finally(onFinally) {
    return this.then(
      (value) => MyPromise.resolve(onFinally()).then(() => value),
      (reason) =>
        MyPromise.resolve(onFinally()).then(() => {
          throw reason
        }),
    )
  }

  static resolve(value) {
    return new MyPromise((resolve) => resolve(value))
  }

  static reject(reason) {
    return new MyPromise((_, reject) => reject(reason))
  }

  static all(promises) {
    return new MyPromise((resolve, reject) => {
      const results = []
      let count = 0
      if (promises.length === 0) return resolve(results)
      promises.forEach((promise, index) => {
        MyPromise.resolve(promise).then(
          (value) => {
            results[index] = value
            if (++count === promises.length) resolve(results)
          },
          (reason) => reject(reason),
        )
      })
    })
  }

  static race(promises) {
    return new MyPromise((resolve, reject) => {
      promises.forEach((promise) => {
        MyPromise.resolve(promise).then(resolve, reject)
      })
    })
  }

  static allSettled(promises) {
    return new MyPromise((resolve) => {
      const results = []
      let count = 0
      if (promises.length === 0) return resolve(results)
      promises.forEach((promise, index) => {
        MyPromise.resolve(promise).then(
          (value) => {
            results[index] = { status: "fulfilled", value }
            if (++count === promises.length) resolve(results)
          },
          (reason) => {
            results[index] = { status: "rejected", reason }
            if (++count === promises.length) resolve(results)
          },
        )
      })
    })
  }

  static any(promises) {
    return new MyPromise((resolve, reject) => {
      const errors = []
      let count = 0
      if (promises.length === 0) return reject(new AggregateError([], "所有Promise都失败了"))
      promises.forEach((promise, index) => {
        MyPromise.resolve(promise).then(
          (value) => resolve(value),
          (reason) => {
            errors[index] = reason
            if (++count === promises.length)
              reject(new AggregateError(errors, "所有Promise都失败了"))
          },
        )
      })
    })
  }
}
```

---

# reference
