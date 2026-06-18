---
date: 2026-05-18
tags:
aliases:
---
实现一个工具类型，接收一个元组 `T`，并返回这个元组的第一个元素的类型。如果是空元组，则返回 `never`。

```ts
type FirstOfArray<T extends any[]> = T extends [] ? never : T[0]

```



# first of Array

## 题目

first of Array