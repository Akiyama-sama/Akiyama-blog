---
date: 2026-05-03
tags:
  - 前端实习挑战
  - 前端
  - CSS
aliases:
---
这个为[[Flex]]的子属性，其作用是在计算[[FFC]]里面子容器宽度，以及剩余宽度时所参照的一个变量

flex 子元素里面宽度的优先级取值：

1. min-with/max-with
2. flex-basis
3. with

这里的 flex-basis 就是其中一个参照值，这个值就用来计算剩余宽度的

$$\text{剩余空间} = \text{父元素主轴宽度} - \sum(\text{每个子元素的 flex-basis})$$

