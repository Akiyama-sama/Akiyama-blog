---
date: 2025-10-26
tags:
---

# 构建自己的 Promise

这篇笔记的目标，不是让我们一下子写出“和浏览器一模一样”的 Promise，而是先把最核心的问题想明白：

1. Promise 到底在解决什么问题？
2. `new Promise((resolve, reject) => {})` 里面的 `resolve` 和 `reject` 是从哪里来的？
3. `.then()` 为什么能等异步完成后再执行？
4. `.then().then().catch()` 为什么能链式调用？

如果这四件事想明白了，Promise 的底层思路就已经抓住了。

## 先别急着写代码：Promise 到底是干嘛的？

前端里最常见的麻烦之一，就是“有些结果现在拿不到，要等一会儿才能拿到”。

比如请求接口：

```js
const user = fetchUser()
console.log(user)
```

这段代码的问题是：`fetchUser()` 往往不是立刻返回真正的数据，而是要等网络请求结束。

所以早期 JavaScript 经常写成回调：

```js
fetchUser(function (user) {
  console.log(user)
})
```

如果事情一多，就会一层套一层：

```js
login(function (user) {
  getProfile(user.id, function (profile) {
    getPosts(profile.id, function (posts) {
      console.log(posts)
    })
  })
})
```

这就是大家常说的 [[回调函数]] 地狱。

Promise 的作用，可以先把它理解成一句人话：

> Promise 就是“一个未来才会拿到结果的占位对象”。

它现在可能还没结果，但它会帮我们记住：

- 以后成功了，该做什么
- 以后失败了，该做什么

## Promise 可以把异步结果分成三种状态

Promise 内部最核心的东西，其实就是一个“状态”：

- `pending`：等待中
- `fulfilled`：已经成功
- `rejected`：已经失败

而且状态一旦从 `pending` 变成成功或失败，就不能再改回去了。

可以把它想成快递：

- `pending`：快递还在路上
- `fulfilled`：快递送到了
- `rejected`：快递丢了或者配送失败

一旦显示“已签收”，就不会再变回“运输中”。

## `resolve` 和 `reject` 到底从哪里来？

这是很多初学者第一次看 Promise 时最疑惑的地方。

我们平时这样写：

```js
const p = new Promise((resolve, reject) => {
  setTimeout(() => {
    resolve("成功了")
  }, 1000)
})
```

看起来像是我们“凭空”拿到了两个函数：`resolve` 和 `reject`。

其实不是凭空出现的。

真正发生的事情是：

1. 我们 `new Promise(...)`
2. Promise 内部先创建好两个函数：`resolve` 和 `reject`
3. 然后 Promise 再把这两个函数，当成参数传给我们写的那个函数
4. 我们在合适的时候手动调用它们，通知 Promise：“成功了”或者“失败了”

也就是说：

- 外面写的函数，是我们传进去的
- `resolve` / `reject`，是 Promise 内部造出来再交给我们的

这背后会用到 [[回调函数]] 和 [[闭包]]，但先不用把术语看得太重。先记住这件事就够了：

> 你不是自己发明了 `resolve` 和 `reject`，而是 Promise 把控制结果的开关交给了你。

## 第一步：先写一个最小骨架

我们先只做最核心的事情：

- 记录状态
- 记录成功值 / 失败原因
- 在合适的时候修改状态

```js
class MyPromise {
  constructor(executor) {
    this.state = "pending"
    this.value = undefined
    this.reason = undefined
    this.onFulfilledCallbacks = []
    this.onRejectedCallbacks = []

    const resolve = (value) => {
      if (this.state !== "pending") return

      this.state = "fulfilled"
      this.value = value
      this.onFulfilledCallbacks.forEach((cb) => cb(value))
    }

    const reject = (reason) => {
      if (this.state !== "pending") return

      this.state = "rejected"
      this.reason = reason
      this.onRejectedCallbacks.forEach((cb) => cb(reason))
    }

    try {
      executor(resolve, reject)
    } catch (error) {
      reject(error)
    }
  }
}
```

这里先只看懂三件事：

