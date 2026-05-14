---
date: 2025-10-25
tags:
  - React
  - 前端实习挑战
  - 前端
---

# 构建自己的 React

这篇笔记不是为了“真的重写 React”，而是用一个极简版本帮助你理解 React 背后的核心思想：

- JSX 最后会变成普通 JavaScript 对象。
- `render` 会把这些对象变成真实 DOM。
- Fiber 会把一次很大的渲染任务拆成很多小任务。
- `commit` 阶段才会真正修改页面。
- 函数组件本质上是“返回 UI 描述的函数”。
- `useState` 的核心是：保存状态，并在状态变化后重新渲染。
- `useEffect` 的核心是：在 DOM 更新完成后执行副作用。

如果你刚入门前端，可以先不用急着记住所有代码。更重要的是理解这条主线：

> JSX → 虚拟 DOM 对象 → Fiber 任务树 → 真实 DOM → 状态更新后重新执行 → commit 后执行副作用

---

## 1. 先从 JSX 开始

我们平时写 React 时，可能会写这样的代码：

```tsx
const element = (
  <div id="app">
    <p>Hello React</p>
  </div>
)
```

这段看起来像 HTML，但它其实不是浏览器原生认识的语法。JavaScript 引擎不能直接执行 JSX，所以 JSX 需要先被编译成普通 JavaScript。

它大致会变成这样的函数调用：

```tsx
const element = createElement(
  "div",
  { id: "app" },
  createElement("p", null, "Hello React"),
)
```

也就是说：

> JSX 只是写 UI 的一种语法糖。真正运行时，它会变成函数调用。

---

## 2. 用对象描述页面

既然 JSX 最后会变成 `createElement(...)`，那 `createElement` 应该返回什么呢？

一个最简单的答案是：返回一个普通对象。

比如这段 JSX：

```tsx
const element = <h1 title="hello">Hello</h1>
```

可以被描述成：

```ts
const element = {
  type: "h1",
  props: {
    title: "hello",
    children: [
      {
        type: "TEXT_ELEMENT",
        props: {
          nodeValue: "Hello",
          children: [],
        },
      },
    ],
  },
}
```

这个对象表达了三件事：

- `type`：要创建什么标签，比如 `div`、`p`、`h1`。
- `props`：标签上的属性，比如 `id`、`title`。
- `children`：它的子节点。

为什么文字也要变成对象？

因为这样可以让所有节点都拥有相似的结构。标签是对象，文字也是对象，后面递归处理时会更简单。

---

## 3. 定义最小的数据结构

我们先定义两个类型：普通元素和文本元素。

```ts
type MyReactElement =
  | {
      type: string
      props: {
        [key: string]: unknown
        children: MyReactElement[]
      }
    }
  | {
      type: "TEXT_ELEMENT"
      props: {
        nodeValue: string | number
        children: []
      }
    }
```

这里有一个关键点：

> 我们自己的 React 不直接操作 JSX，而是操作这些普通对象。

---

## 4. 实现 createElement

`createElement` 要做的事情很简单：

1. 接收标签类型。
2. 接收属性。
3. 接收子元素。
4. 把它们整理成统一的对象结构。

```ts
function createElement(
  type: string,
  props: Record<string, unknown> | null,
  ...children: Array<MyReactElement | string | number>
): MyReactElement {
  return {
    type,
    props: {
      ...props,
      children: children.map((child) => {
        return typeof child === "object" ? child : createTextElement(child)
      }),
    },
  }
}

function createTextElement(text: string | number): MyReactElement {
  return {
    type: "TEXT_ELEMENT",
    props: {
      nodeValue: text,
      children: [],
    },
  }
}
```

现在这段代码：

```tsx
const element = createElement("p", null, "Hello")
```

会得到：

```ts
{
  type: "p",
  props: {
    children: [
      {
        type: "TEXT_ELEMENT",
        props: {
          nodeValue: "Hello",
          children: [],
        },
      },
    ],
  },
}
```

到这里，我们已经完成了第一步：

> 把 JSX 背后的 UI 结构，变成 JavaScript 对象。

---

## 5. 第一个 render：把对象变成真实 DOM

浏览器真正能显示的是 DOM，不是 JavaScript 对象。所以我们需要一个 `render` 函数，把上面的对象变成真实 DOM。

```ts
function render(element: MyReactElement, container: HTMLElement) {
  let dom: Node

  if (element.type === "TEXT_ELEMENT") {
    dom = document.createTextNode(element.props.nodeValue)
  } else {
    dom = document.createElement(element.type)
  }

  const isProperty = (key: string) => key !== "children"

  Object.keys(element.props)
    .filter(isProperty)
    .forEach((name) => {
      ;(dom as any)[name] = (element.props as any)[name]
    })

  element.props.children.forEach((child) => {
    render(child, dom as HTMLElement)
  })

  container.appendChild(dom)
}
```

这个版本的 `render` 做了三件事：

1. 根据 `type` 创建 DOM。
2. 把 `props` 上的属性设置到 DOM 上。
3. 递归渲染所有 `children`。

比如：

```ts
const element = createElement(
  "div",
  { id: "app" },
  createElement("p", null, "Hello React"),
)

const container = document.getElementById("root")!
render(element, container)
```

页面上就会出现：

```html
<div id="app">
  <p>Hello React</p>
</div>
```

---

## 6. 直接递归 render 的问题

上面的 `render` 很直观，但它有一个严重问题：

> 如果页面结构很大，递归渲染会一次性做完所有工作，期间浏览器可能没有机会响应用户操作。

[[浏览器包含哪些进程|浏览器进程]]负责很多事情：

- 执行 JavaScript。
- 处理点击、输入、滚动。
- 计算样式和布局。
- 绘制页面。

如果 JavaScript 一口气执行很久，用户就会感觉页面卡住。

所以我们希望把“渲染整棵树”拆成很多小任务：

```text
大任务：渲染整个页面

拆成：
任务 1：处理 root
任务 2：处理 div
任务 3：处理 p
任务 4：处理文本
...
```

这样浏览器空闲时就做一点，忙的时候先让浏览器处理更重要的事情。

这就是 Fiber 想解决的问题。

---

## 7. Fiber 是什么

你可以先把 Fiber 理解成：

> Fiber 是一个“工作单元”。每个元素对应一个 Fiber。

一个 Fiber 里会保存：

- 当前元素的信息。
- 对应的 DOM 节点。
- 父节点是谁。
- 第一个子节点是谁。
- 下一个兄弟节点是谁。

```ts
type Fiber = {
  type: string
  props: MyReactElement["props"]
  dom: Node | null

  parent: Fiber | null
  child: Fiber | null
  sibling: Fiber | null
}
```

