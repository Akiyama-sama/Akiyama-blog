---
date: 2026-04-30
tags:
  - '#pernamant'
  - Javascript
  - 浏览器
  - 音视频
  - 性能优化
aliases:
  - MediaSource
  - Media Source Extensions
  - MSE
---

这篇笔记的文件名叫 `MediaResource`，但**严格来说，简历里提到的那个 API 实际上是 `MediaSource API`，也就是 `Media Source Extensions (MSE)`**。

一句话理解：

> MSE 允许前端不再只给 `<video>` 一个完整的视频 URL，而是可以把一段一段的媒体二进制数据，主动喂给浏览器播放器。

这也是它特别适合和 [[WebSocket]] 结合的原因。

## 为什么这篇笔记和我的简历有关

它对应的是我简历里的这条经历：

[[前端简历 - v1.2.0#实习经历]]

里面这句最关键：

> 监控点视频播放适配：负责监控点视频播放兼容方案建设，基于 WebSocket + MSE 与海康 SDK 双链路实现多浏览器实时预览、复核场景适配。

所以这篇笔记不只是“API 定义”，更重要的是：

- 这个 API 解决了什么问题
- 为什么它会出现在监控视频播放场景里
- 简历里提到它时，面试官下一步大概率会追问什么

## MSE 到底解决什么问题

普通的 `<video src="xxx.mp4">` 更像是：

- 给浏览器一个完整资源地址
- 浏览器自己决定怎么拉、怎么播

但有些场景需要更细粒度控制，例如：

- 实时流式传输
- 业务层自己决定什么时候追加媒体数据
- 边收边播，而不是整个文件下载完再播
- 根据场景自己管理缓冲区和延迟

这时 MSE 就很有用。

根据 MDN，MSE 的核心作用就是让 JavaScript 创建媒体流，并通过 `<audio>` / `<video>` 播放，而不是只能依赖单个静态 `src` 地址。[MDN 文档](https://developer.mozilla.org/en-US/docs/Web/API/Media_Source_Extensions_API)

## 核心对象

MSE 里最重要的是这几个东西：

### 1. `MediaSource`

它是整个媒体源容器，挂在 `<video>` 上。

你可以把它理解成“浏览器播放器的一个可编程入口”。

### 2. `SourceBuffer`

它是往播放器里真正塞媒体分片的缓冲区。

例如：

- 视频轨一个 `SourceBuffer`
- 音频轨一个 `SourceBuffer`

前提是浏览器支持你传入的容器格式和编解码格式。

### 3. `<video>`

最终播放还是靠标准 HTML 媒体元素，只不过它不再直接指向静态文件 URL，而是接到 `MediaSource`。

## 基本工作流

一个最小思路通常是这样的：

1. 创建 `MediaSource`
2. 把它绑定到 `<video>`
3. 等 `sourceopen`
4. 调用 `addSourceBuffer(mimeCodec)`
5. 持续接收媒体二进制分片
6. 通过 `appendBuffer()` 追加到 `SourceBuffer`
7. 浏览器边缓冲边解码边播放

代码结构大概长这样：

```js
const video = document.querySelector("video")
const mediaSource = new MediaSource()

video.src = URL.createObjectURL(mediaSource)

mediaSource.addEventListener("sourceopen", () => {
  const mimeCodec = 'video/mp4; codecs="avc1.42E01E, mp4a.40.2"'

  if (!MediaSource.isTypeSupported(mimeCodec)) {
    throw new Error("当前浏览器不支持该编码格式")
  }

  const sourceBuffer = mediaSource.addSourceBuffer(mimeCodec)

  socket.onmessage = async (event) => {
    const chunk = await event.data.arrayBuffer()

    if (!sourceBuffer.updating) {
      sourceBuffer.appendBuffer(chunk)
    }
  }
})
```

这里有几个关键点：

- `MediaSource.isTypeSupported()`：先检查浏览器是否支持容器和编码格式
- `addSourceBuffer()`：创建缓冲区
- `appendBuffer()`：把媒体分片塞进去
- `sourceBuffer.updating`：正在追加时不能重复追加，否则很容易报错

相关文档：

- [MediaSource.addSourceBuffer() - MDN](https://developer.mozilla.org/en-US/docs/Web/API/MediaSource/addSourceBuffer)
- [SourceBuffer.appendBuffer() - MDN](https://developer.mozilla.org/en-US/docs/Web/API/SourceBuffer/appendBuffer)

## 为什么它很适合“监控点视频播放适配”

从我的简历描述出发，这里的业务背景大概率是：

- 后端或设备端持续推送视频流
- 前端希望在浏览器里直接播放
- 还要兼顾不同浏览器、不同监控点、不同场景

在这种情况下，`WebSocket + MSE` 很常见，因为它有几个明显优点：

### 1. 可以边收边播

不需要等整个视频文件下载完成。

服务端可以不断把媒体分片推过来，前端收到一段就往 `SourceBuffer` 里 append，一边接收一边播放。

### 2. 适合业务层自己管流

如果视频流不是一个标准静态文件 URL，而是：

- 设备网关转发
- 鉴权后的专用流地址
- 需要业务中间层转码 / 转封装

那 `WebSocket + MSE` 会比单纯 `video.src = xxx` 更灵活。

### 3. 插件依赖更低

很多老监控方案强依赖厂商插件、ActiveX、专有 SDK。

MSE 的价值之一，就是尽可能利用浏览器原生播放能力，把“能走标准 Web 能力的部分”先走通，再对特殊场景保留 SDK 兜底。

这也就解释了我简历里为什么写的是：

- `WebSocket + MSE`
- 海康 SDK 双链路

因为这不是二选一，而更像是：

- 标准浏览器链路优先用 MSE
- 特殊设备 / 特殊协议 / 特殊兼容性问题再走 SDK

## 如果面试官追问“你这个链路具体怎么工作”，可以怎么回答

可以按下面这个顺序讲：

1. 设备流或平台转码流通过 [[WebSocket]] 持续推送到前端
2. 前端创建 `MediaSource` 并挂到 `<video>`
3. 根据流的编码格式创建 `SourceBuffer`
4. 收到媒体二进制分片后按顺序 `appendBuffer`
5. 浏览器解码后在 `<video>` 里播放
6. 如果标准链路不兼容，再切到海康 SDK 方案

如果再往深一点，面试官通常会继续问这些细节。

## 真实落地时最容易踩的坑

### 1. 编码格式不支持

MSE 不是“只要有视频字节流就能播”。

浏览器是否能播，取决于：

- 容器格式
- 编码格式
- 当前浏览器支持情况

所以第一步通常就要做：

```js
MediaSource.isTypeSupported(mimeCodec)
```

这也是为什么监控项目里，经常要做转封装、转码、或者至少做兼容性探测。

### 2. `appendBuffer` 不能乱并发

`SourceBuffer` 在 `updating` 期间不能再次 append。

所以实践里通常要有一个**队列**：

- 收到 chunk 先入队
- 只有在 `updateend` 之后再取下一段继续 append

否则很容易报 `InvalidStateError`。

### 3. 内存和缓冲区会不断膨胀

实时流如果一直 append、不清旧数据，缓冲区会越来越大。

所以直播 / 监控类场景里，常常要主动移除旧时间片段，例如保留最近几十秒：

```js
sourceBuffer.remove(0, oldEndTime)
```

这点在长时间预览场景尤其关键。

### 4. 直播场景要控制延迟

缓冲太多：

- 播放更稳
- 但延迟更大

缓冲太少：

- 延迟更低
- 但更容易卡顿

所以监控视频场景常常不是只要“能播”就行，而是要在**实时性**和**稳定性**之间平衡。

### 5. 断线重连和状态恢复

因为上游通常是实时流，[[WebSocket]] 一断，前端不仅要重连，还要考虑：

- 当前播放器状态是否重建
- 老的 `MediaSource` / `SourceBuffer` 是否清理
- 重连后是否从新 GOP / 新关键帧恢复

这类问题一旦处理不好，就容易出现：

- 黑屏
- 花屏
- 只听到声音看不到画面
- 一直 `append` 但播放器不出帧

## 它和其他技术的边界

### 和普通 `<video src>` 的区别

- `<video src>`：浏览器自己去拉整个资源
- MSE：业务代码自己把媒体分片喂给浏览器

### 和 [[WebRTC]] 的区别

`WebRTC` 更偏真正的实时通信，适合超低延迟互动场景。

MSE 更偏“浏览器可控的流媒体播放”，适合流式媒体分片追加播放。

如果追求极低延迟互动，通常首先想到的是 `WebRTC`；如果是“业务层控制流 + 浏览器播放兼容”，MSE 更常见。

MDN 也明确提到，DASH / MSE 这类方案并不适合真正的实时通信，实时通信更偏向 `WebRTC`。[MDN 文档](https://developer.mozilla.org/en-US/docs/Web/API/Media_Source_Extensions_API)

### 和厂商 SDK 的关系

SDK 方案通常更黑盒，但往往能处理更多厂商私有协议和设备兼容细节。

MSE 方案更标准、更 Web 化，但前提是流格式能被浏览器这一套正确消费。

所以“双链路”本质上是在做：

- 标准能力优先
- 特殊能力兜底

## 这条简历经历，面试官最想听到什么

如果面试官看到我写：

> 基于 WebSocket + MSE 与海康 SDK 双链路实现多浏览器实时预览

他通常不是只想听“我知道 MSE 是个 API”，而是想听我有没有真正做过下面这些事情：

- 我为什么选 MSE
- 视频分片是怎么送到前端的
- 为什么不是直接 `video.src`
- 编码兼容怎么判断
- `SourceBuffer` 队列怎么控
- 长时间播放内存怎么清
- 为什么还需要 SDK 兜底

所以这条经历的真正价值在于：

**我不仅知道 MSE 是什么，而且知道它在真实监控视频项目里，为什么会和 WebSocket、浏览器兼容、缓冲控制、SDK 兜底放在一起出现。**

## 面试版本

- `MediaSource API`，也叫 `Media Source Extensions (MSE)`，允许前端通过 JavaScript 把媒体分片动态喂给 `<video>` / `<audio>` 播放。
- 它的核心对象是 `MediaSource` 和 `SourceBuffer`。
- 常见链路是：[[WebSocket]] 持续推送媒体二进制分片，前端用 `appendBuffer()` 逐段追加，实现边收边播。
- 它适合浏览器内的流式播放、监控预览、业务可控的媒体分发场景。
- 落地难点主要在编码兼容、分片队列控制、缓冲区清理、延迟控制和异常重连。
- 简历里它和海康 SDK 双链路一起出现，说明是在做“标准 Web 播放能力 + 厂商方案兜底”的兼容架构。

## 一句话总结

`MediaSource API / MSE` 的本质，是把“浏览器被动加载完整视频 URL”变成“前端主动向播放器持续喂媒体分片”。它特别适合像我简历里这种 [[WebSocket]] 推流、监控视频预览、多浏览器兼容适配的场景。

# reference
- [MDN: Media Source API](https://developer.mozilla.org/en-US/docs/Web/API/Media_Source_Extensions_API)
- [MDN: MediaSource.addSourceBuffer()](https://developer.mozilla.org/en-US/docs/Web/API/MediaSource/addSourceBuffer)
- [MDN: SourceBuffer.appendBuffer()](https://developer.mozilla.org/en-US/docs/Web/API/SourceBuffer/appendBuffer)