1. `state` 用来记录 Promise 现在处于什么阶段
2. `value` 和 `reason` 分别记录成功结果和失败原因
3. `executor(resolve, reject)` 会立刻执行，所以 `new MyPromise(...)` 的时候，传进去的函数马上就跑了

## 为什么要准备两个回调数组？

注意上面这两个属性：

```js
this.onFulfilledCallbacks = []
this.onRejectedCallbacks = []
```

它们是干嘛的？

因为异步任务经常不会立刻结束。

比如：

```js
const p = new MyPromise((resolve) => {
  setTimeout(() => {
    resolve("1 秒后成功")
  }, 1000)
})
```

这 1 秒里，Promise 还是 `pending`。可我们很可能已经写了：

```js
p.then((value) => {
  console.log(value)
})
```

那这个回调放哪儿？

答案就是：先存起来。

所以 Promise 需要两个“队列”：

- 成功时要执行的回调，先存到 `onFulfilledCallbacks`
- 失败时要执行的回调，先存到 `onRejectedCallbacks`

等以后状态真的改了，再把这些回调拿出来执行。

## 第二步：实现 `then`

`then` 的任务，可以先理解成一句话：

> 给 Promise 注册“成功后要做什么”和“失败后要做什么”。

一个简化版 `then` 可以这样写：

```js
then(onFulfilled, onRejected) {
  return new MyPromise((resolve, reject) => {
    const runFulfilled = (value) => {
      try {
        if (typeof onFulfilled !== "function") {
          resolve(value)
          return
        }

        const result = onFulfilled(value)

        if (result instanceof MyPromise) {
          result.then(resolve, reject)
        } else {
          resolve(result)
        }
      } catch (error) {
        reject(error)
      }
    }

    const runRejected = (reason) => {
      try {
        if (typeof onRejected !== "function") {
          reject(reason)
          return
        }

        const result = onRejected(reason)

        if (result instanceof MyPromise) {
          result.then(resolve, reject)
        } else {
          resolve(result)
        }
      } catch (error) {
        reject(error)
      }
    }

    if (this.state === "fulfilled") {
      runFulfilled(this.value)
    } else if (this.state === "rejected") {
      runRejected(this.reason)
    } else {
      this.onFulfilledCallbacks.push(runFulfilled)
      this.onRejectedCallbacks.push(runRejected)
    }
  })
}
```

第一次看会觉得长，但其实就做了三类事。

### 情况一：这个 Promise 已经成功了

```js
if (this.state === "fulfilled") {
  runFulfilled(this.value)
}
```

那就直接执行成功回调。

### 情况二：这个 Promise 已经失败了

```js
else if (this.state === "rejected") {
  runRejected(this.reason)
}
```

那就直接执行失败回调。

### 情况三：这个 Promise 还没结束

```js
else {
  this.onFulfilledCallbacks.push(runFulfilled)
  this.onRejectedCallbacks.push(runRejected)
}
```

如果它还在 `pending`，就先把回调存起来，等以后 `resolve` / `reject` 时再执行。

## 为什么 `then` 要返回一个新的 Promise？

这是 Promise 链式调用的关键。

比如：

```js
p.then((value) => {
  return value + " -> 第二步"
}).then((value) => {
  console.log(value)
})
```

第一个 `then` 里面返回了一个新值，这个新值要交给“下一个 `then`”。

所以第一个 `then` 不能随便返回，它必须返回一个“新的 Promise 容器”，去接住这次执行的结果。

所以你会看到：

```js
then(onFulfilled, onRejected) {
  return new MyPromise((resolve, reject) => {
    // ...
  })
}
```

这就是链式调用成立的原因。

可以把它想成一节一节的水管：

```js
p.then(...).then(...).then(...)
```

每一个 `then` 都是新接出来的一节管子，上一节流出来的结果，会进入下一节。

## 完整的简化版实现

把上面的代码拼起来，就是这样：

