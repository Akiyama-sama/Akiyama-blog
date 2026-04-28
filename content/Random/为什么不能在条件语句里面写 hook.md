---
date: 2026-04-21
tags:
---
因为 react 在做一个 Fiber 的时候会将 hook 以一个链表的形式给存储在 Fiber 当中，为何？因为这样仅作顺序比遍历即可，无需用 key 做 map 。

如果你在条件语句当中用了 hook，就会导致错位，例如：

这是由 React 的**状态复用逻辑**决定的。React 在“挂载（Mount）”和“更新（Update）”时，对 Hook 的处理逻辑如下
### 挂载阶段 (Mount)
当你第一次调用 `useState` 时，React 会按顺序创建 Hook 节点并连成链表。
- Hook 1: `count`
- Hook 2: `name`
- Hook 3: `age`
### 更新阶段 (Update)

当组件重新渲染时，React 并不知道你代码里的变量名。它唯一能做的就是**重新走到那行代码，并把指针指向链表的下一个节点**。

### 冲突模拟

假设你的代码如下
```JavaScript
function MyComponent() {
  const [count, setCount] = useState(0); // Hook 1

  if (count > 0) {
    const [name, setName] = useState("Alice"); // Hook 2
  }

  const [age, setAge] = useState(25); // Hook 3
}
```

1. **第一次渲染**：`count` 是 0，`if` 不执行。链表结构为：`Hook1(count) -> Hook2(age)`。
2. **触发更新**：你把 `count` 设为 1。
3. **第二次渲染**：
    - 执行到第一个 `useState`：React 找到链表第 1 个节点，匹配给 `count`。**正常**。
    - 执行到 `if` 内部的 `useState`：React 找到链表第 2 个节点。此时链表第 2 个节点存的是上次的 `age` 数据，但现在却被分配给了 `name`。**错位开始**。
    - 执行到最后的 `useState(age)`：React 试图找第 3 个节点，但链表已经结束了。**崩溃或数据彻底错乱**。