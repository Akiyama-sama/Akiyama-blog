---
tags:
  - "#pernamant"
  - Javascript
---
**A1. 要素 (核心零件)**
- **事件源 (Event Target):** 真正被点击的那个最小元素。
- **传播路径 (Path):** Window <-> ... <-> Parent <-> Target。
- **监听器 (Listener):** `element.addEventListener('click', fn, useCapture)`
    - 第三个参数是关键：`false` (默认) 监听冒泡；`true` 监听捕获。

**A2. 结构 (三阶段)** 标准事件流（W3C标准）必然遵循以下顺序：
1. **捕获 (Capturing):** 从外向内。目的在于让父级元素有机会在子级元素之前处理事件。
2. **目标 (Target):** 到达源头。
3. **冒泡 (Bubbling):** 从内向外。**这是我们最常利用的阶段。**

**A3. 系统 (涌现功能)** 这套双向机制涌现出了一个极其重要的设计模式：**[[事件委托]] (Event Delegation)**。 既然所有子元素的事件最终都会“冒泡”给父元素，那我们完全没必要给 1000 个子元素都绑定监听器，只需要给父元素绑定 **1 个**监听器就够了。


**阻止事件流**
有时候我们不希望事件继续传播（比如防止点击子按钮触发父组件的跳转）：
- **`event.stopPropagation()`**:
    - **切断后续传播**。如果在捕获阶段调用，事件就不再往下传；如果在冒泡阶段调用，事件就不再往上传，如果传到有监听捕获/冒泡的其他事件的dom元素，还是会执行，只不过不继续传播到子元素/父元素了
- **`event.stopImmediatePropagation()`**:
    - 比上面更狠。如果一个元素绑定了多个 click 事件，`stopPropagation` 只能阻止事件传给父级，但当前元素剩下的 click 监听器还会执行。而这个方法会把当前元素剩下的监听器也全部杀掉。


1. **纵向传播**：事件在不同 DOM 节点之间传递（冒泡传给父级，捕获传给子级）。
2. **横向执行**：同一个 DOM 节点上，绑定了多个 `click` 监听函数。


## 常见面试题与答案解析

### 1. 什么是 DOM 事件流？

**答案：**

DOM 事件流指的是一个事件从发生到结束，在 DOM 树中的传播过程。

标准的 DOM 事件流分为 3 个阶段：

1. 捕获阶段
2. 目标阶段
3. 冒泡阶段

也就是说，一个点击事件并不是只在目标元素上触发一次，而是会沿着 DOM 树先向下，再在目标点触发，最后再向上传播。

==注意，目标的 dom 注册了捕获/冒泡阶段的回调，是没有方向之分的，即是先执行捕获的回调还是冒泡的回调，主要看是谁先注册==

**解析：**

面试官问这个问题，通常是想确认你是否理解“事件不是只发生在当前元素”，而是一个传播过程。很多后续问题，比如[[事件委托]]、`stopPropagation`、`target/currentTarget`，都建立在这个基础上。

### 2. DOM 事件流的执行顺序是什么？

**答案：**

执行顺序是：

- 捕获：`window -> document -> html -> body -> ... -> target`
- 目标：到达事件源元素
- 冒泡：`target -> ... -> body -> html -> document -> window`

**解析：**

默认情况下，我们平时通过 `addEventListener('click', fn)` 绑定的监听器，监听的是冒泡阶段。

只有当你显式传入 `true`，或者 `{ capture: true }` 时，才会在捕获阶段触发。

### 3. `addEventListener` 的第三个参数有什么作用？

**答案：**

第三个参数用于控制监听器的行为，最常见的是控制是否在捕获阶段执行。

比如：

```js
element.addEventListener('click', fn, true)
element.addEventListener('click', fn, { capture: true })
```

上面都表示在捕获阶段监听。

如果不传，默认相当于：

```js
element.addEventListener('click', fn, false)
```

也就是在冒泡阶段监听。

**解析：**

现代浏览器里第三个参数更常写成对象形式，因为除了 `capture` 之外，还可以配置：

- `once`：只触发一次
- `passive`：告诉浏览器监听器里不会调用 `preventDefault`

### 4. `event.target` 和 `event.currentTarget` 有什么区别？

**答案：**

- `event.target`：真正触发事件的元素。
- `event.currentTarget`：当前正在执行监听函数的元素。

例如点击一个按钮，按钮在 `div` 里面：

- 如果监听器绑在按钮上，二者通常相同。
- 如果监听器绑在 `div` 上，而点击的是按钮：
  - `target` 是按钮
  - `currentTarget` 是 `div`