为什么 Fiber 不直接用 `children` 数组，而要用 `child` 和 `sibling`？

因为这样更方便一步一步地找“下一个要处理的任务”：

```text
先找 child
没有 child 就找 sibling
没有 sibling 就回到 parent，再找 parent 的 sibling
```

这是一种深度优先遍历。

---

## 8. 用 [[requestIdleCallback]] 做工作循环

我们需要一个循环，它在浏览器空闲时处理 Fiber。

```ts
let nextUnitOfWork: Fiber | null = null

function workLoop(deadline: IdleDeadline) {
  let shouldYield = false

  while (nextUnitOfWork && !shouldYield) {
    nextUnitOfWork = performUnitOfWork(nextUnitOfWork)
    shouldYield = deadline.timeRemaining() < 1
  }

  requestIdleCallback(workLoop)
}

requestIdleCallback(workLoop)
```

这里的核心逻辑是：

- `nextUnitOfWork` 表示下一个要处理的 Fiber。
- `performUnitOfWork` 处理一个 Fiber，并返回下一个 Fiber。
- `deadline.timeRemaining()` 表示这次空闲时间还剩多少。
- 如果剩余时间太少，就先停下来，把主线程还给浏览器。

这就是“可中断渲染”的雏形。

---

## 9. 改造 render：不立刻渲染，只创建根任务

有了工作循环后，`render` 不再直接递归创建 DOM。

它只负责创建第一个任务：根 Fiber。

```ts
let wipRoot: Fiber | null = null

function render(element: MyReactElement, container: HTMLElement) {
  wipRoot = {
    type: "ROOT",
    props: {
      children: [element],
    },
    dom: container,
    parent: null,
    child: null,
    sibling: null,
  }

  nextUnitOfWork = wipRoot
}
```

`wipRoot` 的意思是 `work in progress root`，也就是“正在构建中的根节点”。

注意：

> 此时页面还没有更新，我们只是告诉工作循环：有任务要做了。

---

## 10. 执行一个工作单元

`performUnitOfWork` 是 Fiber 版本的核心函数。

它负责三件事：

1. 为当前 Fiber 创建 DOM。
2. 为它的子元素创建子 Fiber。
3. 返回下一个要处理的 Fiber。

```ts
function performUnitOfWork(fiber: Fiber): Fiber | null {
  if (!fiber.dom) {
    fiber.dom = createDom(fiber)
  }

  const elements = fiber.props.children
  let previousSibling: Fiber | null = null

  elements.forEach((element, index) => {
    const newFiber: Fiber = {
      type: element.type,
      props: element.props,
      dom: null,
      parent: fiber,
      child: null,
      sibling: null,
    }

    if (index === 0) {
      fiber.child = newFiber
    } else if (previousSibling) {
      previousSibling.sibling = newFiber
    }

    previousSibling = newFiber
  })

  if (fiber.child) {
    return fiber.child
  }

  let nextFiber: Fiber | null = fiber
  while (nextFiber) {
    if (nextFiber.sibling) {
      return nextFiber.sibling
    }
    nextFiber = nextFiber.parent
  }

  return null
}
```

把创建 DOM 的逻辑拆出来：

```ts
function createDom(fiber: Fiber): Node {
  const dom =
    fiber.type === "TEXT_ELEMENT"
      ? document.createTextNode((fiber.props as any).nodeValue)
      : document.createElement(fiber.type)

  Object.keys(fiber.props)
    .filter((key) => key !== "children")
    .forEach((name) => {
      ;(dom as any)[name] = (fiber.props as any)[name]
    })

  return dom
}
```

到这里，Fiber 树已经可以被一点一点构建出来。

但还有一个问题：

> 我们在构建 Fiber 时，不能立刻把 DOM 加到页面上。

为什么？

因为 Fiber 构建过程可能被中断。如果构建一半就把 DOM 插进页面，用户可能会看到“不完整的页面”。

所以 React 分成两个阶段：

- `render` 阶段：可以被打断，只计算要做什么。
- `commit` 阶段：不能被打断，一次性把结果提交到页面。

---

## 11. commit：真正更新页面

当所有 Fiber 都处理完后，`nextUnitOfWork` 会变成 `null`。

这时说明整棵工作树已经准备好了，可以提交到页面了。

```ts
function commitRoot() {
  if (wipRoot?.child) {
    commitWork(wipRoot.child)
  }
  wipRoot = null
}

function commitWork(fiber: Fiber | null) {
  if (!fiber) return

  const parentDom = fiber.parent?.dom

  if (fiber.dom && parentDom) {
    parentDom.appendChild(fiber.dom)
  }

  commitWork(fiber.child)
  commitWork(fiber.sibling)
}
```

然后把它放进工作循环：

```ts
function workLoop(deadline: IdleDeadline) {
  let shouldYield = false

  while (nextUnitOfWork && !shouldYield) {
    nextUnitOfWork = performUnitOfWork(nextUnitOfWork)
    shouldYield = deadline.timeRemaining() < 1
  }

  if (!nextUnitOfWork && wipRoot) {
    commitRoot()
  }

  requestIdleCallback(workLoop)
}
```

现在，我们已经得到一个极简 Fiber 渲染流程：

```text
render 创建根 Fiber
        ↓
workLoop 空闲时处理一个个 Fiber
        ↓
performUnitOfWork 构建 Fiber 树
        ↓
全部完成后 commitRoot
        ↓
真实 DOM 被插入页面
```

---

## 12. 支持函数组件

前面我们只支持这样的元素：

```tsx
createElement("h1", null, "Hello")
```

但 React 里更常见的是函数组件：

```tsx
function App() {
  return createElement("h1", null, "Hello")
}
```

函数组件的特点是：

> 它本身不对应真实 DOM，它只是执行后返回一个元素对象。

所以 Fiber 的 `type` 需要支持函数：

```ts
type FunctionComponent = (props: any) => MyReactElement

type Fiber = {
  type: string | FunctionComponent
  props: MyReactElement["props"]
  dom: Node | null

  parent: Fiber | null
  child: Fiber | null
  sibling: Fiber | null
}
```

然后在 `performUnitOfWork` 中区分两种 Fiber：

```ts
function performUnitOfWork(fiber: Fiber): Fiber | null {
  const isFunctionComponent = typeof fiber.type === "function"

  if (isFunctionComponent) {
    updateFunctionComponent(fiber)
  } else {
    updateHostComponent(fiber)
  }

  if (fiber.child) {
    return fiber.child
  }

  let nextFiber: Fiber | null = fiber
  while (nextFiber) {
    if (nextFiber.sibling) {
      return nextFiber.sibling
    }
    nextFiber = nextFiber.parent
  }

  return null
}
```

