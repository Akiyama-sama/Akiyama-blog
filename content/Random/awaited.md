---
date: 2026-05-19
tags:
aliases:
---
用来剥开外层的 Promise，拿到内部的真正数据

```ts
type myAwaited<T> = T extends Promise<infer U> ? U : myAwaited<U>
```

这里用到了[[infer]]关键字以及递归

