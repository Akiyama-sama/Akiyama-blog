---
date: 2026-05-19
tags:
aliases:
---
如果说 extends 就像 if else，那么 infer 关键字就像变量声明那样，声明一个变量来记录类型

但出现的场景一般是在 extends 当中的真条件当中，例如

```ts
type Check<T> = T extends 某种待匹配的结构<infer U> ? U : never;
```

[[myReturnType]]这个就是用有 infer 关键字
