---
title: Intersection Observer API
date: 2026-04-26
tags:
  - 前端
  - 浏览器
  - React
  - 性能优化
  - 前端实习挑战
aliases:
  - IntersectionObserver
  - IO
---

Intersection Observer API 允许浏览器异步监听一个目标元素与视口，或某个滚动容器之间的交叉关系。它常用于 [[懒加载]]、无限滚动、曝光埋点、进入视口动画，以及和 [[虚拟列表]] 搭配做列表性能优化。

一句话理解：

> 不要在 `scroll` 事件里反复计算元素位置，而是把“元素是否进入可见区域”这件事交给浏览器观察。

它和 [[浏览器渲染流程]] 的关系是：传统写法往往需要在滚动时频繁调用 `getBoundingClientRect()`，如果读写 DOM 混在一起，容易触发 [[回流(Reflow)]] 或造成主线程压力；Intersection Observer 由浏览器统一调度，回调异步执行，更适合做可见性判断。

## 基本用法

核心构造函数：

```js
const observer = new IntersectionObserver(callback, options)
```

`callback` 会在目标元素与观察区域的交叉状态发生变化时执行：

```js
const observer = new IntersectionObserver((entries, observer) => {
  entries.forEach((entry) => {
    if (entry.isIntersecting) {
      console.log("元素进入视口", entry.target)
    }
  })
})

const target = document.querySelector(".target")
observer.observe(target)
```

常用方法：

- `observe(target)`：开始观察某个 DOM 元素。
- `unobserve(target)`：停止观察某个 DOM 元素。
- `disconnect()`：停止观察所有元素，常用于清理。
- `takeRecords()`：取出还没被回调处理的观察记录，业务里较少直接用。

## options 参数

```js
const observer = new IntersectionObserver(callback, {
  root: null,
  rootMargin: "0px 0px 200px 0px",
  threshold: 0.1,
})
```

| 参数         | 含义                           | 常见用法                                                   |
| ------------ | ------------------------------ | ---------------------------------------------------------- |
| `root`       | 指定观察区域，默认为浏览器视口 | 页面滚动时通常设为 `null`；容器内部滚动时传入滚动容器      |
| `rootMargin` | 扩大或缩小观察区域             | 图片快进入视口前提前加载，例如 `200px`                     |
| `threshold`  | 交叉比例达到多少时触发         | `0` 表示刚碰到就触发，`1` 表示完全进入才触发，也可以传数组 |

`threshold` 的例子：

```js
const observer = new IntersectionObserver(callback, {
  threshold: [0, 0.25, 0.5, 0.75, 1],
})
```

这样当目标元素的可见比例跨过这些阈值时，回调就会被触发。

## entry 里有什么

回调里的每个 `entry` 都是一个 `IntersectionObserverEntry`：

```js
const observer = new IntersectionObserver((entries) => {
  const entry = entries[0]

  console.log(entry.target)
  console.log(entry.isIntersecting)
  console.log(entry.intersectionRatio)
})
```

常用字段：

- `target`：被观察的 DOM 元素。
- `isIntersecting`：是否与观察区域发生交叉。
- `intersectionRatio`：可见比例，范围是 `0` 到 `1`。
- `boundingClientRect`：目标元素自身的位置和大小。
- `rootBounds`：观察区域的位置和大小。
- `intersectionRect`：交叉区域的位置和大小。
- `time`：交叉状态发生的时间。

## 场景一：图片懒加载

这和 [[懒加载]] 里的“图片懒加载”是最典型的连接点：图片先不真正请求，等快进入视口时再把 `data-src` 赋值给 `src`。

```html
<img class="lazy-img" data-src="/images/banner.png" alt="banner" />
```

```js
const observer = new IntersectionObserver(
  (entries, observer) => {
    entries.forEach((entry) => {
      if (!entry.isIntersecting) return

      const img = entry.target
      img.src = img.dataset.src
      observer.unobserve(img)
    })
  },
  {
    root: null,
    rootMargin: "200px 0px",
    threshold: 0,
  },
)

document.querySelectorAll(".lazy-img").forEach((img) => {
  observer.observe(img)
})
```

这里的 `rootMargin: "200px 0px"` 表示图片还没真正进入视口，但距离视口 200px 左右时就开始加载，让用户滚到图片位置时更可能已经加载完成。

## 场景二：无限滚动

无限滚动通常会在列表底部放一个“哨兵元素”，观察它是否进入视口。一旦哨兵出现，就触发下一页请求。

```html
<ul id="list"></ul>
<div id="sentinel"></div>
```

```js
const sentinel = document.querySelector("#sentinel")

const observer = new IntersectionObserver((entries) => {
  const entry = entries[0]
  if (!entry.isIntersecting) return

  loadNextPage()
})

observer.observe(sentinel)
```

这个思路可以和 [[React性能优化]]、[[虚拟列表]] 放在一起理解：

- 无限滚动解决“数据分批加载”的问题。
- 虚拟列表解决“DOM 不要一次性渲染太多”的问题。
- Intersection Observer 解决“什么时候触发加载下一页”的问题。

## 在 React 中使用

在 React 中使用 Intersection Observer，本质上是在组件挂载后创建一个浏览器观察器，所以它属于 [[useEffect]] 处理的副作用。DOM 节点一般用 `useRef` 保存，组件卸载时要调用 `disconnect()` 清理。

