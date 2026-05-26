---
date: 2026-05-18
tags:
aliases:
---
```ts
type myPick<T,k extends keyof T> = {
	[P in keyof K]:T[P]
} 
```

[[Typescript 类型的高级用法]]

