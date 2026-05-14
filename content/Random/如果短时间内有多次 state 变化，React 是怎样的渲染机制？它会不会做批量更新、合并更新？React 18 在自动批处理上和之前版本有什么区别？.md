---
date: 2025-11-30
tags:
  - 前端实习挑战
  - 前端
  - React
---
React 针对短时间内的多次状态更新，采用的是 **‘批量更新 (Batching)’** 机制。它会将多个 state 更新推入队列，合并后只触发一次 Render，从而避免不必要的 DOM 操作，提升性能。


- **在 React 17 及之前**：批处理仅在 **React 合成事件**（如 `onClick`）中生效。如果在 `setTimeout`、`Promise` 或原生 `addEventListener` 中更新状态，React 无法自动批处理，会导致**多次渲染**。
    
- **在 React 18 中**：引入了 **Automatic Batching**。只要使用 `createRoot` 初始化应用，无论状态更新在哪里触发（包括异步操作和原生事件），React **默认都会**进行批处理，合并为一次渲染。