```tsx
import { useEffect, useRef, useState } from "react"

function LazyImage({ src, alt }: { src: string; alt: string }) {
  const imgRef = useRef<HTMLImageElement | null>(null)
  const [visible, setVisible] = useState(false)

  useEffect(() => {
    const img = imgRef.current
    if (!img) return

    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          setVisible(true)
          observer.unobserve(entry.target)
        }
      },
      {
        root: null,
        rootMargin: "200px 0px",
        threshold: 0,
      },
    )

    observer.observe(img)

    return () => {
      observer.disconnect()
    }
  }, [])

  return <img ref={imgRef} src={visible ? src : undefined} alt={alt} />
}
```

这里要注意两件事：

- 创建 observer 是副作用，不应该写在组件渲染主体里。
- 清理 observer 很重要，否则组件卸载后观察器还可能持有 DOM 引用，造成不必要的内存占用。

## 封装成自定义 Hook

如果多个组件都需要判断“元素是否进入视口”，可以抽象成 [[自定义hook]]。

```tsx
import { RefObject, useEffect, useState } from "react"

type UseIntersectionOptions = IntersectionObserverInit & {
  once?: boolean
}

export function useIntersection<T extends Element>(
  ref: RefObject<T>,
  options: UseIntersectionOptions = {},
) {
  const { once = false, ...observerOptions } = options
  const [entry, setEntry] = useState<IntersectionObserverEntry | null>(null)

  useEffect(() => {
    const target = ref.current
    if (!target) return

    const observer = new IntersectionObserver(([nextEntry]) => {
      setEntry(nextEntry)

      if (once && nextEntry.isIntersecting) {
        observer.unobserve(nextEntry.target)
      }
    }, observerOptions)

    observer.observe(target)

    return () => {
      observer.disconnect()
    }
  }, [ref, once, observerOptions.root, observerOptions.rootMargin, observerOptions.threshold])

  return entry
}
```

使用方式：

```tsx
function LoadMoreTrigger({ onLoadMore }: { onLoadMore: () => void }) {
  const triggerRef = useRef<HTMLDivElement | null>(null)
  const entry = useIntersection(triggerRef, {
    rootMargin: "300px 0px",
  })

  useEffect(() => {
    if (entry?.isIntersecting) {
      onLoadMore()
    }
  }, [entry?.isIntersecting, onLoadMore])

  return <div ref={triggerRef} />
}
```

实际项目里还要考虑 `onLoadMore` 是否稳定，可以用 [[useCallback]] 包一层，避免父组件每次渲染都传入新函数。

## React 场景拆解

### 1. 图片、卡片、模块懒加载

适合首页信息流、图文列表、瀑布流页面。Intersection Observer 负责判断元素是否快出现；真正的资源加载可以配合浏览器原生 `loading="lazy"`，或者业务自己的状态控制。

关联：[[懒加载]]、[[React性能优化]]、[[浏览器缓存策略]]

### 2. 无限滚动分页

适合消息列表、商品列表、发现页。底部哨兵进入视口后，请求下一页。请求状态通常要加保护：

- `isLoading` 为真时不要重复请求。
- `hasMore` 为假时停止观察或不再请求。
- 请求失败时要提供重试入口。

关联：[[虚拟列表]]、[[如何实现高性能的 AI 聊天列表]]、[[Tanstack Store]]

### 3. 曝光埋点

当广告位、推荐卡片、文章模块进入视口时上报曝光。一般会设置 `threshold: 0.5`，表示元素至少露出 50% 才算真正曝光，并且上报后 `unobserve`，避免重复打点。

关联：[[防抖 (Debounce)]]、[[节流 (Throttle)]]、[[性能测试]]

### 4. 进入视口动画

当元素进入视口时添加 class，让 CSS 动画执行。这里最好只把“是否进入视口”作为触发条件，动画本身交给 CSS 或 [[requestAnimationFrame]] 处理。

关联：[[CSS animation]]、[[transition 与 animation属性的区别]]、[[requestAnimationFrame]]

## 常见坑

1. 观察目标必须是真实 DOM 元素，不能直接观察 React 组件本身。
2. 如果 `root` 是滚动容器，容器必须真的产生滚动，通常需要固定高度和 `overflow: auto`。
3. `threshold: 1` 表示完全进入才触发，在元素比视口还大时可能永远达不到。
4. `rootMargin` 可以提前触发，也可以用负值延后触发。
5. React 中要在 `useEffect` 里创建和清理 observer，避免重复创建和内存泄漏。
6. 如果 options 对象每次渲染都重新创建，自定义 Hook 里的 effect 可能频繁重跑，需要用稳定依赖或 `useMemo`。

## 面试回答模板

Intersection Observer API 是浏览器提供的异步可见性观察 API。它可以监听目标元素和视口或指定滚动容器之间的交叉状态，常用于图片懒加载、无限滚动、曝光埋点和进入视口动画。相比手写 `scroll` 监听再调用 `getBoundingClientRect()`，它不需要在高频滚动事件里反复计算位置，浏览器可以统一调度，性能和代码可维护性更好。

在 React 里，它通常和 `useRef`、`useEffect` 一起使用：`useRef` 保存 DOM 节点，`useEffect` 在挂载后创建 observer，并在清理函数里 `disconnect()`。如果多个组件都要复用这套逻辑，可以封装为 `useIntersection` 自定义 Hook。

## 相关笔记

- [[懒加载]]
- [[虚拟列表]]
- [[React性能优化]]
- [[useEffect]]
- [[自定义hook]]
- [[浏览器渲染流程]]
- [[回流(Reflow)]]
- [[requestAnimationFrame]]
- [[防抖与节流]]
