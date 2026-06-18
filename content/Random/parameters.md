---
date: 2026-06-17
tags:
aliases:
---

# parameters

## 题目

实现 `Parameters<T>`，获取函数类型的参数，并以元组类型返回。

```ts
type Parameters<T> = T extends (...args:infer P)=> any ? P : never
```