**解析：**

这是[[事件委托]]最常考的知识点。父元素通过 `event.target` 判断“到底是哪个子元素触发了事件”，从而只绑定一个监听器就处理多个子元素。

### 5. `preventDefault`、`stopPropagation`、`stopImmediatePropagation` 有什么区别？

**答案：**

- `event.preventDefault()`：阻止默认行为。
  - 比如阻止 `a` 标签跳转、阻止表单提交。
- `event.stopPropagation()`：阻止事件继续传播。
  - 但不会阻止当前元素上其他同类型监听器执行。
- `event.stopImmediatePropagation()`：不仅阻止继续传播，还会阻止当前元素后续其他同类型监听器执行。

**解析：**

这是一个非常经典的对比题。

可以这样记：

- `preventDefault` 管“默认动作”
- `stopPropagation` 管“纵向传播”
- `stopImmediatePropagation` 管“纵向传播 + 当前节点横向监听器”

### 6. 什么是事件委托？为什么它依赖冒泡？

**答案：**

事件委托就是不把事件监听器绑在每个子元素上，而是统一绑到它们的父元素上，再通过事件冒泡和 `event.target` 来判断具体点击了谁。

**解析：**

例如一个列表有 1000 个 `li`，没必要给 1000 个节点都绑 `click`，只需要给 `ul` 绑 1 个监听器。

优点：

- 减少监听器数量
- 降低内存开销
- 动态添加的子元素也能自动响应事件

它之所以可行，本质上就是因为子元素的事件会冒泡到父元素。

### 7. 哪些事件不冒泡？

**答案：**

常见的不冒泡事件有：

- `focus`
- `blur`
- `mouseenter`
- `mouseleave`
- `load`
- `unload`

**解析：**

这个问题经常和事件委托一起考。

因为事件委托通常依赖冒泡，所以像 `focus`、`blur` 这种事件不能直接按普通冒泡思路处理。

不过浏览器也提供了可冒泡的替代事件：

- `focusin`
- `focusout`

### 8. 如果同一个元素同时绑定了捕获和冒泡监听器，谁先执行？

**答案：**

同一个元素上，如果同时有捕获监听器和冒泡监听器，捕获监听器先执行，冒泡监听器后执行。

例如：

```js
btn.addEventListener('click', () => console.log('bubble'))
btn.addEventListener('click', () => console.log('capture'), true)
```

点击按钮时，会先输出 `capture`，再输出 `bubble`。

**解析：**

虽然事件到达目标元素后进入目标阶段，但浏览器在执行具体监听器时，仍然会区分它到底是“以捕获方式注册的”，还是“以冒泡方式注册的”。

### 9. 为什么前端开发里更常用冒泡，而不是捕获？

**答案：**

因为冒泡更符合大多数业务场景，尤其适合事件委托、组件交互和父组件统一接管子元素事件。

**解析：**

捕获并不是不能用，而是用得少。它更适合某些“父级需要抢先处理”的场景，比如：

- 全局埋点
- 全局拦截
- 某些安全或权限控制逻辑

而日常 UI 交互大部分都发生在目标元素触发后再向上传递，所以冒泡更自然。

### 10. 事件流和 React 事件机制有什么关系？

**答案：**

React 的合成事件本质上也是建立在原生 DOM 事件流之上的，只不过 React 在上层做了一层封装。

**解析：**

React 早期通过事件委托把大量事件统一挂到 `document` 上，后面版本调整为挂到 root 容器上，但底层仍然离不开 DOM 的捕获和冒泡机制。

所以如果你不理解 DOM 事件流，就很难真正理解 React 的事件系统。

### 11. 面试时怎么一句话解释 DOM 事件流？

**答案：**

DOM 事件流就是事件在 DOM 树中传播的过程，顺序是先捕获、再到目标、最后冒泡；前端中大量事件处理、事件委托和传播控制都建立在这个机制之上。

## 面试速记版

- DOM 事件流分为：捕获、目标、冒泡。
- 默认 `addEventListener` 监听的是冒泡阶段。
- `target` 是真正触发事件的元素，`currentTarget` 是当前执行监听器的元素。
- `preventDefault` 阻止默认行为，`stopPropagation` 阻止传播，`stopImmediatePropagation` 连同当前节点后续监听器也一起阻止。
- [[事件委托]] 依赖冒泡，本质是父元素统一监听，靠 `event.target` 判断子元素。
- `focus`、`blur`、`mouseenter`、`mouseleave` 等常见事件不冒泡。



# reference
https://www.youtube.com/watch?v=XF1_MlZ5l6M
