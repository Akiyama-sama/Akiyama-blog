---
date: 2025-11-22
tags:
  - CSS
---
全称为Block Formatting Context块级上下文

**特性**：
- 内部block会垂直一个一个放置
- 同一个BFC上下文会发生外边距折叠，不同BFC的元素不会发生这样的折叠
- BFC 就像是一个隔离的作用域，其内部元素的布局不会影响到外部
- BFC 会包含浮动元素（清除浮动）：BFC在计算自身高度时，会将内部的浮动元素（`float`）也计算在内。

# 触发条件
- 根元素（）
- 浮动元素（float 不为 none）
- 绝对定位元素（position 为 absolute 或 fixed）
- 行内块元素（display: inline-block）
- 表格单元格（display: table-cell，表格默认）
- 弹性盒子（display: flex / inline-flex）
- 网格布局（display: grid / inline-grid）
- overflow 值为 hidden、auto、scroll（不为 visible）
- display: flow-root（专门用于创建无副作用的 BFC）