```js
class MyPromise {
  constructor(executor) {
    this.state = "pending"
    this.value = undefined
    this.reason = undefined
    this.onFulfilledCallbacks = []
    this.onRejectedCallbacks = []

    const resolve = (value) => {
      if (this.state !== "pending") return

      this.state = "fulfilled"
      this.value = value
      this.onFulfilledCallbacks.forEach((cb) => cb(value))
    }

    const reject = (reason) => {
      if (this.state !== "pending") return

      this.state = "rejected"
      this.reason = reason
      this.onRejectedCallbacks.forEach((cb) => cb(reason))
    }

    try {
      executor(resolve, reject)
    } catch (error) {
      reject(error)
    }
  }

  then(onFulfilled, onRejected) {
    return new MyPromise((resolve, reject) => {
      const runFulfilled = (value) => {
        try {
          if (typeof onFulfilled !== "function") {
            resolve(value)
            return
          }

          const result = onFulfilled(value)

          if (result instanceof MyPromise) {
            result.then(resolve, reject)
          } else {
            resolve(result)
          }
        } catch (error) {
          reject(error)
        }
      }

      const runRejected = (reason) => {
        try {
          if (typeof onRejected !== "function") {
            reject(reason)
            return
          }

          const result = onRejected(reason)

          if (result instanceof MyPromise) {
            result.then(resolve, reject)
          } else {
            resolve(result)
          }
        } catch (error) {
          reject(error)
        }
      }

      if (this.state === "fulfilled") {
        runFulfilled(this.value)
      } else if (this.state === "rejected") {
        runRejected(this.reason)
      } else {
        this.onFulfilledCallbacks.push(runFulfilled)
        this.onRejectedCallbacks.push(runRejected)
      }
    })
  }

  catch(onRejected) {
    return this.then(undefined, onRejected)
  }
}
```

## 跑一个例子看看

```js
const p = new MyPromise((resolve, reject) => {
  setTimeout(() => {
    resolve("第一步成功")
  }, 1000)
})

p
  .then((value) => {
    console.log(value)
    return value + " -> 第二步"
  })
  .then((value) => {
    console.log(value)
    throw new Error("这里故意报错")
  })
  .catch((error) => {
    console.log("捕获到错误：", error.message)
  })
```

这段代码的执行过程可以这样理解：

1. `new MyPromise(...)` 时，内部函数立刻执行
2. 里面的 `setTimeout` 先挂起，Promise 状态仍然是 `pending`
3. `then` 先把回调存到数组里
4. 1 秒后调用 `resolve("第一步成功")`
5. Promise 状态变成 `fulfilled`
6. 之前存起来的成功回调被依次执行
7. 第一个 `then` 返回的新值，会交给下一个 `then`
8. 第二个 `then` 抛错后，会进入 `catch`

## 这份代码已经能帮我们理解什么？

写到这里，其实 Promise 最重要的几个点已经出来了：

- Promise 内部本质上有一个状态
- `resolve` / `reject` 用来改变状态
- `then` 会注册回调
- 如果异步还没完成，回调就先存起来
- `then` 返回新的 Promise，所以可以链式调用

## 但它还不是真正完整的 Promise

这份代码是“教学版”，不是“生产版”。

真正的 Promise 规范比这复杂得多，至少还有这些细节：

- 真正的 Promise 回调会放进微任务队列，而不是像这里这样直接同步执行
- `resolve` 一个 Promise 时，还要继续“接管”那个 Promise 的状态
- 还要更完整地处理 thenable 对象
- 还会有 `finally`、`Promise.all`、`Promise.race` 等静态方法

所以这篇笔记最重要的目标不是“照抄源码”，而是建立一个正确的脑内模型：

> Promise = 状态管理 + 回调收集 + 链式传递结果

一旦这个模型立起来，后面再看原生 Promise、`async/await`、甚至手写题，都会顺很多。

## 一句话总结

如果只记一句话，我会记这句：

> Promise 就像一个“未来结果的代理人”，它先把成功和失败的处理方式记下来，等异步任务真的结束，再按状态把对应的回调执行掉。

## 相关笔记

- [[Promise]]
- [[Promise底层讲解]]
- [[回调函数]]
- [[闭包]]
- [[async await]]
