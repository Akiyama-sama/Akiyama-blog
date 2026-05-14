---
date: 2026-05-10
tags:
aliases:
---
用来闭包那些不渲染的变量，例如 setTimeout 的 id 或者等等这些，用来将这个变量脱离于 React 生命周期存在

特性：
- 修改ref.current 时同步修改，而非 useState 把它放在 hook 数组当中，等到下一次 render 阶段渲染

