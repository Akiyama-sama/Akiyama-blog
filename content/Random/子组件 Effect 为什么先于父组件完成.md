---
date: 2026-04-26
tags:
  - React
  - useEffect
  - 前端实习挑战
  - 前端
---

# 子组件 Effect 为什么先于父组件完成

这篇笔记详细解释一个 React 里很容易让人困惑的现象：

> 子组件的 `useEffect` 通常会先于父组件的 `useEffect` 执行。

如果你是在看 [[构建自己的React]]，可以先记住简化结论：

> React 提交 effect 时，会沿着 Fiber 树做深度优先遍历，并且在这个阶段先处理子 Fiber，再处理父 Fiber。

---

## 1. 先看现象

假设有这样一段代码：

```tsx
function Parent() {
  useEffect(() => {
    console.log("Parent effect")
  }, [])

  return <Child />
}

function Child() {
  useEffect(() => {
    console.log("Child effect")
  }, [])

  return <div>Child</div>
}
```

很多人第一反应是：

```text
Parent effect
Child effect
```

因为从代码结构上看，`Parent` 包着 `Child`，似乎父组件应该更早完成。

但实际常见输出是：

```text
Child effect
Parent effect
```

这不是因为子组件先渲染，也不是因为 `useEffect` 有特殊的“子优先规则”。

真正原因要从 Fiber 树的遍历顺序说起。

---

## 2. 渲染阶段和提交阶段不是一回事

React 更新大致可以分成两个阶段：

```text
render 阶段
  ↓
计算新的 Fiber 树
  ↓
commit 阶段
  ↓
把变化提交到 DOM，并执行 effect
```

在 `render` 阶段，React 会执行函数组件，得到新的 UI 描述。

在 `commit` 阶段，React 才会：

- 插入、更新、删除 DOM。
- 执行 layout effect。
- 安排并执行 passive effect，也就是普通 `useEffect`。

所以要理解 `useEffect` 的顺序，重点不是看组件函数谁先被调用，而是看：

> commit 阶段是按照什么顺序遍历 Fiber 树并提交 effect 的。

---

## 3. Parent 和 Child 会形成一棵 Fiber 树

上面的组件大致会形成这样的 Fiber 结构：

```text
Parent Fiber
  ↓ child
Child Fiber
  ↓ child
div Fiber
```

每个 Fiber 都可以理解为一个工作单元。

它们之间通过几个指针连起来：

```ts
type Fiber = {
  parent: Fiber | null
  child: Fiber | null
  sibling: Fiber | null
}
```

也就是：

- `parent` 指向父 Fiber。
- `child` 指向第一个子 Fiber。
- `sibling` 指向下一个兄弟 Fiber。

