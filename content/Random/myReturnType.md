---
date: 2026-05-19
tags:
aliases:
---
获取函数返回值的类型

```ts
type myReturnType<T> = T extends (...args:any[]) => infer R ? R : never
```

