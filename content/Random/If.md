---
date: 2026-05-19
tags:
aliases:
---
实现一个工具类型 `If<C, F T,>`，接收一个布尔值类型 `C`（`true` 或 `false`）。如果 `C` 是 `true`，返回类型 `T`；如果 `C` 是 `false`，返回类型 `F`。


```ts
type If<C extends boloan,T,F> = C extends true ? T : F
```

# If

## 题目

If