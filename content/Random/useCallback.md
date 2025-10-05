---
tags:
  - '#pernamant'
---
useCallback 是一个用于性能优化的Hook，可以用于缓存调用的函数，只有依赖值发生变化，才会更新调用的函数，避免每次渲染时创建新的函数

## 基本语法
```ts
const memoizedCallback = useCallback(
  () => {
    doSomething(a, b);
  },                    
  [a, b],
);
```
第一个参数为要缓存的[[回调函数]]
第二个参数是依赖数组，当依赖值发生变化才会更新缓存的函数

工作原理
- 组件首次渲染时，React会创建回调函数并返回其引用
- 后续渲染时，如果依赖数组没有变化，继续返回之前缓存的回调函数
- 如果依赖数组发生变化，React会创建新的回调函数并缓存
## 与[[useMemo]]的区别
useCallback和useMemo都是用于优化性能的Hook，它们的区别在于：
```typescript
// useCallback缓存函数引用
const memoizedCallback = useCallback(() => {
  doSomething(a, b);
}, [a, b]);
// useMemo缓存函数执行结果
const memoizedValue = useMemo(() => {
  return computeExpensiveValue(a, b);
}, [a, b]);
```


# reference
[[useCallback AI讲解]]