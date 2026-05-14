---
date: 2025-11-29
tags:
  - React
  - 前端实习挑战
  - 前端
---
useLayoutEffect相较于useEffect，他自己的setup函数是在浏览器绘制之前执行的，而useEffect是在挂载之后执行的，详细看[[浏览器渲染流程]]

useLayoutEffect在绘制之前执行意味着这是一段同步代码，会阻塞浏览器渲染，因此只用到一些特殊场景，而useEffect的setup函数是异步执行，不阻塞浏览器渲染


一般用于需要计算布局位置来决定渲染数据的逻辑，例如

想象一下悬停时出现在某个元素旁边的 tooltip。如果有足够的空间，tooltip 应该出现在元素的上方，但是如果不合适，它应该出现在下面。为了让 tooltip 渲染在最终正确的位置，你需要知道它的高度（即它是否适合放在顶部）。

要做到这一点，你需要分两步渲染：

1. 将 tooltip 渲染到任何地方（即使位置不对）。
2. 测量它的高度并决定放置 tooltip 的位置。
3. 把 tooltip 渲染放在正确的位置。

**所有这些都需要在浏览器重新绘制屏幕之前完成**。你不希望用户看到 tooltip 在移动。调用 `useLayoutEffect` 在浏览器重新绘制屏幕之前执行布局测量：




# reference
https://zh-hans.react.dev/reference/react/useLayoutEffect