宿主组件就是 `div`、`p`、`span` 这类真实 DOM 标签：

```ts
function updateHostComponent(fiber: Fiber) {
  if (!fiber.dom) {
    fiber.dom = createDom(fiber)
  }

  reconcileChildren(fiber, fiber.props.children)
}
```

函数组件需要先执行函数，拿到返回的元素：

```ts
function updateFunctionComponent(fiber: Fiber) {
  const children = [(fiber.type as FunctionComponent)(fiber.props)]
  reconcileChildren(fiber, children)
}
```

`reconcileChildren` 负责把子元素变成子 Fiber：

```ts
function reconcileChildren(fiber: Fiber, elements: MyReactElement[]) {
  let previousSibling: Fiber | null = null

  elements.forEach((element, index) => {
    const newFiber: Fiber = {
      type: element.type,
      props: element.props,
      dom: null,
      parent: fiber,
      child: null,
      sibling: null,
    }

    if (index === 0) {
      fiber.child = newFiber
    } else if (previousSibling) {
      previousSibling.sibling = newFiber
    }

    previousSibling = newFiber
  })
}
```

函数组件没有自己的 DOM，所以提交时要往上找最近的真实 DOM 父节点：

```ts
function commitWork(fiber: Fiber | null) {
  if (!fiber) return

  let parentFiber = fiber.parent
  while (parentFiber && !parentFiber.dom) {
    parentFiber = parentFiber.parent
  }

  const parentDom = parentFiber?.dom

  if (fiber.dom && parentDom) {
    parentDom.appendChild(fiber.dom)
  }

  commitWork(fiber.child)
  commitWork(fiber.sibling)
}
```

到这里，我们自己的 React 已经支持函数组件了。

---

## 13. useState 要解决什么问题

函数组件每次执行都会重新运行函数体：

```tsx
function Counter() {
  const count = 0

  return createElement("button", null, count)
}
```

如果 `count` 只是普通变量，每次执行 `Counter` 都会重新变成 `0`。

所以 `useState` 要解决的问题是：

> 函数组件重新执行时，状态不能丢；状态变化时，页面还要重新更新。

可以把 `useState` 想象成 React 给函数组件准备的一个“小抽屉”：

- 第一次执行组件时，抽屉里没有值，就放入初始值。
- 后面组件重新执行时，不再使用初始值，而是从抽屉里取出上一次保存的值。
- 调用 `setState` 时，不是立刻改 DOM，而是告诉 React：“这里有一个状态更新，请重新算一遍 UI。”

---

## 14. 为什么 useState 不能只是普通变量

先看一个不使用 `useState` 的例子：

```tsx
function Counter() {
  let count = 0

  return createElement(
    "button",
    {
      onclick: () => {
        count++
        console.log(count)
      },
    },
    count,
  )
}
```

你点击按钮时，`count` 的确可能在事件函数里变成 `1`、`2`、`3`。

但页面不会自动变，因为这里少了两件事：

1. 没有人通知框架重新执行 `Counter`。
2. 重新执行 `Counter` 时，`let count = 0` 又会从头开始。

所以真正的状态系统至少要做到三件事：

```text
保存旧状态
  ↓
接收状态更新
  ↓
触发重新渲染
```

这就是 `useState` 的核心价值。

---

## 15. 为 Fiber 加上旧树和 hooks

为了支持状态更新，我们需要知道“上一次渲染的结果”。

所以 Fiber 要加几个字段：

```ts
type Hook<T = unknown> = {
  state: T
  queue: Array<T | ((previousState: T) => T)>
}

type Fiber = {
  type: string | FunctionComponent
  props: MyReactElement["props"]
  dom: Node | null

  parent: Fiber | null
  child: Fiber | null
  sibling: Fiber | null

  alternate?: Fiber | null
  hooks?: Hook[]
  effectTag?: "PLACEMENT" | "UPDATE" | "DELETION"
}
```

这里新增的字段很重要：

- `alternate`：指向上一次渲染时对应的旧 Fiber。
- `hooks`：保存当前函数组件用到的 hook。
- `effectTag`：记录这个 Fiber 最后要对 DOM 做什么操作。

还需要几个全局变量：

```ts
let currentRoot: Fiber | null = null
let wipRoot: Fiber | null = null
let nextUnitOfWork: Fiber | null = null

let wipFiber: Fiber | null = null
let hookIndex = 0

let deletions: Fiber[] = []
```

这些变量分别表示：

- `currentRoot`：当前页面上已经提交过的 Fiber 树。
- `wipRoot`：正在构建中的新 Fiber 树。
- `nextUnitOfWork`：下一个要处理的 Fiber。
- `wipFiber`：当前正在执行的函数组件 Fiber。
- `hookIndex`：当前执行到第几个 hook。
- `deletions`：这次更新里需要删除的旧 Fiber。

---

## 16. 在函数组件里准备 hooks

每次执行函数组件前，要重置 hook 环境：

```ts
function updateFunctionComponent(fiber: Fiber) {
  wipFiber = fiber
  hookIndex = 0
  wipFiber.hooks = []

  const children = [(fiber.type as FunctionComponent)(fiber.props)]
  reconcileChildren(fiber, children)
}
```

这段代码的意思是：

1. 记录当前正在执行哪个函数组件。
2. 把 hook 下标重置为 `0`。
3. 准备一个新的 `hooks` 数组。
4. 执行函数组件，拿到它返回的 UI。
5. 把返回的 UI 继续变成 Fiber。

这也解释了为什么 React 要求 hook 不能写在条件语句里。

