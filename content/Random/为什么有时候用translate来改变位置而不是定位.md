---
date: 2025-11-20
tags:
  - #CSS
  - 前端实习挑战
  - 前端
  - CSS
---
translate是[[transition关键字]]中的一个属性，其操作的是渲染层，而不是布局层（例如利用top，left，right，bottom），这样浏览器不会因为位置的改变而重新计算布局（reflow），从而提高性能

且translate可以用到GPU加速，这样在涉及到调整位置的场景下，优先考虑用translate，合理利用 `will-change` 属性，告知浏览器即将发生的一些变化（如 `transform` 或 `opacity` ），预先做一些优化处理，提高动画的流畅度


