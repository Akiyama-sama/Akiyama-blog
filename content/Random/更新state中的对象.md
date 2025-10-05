---
tags:
  - '#pernamant'
  - React
---
## 什么是 mutation？

你可以在 state 中存放任意类型的 JavaScript 值。

```
const [x, setX] = useState(0);
```

到目前为止，你已经尝试过在 state 中存放数字、字符串和布尔值，这些类型的值在 JavaScript 中是不可变（immutable）的，这意味着它们不能被改变或是只读的。你可以通过替换它们的值以触发一次重新渲染。

state `x` 从 `0` 变为 `5`，但是数字 `0` 本身并没有发生改变。在 JavaScript 中，无法对内置的原始值，如数字、字符串和布尔值，进行任何更改。

现在考虑 state 中存放对象的情况：

```
const [position, setPosition] = useState({ x: 0, y: 0 });
```

从技术上来讲，可以改变对象自身的内容。**当你这样做时，就制造了一个 mutation**：

然而，虽然严格来说 React state 中存放的对象是可变的，但你应该像处理数字、布尔值、字符串一样将它们视为不可变的。因此你应该替换它们的值，而不是对它们进行修改。

## 将 state 视为只读的

换句话说，你应该 **把所有存放在 state 中的 JavaScript 对象都视为只读的**。

在下面的例子中，我们用一个存放在 state 中的对象来表示指针当前的位置。当你在预览区触摸或移动光标时，红色的点本应移动。但是实际上红点仍停留在原处：