> [!tip] 双向链接
> 这里讲的是所有 hook 的共同规则，不只适用于 `useState`。后面讲 [[#20. useEffect 要解决什么问题|useEffect]] 时也会继续用到同一套 `wipFiber + hookIndex` 机制。

---

## 17. 为什么不能在条件语句里写 hook

先看一个错误例子：

```tsx
function UserCard({ isLogin }) {
  if (isLogin) {
    const [user, setUser] = useState(null)
  }

  const [theme, setTheme] = useState("light")

  return createElement("div", null, theme)
}
```

这段代码的问题不在于 `if` 本身，而在于：

> hook 是靠“调用顺序”找到旧状态的。

前面我们的实现里，`useState` 会这样找旧 hook：

```ts
const oldHook = wipFiber?.alternate?.hooks?.[hookIndex]
```

然后每调用一次 hook，就会把 `hookIndex` 加一：

```ts
wipFiber?.hooks?.push(hook)
hookIndex++
```

所以 React 并不是通过变量名找到状态的。

它不是这样找的：

```text
找到名字叫 user 的状态
找到名字叫 theme 的状态
```

而是这样找的：

```text
找到第 0 个 hook
找到第 1 个 hook
找到第 2 个 hook
```

### 第一次渲染：isLogin 是 true

```tsx
// 假设这次 isLogin 是 true
function UserCard({ isLogin }) {
  if (isLogin) {
    useState(null) // 第 0 个 hook：user
  }

  useState("light") // 第 1 个 hook：theme
}
```

这时 hook 顺序是：

```text
第 0 个 hook：user
第 1 个 hook：theme
```

### 第二次渲染：isLogin 变成 false

```tsx
// 假设这次 isLogin 是 false
function UserCard({ isLogin }) {
  if (isLogin) {
    useState(null) // 被跳过
  }

  useState("light") // 现在变成第 0 个 hook
}
```

这时 hook 顺序变成：

```text
第 0 个 hook：theme
```

问题来了：旧 Fiber 上的第 0 个 hook 原本是 `user`，但这次第 0 个 hook 变成了 `theme`。

于是 React 会把 `user` 的旧状态错误地当成 `theme` 的旧状态。

这就是为什么 hook 不能写在条件语句、循环、提前 `return` 后面：

```tsx
// 不推荐：条件语句里调用 hook
if (someCondition) {
  useState(0)
}

// 不推荐：循环里调用 hook
for (const item of list) {
  useState(item)
}

// 不推荐：提前 return 导致后面的 hook 有时不执行
if (!data) {
  return createElement("p", null, "Loading")
}

useState("ready")
```

正确做法是：

> hook 放在函数组件最顶层，让每次渲染都按完全相同的顺序调用。

比如可以这样写：

```tsx
function UserCard({ isLogin }) {
  const [user, setUser] = useState(null)
  const [theme, setTheme] = useState("light")

  if (!isLogin) {
    return createElement("div", null, theme)
  }

  return createElement("div", null, user ? user.name : "Loading")
}
```

如果某些逻辑确实只想在条件满足时执行，也应该把条件放进 hook 内部，而不是把 hook 放进条件内部。

比如 `useEffect` 也是一样：

```tsx
useEffect(() => {
  if (!isLogin) return

  // 只有登录后才执行具体逻辑
  fetchUser()
}, [isLogin])
```

这就是 hook 的第一条规则：

> 不要在条件语句、循环或嵌套函数里调用 hook。

它背后的根本原因是：

> React 需要稳定的 hook 调用顺序，才能用 `hookIndex` 找回上一次渲染保存的状态和副作用。

---

## 18. 实现一个极简 useState

`useState` 的核心流程是：
1. 根据 `hookIndex` 找到旧 hook。
2. 创建一个新的 hook。
3. 把旧 hook 队列里的更新依次执行。
4. 返回最新状态和 `setState`。
5. `setState` 被调用后，创建新的 `wipRoot`，启动新一轮渲染。

```ts
function useState<T>(
  initialState: T,
): [T, (action: T | ((previousState: T) => T)) => void] {
  const oldHook = wipFiber?.alternate?.hooks?.[hookIndex] as Hook<T> | undefined

  const hook: Hook<T> = {
    state: oldHook ? oldHook.state : initialState,
    queue: [],
  }

  const actions = oldHook ? oldHook.queue : []

  actions.forEach((action) => {
    hook.state =
      typeof action === "function"
        ? (action as (previousState: T) => T)(hook.state)
        : action
  })

  const setState = (action: T | ((previousState: T) => T)) => {
    hook.queue.push(action)

    if (!currentRoot) return

    wipRoot = {
      ...currentRoot,
      parent: null,
      child: null,
      sibling: null,
      alternate: currentRoot,
    }

    nextUnitOfWork = wipRoot
    deletions = []
  }

  wipFiber?.hooks?.push(hook)
  hookIndex++

  return [hook.state, setState]
}
```

现在就可以写一个计数器：

```tsx
function Counter() {
  const [count, setCount] = useState(0)

  return createElement(
    "button",
    {
      onclick: () => setCount((count) => count + 1),
    },
    count,
  )
}
```

点击按钮时发生了什么？

```text
点击按钮
  ↓
调用 setCount
  ↓
把更新动作放进 hook.queue
  ↓
创建新的 wipRoot
  ↓
workLoop 重新构建 Fiber 树
  ↓
useState 读取旧 hook，并执行 queue
  ↓
得到新的 count
  ↓
新旧 Fiber 比较
  ↓
commit 只更新变化的 DOM
```

这就是 `useState` 的最小心智模型。

---

## 19. setState 为什么不是立刻改状态

刚入门时，很容易以为 `setCount(1)` 就是“立刻把 `count` 改成 `1`”。

但在 React 的模型里，更准确的理解是：

> `setState` 是提交一个更新请求，然后 React 安排一次重新渲染。

为什么要这样设计？

因为状态更新后，React 不只要改一个变量，还要重新计算 UI：

```text
新状态是什么？
  ↓
组件会返回什么新元素？
  ↓
新 Fiber 树长什么样？
  ↓
和旧 Fiber 树相比，哪里变了？
  ↓
真实 DOM 应该怎么最小化更新？
```

所以 `setState` 做的事情不是直接操作 DOM，而是开启一轮新的计算。

这也是为什么我们常说：

> UI 是状态的函数。状态变了，UI 重新计算。

---

## 20. useEffect 要解决什么问题

> [!tip] 双向链接
> 如果你还不理解为什么 hook 必须按固定顺序调用，先回看 [[#17. 为什么不能在条件语句里写 hook|为什么不能在条件语句里写 hook]]。`useEffect` 和 `useState` 一样，都依赖 `hookIndex` 找到自己的旧 hook。

前面我们已经知道：

> `useState` 负责保存状态，状态变化后重新计算 UI。

但前端组件不只负责“算 UI”，还经常需要做一些和外部世界有关的事情，比如：

- 页面渲染后请求接口。
- 监听浏览器事件。
- 设置定时器。
- 手动修改 `document.title`。
- 连接 WebSocket。

这些事情有一个共同点：

> 它们不是直接计算 UI 的一部分，而是组件渲染完成后额外发生的事情。

React 把这类事情叫做 **副作用**，也就是 effect。

例如：

```tsx
function Counter() {
  const [count, setCount] = useState(0)

  useEffect(() => {
    document.title = `count: ${count}`
  })

  return createElement(
    "button",
    {
      onclick: () => setCount((count) => count + 1),
    },
    count,
  )
}
```

这里的 `document.title = ...` 就是副作用。

为什么它不应该直接写在渲染逻辑里？

因为渲染阶段最好保持“纯粹”：

```text
输入 props 和 state
  ↓
返回 UI 描述
```

而修改标题、请求接口、订阅事件这些事情，应该等 DOM 提交完成后再做。

所以 `useEffect` 的核心作用是：

> 在组件渲染并提交到页面之后，执行一段副作用代码。

---

## 21. useEffect 的三个常见用法

### 每次渲染后都执行

如果不传依赖数组，effect 会在每次提交后执行：

```tsx
useEffect(() => {
  console.log("组件渲染完成")
})
```

适合做一些每次 UI 更新后都要同步的事情。

### 只在首次渲染后执行

如果传空数组，effect 只在组件第一次提交后执行：

```tsx
useEffect(() => {
  console.log("组件第一次挂载")
}, [])
```

常见场景是请求初始数据：

```tsx
useEffect(() => {
  fetch("/api/user")
    .then((response) => response.json())
    .then((user) => console.log(user))
}, [])
```

### 依赖变化后才执行

如果传入依赖数组，只有依赖发生变化时才执行：

```tsx
useEffect(() => {
  document.title = `count: ${count}`
}, [count])
```

它的意思是：

> 只有 `count` 和上一次不一样时，才重新执行这个 effect。

---

## 22. useEffect 为什么需要清理函数

有些副作用不是“一次性动作”，而是会留下东西。

比如监听事件：

```tsx
useEffect(() => {
  const handleResize = () => {
    console.log(window.innerWidth)
  }

  window.addEventListener("resize", handleResize)
})
```

如果组件每次更新都重新添加监听，但从不删除旧监听，监听函数会越来越多。

所以 effect 可以返回一个清理函数：

```tsx
useEffect(() => {
  const handleResize = () => {
    console.log(window.innerWidth)
  }

  window.addEventListener("resize", handleResize)

  return () => {
    window.removeEventListener("resize", handleResize)
  }
}, [])
```

清理函数通常会在两种时机执行：

- 组件卸载时。
- 下一次 effect 重新执行前。

可以把它理解成：

```text
先清理旧副作用
  ↓
再执行新副作用
```

这样就不会留下过期的事件监听、定时器或连接。

---

## 23. 为什么 useEffect 的回调不能直接写成 async 函数

很多新手会这样写请求：

```tsx
useEffect(async () => {
  const response = await fetch("/api/user")
  const user = await response.json()
  console.log(user)
}, [])
```

这看起来很自然，但在 React 里是不推荐的。

原因不是 `useEffect` 里面不能写异步代码，而是：

> `useEffect` 传入的回调本身不能是 `async` 函数。

为什么？

因为 `async` 函数一定会返回一个 `Promise`。

比如：

```ts
async function getUser() {
  return "user"
}

const result = getUser()
console.log(result) // Promise
```

而 `useEffect` 对回调返回值有明确约定：

```text
返回 undefined：不需要清理
返回 function：这是清理函数
```

也就是说，React 期望 effect 的返回值只能是：

```ts
void | (() => void)
```

但如果你传入 `async` 函数，它的返回值会变成：

```ts
Promise<void>
```

这会让 React 分不清：

```text
你返回的是清理函数？
还是一个 Promise？
这个 Promise 什么时候完成？
完成后又该不该当成 cleanup？
```

所以这样的写法是不对的：

```tsx
useEffect(async () => {
  const response = await fetch("/api/user")
  const user = await response.json()
  console.log(user)
}, [])
```

正确写法是在 effect 内部定义并调用异步函数：

```tsx
useEffect(() => {
  async function fetchUser() {
    const response = await fetch("/api/user")
    const user = await response.json()
    console.log(user)
  }

  fetchUser()
}, [])
```

或者使用立即执行函数：

```tsx
useEffect(() => {
  ;(async () => {
    const response = await fetch("/api/user")
    const user = await response.json()
    console.log(user)
  })()
}, [])
```

这两种写法的共同点是：

> effect 回调本身仍然是普通函数，返回值仍然是 `undefined` 或清理函数。

如果异步请求还需要处理组件卸载，可以配合清理函数：

```tsx
useEffect(() => {
  let ignore = false

  async function fetchUser() {
    const response = await fetch("/api/user")
    const user = await response.json()

    if (!ignore) {
      setUser(user)
    }
  }

  fetchUser()

  return () => {
    ignore = true
  }
}, [])
```

这里的 `ignore` 用来避免一种情况：

```text
请求还没回来
  ↓
组件已经卸载或 effect 已经过期
  ↓
请求返回后还想 setUser
```

所以最适合新手记住的规则是：

> `useEffect` 里面可以写异步逻辑，但传给 `useEffect` 的那个函数不要写成 `async`。

---

## 24. 给 Hook 增加 effect 信息

前面的 `Hook` 只保存了 `state` 和 `queue`。

为了支持 `useEffect`，我们可以让 hook 也保存 effect 相关信息：

```ts
type EffectCallback = () => void | (() => void)

type Hook<T = unknown> = {
  state?: T
  queue?: Array<T | ((previousState: T) => T)>

  effect?: EffectCallback
  deps?: unknown[]
  cleanup?: void | (() => void)
  hasChanged?: boolean
}
```

这里几个字段的含义是：

- `effect`：用户传进来的副作用函数。
- `deps`：依赖数组。
- `cleanup`：上一次 effect 返回的清理函数。
- `hasChanged`：这次依赖是否发生变化。

为了判断依赖有没有变，我们写一个工具函数：

```ts
function areDepsChanged(previousDeps?: unknown[], nextDeps?: unknown[]) {
  if (!previousDeps || !nextDeps) return true
  if (previousDeps.length !== nextDeps.length) return true

  return previousDeps.some((previousDep, index) => {
    return !Object.is(previousDep, nextDeps[index])
  })
}
```

这里用 `Object.is` 是因为它比 `===` 更适合处理一些特殊值，比如 `NaN`。

---

## 25. 实现一个极简 useEffect

`useEffect` 和 `useState` 一样，也依赖 `wipFiber` 和 `hookIndex`。

因为它们都属于 hook，所以都要按照调用顺序存进 `hooks` 数组。

```ts
function useEffect(effect: EffectCallback, deps?: unknown[]) {
  const oldHook = wipFiber?.alternate?.hooks?.[hookIndex]

  const hasChanged = areDepsChanged(oldHook?.deps, deps)

  const hook: Hook = {
    effect,
    deps,
    cleanup: oldHook?.cleanup,
    hasChanged,
  }

  wipFiber?.hooks?.push(hook)
  hookIndex++
}
```

这段代码并没有立刻执行 `effect`。

这点非常关键：

> `useEffect` 在渲染阶段只负责登记副作用，不负责执行副作用。

为什么？

因为渲染阶段可能被中断。如果渲染中途就执行副作用，可能会出现“UI 还没提交，但副作用已经发生”的问题。

所以 effect 应该等到 `commit` 阶段之后再执行。

---

## 26. 在 commit 后执行 effects

我们可以在 `commitRoot` 的最后执行 effect：

```ts
function commitRoot() {
  deletions.forEach(commitWork)

  if (wipRoot?.child) {
    commitWork(wipRoot.child)
  }

  currentRoot = wipRoot
  wipRoot = null

  commitEffects(currentRoot?.child ?? null)
}
```

然后递归遍历 Fiber 树，找到函数组件上的 hooks。

这里要注意遍历顺序：先处理子节点，再处理当前节点。

```ts
function commitEffects(fiber: Fiber | null) {
  if (!fiber) return

  commitEffects(fiber.child)

  fiber.hooks?.forEach((hook) => {
    if (!hook.effect || !hook.hasChanged) return

    if (typeof hook.cleanup === "function") {
      hook.cleanup()
    }

    hook.cleanup = hook.effect()
  })

  commitEffects(fiber.sibling)
}
```

这段代码的执行顺序是：

```text
DOM 更新完成
  ↓
从子 Fiber 往父 Fiber 遍历 effect
  ↓
找到发生变化的 effect
  ↓
先执行旧 cleanup
  ↓
再执行新 effect
  ↓
保存新的 cleanup
```

这也解释了一个常见现象：

> 子组件的 `useEffect` 通常会先于父组件的 `useEffect` 执行。

原因很简单：React 在提交 effect 时会沿着 Fiber 树做深度优先遍历，并在这个阶段先处理子 Fiber，再处理父 Fiber。这样子组件完成自己的副作用后，父组件再执行自己的副作用。

如果你想看更完整的执行顺序和 Fiber 遍历过程，可以看 [[子组件 Effect 为什么先于父组件完成]]。

这就实现了一个非常简化的 `useEffect`。

---

## 27. useEffect 和 useState 的关系

`useState` 和 `useEffect` 都是 hook，但它们负责的事情不同：

| Hook | 负责什么 | 什么时候发挥作用 |
| --- | --- | --- |
| `useState` | 保存状态，触发重新渲染 | 渲染阶段读取状态，事件中触发更新 |
| `useEffect` | 执行副作用 | DOM 提交完成之后执行 |

可以用一句话区分它们：

> `useState` 决定 UI 长什么样；`useEffect` 负责 UI 出现之后还要做什么。

例如：

```tsx
function UserProfile() {
  const [user, setUser] = useState(null)

  useEffect(() => {
    fetch("/api/user")
      .then((response) => response.json())
      .then((data) => setUser(data))
  }, [])

  if (!user) {
    return createElement("p", null, "Loading...")
  }

  return createElement("h1", null, user.name)
}
```

这段代码里：

```text
第一次渲染
  ↓
user 是 null
  ↓
页面显示 Loading...
  ↓
commit 完成后执行 useEffect
  ↓
请求接口
  ↓
接口返回后 setUser
  ↓
重新渲染
  ↓
页面显示 user.name
```

这就是很多 React 页面加载数据的基本模式。

---

## 28. useEffect 的新手心智模型

刚入门时，可以先这样理解：

```text
useState：组件自己的记忆
useEffect：组件渲染后的后续动作
```

再具体一点：

- 想让页面因为某个值变化而更新，用 `useState`。
- 想在页面渲染后做请求、订阅、定时器、同步标题，用 `useEffect`。
- effect 里用到了会变化的值，就把它放进依赖数组。
- effect 留下了外部资源，就返回清理函数。

最重要的是不要把 `useEffect` 当成“万能工具”。

如果某个值可以直接通过 `props` 或 `state` 算出来，就不要放进 `useEffect`：

```tsx
// 不推荐：没必要多存一个 fullName
useEffect(() => {
  setFullName(firstName + lastName)
}, [firstName, lastName])

// 更推荐：渲染时直接计算
const fullName = firstName + lastName
```

`useEffect` 更适合处理“React 外部世界”的事情，而不是普通的数据计算。

---

## 29. 为什么需要比较新旧节点

目前前面的 `commitWork` 还有一个问题：它只会 `appendChild`。

也就是说，每次状态更新时，它可能会重新追加 DOM，而不是更新已有 DOM。

比如第一次渲染：

```html
<button>0</button>
```

点击后如果只是重新追加，就可能变成：

```html
<button>0</button>
<button>1</button>
```

但我们真正想要的是：

```html
<button>1</button>
```

所以更新时不能简单地“全部重新插入”。我们需要比较新旧节点：

- 如果类型相同，复用旧 DOM，只更新变化的属性。
- 如果类型不同，创建新 DOM，替换旧 DOM。
- 如果旧节点不存在，说明是新增。
- 如果新节点不存在，说明是删除。

这个比较过程通常叫：

> reconciliation，中文常翻译为“协调”或“调和”。

---

## 30. 给 Fiber 标记操作类型

我们可以用 `effectTag` 标记每个 Fiber 最后要做什么：

```ts
type EffectTag = "PLACEMENT" | "UPDATE" | "DELETION"
```

三种情况分别是：

| 标记 | 含义 | 最后对 DOM 做什么 |
| --- | --- | --- |
| `PLACEMENT` | 新增节点 | `appendChild` |
| `UPDATE` | 更新节点 | 更新属性或文本 |
| `DELETION` | 删除节点 | `removeChild` |

这样，`render` 阶段只负责计算：

```text
这个 Fiber 应该新增？
这个 Fiber 应该更新？
这个 Fiber 应该删除？
```

真正操作 DOM 的事情，仍然放到 `commit` 阶段统一完成。

---

## 31. 改造 reconcileChildren：比较新旧 Fiber

原来的 `reconcileChildren` 只是把子元素变成 Fiber。

现在它要多做一步：拿新元素和旧 Fiber 比较。

```ts
function reconcileChildren(fiber: Fiber, elements: MyReactElement[]) {
  let index = 0
  let oldFiber = fiber.alternate?.child ?? null
  let previousSibling: Fiber | null = null

  while (index < elements.length || oldFiber) {
    const element = elements[index]
    let newFiber: Fiber | null = null

    const sameType = element && oldFiber && element.type === oldFiber.type

    if (sameType) {
      newFiber = {
        type: oldFiber.type,
        props: element.props,
        dom: oldFiber.dom,
        parent: fiber,
        child: null,
        sibling: null,
        alternate: oldFiber,
        effectTag: "UPDATE",
      }
    }

    if (element && !sameType) {
      newFiber = {
        type: element.type,
        props: element.props,
        dom: null,
        parent: fiber,
        child: null,
        sibling: null,
        alternate: null,
        effectTag: "PLACEMENT",
      }
    }

    if (oldFiber && !sameType) {
      oldFiber.effectTag = "DELETION"
      deletions.push(oldFiber)
    }

    if (oldFiber) {
      oldFiber = oldFiber.sibling
    }

    if (index === 0) {
      fiber.child = newFiber
    } else if (previousSibling && newFiber) {
      previousSibling.sibling = newFiber
    }

    previousSibling = newFiber
    index++
  }
}
```

这段代码可以拆成四种情况理解。

### 情况一：类型相同，更新节点

```text
旧节点：<button>0</button>
新节点：<button>1</button>
```

它们都是 `button`，所以真实 DOM 可以复用。

新 Fiber 会带上：

```ts
effectTag: "UPDATE"
dom: oldFiber.dom
alternate: oldFiber
```

意思是：

> 不要创建新 DOM，直接复用旧 DOM，后面只更新变化的属性和文本。

### 情况二：旧节点没有，新节点有，新增节点

```text
旧节点：没有
新节点：<p>Hello</p>
```

这说明页面上要新增一个 DOM。

新 Fiber 会带上：

```ts
effectTag: "PLACEMENT"
dom: null
```

意思是：

> 这是一个新节点，后面 commit 时插入页面。

### 情况三：旧节点有，新节点没有，删除节点

```text
旧节点：<p>Hello</p>
新节点：没有
```

这说明页面上要删除一个 DOM。

旧 Fiber 会被放进 `deletions`：

```ts
oldFiber.effectTag = "DELETION"
deletions.push(oldFiber)
```

意思是：

> 这个旧节点在新 UI 里不存在了，commit 时删除它。

### 情况四：类型不同，替换节点

```text
旧节点：<p>Hello</p>
新节点：<h1>Hello</h1>
```

类型不同，旧 DOM 不能复用。

这会被拆成两步：

```text
删除旧 p
新增 h1
```

---

## 32. 更新 DOM 属性

当 Fiber 的 `effectTag` 是 `UPDATE` 时，说明节点类型没变，可以复用 DOM。

但属性可能变了，比如：

```tsx
<button disabled={false}>提交</button>
```

变成：

```tsx
<button disabled={true}>提交</button>
```

所以需要比较新旧 `props`。

```ts
const isEvent = (key: string) => key.startsWith("on")
const isProperty = (key: string) => key !== "children" && !isEvent(key)
const isNew = (previous: any, next: any) => (key: string) => previous[key] !== next[key]
const isGone = (_previous: any, next: any) => (key: string) => !(key in next)

function updateDom(dom: Node, previousProps: any, nextProps: any) {
  Object.keys(previousProps)
    .filter(isEvent)
    .filter((key) => !(key in nextProps) || isNew(previousProps, nextProps)(key))
    .forEach((name) => {
      const eventType = name.toLowerCase().substring(2)
      dom.removeEventListener(eventType, previousProps[name])
    })

  Object.keys(previousProps)
    .filter(isProperty)
    .filter(isGone(previousProps, nextProps))
    .forEach((name) => {
      ;(dom as any)[name] = ""
    })

  Object.keys(nextProps)
    .filter(isProperty)
    .filter(isNew(previousProps, nextProps))
    .forEach((name) => {
      ;(dom as any)[name] = nextProps[name]
    })

  Object.keys(nextProps)
    .filter(isEvent)
    .filter(isNew(previousProps, nextProps))
    .forEach((name) => {
      const eventType = name.toLowerCase().substring(2)
      dom.addEventListener(eventType, nextProps[name])
    })
}
```

这个函数做了四类事情：

1. 删除旧的、已经不存在或已经变化的事件。
2. 删除旧的、已经不存在的普通属性。
3. 设置新的、发生变化的普通属性。
4. 添加新的、发生变化的事件。

对文本节点来说，`nodeValue` 也是属性，所以文本更新也能走这套逻辑。

比如：

```text
旧文本：0
新文本：1
```

最后会变成：

```ts
dom.nodeValue = 1
```

---

## 33. commit 阶段只处理有变化的节点

现在 `commitWork` 不能再无脑 `appendChild`。

它要根据 `effectTag` 做不同操作：

```ts
function commitRoot() {
  deletions.forEach(commitWork)

  if (wipRoot?.child) {
    commitWork(wipRoot.child)
  }

  currentRoot = wipRoot
  wipRoot = null
}

function commitWork(fiber: Fiber | null) {
  if (!fiber) return

  let parentFiber = fiber.parent
  while (parentFiber && !parentFiber.dom) {
    parentFiber = parentFiber.parent
  }

  const parentDom = parentFiber?.dom

  if (fiber.effectTag === "PLACEMENT" && fiber.dom && parentDom) {
    parentDom.appendChild(fiber.dom)
  } else if (fiber.effectTag === "UPDATE" && fiber.dom) {
    updateDom(fiber.dom, fiber.alternate?.props ?? {}, fiber.props)
  } else if (fiber.effectTag === "DELETION" && parentDom) {
    commitDeletion(fiber, parentDom)
    return
  }

  commitWork(fiber.child)
  commitWork(fiber.sibling)
}
```

这里还有一个细节：函数组件本身没有 DOM，所以删除时也要往下找真正的 DOM 节点。

```ts
function commitDeletion(fiber: Fiber, parentDom: Node) {
  if (fiber.dom) {
    parentDom.removeChild(fiber.dom)
  } else if (fiber.child) {
    commitDeletion(fiber.child, parentDom)
  }
}
```

现在更新流程就变成：

```text
setState
  ↓
创建新的 wipRoot
  ↓
重新执行函数组件，得到新元素
  ↓
reconcileChildren 比较新旧 Fiber
  ↓
给 Fiber 打上 PLACEMENT / UPDATE / DELETION 标记
  ↓
commitRoot 统一提交
  ↓
只新增、更新、删除真正变化的 DOM
```

---

## 34. 用计数器串起完整流程

还是这个组件：

```tsx
function Counter() {
  const [count, setCount] = useState(0)

  return createElement(
    "button",
    {
      onclick: () => setCount((count) => count + 1),
    },
    count,
  )
}
```

第一次渲染时：

```text
没有旧 Fiber
  ↓
button 是 PLACEMENT
  ↓
文本 0 是 PLACEMENT
  ↓
commit 后页面出现 <button>0</button>
```

点击按钮后：

```text
setCount(count => count + 1)
  ↓
旧 hook 的 queue 里多了一个更新函数
  ↓
重新执行 Counter
  ↓
useState 得到新 count：1
  ↓
返回新的 button 元素
  ↓
新 button 和旧 button 类型相同：UPDATE
  ↓
新文本 1 和旧文本 0 都是 TEXT_ELEMENT：UPDATE
  ↓
commit 时复用旧 button，只把文本 nodeValue 从 0 改成 1
```

最终页面不是重新追加一个按钮，而是只更新按钮里的文本。

这就是“只更新变化节点”的核心思路。

---

## 35. 这个简化版 diff 的限制

上面的比较逻辑已经能帮助理解 React 的基本思路，但它仍然非常简化。

它目前主要按顺序比较子节点：

```text
旧 children[0] 对比 新 children[0]
旧 children[1] 对比 新 children[1]
旧 children[2] 对比 新 children[2]
```

如果列表只是简单追加，效果还可以。

但如果列表发生重新排序：

```text
旧：A B C
新：B A C
```

这个简化算法可能会误以为很多节点都变了。

真实 React 会借助 `key` 来识别列表里的节点身份：

```tsx
items.map((item) => <li key={item.id}>{item.name}</li>)
```

`key` 的意义是告诉 React：

> 不要只按位置判断节点，要按稳定身份判断节点。

这也是为什么[[React遍历的时候为什么不推荐用索引作为key值]]


---

## 36. React.memo：让没变的子组件跳过重新渲染

前面讲 diff 时，我们重点解决的是：

> 已经进入更新流程后，如何比较新旧 Fiber，并只更新变化的 DOM。

但还有一个更早的问题：

> 如果一个子组件的 `props` 根本没变，能不能连这个子组件的重新计算都跳过？

这就是 `React.memo` 要解决的问题。

假设有这样的组件：

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

当 `Parent` 的 `count` 变化时，`Parent` 会重新渲染。默认情况下，`Child` 也会跟着重新执行一次，即使它收到的 `name` 仍然是 `"Akiyama"`。

如果 `Child` 很重，这就可能浪费性能。

可以用 `React.memo` 包住子组件：

```tsx
const Child = React.memo(function Child({ name }) {
  console.log("Child render")
  return <p>{name}</p>
})
```

这样当父组件重新渲染时，React 会先比较 `Child` 的新旧 `props`：

```text
旧 props：{ name: "Akiyama" }
新 props：{ name: "Akiyama" }
  ↓
浅比较后发现没变
  ↓
跳过 Child 的重新渲染
```

你可以把 `React.memo` 理解成函数组件版本的“是否需要更新”判断：

```text
props 没变 → 复用上一次的渲染结果
props 变了 → 重新执行组件
```

不过它不是万能优化。因为 `React.memo` 默认做的是浅比较：

```tsx
<Child user={{ name: "Akiyama" }} />
```

这里每次父组件渲染都会创建一个新的对象，虽然内容一样，但引用不同：

```text
旧 user !== 新 user
```

所以 `React.memo` 仍然会失效。

这时通常要配合 [[useMemo]] 或 [[useCallback]] 稳定传给子组件的对象和函数引用。

更详细的使用场景、失效原因和自定义比较函数，可以看 [[React.memo]]。它也属于 [[React性能优化]] 里的组件级优化手段。

---

## 37. 这套实现和真实 React 的差距

到这里，我们已经理解了 React 的几个关键思想，但这个版本仍然非常简化。

真实 React 还会处理很多复杂问题，例如：

- 更复杂的 diff 算法，尤其是列表移动和 `key`。
- 更完善的事件系统，不是简单地直接绑定 DOM 事件。
- 更复杂的优先级调度，不同更新有不同紧急程度。
- 更完整的 hook 实现，包括 `useMemo`、`useRef`、`useLayoutEffect` 等。
- 更丰富的组件级优化，例如 `React.memo`、`PureComponent`、跳过子树渲染等。
- 更精细的更新批处理。
- 并发渲染、Suspense、错误边界等高级能力。

但对入门理解来说，你只要先抓住这几句话：

> JSX 是 UI 的语法糖。
>
> `createElement` 把 UI 变成对象。
>
> `render` 根据对象构建 Fiber 任务。
>
> Fiber 让渲染可以被拆成小任务。
>
> `useState` 保存状态，并触发重新渲染。
>
> `useEffect` 登记副作用，并在 DOM 提交完成后执行。
>
> `reconcileChildren` 比较新旧 Fiber，并标记变化。
>
> `commit` 阶段才真正操作 DOM，而且只操作变化的部分。

---

## 38. 总结

我们从最小版本一步步构建了自己的 React：

1. JSX 被转成 `createElement`。
2. `createElement` 返回普通 JavaScript 对象。
3. `render` 可以把对象递归变成 DOM。
4. 为了解决大任务阻塞，引入 Fiber。
5. Fiber 把渲染拆成一个个工作单元。
6. `workLoop` 在浏览器空闲时处理工作。
7. 函数组件是执行后返回 UI 对象的函数。
8. `useState` 通过 hook 数组和调用顺序保存状态。
9. hook 不能写在条件语句里，因为 React 依赖稳定的 `hookIndex` 顺序找回旧 hook。
10. `setState` 不是直接改 DOM，而是安排一次重新渲染。
11. `useEffect` 在渲染阶段登记副作用，在 commit 后执行副作用。
12. effect 回调不能直接是 `async` 函数，因为 React 只接受 `undefined` 或 cleanup 函数作为返回值。
13. effect 依赖变化时，先执行旧 cleanup，再执行新 effect。
14. 重新渲染时会生成新的 Fiber 树。
15. 新 Fiber 通过 `alternate` 找到旧 Fiber。
16. 新旧 Fiber 类型相同就复用 DOM，只更新变化属性。
17. 新节点不存在于旧树中就新增。
18. 旧节点不存在于新树中就删除。
19. `commit` 统一执行新增、更新、删除，并在 DOM 更新后执行 effect。
20. `React.memo` 可以在子组件 `props` 没变时跳过子组件重新渲染。

如果你能理解这条链路，再去看 React 官方文档里的渲染、状态、协调、Fiber，就会轻松很多。

---

## reference

- [Build your own React](https://pomb.us/build-your-own-react/)
- [didact-explain](https://github.com/chinanf-boy/didact-explain?tab=readme-ov-file#1-%E6%B8%B2%E6%9F%93dom%E5%85%83%E7%B4%A0)
