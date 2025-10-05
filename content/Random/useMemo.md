---
tags:
  - '#pernamant'
---
useMemo的基本语法如下：

```typescript
const memoizedValue = useMemo(() => computeExpensiveValue(a, b), [a, b]);
```
- 第一个参数是一个函数，返回需要被缓存的值
- 第二个参数是依赖项数组，只有当依赖项发生变化时，useMemo才会重新计算
- useMemo会在渲染期间执行，而不是在渲染之后

useMemo的工作原理：
1. 在组件首次渲染时，React会执行传入useMemo的函数，并缓存其返回值
2. 在后续渲染中，如果依赖项没有变化，React会直接返回缓存的值，而不会重新执行函数
3. 如果依赖项发生变化，React会重新执行函数，并缓存新的返回值


# reference