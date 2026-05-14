---
date: 2026-05-11
tags:
aliases:
---
含义为页面什么时候可以稳定响应用户操作

TTI 测试的前提为：
- 页面已渲染（FCP 已发生）
- 事件监听已绑定
- 主线程空闲（无长任务）

TTI 差的原因：
- JS 任务过重(大 bunlde，长任务阻塞主线程。。。):


优化手段：

（1）代码拆分
（2）减少主线程压力
- Web Worker
- 拆分长任务
（3）[[PRPL 模式]]
- Preload
- Render
- Pre-cache
- Lazy-load
