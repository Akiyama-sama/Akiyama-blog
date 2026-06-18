---
date: 2026-06-17
tags:
aliases:
---


# includes

## 题目

实现一个类型版 `Array.includes`，判断元组中是否包含某个元素类型，返回 `true` 或 `false`。


```ts
type MyIncludes<T extends readonly any[], F> =
  T extends [infer First, ...infer Rest]
    ? [First] extends [F]
      ? true
      : MyIncludes<Rest, F>
    : false;
```



