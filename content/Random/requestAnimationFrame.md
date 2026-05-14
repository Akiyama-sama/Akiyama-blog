---
date: 2026-02-10
tags:
  - 
  - Javascript
  - 浏览器
  - 性能优化
  - 前端实习挑战
  - 前端
aliases:
  - rAF
  - raf
  - RAF
---

`requestAnimationFrame`，通常简写为 `rAF`，是浏览器提供的一个 API，用来在**下一次浏览器重绘之前**执行某个回调。

它最适合做两类事：

- 和视觉刷新强相关的动画
- 想把高频更新“对齐到浏览器绘制节奏”的任务

一句话理解：

> `setTimeout` 是“过多久再试试”，`requestAnimationFrame` 是“浏览器下次要画面了，你这时候来更新”。

## 基本用法

```js
const id = requestAnimationFrame((timestamp) => {
  console.log("当前帧时间戳", timestamp)
})

cancelAnimationFrame(id)
```

- `requestAnimationFrame(fn)`：注册一个回调，等下次重绘前执行。
- `cancelAnimationFrame(id)`：取消已经注册但还没执行的回调。
- `timestamp`：浏览器传给回调的高精度时间戳，表示当前这一帧的时间。

## 它和 `setTimeout` 有什么区别

### 1. 触发依据不同

- `setTimeout(fn, 16)`：本质上是“最少等待 16ms 后，把回调放进任务队列”。
- `requestAnimationFrame(fn)`：本质上是“浏览器下一次准备绘制前，执行这个回调”。

所以它们的本体就不是一类东西：

- `setTimeout` 更接近[[事件循环 Event loop]]里的定时任务。
- `requestAnimationFrame` 更接近[[渲染更新阶段]]里的“帧前回调”。

### 2. 是否和屏幕刷新同步

`requestAnimationFrame` 会尽量和屏幕刷新频率对齐。

这意味着：

- 在 60Hz 屏幕上，大约一秒执行 60 次
- 在 120Hz 屏幕上，大约一秒执行 120 次

它**不是固定 16.7ms**，而是跟着设备刷新率走。

### 3. 后台标签页行为不同

- `setTimeout` 在后台标签页通常只是被降频，不一定完全停。
- `requestAnimationFrame` 在页面不可见时通常会暂停或大幅降频。

所以它更省电，也更符合“只有真正需要渲染时才执行”的思路。

## 为什么动画更适合用它

浏览器的画面更新不是“你改一次 DOM，它就立刻画一次”，而是按自己的渲染节奏统一处理。这个过程可以结合 [[浏览器渲染流程]] 一起看：

1. 执行 JavaScript
2. 处理样式计算
3. 处理布局
4. 处理[[重绘(Repaint)]]
5. 合成并显示到屏幕

而 `requestAnimationFrame` 就插在“浏览器准备绘制前”的关键位置上。

也可以结合 [[渲染更新阶段]] 来记：

- 检查窗口变化
- 检查滚动
- **执行 `requestAnimationFrame` 回调**
- 执行 Style / Layout
- 执行 Paint

这就是它比 `setTimeout` 更适合动画的根本原因：它不是瞎猜时间，而是直接贴着浏览器的渲染节奏执行。

## 它和 [[事件循环 Event loop]] 的关系

很多人会把 `requestAnimationFrame` 误以为是宏任务或微任务，其实更准确地说，它是**渲染前的回调机制**。

可以这样粗略理解一轮浏览器节奏：

1. 执行一个宏任务
2. 清空[[微任务]]
3. 浏览器判断是否需要渲染
4. 如果需要，先执行 `requestAnimationFrame`
5. 再进行样式、布局、绘制
6. 进入下一轮循环

所以它和 `Promise.then`、`setTimeout` 的位置都不一样：

- `Promise.then` 更靠近当前任务末尾
- `setTimeout` 进入未来某一轮任务队列
- `requestAnimationFrame` 挂在“下一次渲染前”

这也是为什么在面试里常会把它和 `Promise.then`、`setTimeout` 放在一起考。

## 典型写法：递归调度动画

`requestAnimationFrame` 默认只执行一次。

如果想持续动画，就要在回调里再次调用自己：

```js
let rafId = null
let x = 0

function step() {
  x += 2
  box.style.transform = `translateX(${x}px)`

  if (x < 300) {
    rafId = requestAnimationFrame(step)
  }
}

rafId = requestAnimationFrame(step)
```

结束时记得清理：

```js
cancelAnimationFrame(rafId)
```

这和 `setInterval` 最大的不同是：不是机械地“每隔多久执行一次”，而是“每一帧需要的时候再继续”。

## 为什么推荐用时间差，而不是每帧固定加 1

如果你写成“每次回调都 `x += 1`”，那在 60Hz 和 120Hz 的设备上，速度会不一样。

更稳的写法是利用 `timestamp` 算时间差：

