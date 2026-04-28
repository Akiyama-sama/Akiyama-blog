---
date: 2026-04-26
tags:
  - React
  - 性能优化
---

# React.memo

`React.memo` 是 React 提供的一个组件级性能优化工具。

一句话理解：

> `React.memo` 可以让函数组件在 `props` 没有变化时，跳过这次重新渲染。

如果你是从 [[构建自己的React]] 过来的，可以把它理解成：

> diff 解决的是“已经重新渲染后，DOM 怎么少改”；`React.memo` 解决的是“如果子组件输入没变，能不能连子组件函数都少执行一次”。

相关位置：[[构建自己的React#36. React.memo：让没变的子组件跳过重新渲染|React.memo：让没变的子组件跳过重新渲染]]。

---

## 1. React.memo 解决什么问题

默认情况下，只要父组件重新渲染，子组件通常也会跟着重新执行。

```tsx
function Parent() {
  const [count, setCount] = useState(0)

  return (
    <div>
      <button onClick={() => setCount(count + 1)}>+1</button>
      <Child name="Akiyama" />
    </div>
  )
}

function Child({ name }) {
  console.log("Child render")
  return <p>{name}</p>
}
```

当点击按钮时，`count` 变化，`Parent` 重新渲染。

但 `Child` 收到的 `name` 一直是 `"Akiyama"`，理论上它的结果不会变。

如果 `Child` 很简单，重新执行一次没什么问题。

但如果 `Child` 很重，比如：

- 渲染很多列表项。
- 做复杂计算。
- 包含大量子组件。
- 频繁被父组件带着更新。

那这些“不必要的重新渲染”就可能变成性能问题。

---

## 2. 基本用法

用 `React.memo` 包住函数组件：

```tsx
const Child = React.memo(function Child({ name }) {
  console.log("Child render")
  return <p>{name}</p>
})
```

现在当父组件重新渲染时，React 会先比较 `Child` 的新旧 `props`。

```text
旧 props：{ name: "Akiyama" }
新 props：{ name: "Akiyama" }
  ↓
props 没变
  ↓
跳过 Child 重新渲染
```

如果 `props` 变了：

```text
旧 props：{ name: "Akiyama" }
新 props：{ name: "Luna" }
  ↓
props 变了
  ↓
重新执行 Child
```

---

## 3. React.memo 和 diff 的区别

这两个概念很容易混在一起。

| 机制 | 解决的问题 | 发生位置 |
| --- | --- | --- |
| diff / reconciliation | 新旧节点怎么比较，DOM 怎么少更新 | 渲染和提交更新过程中 |
| `React.memo` | 子组件 props 没变时，能不能跳过子组件重新执行 | 子组件重新渲染前 |

可以这样理解：

```text
没有 React.memo：
父组件更新
  ↓
子组件函数重新执行
  ↓
生成新的子树
  ↓
diff 比较新旧子树
  ↓
尽量少改 DOM
```

```text
有 React.memo 且 props 没变：
父组件更新
  ↓
比较子组件 props
  ↓
发现 props 没变
  ↓
跳过子组件函数执行
  ↓
也不用继续比较这部分子树
```

所以 `React.memo` 更像是一个“子树级别的提前刹车”。

这也是它和 [[构建自己的React#29. 为什么需要比较新旧节点|新旧 Fiber 比较]] 的关系。

---

## 4. 默认是浅比较

`React.memo` 默认使用浅比较。

浅比较的意思是：只比较第一层值是否相同。

```tsx
<Child name="Akiyama" age={18} />
```

这种 primitive 值比较很稳定：

```text
"Akiyama" === "Akiyama"
18 === 18
```

但对象、数组、函数比较的是引用：

```tsx
<Child user={{ name: "Akiyama" }} />
```

每次父组件渲染时，都会创建一个新对象：

```text
旧 user：{ name: "Akiyama" }
新 user：{ name: "Akiyama" }
旧 user !== 新 user
```

虽然内容看起来一样，但引用变了，所以 `React.memo` 会认为 props 变了。

函数也是一样：

```tsx
<Child onClick={() => console.log("click")} />
```

每次渲染都会创建一个新的函数引用。

---

## 5. 为什么经常要配合 useMemo 和 useCallback

如果传给 memo 子组件的是对象或数组，可以用 [[useMemo]] 稳定引用：

```tsx
function Parent({ name }) {
  const user = useMemo(() => {
    return { name }
  }, [name])

  return <Child user={user} />
}

const Child = React.memo(function Child({ user }) {
  return <p>{user.name}</p>
})
```

如果传给 memo 子组件的是函数，可以用 [[useCallback]] 稳定引用：

```tsx
function Parent() {
  const handleClick = useCallback(() => {
    console.log("click")
  }, [])

  return <Child onClick={handleClick} />
}

const Child = React.memo(function Child({ onClick }) {
  return <button onClick={onClick}>Click</button>
})
```

三者关系可以这样记：

```text
React.memo：缓存组件结果
useMemo：缓存计算结果或对象引用
useCallback：缓存函数引用
```

更多整体策略可以看 [[React性能优化]]。

---

## 6. 自定义比较函数

`React.memo` 可以传第二个参数，自定义比较逻辑：

```tsx
const Child = React.memo(
  function Child({ user }) {
    return <p>{user.name}</p>
  },
  (prevProps, nextProps) => {
    return prevProps.user.id === nextProps.user.id
  },
)
```

这个函数返回值的含义很容易记反：

```text
返回 true：认为 props 没变，跳过重新渲染
返回 false：认为 props 变了，需要重新渲染
```

也就是说，它和 `shouldComponentUpdate` 的含义刚好相反。

`shouldComponentUpdate` 是：

```text
返回 true：需要更新
返回 false：跳过更新
```

`React.memo` 的自定义比较函数是：

```text
返回 true：相等，跳过更新
返回 false：不相等，需要更新
```

---

## 7. 什么时候适合用 React.memo

适合使用的场景：

- 子组件渲染成本比较高。
- 父组件经常更新，但子组件 props 经常不变。
- 子组件接收的 props 比较稳定。
- 大列表、复杂卡片、图表、编辑器等重组件。

不太适合的场景：

- 子组件非常简单。
- props 每次都会变化。
- 为了 memo 还要写很多复杂比较逻辑。
- 没有真实性能问题，只是提前焦虑。

原因是 `React.memo` 本身也有成本：

```text
每次父组件更新
  ↓
React.memo 要比较 props
  ↓
比较本身也需要时间
```

如果组件本来就很轻，比较成本可能比重新渲染还不划算。

---

## 8. 常见误区

### 误区一：React.memo 能阻止组件内部 state 更新

不能。

```tsx
const Counter = React.memo(function Counter() {
  const [count, setCount] = useState(0)

  return <button onClick={() => setCount(count + 1)}>{count}</button>
})
```

点击按钮时，`Counter` 自己的 state 变了，它还是会重新渲染。

`React.memo` 只比较父组件传进来的 `props`，不能阻止组件自己的 state 更新。

### 误区二：React.memo 能阻止 context 更新

不一定。

如果组件内部读取了 context，当 context 值变化时，组件仍然可能重新渲染。

### 误区三：用了 React.memo 就一定更快

不一定。

它只是增加了一个“props 比较关卡”。如果比较成本高，或者 props 总是变，那收益就很小。

---

## 9. 最小心智模型

最后用一句话总结：

> `React.memo` 是函数组件的 props 级缓存：父组件更新时，如果 memo 子组件的新旧 props 浅比较没变，就跳过这个子组件的重新渲染。

更短一点：

```text
props 没变 → 跳过
props 变了 → 重渲染
```

它适合和 [[useMemo]]、[[useCallback]] 一起理解，也属于 [[React性能优化]] 的组件级优化。
