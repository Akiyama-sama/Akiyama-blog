---
date: 2026-04-30
tags:
  - '#pernamant'
  - Javascript
  - 浏览器
  - 图形
  - 性能优化
---

`Canvas` 是 HTML5 提供的一个**位图绘图区域**，可以通过 JavaScript 在这个区域里动态绘制图形、图片、文字和动画。

一句话理解：

> `Canvas` 更像一块“画布”，你拿着画笔往上画；画完之后，浏览器只保留结果，不保留你画图时的每个“图形对象”。

## 基本概念

最常见的写法：

```html
<canvas id="myCanvas" width="300" height="150"></canvas>
```

```js
const canvas = document.getElementById("myCanvas")
const ctx = canvas.getContext("2d")
```

- `canvas` 元素：页面上的画布容器
- `getContext("2d")`：获取 2D 绘图上下文
- `ctx`：真正用来画图的对象

也就是说，`canvas` 本身只是一个标签，真正干活的是 `CanvasRenderingContext2D`。

## Canvas 的核心特点

- 它是**基于像素**绘制的。
- 它是**命令式**绘图，不是声明式描述。
- 它更适合频繁变化的图形，比如动画、游戏、数据可视化。
- 画上去的内容默认不会自动保存“对象结构”，你需要自己管理状态。

这也是它和 [[Canvas 和 SVG 有什么区别？]] 的根本分界点：

- `Canvas` 更像“直接画”
- `SVG` 更像“用标签描述图形”

## 为什么说它是“即时绘制”

例如你执行：

```js
ctx.fillStyle = "red"
ctx.fillRect(10, 10, 100, 100)
```

这不是创建了一个“红色矩形节点”，而是直接把对应像素画到了画布上。

之后如果你想移动这个矩形，不是像操作 DOM 那样改它的 `style`，而通常是：

1. 清空画布
2. 重新计算新位置
3. 再画一遍

所以 `Canvas` 的思路更接近“每一帧重绘整个场景”。

## 常见使用场景

- 图表、数据可视化
- 白板、画板、签名板
- 小游戏
- 粒子效果、复杂动画
- 图片编辑、裁剪、滤镜处理

如果只是：

- Logo
- Icon
- 简单矢量图
- 需要无损缩放的图形

那很多时候 [[Canvas 和 SVG 有什么区别？]] 里提到的 `SVG` 会更合适。

## 常用 API

### 1. 画矩形

```js
ctx.fillStyle = "skyblue"
ctx.fillRect(20, 20, 120, 80)

ctx.strokeStyle = "navy"
ctx.strokeRect(20, 20, 120, 80)

ctx.clearRect(30, 30, 20, 20)
```

- `fillRect`：填充矩形
- `strokeRect`：绘制矩形边框
- `clearRect`：清空某块区域

### 2. 路径绘图

```js
ctx.beginPath()
ctx.moveTo(50, 50)
ctx.lineTo(150, 50)
ctx.lineTo(100, 120)
ctx.closePath()
ctx.stroke()
ctx.fill()
```

常见路径 API：

- `beginPath()`
- `moveTo()`
- `lineTo()`
- `arc()`
- `closePath()`
- `stroke()`
- `fill()`

### 3. 绘制文字

```js
ctx.font = "24px serif"
ctx.fillStyle = "#333"
ctx.fillText("Hello Canvas", 20, 50)
```

### 4. 绘制图片

```js
const img = new Image()
img.src = "/demo.png"

img.onload = () => {
  ctx.drawImage(img, 0, 0, 200, 120)
}
```

`drawImage` 是很重要的 API，因为很多图片处理、本地截图、裁剪、缩放，都会围绕它展开。

## Canvas 的坐标系

默认情况下：

- 原点在左上角
- 向右是 `x` 正方向
- 向下是 `y` 正方向

这和很多数学坐标系不一样，所以做图形计算时要注意。

## Canvas 的状态机

`ctx` 其实维护着一套“当前绘图状态”，比如：

- 当前颜色
- 当前线宽
- 当前透明度
- 当前变换矩阵
- 当前阴影

例如：

```js
ctx.fillStyle = "red"
ctx.fillRect(0, 0, 50, 50)

ctx.fillRect(60, 0, 50, 50)
```

第二个矩形也会继续使用红色，因为绘图状态会延续。

可以用下面两个 API 临时保存和恢复状态：

```js
ctx.save()
ctx.translate(100, 100)
ctx.rotate(Math.PI / 4)
ctx.restore()
```

- `save()`：保存当前状态
- `restore()`：恢复到上一次保存的状态

这在复杂图形、组件化绘制、动画里非常常见。

## 和 DOM 的一个重要区别

`Canvas` 画上去的图形通常**不是独立 DOM 节点**。

这意味着：

- 你不能直接给“画出来的圆形”绑定 `onclick`
- 你不能像操作普通元素一样给每个图形加 CSS
- 你需要自己管理图形数据、重绘逻辑、命中测试

