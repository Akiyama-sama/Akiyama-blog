---
date: 2025-11-30
tags:
  - React
  - 前端实习挑战
  - 前端
  - CSS
---
Flex 布局显示声明这个容器启用[[FFC]]

flex 是一个复合属性，包含三个子属性：flex-grow、flex-shrink 和 flex-basis。

- flex-grow：定义项目的放大比例，默认为0，即不放大。设为1时表示可伸展以填充剩余空间。
- flex-shrink：定义项目的缩小比例，默认为1，表示空间不足时可被压缩。
- [[flex-basis]]：定义项目在分配多余空间之前的初始主轴尺寸，类似于设置 width，但作用于主轴方向。值为 0% 时，表示不考虑原有尺寸，完全由剩余空间重新分配。

缩写
- flex:1  即 flex: 1,1,0%的缩写
- flex:auto 即 flex:1,1,auto 的缩写