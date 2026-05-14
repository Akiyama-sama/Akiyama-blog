---
date: 2026-04-28
tags:
---
`Promise.allSettled()` 会等待传入的所有 Promise 都结束，不管它们是成功还是失败。

## 返回结果

它返回一个新的 Promise，并且最终一定会 `resolve`，结果是一个数组，数组顺序和传入顺序一致。

- 成功的项：`{ status: 'fulfilled', value: xxx }`
- 失败的项：`{ status: 'rejected', reason: xxx }`

```js
Promise.allSettled([
  Promise.resolve(1),
  Promise.reject("error"),
  3
]).then((res) => {
  console.log(res)
  // [
  //   { status: 'fulfilled', value: 1 },
  //   { status: 'rejected', reason: 'error' },
  //   { status: 'fulfilled', value: 3 }
  // ]
})
```

## 和 Promise.all 的区别

`Promise.all()` 和 `Promise.allSettled()` 都是把多个异步任务收集起来一起处理，但处理失败的方式完全不同。

| 方法 | 是否等待全部结束 | 遇到一个失败会怎样 | 最终结果 |
| --- | --- | --- | --- |
| `Promise.all()` | 不一定 | 立即 `reject`，直接短路 | 成功值数组 |
| `Promise.allSettled()` | 会 | 不短路，继续等剩余任务完成 | 每一项状态对象数组 |

### 1. 失败时是否短路

- `Promise.all()`：只要有一个失败，整个结果立刻失败。
- `Promise.allSettled()`：不会因为某一个失败就提前结束。

```js
Promise.all([
  Promise.resolve("A"),
  Promise.reject("B failed"),
  Promise.resolve("C")
]).catch((err) => {
  console.log(err) // B failed
})
```

```js
Promise.allSettled([
  Promise.resolve("A"),
  Promise.reject("B failed"),
  Promise.resolve("C")
]).then((res) => {
  console.log(res)
})
```

### 2. 返回值结构不同

- `Promise.all()` 成功时返回纯值数组，如 `[v1, v2, v3]`
- `Promise.allSettled()` 返回带状态的对象数组，方便区分哪个成功、哪个失败

### 3. 使用场景不同

- `Promise.all()`：适合“必须全部成功”的场景
  - 例如页面初始化时，同时请求用户信息、权限信息、菜单信息，少一个都不能正常渲染
- `Promise.allSettled()`：适合“我想知道每个任务结果”的场景
  - 例如批量上传图片、批量发送请求、批量校验表单，希望最后统一看哪些成功、哪些失败

## 怎么选

- 任务之间互相依赖，少一个都不行：用 `Promise.all()`
- 任务彼此独立，只想最后统一收集结果：用 `Promise.allSettled()`

## reference
[[Promise_all]]
[[Promise]]
