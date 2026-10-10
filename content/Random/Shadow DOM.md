---
date: 2026-10-01
tags:
aliases:
---
Shadow DOM（阴影 DOM）是 Web Components 规范四大核心技术之一（其余为 Custom Elements、HTML Templates 和 ES Modules）。

它的核心作用是**封装**：允许你将一棵独立的 DOM 树附加到一个元素上，这棵树内部的结构（HTML）**和**样式（CSS）会与外部的主文档完全隔离，互不干扰。

Shadow DOM 引入了几术语：

```
主文档 (Light DOM)
  └─ <div id="host">   <--- Shadow Host (宿主元素)
       │
       └── #shadow-root (open) <--- Shadow Root (根节点，隔离边界)
             ├── <style> ... </style> <--- 局域样式 (不外溢，不被外浸)
             └── <button class="btn">Click</button> <--- Shadow Tree (阴影树)
```

- **Shadow Host（宿主）**：普通的 Light DOM 节点（如一个 `<div>`），Shadow DOM 挂载在其之下。
- **Shadow Root（根节点）**：Shadow DOM 树的入口节点，是**隔离边界的起点**。
- **Shadow Tree（阴影树）**：挂载在 Shadow Root 下面的完整 DOM 子树。