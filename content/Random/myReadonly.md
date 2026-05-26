---
date: 2026-05-18
tags:
aliases:
---
```ts
type MyReadonly<T> = {
  readonly [P in keyof T]: T[P];
};
```