这一点和我们平时基于 DOM 的交互思路差别很大，也和 [[事件委托]] 这类“事件沿 DOM 树传播”的机制不同。

## Canvas 和浏览器渲染流程的关系

`Canvas` 最终当然还是要显示到页面上，所以它也在 [[浏览器渲染流程]] 里。

但它和普通 DOM 元素的区别在于：

- DOM 场景下，你常常在改“结构”或“样式”
- Canvas 场景下，你更多是在改“像素结果”

通常来说：

- 改动画布内容，主要影响[[重绘(Repaint)]]
- 如果改的是 `canvas.width`、`canvas.height` 或影响布局的样式，仍然可能触发[[回流(Reflow)]]

所以 `Canvas` 不等于“完全没有重排重绘问题”，只是问题形式不一样。

也可以结合 [[回流和重绘]]、[[如何减少回流以及重绘]] 一起理解。

## Canvas 动画为什么经常搭配 [[requestAnimationFrame]]

因为 `Canvas` 动画通常是：

1. 清空上一帧
2. 更新状态
3. 重新绘制当前帧

这天然适合交给 [[requestAnimationFrame]] 来驱动。

一个最基础的动画例子：

```js
let x = 0

function render() {
  ctx.clearRect(0, 0, canvas.width, canvas.height)

  ctx.fillStyle = "tomato"
  ctx.fillRect(x, 40, 50, 50)

  x += 2

  if (x < 250) {
    requestAnimationFrame(render)
  }
}

requestAnimationFrame(render)
```

这和普通 DOM 动画的思路不同：

- DOM 动画常常是“改某个元素的属性”
- Canvas 动画常常是“整帧重画”

所以在高频更新图形时，Canvas 和 [[requestAnimationFrame]] 往往是强绑定出现的。

## 一个很容易忽略的点：画布尺寸和 CSS 尺寸不是一回事

下面这两种写法意义不同：

```html
<canvas width="300" height="150"></canvas>
```

```css
canvas {
  width: 300px;
  height: 150px;
}
```

- HTML 属性里的 `width` / `height` 决定**画布像素缓冲区大小**
- CSS 里的 `width` / `height` 决定**显示尺寸**

如果两者不匹配，图像可能会被拉伸，或者在高分屏下显得发糊。

所以 Canvas 清晰度问题，经常会和设备像素比一起讨论。

## Canvas 的性能注意点

### 1. 不要每次都创建大量对象

高频动画场景里，频繁创建临时对象会增加 GC 压力。

### 2. 减少不必要的全量重绘

虽然很多 Canvas 动画会整帧重画，但如果场景很复杂，也可以考虑只重绘脏区域。

### 3. 复杂动画优先考虑和帧率同步

这就是为什么它常和 [[requestAnimationFrame]] 搭配。

### 4. 减少昂贵绘制操作

比如：

- 过多阴影
- 过多路径
- 过大的透明叠加
- 超大尺寸图片反复缩放

### 5. 注意主线程压力

Canvas 的 2D 绘制通常仍然发生在前端主线程参与的渲染链路里，如果你一边做大量 JS 计算，一边还要高频画图，仍然会卡顿。

这可以和 [[渲染进程]]、[[事件循环 Event loop]] 放在一起理解。

## Canvas 的局限

- 放大后会失真，因为它是位图。
- 图形本身没有天然语义。
- 交互命中、拖拽、选中等逻辑要自己做。
- SEO 和可访问性不如普通 DOM / SVG 自然。

所以它很强，但不是所有图形问题都该用它。

## Canvas 和 SVG 怎么选

可以用一个简单思路判断：

- **图形是否复杂且需要高频更新？**
  - 是：更偏向 `Canvas`
- **图形是否需要无损缩放、结构清晰、便于 DOM/CSS 控制？**
  - 是：更偏向 `SVG`

更完整的对比看：

[[Canvas 和 SVG 有什么区别？]]

## 面试版本

- `Canvas` 是 HTML5 提供的位图绘图方案，本质是通过 JavaScript 在一块像素画布上进行即时绘制。
- 它是命令式、基于像素的，更适合游戏、数据可视化、粒子效果、画板这类高频更新场景。
- `Canvas` 画出的内容通常不是独立 DOM 节点，所以事件、状态、命中检测、重绘逻辑往往都要自己管理。
- Canvas 动画通常搭配 [[requestAnimationFrame]]，因为它天然符合“清空上一帧 -> 更新状态 -> 绘制下一帧”的节奏。
- 它和 `SVG` 的核心区别是：`Canvas` 偏位图和性能，`SVG` 偏矢量和结构化。

## 一句话总结

`Canvas` 是浏览器里的一块可编程像素画布。它适合高频图形更新和复杂动画，但代价是你要自己负责状态管理、命中检测和重绘策略；真正想把它用好，往往还要配合理解 [[requestAnimationFrame]]、[[浏览器渲染流程]]、[[重绘(Repaint)]] 和 [[回流(Reflow)]]。

# reference
