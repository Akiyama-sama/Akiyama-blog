---
date: 2026-05-18
tags:
aliases:
---
给你一个由「字面量」组成的元组（数组），你需要写一个工具类型，把这个元组里的每个元素，同时变成新对象的「键（Key）」和「值（Value）」。

我们想**获取元组中所有元素的值组成的联合类型**，就要使用 `T[number]`

```ts

type TupleToObject<T extends readonly any[] > = {
	[P in T[Number]]: P
}
```