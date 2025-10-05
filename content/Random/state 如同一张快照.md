---
tags:
  - '#pernamant'
---
**设置 state 只会为下一次渲染变更 state 的值**。在第一次渲染期间，`number` 为 `0`。这也就解释了为什么在 **那次渲染中的** `onClick` 处理函数中，即便在调用了 `setNumber(number + 1)` 之后，`number` 的值也仍然是 `0`：

```js
<button onClick={() => {
setNumber(number + 1);
setNumber(number + 1);
setNumber(number + 1);
}}>+3</button>
```

以下是这个按钮的点击事件处理函数通知 React 要做的事情：

1. `setNumber(number + 1)`：`number` 是 `0` 所以 `setNumber(0 + 1)`。
- React 准备在下一次渲染时将 `number` 更改为 `1`。
2. `setNumber(number + 1)`：`number` 是`0` 所以 `setNumber(0 + 1)`。
- React 准备在下一次渲染时将 `number` 更改为 `1`。
3. `setNumber(number + 1)`：`number` 是`0` 所以 `setNumber(0 + 1)`。
- React 准备在下一次渲染时将 `number` 更改为 `1`。

尽管你调用了三次 `setNumber(number + 1)`，但在 **这次渲染的** 事件处理函数中 `number` 会一直是 `0`，所以你会三次将 state 设置成 `1`。这就是为什么在你的事件处理函数执行完以后，React 重新渲染的组件中的 `number` 等于 `1` 而不是 `3`。

你还可以通过在心里把 state 变量替换成它们在你代码中的值来想象这个过程。由于 **这次渲染** 中的 state 变量 `number` 是 `0`，其事件处理函数看起来会像这样：

```text
<button onClick={() => {
setNumber(0 + 1);
setNumber(0 + 1);
setNumber(0 + 1);
}}>+3</button>
```

对于下一次渲染来说，`number` 是 `1`，因此 **那次渲染中的** 点击事件处理函数看起来会像这样：

```text
<button onClick={() => {
setNumber(1 + 1);
setNumber(1 + 1);
setNumber(1 + 1);
}}>+3</button>
```

这就是为什么再次点击按钮会将计数器设置为 `2`，下次点击时会设为 `3`，依此类推。
## 随时间变化的 state

好的，刚才那些很有意思。试着猜猜点击这个按钮会发出什么警告：

如果你使用之前替换的方法，你就能猜到这个提示框将会显示 “0”：

```text
setNumber(0 + 5);
alert(0);
```

但如果你在这个提示框上加上一个定时器， 使得它在组件重新渲染 **之后** 才触发，又会怎样呢？是会显示 “0” 还是 “5” ？猜一猜！

惊讶吗？你如果使用替代法，就能看到被传入提示框的 state “快照”。

```text
setNumber(0 + 5);
setTimeout(() => {
alert(0);
}, 3000);
```

到提示框运行时，React 中存储的 state 可能已经发生了更改，但它是使用用户与之交互时状态的快照进行调度的！

**一个 state 变量的值永远不会在一次渲染的内部发生变化，** 即使其事件处理函数的代码是异步的。在 **那次渲染的** `onClick` 内部，`number` 的值即使在调用 `setNumber(number + 5)` 之后也还是 `0`。它的值在 React 通过调用你的组件“获取 UI 的快照”时就被“固定”了。





# reference
