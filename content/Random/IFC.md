---
date: 2025-11-22
tags:
  - CSS
  - 前端实习挑战
  - 前端
---
Inline Formatting Context行内上下文

**触发元素与子元素之间的相互影响**

- 子元素水平排列    
- 子元素（如 `<span>`, `<a>`）的 `margin-top` 和 `margin-bottom` 不会撑开行框的高度，高度主要由内部元素的 `line-height` 和 `font-size` 决定。 
- 子元素在水平方向上受 `text-align` 属性控制（left, center, right, justify）。

**触发元素与兄弟元素之间的相互影响**

- 如果兄弟元素为浮动元素，那么触发元素里面的字内容会环绕着兄弟元素
- IFC 容器本身通常是一个块级容器，它与其兄弟元素的关系遵循块级布局规则。

**触发规则**

- 自动触发：一个块级元素

