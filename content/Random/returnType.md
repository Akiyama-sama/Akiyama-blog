---
date: 2026-06-17
tags:
aliases:
---


# returnType

## 题目

实现 `ReturnType<T>`，获取函数类型的返回值类型。

```ts
type myReturnType<T> = T extends (...args:any[]) => infer R ? R : never
```

