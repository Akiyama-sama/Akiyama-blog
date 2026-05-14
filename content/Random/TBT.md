---
date: 2026-05-11
tags:
aliases:
---
TBT 衡量：

从 [[首次内容绘制（FCP）|FCP]] 到 [[TTI]] 期间，主线程被阻塞的总时间

规则：

- 单个任务 > 50ms → 视为“长任务”
- 超出部分计入 TBT


**优化手段**

（1）拆分长任务
- [[requestIdleCallback]]
- [[requestAnimationFrame]]

（2）减少 DOM 操作

（3）减少 JS 体积

- Tree shaking
- 删除无用代码
- 控制第三方脚本