---
tags:
  - 
  - 前端实习挑战
  - 前端
  - HTML
aliases:
  - FCP
---

FCP是网页开始呈现任何内容（图片、文本等等）的时间

FCP 差的原因本质上是：
- 服务端返回js/css 文件时间过长
- js/css 文件执行阻塞[[渲染进程]]当中的GUI 线程
- 字体加载导致文字不可见

解决方案：

- JS 加 `defer / async`
- CSS 提取关键 CSS + 延迟加载非关键 CSS
- JS 代码拆分
- 避免 FOIT，优先展示系统字体（降级字体处理）



# reference
