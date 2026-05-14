---
date: 2026-05-10
tags:
aliases:
---
# requestIdleCallback

`requestIdleCallback` 是浏览器提供的一个调度 API，用来把一些**不紧急**的任务放到主线程空闲时执行。

它的典型场景不是处理立即影响交互的逻辑，而是把优先级较低的工作延后，比如：

- 大量数据的预处理
- 缓存写入
- 埋点上报
- 非首屏内容准备
- 分片执行一些计算任务，避免一次性阻塞主线程

## 基本用法

```ts
const id = requestIdleCallback((deadline) => {
  while (deadline.timeRemaining() > 0) {
    // 做一些低优先级任务
  }
}, { timeout: 1000 })
```

- 回调参数 `deadline` 表示当前这段空闲时间的信息。
- `deadline.timeRemaining()` 表示当前空闲片段大概还剩多少时间可用。
- `timeout` 表示即使浏览器一直很忙，超过这个时间也要尽快执行。

如果任务不再需要，可以取消：

```ts
cancelIdleCallback(id)
```

## 核心理解

可以把它理解为：浏览器先保证高优先级工作，比如用户输入、动画、布局、绘制；如果这一帧还有空余时间，再来执行 `requestIdleCallback` 注册的任务。

所以它有几个特点：

- 适合低优先级、可延后任务
- 不保证立刻执行
- 页面繁忙时可能会被延迟很久
- 通常要配合 `timeout` 使用，避免任务一直饿死

## 和 `setTimeout` 的区别

`setTimeout` 只是“过一段时间后放进任务队列”，并不关心浏览器当前忙不忙；`requestIdleCallback` 则是“等浏览器空闲了再做”。

所以：

- `setTimeout` 更像时间驱动
- `requestIdleCallback` 更像空闲驱动

## 使用注意

1. 不要把关键交互逻辑放进去，因为它不保证及时执行。
2. 单次任务不要太重，否则即使在空闲阶段也可能卡顿。
3. 更适合拆成小任务，分批处理。
4. 兼容性不是所有环境都一样，使用时通常需要降级方案。

## 一个常见场景

比如你有一批列表项的额外信息需要预计算，但这些信息不会影响首屏渲染，就可以先把页面交互跑起来，再用 `requestIdleCallback` 在空闲时慢慢处理这部分工作，减少首屏阻塞。
