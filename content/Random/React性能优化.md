---
date: 2025-11-29
tags: 
---
# 组件级别优化

- 用 [[React.memo]] 包装函数组件。当父组件更新时，如果子组件的 props 没发生变化，memo 子组件可以跳过重新渲染。更完整的机制可以看 [[构建自己的React#36. React.memo：让没变的子组件跳过重新渲染|构建自己的 React 里的 React.memo 解释]]
- PureComponent:类组件的memo
- children组合模式：将不变的子组件作为children传入，这样即使父组件的state发生变化，传入的children也不会重新渲染

# 数据与函数引用缓存

- [[useMemo]]来缓存计算结果，防止每次渲染都要高开销计算：例如大数组过滤，排序
- [[useCallback]]来缓存函数引用，防止函数每次渲染地址都变，导致接收该函数的子组件（配合 `React.memo` 时）失效而重新渲染。

# 列表渲染优化

- 用唯一且稳定的值作为key，而不是列表的index，这样能帮助diff算法复用dom节点：[[构建自己的React]]
- 虚拟列表：如react-window可以用其渲染仅在视口中的列表

# 加载策略

React.lazy

## 相关笔记

- [[React.memo]]
- [[构建自己的React#36. React.memo：让没变的子组件跳过重新渲染|构建自己的 React：React.memo]]
- [[useMemo]]
- [[useCallback]]
