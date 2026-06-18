---
date: 2026-06-17
tags:
aliases:
---


# concat

## 题目

实现一个类型版 `Array.concat`，接收两个数组/元组类型，并返回合并后的新数组类型。

```ts
type MyConcat<T extends any[],F extends any[]> = [...T,...F]
```