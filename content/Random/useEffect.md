---
tags:
  - #pernamant
  - 前端实习挑战
  - 前端
  - React
---
## 为什么需要useEffect
了解useEffect之前得了解React中的两种逻辑处理方式，就能知道为什么需要useEffcect了

1. 渲染组件：可能是由传递过来的props，对这些props进行转化，变为jsx中显示的组件，渲染组件部分的代码必须是纯粹的，传递什么参数，就会得到唯一样式的组件。而不会做其他任何事情
2. 事件处理程序：组件内部的除了渲染组件代码部分的事件处理函数，这些函数可能会代替渲染组件部分的代码来执行副作用：例如按钮点击而引起的处理函数（[[副作用]]）

但还有一种场景下这两种并不能胜任，例如当组件挂载的时候而引起的副作用，而不是由特定事件而引起的副作用。这时候useEffect就能很好的处理这部分的逻辑

**useEffect允许你指定由渲染自身，而不是特定事件而引起的副作用**

例如在一个ChatRoom组件当中
```jsx
const serverUrl = 'https://localhost:1234';

function ChatRoom({ roomId }) {
  const [count,setCount]=useState(0);
  useEffect(() => {
    const connection = createConnection(serverUrl, roomId);
    connection.connect();
    return () => {
      connection.disconnect();
    };
  }, [roomId]);
  const handleCountChange=()=>{
	  setCount(count+1);
  }
  return {
	<>
	  <div>ChatRoom ${roomID}</div>
	  <div>count:${count}</div>
	  <button onclick={handleCountChange}count++<button/>
	</>
  
  }
}
```

渲染组件的代码部分：`const [count,setCount]=useState(0);`给定了状态，组件根据这个State和传递过来的props来渲染此组件
```jsx
	<>
	  <div>ChatRoom ${roomID}</div>
	  <div>count:${count}</div>
	  <button onclick={handleCountChange}count++<button/>
	</>
```

根据props渲染出来的组件是唯一的，就是纯函数，也就是我们说的React逻辑处理的第一种方式
```jsx
<ChatRoom props={roomId=1}/>//都是一模一样的，因为是纯函数
<ChatRoom props={roomId=1}/>
<ChatRoom props={roomId=1}/>
```

在其中`handleCountChange`这个事件处理函数就是我之前说的第二种逻辑处理方式，即由特定事件引发的副作用（即这个handleCountChange函数）。

而这些特定事件没有包括渲染自身等等事件，所以就由useEffect出手啦


在自身组件渲染时，就会触发useEffect()，其中（）里面有两个参数，一个传递的箭头函数，一个是数组，箭头函数中执行的这部分是核心代码
```jsx
const connection = createConnection(serverUrl, roomId);
connection.connect();
```
即当组件挂载时，客户端与聊天室建立连接（副作用），你不可能在这里添加一个button，说点击一下再和聊天室建立连接吧（事件处理程序），这样体验太糟糕了。

## 深入解剖useEffect的结构

我们还是用ChatRoom的例子
```jsx
useEffect(() => {
    const connection = createConnection(serverUrl, roomId);
    connection.connect();
    return () => {
      connection.disconnect();
    };
  }, [roomId]);
```

可以看出useEffect有两个参数，一个箭头函数，一个数组，其中这个数组的是什么作用呢？实际上，这个数据是一个依赖项，可以控制useEffect的执行时机：
```jsx
useEffect(() => {
  // 这里的代码会在每次渲染后运行
});

useEffect(() => {
  // 这里的代码只会在组件挂载（首次出现）时运行
}, []);

useEffect(() => {
  // 这里的代码不但会在组件挂载时运行，而且当 a 或 b 的值自上次渲染后发生变化后也会运行
}, [a, b]);
```
再来看一下剪头函数内部
```jsx
useEffect(() => {
    const connection = createConnection(serverUrl, roomId);
    connection.connect();//被useEffect包裹的副作用

	//这个return返回的是一个清理函数
    return () => {
      connection.disconnect();
    };
  }, [roomId]);
```
里面除了被包裹的核心副作用代码之外，有一个return语句，返回的是一个函数，这个函数的作用是
清理上一次渲染组件时的副作用。但执行时期并不是想象中卸载组件的那时候，而是当重新渲染组件的时候（注意，这里不是说的卸载组件），会执行这个函数，用于清理上一次渲染时产生的副作用，并且执行新的useEffect中的核心代码

例如组件生命周期对应的组件的行为
3. `ChatRoom` 组件挂载，`roomId` 设置为 `"general"`
4. `ChatRoom` 组件更新，`roomId` 设置为 `"travel"`
5. `ChatRoom` 组件更新，`roomId` 设置为 `"music"`
6. `ChatRoom` 组件卸载
在组件生命周期的每个阶段，Effect 执行了不同的操作：
7. Effect 连接到了 `"general"` 聊天室
8. Effect 断开了与 `"general"` 聊天室的连接，并连接到了 `"travel"` 聊天室
9. Effect 断开了与 `"travel"` 聊天室的连接，并连接到了 `"music"` 聊天室
10. Effect 断开了与 `"music"` 聊天室的连接





# reference