```js
let rafId = null
let start = null

function step(timestamp) {
  if (start === null) start = timestamp

  const elapsed = timestamp - start
  const progress = Math.min(elapsed / 1000, 1)

  box.style.transform = `translateX(${progress * 300}px)`

  if (progress < 1) {
    rafId = requestAnimationFrame(step)
  }
}

rafId = requestAnimationFrame(step)
```

这样动画速度由“真实时间”决定，而不是由“帧数”决定。

## 和 [[回流(Reflow)]]、[[重绘(Repaint)]] 的关系

`requestAnimationFrame` 并不自动保证性能好，它只是给了你一个“更适合更新视觉状态的时机”。

如果你在回调里做了这些事情，依然可能卡：

- 频繁读取布局信息，如 `offsetTop`、`clientWidth`、`getBoundingClientRect()`
- 紧接着又频繁写样式
- 修改会触发布局的属性，如 `width`、`height`、`top`、`left`

这样仍然可能触发 [[回流(Reflow)]]，继而带来更多[[重绘(Repaint)]]。

所以常见优化思路是：

- 尽量用 `transform`、`opacity` 做动画
- 避免在同一帧里来回“读布局 -> 写样式 -> 再读布局”
- 复杂可见性判断交给 [[Intersection Observer API]]

这也能和 [[为什么有时候用translate来改变位置而不是定位]] 连起来理解。

## 一个很常见的用法：用它做“按帧节流”

当 `scroll`、`resize`、`mousemove` 这种事件高频触发时，如果每次都立刻执行重逻辑，主线程会很忙。

这时可以不用传统时间间隔节流，而是用“每一帧最多执行一次”的方式：

```js
let ticking = false

window.addEventListener("scroll", () => {
  if (ticking) return

  ticking = true

  requestAnimationFrame(() => {
    updateStickyHeader()
    ticking = false
  })
})
```

这种思路和 [[防抖与节流]] 有关系，但它不是按“毫秒间隔”限频，而是按“屏幕帧率”限频。

所以更准确地说，它是一种**渲染对齐型节流**。

## 它不适合什么场景

`requestAnimationFrame` 并不是所有异步调度都该用。

不太适合：

- 纯业务延时逻辑，比如 3 秒后弹 toast
- 轮询接口
- 与视觉刷新无关的异步任务

这类事情仍然更适合 `setTimeout`、`setInterval`，或者更高层的调度方案。

## 和 React 的联系

在 React 里，它经常和下面几个点串起来：

- [[useLayoutEffect]]：它发生在浏览器绘制前，适合做布局测量；而 `requestAnimationFrame` 适合把视觉更新对齐到下一帧。
- [[React需要让函数变得纯粹]]：动画、DOM 操作本质上都属于副作用，不应该塞进渲染函数本体里。
- 高频状态更新场景：有时可以把频繁的外部输入先缓冲，再在 `requestAnimationFrame` 中统一提交一次更新。

你仓库里这段就很贴切：

[[如何实现高性能的 AI 聊天列表]]

它提到可以把流式 token 暂存起来，再借助 `requestAnimationFrame` 按帧刷新 UI，这本质上是在做“数据流速度”和“渲染速度”的解耦。

## 和 [[Intersection Observer API]] 的联系

这两个 API 经常一起出现，但职责不一样：

- `Intersection Observer` 负责判断“元素是否进入视口”
- `requestAnimationFrame` 负责“进入后每一帧怎么更新动画”

所以常见组合是：

1. 用 `Intersection Observer` 作为进入视口的触发器
2. 用 `requestAnimationFrame` 执行真正的逐帧动画

这比在 `scroll` 里手动计算位置再自己驱动动画更符合浏览器的工作方式。

## 面试里很容易被问到的点

### 1. `requestAnimationFrame` 比 `setTimeout(fn, 16)` 好在哪里？

- 它和屏幕刷新同步，不是盲猜 16ms。
- 页面隐藏时会暂停或降频，更省资源。
- 更适合动画和视觉更新。

### 2. 它是不是宏任务？

通常不把它归到传统的宏任务 / 微任务分类里，更准确地说，它是**浏览器渲染前调度的回调**。

### 3. 它是不是一定不会卡？

不是。

如果回调里做了大量计算、强制同步布局、频繁触发 [[回流(Reflow)]] / [[重绘(Repaint)]]，照样会掉帧。

### 4. 为什么动画里最好使用 `transform`？

因为直接改 `left/top/width/height` 更容易触发布局，而 `transform` 往往只影响合成阶段，性能通常更好。详细看：

[[为什么有时候用translate来改变位置而不是定位]]

## 一句话总结

`requestAnimationFrame` 是浏览器提供的“渲染前回调”。它最适合把动画和高频 UI 更新对齐到浏览器下一帧，从而比 `setTimeout` 更平滑、更省资源；但它不是性能银弹，真正的关键仍然是理解 [[事件循环 Event loop]]、[[浏览器渲染流程]]、[[回流(Reflow)]] 和 [[重绘(Repaint)]]。

# reference
