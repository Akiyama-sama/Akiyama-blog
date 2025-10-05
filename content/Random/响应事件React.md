---
tags:
  - '#pernamant'
  - React
---
## 添加事件处理函数

如需添加一个事件处理函数，你需要先定义一个函数，然后 [将其作为 prop 传入](https://zh-hans.react.dev/learn/passing-props-to-a-component) 合适的 JSX 标签。例如，这里有一个没绑定任何事件的按钮：

按照如下三个步骤，即可让它在用户点击时显示消息：

1. 在 `Button` 组件 **内部** 声明一个名为 `handleClick` 的函数。
2. 实现函数内部的逻辑（使用 `alert` 来显示消息）。
3. 添加 `onClick={handleClick}` 到 `<button>` JSX 中。

你可以定义 `handleClick` 函数然后 [将其作为 prop 传入](https://zh-hans.react.dev/learn/passing-props-to-a-component) `<button>`。其中 `handleClick` 是一个 **事件处理函数** 。事件处理函数有如下特点:

- 通常在你的组件 **内部** 定义。
- 名称以 `handle` 开头，后跟事件名称。

> 按照惯例，通常将事件处理程序命名为 `handle`，后接事件名。你会经常看到 `onClick={handleClick}`，`onMouseEnter={handleMouseEnter}` 等。

或者，你也可以在 JSX 中定义一个内联的事件处理函数：

```text
<button onClick={function handleClick() {
alert('你点击了我！');
}}>
```

或者，直接使用更为简洁箭头函数：

```text
<button onClick={() => {
alert('你点击了我！');
}}>
```

以上所有方式都是等效的。当函数体较短时，内联事件处理函数会很方便。

### 陷阱

传递给事件处理函数的函数应直接传递，而非调用。例如：

| 传递一个函数（正确） | 调用一个函数（错误） |
| --- | --- |
| `<button onClick={handleClick}>` | `<button onClick={handleClick()}>` |

区别很微妙。在第一个示例中，`handleClick` 函数作为 `onClick` 事件处理函数传递。这会让 React 记住它，并且只在用户点击按钮时调用你的函数。

在第二个示例中，`handleClick()` 中最后的 `()` 会在 [渲染](https://zh-hans.react.dev/learn/render-and-commit) 过程中 **立即** 触发函数，即使没有任何点击。这是因为位于 [JSX `{}`](https://zh-hans.react.dev/learn/javascript-in-jsx-with-curly-braces) 之间的 JavaScript 会立即执行。

当你编写内联代码时，同样的陷阱可能会以不同的方式出现：

| 传递一个函数（正确） | 调用一个函数（错误） |
| --- | --- |
| `<button onClick={() => alert('...')}>` | `<button onClick={alert('...')}>` |

如果按如下方式传递内联代码，并不会在点击时触发，而是会在每次组件渲染时触发：

```text
// 这个 alert 在组件渲染时触发，而不是点击时触发！
<button onClick={alert('你点击了我！')}>
```

如果你想要定义内联事件处理函数，请将其包装在匿名函数中，如下所示：

```text
<button onClick={() => alert('你点击了我！')}>
```

这里创建了一个稍后调用的函数，而不会在每次渲染时执行其内部代码。

在这两种情况下，你都应该传递一个函数：

- `<button onClick={handleClick}>` 传递了 `handleClick` 函数。
- `<button onClick={() => alert('...')}>` 传递了 `() => alert('...')` 函数。

> [了解更多箭头函数的信息](https://zh.javascript.info/arrow-functions-basics)。

### 在事件处理函数中读取 props

由于事件处理函数声明于组件内部，因此它们可以直接访问组件的 props。示例中的按钮，当点击时会弹出带有 `message` prop 的 alert：

此处有两个按钮，会展示不同的消息。你可以尝试更改传递给它们的消息。

### 将事件处理函数作为 props 传递

通常，我们会在父组件中定义子组件的事件处理函数。比如：置于不同位置的 `Button` 组件，可能最终执行的功能也不同 —— 也许是播放电影，也许是上传图片。

```js
function Button({ onClick, children }) {
  return (
    <button onClick={onClick}>
      {children}
    </button>
  );
}

function PlayButton({ movieName }) {
  function handlePlayClick() {
    alert(`正在播放 ${movieName}！`);
  }

  return (
    <Button onClick={handlePlayClick}>
      播放 "{movieName}"
    </Button>
  );
}

function UploadButton() {
  return (
    <Button onClick={() => alert('正在上传！')}>
      上传图片
    </Button>
  );
}

export default function Toolbar() {
  return (
    <div>
      <PlayButton movieName="魔女宅急便" />
      <UploadButton />
    </div>
  );
}

```
示例中，`Toolbar` 组件渲染了一个 `PlayButton` 组件和 `UploadButton` 组件：

- `PlayButton` 将 `handlePlayClick` 作为 `onClick` prop 传入 `Button` 组件内部。
- `UploadButton` 将 `() => alert('正在上传！')` 作为 `onClick` prop 传入 `Button` 组件内部。

最后，你的 `Button` 组件接收一个名为 `onClick` 的 prop。它直接将这个 prop 以 `onClick={onClick}` 方式传递给浏览器内置的 `<button>`。当点击按钮时，React 会调用传入的函数。

如果你遵循某个 [设计系统](https://uxdesign.cc/everything-you-need-to-know-about-design-systems-54b109851969) 时，按钮之类的组件通常会包含样式，但不会指定行为。而 `PlayButton` 和 `UploadButton` 之类的组件则会向下传递事件处理函数。

### 命名事件处理函数 prop

内置组件（`<button>` 和 `<div>`）仅支持 [浏览器事件名称](https://zh-hans.react.dev/reference/react-dom/components/common#common-props)，例如 `onClick`。但是，当你构建自己的组件时，你可以按你个人喜好命名事件处理函数的 prop。

> 按照惯例，事件处理函数 props 应该以 `on` 开头，后跟一个大写字母。

例如，`Button` 组件的 `onClick` prop 本来也可以被命名为 `onSmash`：
```js
function Button({ onSmash, children }) {
  return (
    <button onClick={onSmash}>
      {children}
    </button>
  );
}

export default function App() {
  return (
    <div>
      <Button onSmash={() => alert('正在播放！')}>
        播放电影
      </Button>
      <Button onSmash={() => alert('正在上传！')}>
        上传图片
      </Button>
    </div>
  );
}

```

上述示例中，`<button onClick={onSmash}>` 代表浏览器内置的 `<button>`（小写）仍然需要使用 `onClick` prop，而自定义的 `Button` 组件接收到的 prop 名称可由你决定！

当你的组件支持多种交互时，你可以根据不同的应用程序命名事件处理函数 prop。例如，一个 `Toolbar` 组件接收 `onPlayMovie` 和 `onUploadImage` 两个事件处理函数：

请注意，`App` 组件并不需要知道 `Toolbar` 将会对 `onPlayMovie` 和 `onUploadImage` 做 **什么** 。上述示例是 `Toolbar` 的实现细节。其中，`Toolbar` 将它们作为 `onClick` 处理函数传递给了 `Button` 组件，其实还可以通过键盘快捷键来触发它们。根据应用程序特定的交互方式（如 `onPlayMovie`）来命名 prop ，可以让你灵活地更改以后使用它们的方式。

## 事件传播

事件处理函数还将捕获任何来自子组件的事件。通常，我们会说事件会沿着树向上“冒泡”或“传播”：它从事件发生的地方开始，然后沿着树向上传播。

下面这个 `<div>` 包含两个按钮。`<div>` 和每个按钮都有自己的 `onClick` 处理函数。你认为点击按钮时会触发哪些处理函数？

如果你点击任一按钮，它自身的 `onClick` 将首先执行，然后父级 `<div>` 的 `onClick` 会接着执行。因此会出现两条消息。如果你点击 toolbar 本身，将只有父级 `<div>` 的 `onClick` 会执行。

### 陷阱

在 React 中所有事件都会传播，除了 `onScroll`，它仅适用于你附加到的 JSX 标签。

### 阻止传播

事件处理函数接收一个 **事件对象** 作为唯一的参数。按照惯例，它通常被称为 `e` ，代表 “event”（事件）。你可以使用此对象来读取有关事件的信息。

这个事件对象还允许你阻止传播。如果你想阻止一个事件到达父组件，你需要像下面 `Button` 组件那样调用 `e.stopPropagation()` ：

```js
export default function Toolbar() {
  return (
    <div className="Toolbar" onClick={() => {
      alert('你点击了 toolbar ！');
    }}>
      <button onClick={() => alert('正在播放！')}>
        播放电影
      </button>
      <button onClick={() => alert('正在上传！')}>
        上传图片
      </button>
    </div>
  );
}

```
当你点击按钮时：

1. React 调用了传递给 `<button>` 的 `onClick` 处理函数。
2. 定义在 `Button` 中的处理函数执行了如下操作：
- 调用 `e.stopPropagation()`，阻止事件进一步冒泡。
- 调用 `onClick` 函数，它是从 `Toolbar` 组件传递过来的 prop。
3. 在 `Toolbar` 组件中定义的函数，显示按钮对应的 alert。
4. 由于传播被阻止，父级 `<div>` 的 `onClick` 处理函数不会执行。

由于调用了 `e.stopPropagation()`，点击按钮现在将只显示一个 alert（来自 `<button>`），而并非两个（分别来自 `<button>` 和父级 toolbar `<div>`）。点击按钮与点击周围的 toolbar 不同，因此阻止传播对这个 UI 是有意义的。

### 阻止默认行为

某些浏览器事件具有与事件相关联的默认行为。例如，点击 `<form>` 表单内部的按钮会触发表单提交事件，默认情况下将重新加载整个页面：
你可以调用事件对象中的 `e.preventDefault()` 来阻止这种情况发生：
```js
export default function Signup() {
  return (
    <form onSubmit={e => {
      e.preventDefault();
      alert('提交表单！');
    }}>
      <input />
      <button>发送</button>
    </form>
  );
}

```
不要混淆 `e.stopPropagation()` 和 `e.preventDefault()`。它们都很有用，但二者并不相关：

- [`e.stopPropagation()`](https://developer.mozilla.org/docs/Web/API/Event/stopPropagation) 阻止触发绑定在外层标签上的事件处理函数。
- [`e.preventDefault()`](https://developer.mozilla.org/docs/Web/API/Event/preventDefault) 阻止少数事件的默认浏览器行为。

# 小练习

## 关联事件

`ColorSwitch` 组件渲染了一个按钮。它应该改变页面颜色。将它与从父组件接收的 `onChangeColor` 事件处理函数关联，以便在点击按钮时改变颜色。

如此操作后，你会发现点击按钮时，也会增加页面点击计数器的值。而编写父组件的同事坚持认为 `onChangeColor` 不应该使得计数器的值递增。应该如何处理？修改问题使得点击按钮 **只** 改变颜色，并且 **不** 增加计数器。

```js
export default function ColorSwitch({
  onChangeColor
}) {
  return (
    <button onClick={e => {
      e.stopPropagation();
      onChangeColor();
    }}>
      改变颜色
    </button>
  );
}

```
在子组件中调用 e.stopPropagation();
注意是调用 onChangeColor();
而不是传递：onChangeColor

这里本来onClick传递的是一个箭头函数e=>{}这个箭头函数里面写的表达式应该是javascript了。


# reference
