---
tags:
  - '#pernamant'
  - React
---
你可以更新多个 state 变量——甚至来自多个组件的 state 变量——而不会触发太多的 [重新渲染](https://zh-hans.react.dev/learn/render-and-commit#re-renders-when-state-updates)。但这也意味着只有在你的事件处理函数及其中任何代码执行完成 **之后**，UI 才会更新。这种特性也就是 **批处理**，它会使你的 React 应用运行得更快。它还会帮你避免处理只​​更新了一部分 state 变量的令人困惑的“半成品”渲染。

**React 不会跨 *多个* 需要刻意触发的事件（如点击）进行批处理**——每次点击都是单独处理的。请放心，React 只会在一般来说安全的情况下才进行批处理。这可以确保，例如，如果第一次点击按钮会禁用表单，那么第二次点击就不会再次提交它。


==简单来说：
- **函数形式的更新（`setNumber(n => n + 1)`）**：这种更新方式可以确保每次更新基于 **最新的 `number` 值**。React 会在更新时将当前的最新 state 值作为参数传递给 `n`，所以在第二次 `setNumber` 调用时，`n` 是已经更新过的 `5`。
    
- **直接传值（`setNumber(number + 1)`）**：这种更新方式每次都是基于 **事件触发时的 `number` 值**，即使你调用了多次 `setNumber`，每次它都使用的是同一个 `number` 值（即事件触发时的值），因此不会更新为预期的递增值。
## 在下次渲染前多次更新同一个 state

这是一个不常见的用例，但是如果你想在下次渲染之前多次更新同一个 state，你可以像 `setNumber(n => n + 1)` 这样传入一个根据队列中的前一个 state 计算下一个 state 的 **函数**，而不是像 `setNumber(number + 1)` 这样传入 **下一个 state 值**。这是一种告诉 React “用 state 值做某事”而不是仅仅替换它的方法。

现在尝试递增计数器：

在这里，`n => n + 1` 被称为 **更新函数**。当你将它传递给一个 state 设置函数时：

1. React 会将此函数加入队列，以便在事件处理函数中的所有其他代码运行后进行处理。
2. 在下一次渲染期间，React 会遍历队列并给你更新之后的最终 state。

```text
setNumber(n => n + 1);
setNumber(n => n + 1);
setNumber(n => n + 1);
```

下面是 React 在执行事件处理函数时处理这几行代码的过程：

1. `setNumber(n => n + 1)`：`n => n + 1` 是一个函数。React 将它加入队列。
2. `setNumber(n => n + 1)`：`n => n + 1` 是一个函数。React 将它加入队列。
3. `setNumber(n => n + 1)`：`n => n + 1` 是一个函数。React 将它加入队列。

当你在下次渲染期间调用 `useState` 时，React 会遍历队列。之前的 `number` state 的值是 `0`，所以这就是 React 作为参数 `n` 传递给第一个更新函数的值。然后 React 会获取你上一个更新函数的返回值，并将其作为 `n` 传递给下一个更新函数，以此类推：

| 更新队列 | `n` | 返回值 |
| --- | --- | --- |
| `n => n + 1` | `0` | `0 + 1 = 1` |
| `n => n + 1` | `1` | `1 + 1 = 2` |
| `n => n + 1` | `2` | `2 + 1 = 3` |

React 会保存 `3` 为最终结果并从 `useState` 中返回。

这就是为什么在上面的示例中点击“+3”正确地将值增加“+3”。

### 如果你在替换 state 后更新 state 会发生什么

这个事件处理函数会怎么样？你认为 `number` 在下一次渲染中的值是什么？

```text
<button onClick={() => {
setNumber(number + 5);
setNumber(n => n + 1);
}}>
```

这是事件处理函数告诉 React 要做的事情：

1. `setNumber(number + 5)`：`number` 为 `0`，所以 `setNumber(0 + 5)`。React 将 *“替换为 `5`”* 添加到其队列中。
2. `setNumber(n => n + 1)`：`n => n + 1` 是一个更新函数。 React 将 **该函数** 添加到其队列中。

在下一次渲染期间，React 会遍历 state 队列：

| 更新队列 | `n` | 返回值 |
| --- | --- | --- |
| “替换为 `5`” | `0`（未使用） | `5` |
| `n => n + 1` | `5` | `5 + 1 = 6` |

React 会保存 `6` 为最终结果并从 `useState` 中返回。

### 注意

你可能已经注意到，`setState(x)` 实际上会像 `setState(n => x)` 一样运行，只是没有使用 `n`！

### 如果你在更新 state 后替换 state 会发生什么

让我们再看一个例子。你认为 `number` 在下一次渲染中的值是什么？

```text
<button onClick={() => {
setNumber(number + 5);
setNumber(n => n + 1);
setNumber(42);
}}>
```


以下是 React 在执行事件处理函数时处理这几行代码的过程：

1. `setNumber(number + 5)`：`number` 为 `0`，所以 `setNumber(0 + 5)`。React 将 *“替换为 `5`”* 添加到其队列中。
2. `setNumber(n => n + 1)`：`n => n + 1` 是一个更新函数。React 将该函数添加到其队列中。
3. `setNumber(42)`：React 将 *“替换为 `42`”* 添加到其队列中。

在下一次渲染期间，React 会遍历 state 队列：

| 更新队列 | `n` | 返回值 |
| --- | --- | --- |
| “替换为 `5`” | `0`（未使用） | `5` |
| `n => n + 1` | `5` | `5 + 1 = 6` |
| “替换为 `42`” | `6`（未使用） | `42` |

然后 React 会保存 `42` 为最终结果并从 `useState` 中返回。

总而言之，以下是你可以考虑传递给 `setNumber` state 设置函数的内容：

- **一个更新函数**（例如：`n => n + 1`）会被添加到队列中。
- **任何其他的值**（例如：数字 `5`）会导致“替换为 `5`”被添加到队列中，已经在队列中的内容会被忽略。

事件处理函数执行完成后，React 将触发重新渲染。在重新渲染期间，React 将处理队列。更新函数会在渲染期间执行，因此 **更新函数必须是 [纯函数](https://zh-hans.react.dev/learn/keeping-components-pure)** 并且只 **返回** 结果。不要尝试从它们内部设置 state 或者执行其他副作用。在严格模式下，React 会执行每个更新函数两次（但是丢弃第二个结果）以便帮助你发现错误。

### 命名惯例

通常可以通过相应 state 变量的第一个字母来命名更新函数的参数：

```text
setEnabled(e => !e);
setLastName(ln => ln.reverse());
setFriendCount(fc => fc * 2);
```

如果你喜欢更冗长的代码，另一个常见的惯例是重复使用完整的 state 变量名称，如 `setEnabled(enabled => !enabled)`，或使用前缀，如 `setEnabled(prevEnabled => !prevEnabled)`。


# 小练习

修复请求计数器你正在开发一个艺术市场应用，该应用允许一个用户为一个艺术品同时提交多个订单。每次用户按下“购买”按钮，“等待”计数器应该增加一。三秒后，“等待”计数器应该减少，“完成”计数器应该增加。

但是，“等待”计数器的行为并不符合预期。当你按下“购买”按钮时，它会减少到 `-1`（这本应该是不可能的）。如果你快速点击两次，两个计数器似乎都会出现无法预测的行为。
```js
import { useState } from 'react';

export default function RequestTracker() {
  const [pending, setPending] = useState(0);
  const [completed, setCompleted] = useState(0);

  async function handleClick() {
    setPending(p => p + 1);
    await delay(3000);
    setPending(p => p - 1);
    setCompleted(c => c + 1);
  }

  return (
    <>
      <h3>
        等待：{pending}
      </h3>
      <h3>
        完成：{completed}
      </h3>
      <button onClick={handleClick}>
        购买
      </button>
    </>
  );
}

function delay(ms) {
  return new Promise(resolve => {
    setTimeout(resolve, ms);
  });
}

```
在 `handleClick` 事件处理函数内部，`pending` 和 `completed` 的值与他们在点击事件发生时的值相对应。对于第一次渲染，`pending` 为 `0` ，因此 `setPending(pending - 1)` 变成了 `setPending(-1)`，而这是错误的。既然你想要 _增加_ 或 _减少_ 计数器，你可以改为传递更新函数，而不是将计数器设置为在点击期间确定的具体值


# 与AI的问答
<button onClick={() => { setNumber(number + 5); // 第一个更新 setNumber(n => n + 1); // 第二个更新 }}>增加数字</button>那为什么执行这里setNumber(n => n + 1); 的n会更新为5，而上面的例子不会更新

###### ChatGPT 说：

在你提到的这两种情况中，**`setNumber(n => n + 1)`** 的行为不同，主要是因为它们使用了不同的方式更新 `state`，而 React 如何处理这些更新也有所不同。我们来详细分析一下。

### 第一种情况：

javascript

复制编辑

`<button onClick={() => {   setNumber(number + 5);  // 第一个更新   setNumber(n => n + 1);  // 第二个更新 }}>增加数字</button>`

这里有两个 `setNumber` 调用：

1. `setNumber(number + 5)`
2. `setNumber(n => n + 1)`

#### 为什么 `n` 会更新为 `5`？

- `setNumber(n => n + 1)` 使用的是 **函数形式的 state 更新**，也就是说，它会接收到 **最新的 state 值**，并基于该值进行更新。React 会将 `n => n + 1` 视为一个函数，并将 **当前 `number` 的最新值**（即第一个 `setNumber(number + 5)` 更新后的值）传递给 `n`。
    
- 当你调用 `setNumber(number + 5)` 时，这个更新并不会立即生效，而是被放入更新队列。React 在处理这两个更新时，并没有立刻更新 `number`，所以 **当 React 处理第二个更新时，它使用的是第一个更新后的 `number` 值**（即 `number + 5` 的结果，也就是 `5`）。
    

### 第二种情况：

javascript


`<button onClick={() => {   setNumber(number + 1);   setNumber(number + 1);   setNumber(number + 1); }}>增加数字</button>`

这里有三个 `setNumber` 调用：

1. `setNumber(number + 1)`
2. `setNumber(number + 1)`
3. `setNumber(number + 1)`

#### 为什么这些 `setNumber` 的 `number` 都是 `0`？

- 这三个 `setNumber` 都使用的是 **直接传递 `number + 1`**，它们依赖的是 **事件触发时的 `number` 的值**（即点击时传递的当前 `number` 值）。由于 `setNumber` 是异步更新的，React 不会立刻应用这个更新，而是将它们批量处理。所有的更新操作都会使用 **事件触发时的 `number` 值**，即最初的 `0`。
    
- 在这种情况下，**每个 `setNumber(number + 1)`** 的 `number` 值都是 `0`，因为更新没有立即生效，所以每次 `setNumber` 都是基于最初的 `number` 值进行计算的，而不是之前更新后的值。
    

### 关键区别：

- **函数形式的更新（`setNumber(n => n + 1)`）**：这种更新方式可以确保每次更新基于 **最新的 `number` 值**。React 会在更新时将当前的最新 state 值作为参数传递给 `n`，所以在第二次 `setNumber` 调用时，`n` 是已经更新过的 `5`。
    
- **直接传值（`setNumber(number + 1)`）**：这种更新方式每次都是基于 **事件触发时的 `number` 值**，即使你调用了多次 `setNumber`，每次它都使用的是同一个 `number` 值（即事件触发时的值），因此不会更新为预期的递增值。
    

### 小结：

1. **`setNumber(n => n + 1)`** 使用函数更新时，`n` 会始终是 **当前的 state**，因此每次都基于最新的 `number` 值进行更新。
2. **`setNumber(number + 1)`** 使用值直接更新时，React 会批量处理所有更新，并且每次更新都会使用 **当前事件触发时的 `number` 值**，因此没有递增效果。
# reference
