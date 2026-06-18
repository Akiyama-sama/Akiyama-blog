---
date: 2026-06-17
tags:
aliases:
---


# myReadonly2

## 题目

实现增强版 [[myReadonly]]，可以指定某些键变成只读；如果不传键，则默认全部只读。

 先看有没有传 Key，没有就全部只读，也就是[[myReadonly]]的写法，如果有这个 key，就指定这个 key 只读

```ts
// 需要 readonly 的部分
type R1<T, K> = {
  readonly [P in K]: T[P]
}

// 不需要 readonly 的部分
type R2<T, K> = {
  [P in Exclude<keyof T, K>]: T[P]
}

// 合并

type MyReadonly<T, K = keyof T> = R1<T, K> & R2<T, K>
```