这和 [[构建自己的React#7. Fiber 是什么|Fiber 是什么]] 里的结构是同一套心智模型。

---

## 4. Fiber 遍历通常是深度优先

React 处理 Fiber 树时，经常使用深度优先遍历。

深度优先的意思是：

```text
先一路往子节点走到底
  ↓
子节点处理完
  ↓
再回到父节点
  ↓
再处理兄弟节点
```

对于这棵树：

```text
Parent
  └─ Child
      └─ div
```

深度优先会先进入 `Parent`，再进入 `Child`，再进入 `div`。

但关键在于：

> 进入一个节点的顺序，不等于完成一个节点的顺序。

这就像你读一本书的目录：

```text
进入第一章
  进入第一节
    进入第一小节
    完成第一小节
  完成第一节
完成第一章
```

最深的内容往往最先完成。

---

## 5. effect 提交更像“完成时处理”

为了理解子组件 effect 为什么先执行，可以先看一个简化版递归：

```ts
function commitEffects(fiber: Fiber | null) {
  if (!fiber) return

  commitEffects(fiber.child)

  runEffects(fiber)

  commitEffects(fiber.sibling)
}
```

这段代码的顺序是：

1. 先处理当前 Fiber 的子 Fiber。
2. 子 Fiber 都处理完后，才执行当前 Fiber 的 effect。
3. 最后处理兄弟 Fiber。

如果代入 `Parent → Child`：

```text
commitEffects(Parent)
  ↓
commitEffects(Child)
  ↓
runEffects(Child)
  ↓
runEffects(Parent)
```

所以输出就是：

```text
Child effect
Parent effect
```

这就是“子组件 effect 先于父组件完成”的最小解释。

---

## 6. 为什么不是父组件先 effect

很多人会把“父组件先渲染”和“父组件 effect 先执行”混在一起。

但它们是两件事。

函数组件执行顺序可以近似理解为：

```text
执行 Parent 函数组件
  ↓
发现它返回 Child
  ↓
执行 Child 函数组件
```

这说明父组件确实更早进入渲染流程。

但是 effect 不在渲染阶段执行。

`useEffect` 在渲染阶段只是登记：

```text
Parent 登记一个 effect
Child 登记一个 effect
```

真正执行 effect 要等到 commit 之后。

而 commit effect 时的遍历顺序是子 Fiber 优先完成，所以子组件 effect 会先执行。

---

## 7. 和 DOM 提交顺序有什么关系

你可以把一次更新拆成两层：

```text
第一层：DOM 变化提交
第二层：effect 执行
```

普通 `useEffect` 不会阻塞浏览器绘制，它属于 passive effect。

大致心智模型是：

```text
计算 Fiber 树
  ↓
提交 DOM 变化
  ↓
浏览器有机会绘制
  ↓
执行 useEffect
```

当 React 开始执行这些 passive effects 时，它会遍历 Fiber 树上的 effect。

在这个遍历里，子 Fiber 的 effect 会先于父 Fiber 的 effect 被处理。

所以更精确地说：

> 不是子组件的 DOM 一定晚于或早于父组件，而是 passive effect 的提交遍历呈现出子组件先于父组件的顺序。

---

## 8. cleanup 的顺序也要注意

如果 effect 返回 cleanup：

```tsx
function Parent() {
  useEffect(() => {
    console.log("Parent effect")

    return () => {
      console.log("Parent cleanup")
    }
  }, [])

  return <Child />
}

function Child() {
  useEffect(() => {
    console.log("Child effect")

    return () => {
      console.log("Child cleanup")
    }
  }, [])

  return <div>Child</div>
}
```

在很多场景下，你会观察到 mount effect 是子先父后：

```text
Child effect
Parent effect
```

cleanup 的具体顺序要看触发场景和 React 内部处理的 effect 类型，不要只用一句“永远子先父后”概括所有情况。

对新手来说，先抓住这点就够了：

> `useEffect` 的执行顺序由 commit 阶段的 Fiber 遍历决定，不是由 JSX 书写顺序直接决定。

---

## 9. 为什么 React 要这样设计

从 Fiber 的角度看，子节点是父节点 UI 的一部分。

当 React 在 commit 阶段处理 effect 时，采用深度优先的完成顺序，有几个好处：

- 和 Fiber 树的递归结构一致。
- 子树先处理完，父节点再做自己的 effect。
- 父组件 effect 执行时，可以认为子组件对应的提交工作已经完成。

这和很多树结构算法是类似的。

比如删除一个文件夹时，通常也是：

```text
先处理里面的文件
再处理外面的文件夹
```

也就是先子后父。

---

## 10. 和 useLayoutEffect 一样吗

`useEffect` 和 `useLayoutEffect` 都属于 effect，但时机不同：

| Hook | 执行时机 | 是否阻塞绘制 |
| --- | --- | --- |
| `useLayoutEffect` | DOM 更新后、浏览器绘制前 | 会阻塞绘制 |
| `useEffect` | 浏览器绘制后或非阻塞时机 | 不阻塞绘制 |

这篇笔记主要讲普通 `useEffect`。

如果你观察 `useLayoutEffect`，也可能看到类似的子先父后现象，但理解重点仍然是：

> effect 顺序来自 Fiber commit 阶段的遍历，不是来自组件代码的视觉嵌套顺序。

---

## 11. 最小心智模型

最后用一句话总结：

> 子组件 `useEffect` 先于父组件完成，是因为 React 在 commit 阶段执行 effect 时，会深度优先遍历 Fiber 树，并在这个过程中先处理子 Fiber，再处理父 Fiber。

更短一点：

```text
组件结构：Parent → Child
Effect 提交：Child → Parent
```

如果你正在实现一个极简 React，可以参考 [[构建自己的React#26. 在 commit 后执行 effects|在 commit 后执行 effects]] 里的 `commitEffects`。
