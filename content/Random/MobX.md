---
date: 2026-05-21
tags:
  - state-management
aliases:
  - MobX
---

## MobX 是什么

MobX 是一个状态管理库，核心思路是：**把状态变成可观察的，状态一变，依赖它的地方自动更新**。

你可以把它理解成“自动追踪依赖的响应式状态管理”。

## 一句话理解

- `state` 是数据
- `observer` 组件会自动订阅这些数据
- 数据变了，界面自己刷新

## 核心概念

### 1. `observable`

可观察状态，类似“被 MobX 管起来的数据”。

### 2. `computed`

派生值，基于现有状态计算出来，适合做缓存后的衍生数据。

### 3. `action`

修改状态的操作，通常把更新逻辑放在这里。

### 4. `observer`

把 React 组件包起来，让组件自动响应状态变化。

## 最小例子

```tsx
import { makeAutoObservable } from "mobx"
import { observer } from "mobx-react-lite"

class CounterStore {
  count = 0

  constructor() {
    makeAutoObservable(this)
  }

  increment() {
    this.count += 1
  }
}

const counterStore = new CounterStore()

const Counter = observer(() => {
  return (
    <button onClick={() => counterStore.increment()}>
      {counterStore.count}
    </button>
  )
})
```

## 使用流程

1. 定义一个 store
2. 用 `makeAutoObservable` 让它变成响应式
3. 在组件里读取状态
4. 用 `observer` 包裹组件
5. 修改状态时界面自动更新

## 和 Redux 的区别

- MobX 更像“自动响应式”
- Redux 更像“显式状态流转”
- MobX 上手更快，写法更自由
- Redux 约束更强，适合更统一的大型状态流

## 适合场景

- 表单状态
- 页面局部状态
- 需要快速开发的中小型项目

## 注意点

- 不要把所有状态都塞进全局 store
- 只把“多个组件共享、会频繁变化”的状态放进 MobX
- 复杂项目里也要保持状态边界清晰

## 先记住这句话

**MobX 的重点不是“怎么手动通知更新”，而是“让状态变化自动驱动 UI 更新”。**