Unable to establish connection with the sandpack bundler. Make sure you are online or try again later. If the problem persists, please report it via [email](https://zh-hans.react.dev/learn/) or submit an issue on [GitHub.](https://github.com/codesandbox/sandpack/issues)

问题出在下面这段代码中。

```
onPointerMove={e => {
position.x = e.clientX;
position.y = e.clientY;
}}
```

这段代码直接修改了 [上一次渲染中](https://zh-hans.react.dev/learn/state-as-a-snapshot#rendering-takes-a-snapshot-in-time) 分配给 `position` 的对象。但是因为并没有使用 state 的设置函数，React 并不知道对象已更改。所以 React 没有做出任何响应。这就像在吃完饭之后才尝试去改变要点的菜一样。虽然在一些情况下，直接修改 state 可能是有效的，但我们并不推荐这么做。你应该把在渲染过程中可以访问到的 state 视为只读的。

在这种情况下，为了真正地 [触发一次重新渲染](https://zh-hans.react.dev/learn/state-as-a-snapshot#setting-state-triggers-renders)，**你需要创建一个新对象并把它传递给 state 的设置函数**：

```
onPointerMove={e => {
setPosition({
x: e.clientX,
y: e.clientY
});
}}
```

通过使用 `setPosition`，你在告诉 React：

- 使用这个新的对象替换 `position` 的值
- 然后再次渲染这个组件

## 使用展开语法复制对象

在之前的例子中，始终会根据当前指针的位置创建出一个新的 `position` 对象。但是通常，你会希望把 **现有** 数据作为你所创建的新对象的一部分。例如，你可能只想要更新表单中的一个字段，其他的字段仍然使用之前的值。

下面的代码中，输入框并不会正常运行，因为 `onChange` 直接修改了 state ：

例如，下面这行代码修改了上一次渲染中的 state：

```
person.firstName = e.target.value;
```

想要实现你的需求，最可靠的办法就是创建一个新的对象并将它传递给 `setPerson`。但是在这里，你还需要 **把当前的数据复制到新对象中**，因为你只改变了其中一个字段：

```
setPerson({
firstName: e.target.value, // 从 input 中获取新的 first name
lastName: person.lastName,
email: person.email
});
```

你可以使用 `...` [对象展开](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Operators/Spread_syntax#spread_in_object_literals) 语法，这样你就不需要单独复制每个属性。

```
setPerson({
...person, // 复制上一个 person 中的所有字段
firstName: e.target.value // 但是覆盖 firstName 字段 
});
```

现在表单可以正常运行了！

## 更新一个嵌套对象

考虑下面这种结构的嵌套对象：

```text
const [person, setPerson] = useState({
name: 'Niki de Saint Phalle',
artwork: {
title: 'Blue Nana',
city: 'Hamburg',
image: 'https://i.imgur.com/Sd1AgUOm.jpg',
}
});
```

如果你想要更新 `person.artwork.city` 的值，用 mutation 来实现的方法非常容易理解：

```text
person.artwork.city = 'New Delhi';
```

但是在 React 中，你需要将 state 视为不可变的！为了修改 `city` 的值，你首先需要创建一个新的 `artwork` 对象（其中预先填充了上一个 `artwork` 对象中的数据），然后创建一个新的 `person` 对象，并使得其中的 `artwork` 属性指向新创建的 `artwork` 对象：

```text
const nextArtwork = { ...person.artwork, city: 'New Delhi' };
const nextPerson = { ...person, artwork: nextArtwork };
setPerson(nextPerson);
```

或者，写成一个函数调用：

```text
setPerson({
...person, // 复制其它字段的数据 
artwork: { // 替换 artwork 字段 
...person.artwork, // 复制之前 person.artwork 中的数据
city: 'New Delhi' // 但是将 city 的值替换为 New Delhi！
}
});
```

这虽然看起来有点冗长，但对于很多情况都能有效地解决问题：

### ==使用 Immer 编写简洁的更新逻辑

如果你的 state 有多层的嵌套，你或许应该考虑 [将其扁平化](https://zh-hans.react.dev/learn/choosing-the-state-structure#avoid-deeply-nested-state)。但是，如果你不想改变 state 的数据结构，你可能更喜欢用一种更便捷的方式来实现嵌套展开的效果。[Immer](https://github.com/immerjs/use-immer) 是一个非常流行的库，它可以让你使用简便但可以直接修改的语法编写代码，并会帮你处理好复制的过程。通过使用 Immer，你写出的代码看起来就像是你“打破了规则”而直接修改了对象：

```
updatePerson(draft => {
draft.artwork.city = 'Lagos';
});
```

但是不同于一般的 mutation，它并不会覆盖之前的 state！

#### 为什么在 React 中不推荐直接修改 state？

有以下几个原因：

- **调试**：如果你使用 `console.log` 并且不直接修改 state，你之前日志中的 state 的值就不会被新的 state 变化所影响。这样你就可以清楚地看到两次渲染之间 state 的值发生了什么变化
- **优化**：React 常见的 [优化策略](https://zh-hans.react.dev/reference/react/memo) 依赖于如果之前的 props 或者 state 的值和下一次相同就跳过渲染。如果你从未直接修改 state ，那么你就可以很快看到 state 是否发生了变化。如果 `prevObj === obj`，那么你就可以肯定这个对象内部并没有发生改变。
- **新功能**：我们正在构建的 React 的新功能依赖于 state 被 [像快照一样看待](https://zh-hans.react.dev/learn/state-as-a-snapshot) 的理念。如果你直接修改 state 的历史版本，可能会影响你使用这些新功能。
- **需求变更**：有些应用功能在不出现任何修改的情况下会更容易实现，比如实现撤销/恢复、展示修改历史，或是允许用户把表单重置成某个之前的值。这是因为你可以把 state 之前的拷贝保存到内存中，并适时对其进行再次使用。如果一开始就用了直接修改 state 的方式，那么后面要实现这样的功能就会变得非常困难。
- **更简单的实现**：React 并不依赖于 mutation ，所以你不需要对对象进行任何特殊操作。它不需要像很多“响应式”的解决方案一样去劫持对象的属性、总是用代理把对象包裹起来，或者在初始化时做其他工作。这也是 React 允许你把任何对象存放在 state 中——不管对象有多大——而不会造成有任何额外的性能或正确性问题的原因。

在实践中，你经常可以“侥幸”直接修改 state 而不出现什么问题，但是我们强烈建议你不要这样做，这样你就可以使用我们秉承着这种理念开发的 React 新功能。未来的贡献者甚至是你未来的自己都会感谢你的！


# 小练习
修复错误的 state 更新代码这个表单有几个 bug。试着点击几次增加分数的按钮。你会注意到分数并没有增加。然后试着编辑一下名字字段，你会注意到分数突然“响应”了你之前的修改。最后，试着编辑一下姓氏字段，你会发现分数完全消失了。
```js
import { useState } from 'react';

export default function Scoreboard() {
  const [player, setPlayer] = useState({
    firstName: 'Ranjani',
    lastName: 'Shettar',
    score: 10,
  });

  function handlePlusClick() {
    setPlayer({
      ...player,
      score: player.score + 1,
    });
  }

  function handleFirstNameChange(e) {
    setPlayer({
      ...player,
      firstName: e.target.value,
    });
  }

  function handleLastNameChange(e) {
    setPlayer({
      ...player,
      lastName: e.target.value
    });
  }

  return (
    <>
      <label>
        Score: <b>{player.score}</b>
        {' '}
        <button onClick={handlePlusClick}>
          +1
        </button>
      </label>
      <label>
        First name:
        <input
          value={player.firstName}
          onChange={handleFirstNameChange}
        />
      </label>
      <label>
        Last name:
        <input
          value={player.lastName}
          onChange={handleLastNameChange}
        />
      </label>
    </>
  );
}

```


##  发现并修复 mutation

在静止的背景上有一个可以拖动的方形。你可以使用下拉框来修改方形的颜色。

但是这里有个 bug。当你先移动了方形，再去修改它的颜色时，背景会突然“跳”到方形所在的位置（实际上背景的位置并不应该发生变化！）。但是这并不是我们想要的，`Background` 的 `position` 属性被设置为 `initialPosition`，也就是 `{ x: 0, y: 0 }`。为什么修改颜色之后，背景会移动呢？

```js
 function handleMove(dx, dy) {
    setShape({
      ...shape,
      position: {
        x: shape.position.x + dx,
        y: shape.position.y + dy,
      }
    });
  }
```
# reference
