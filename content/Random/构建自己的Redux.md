---
date: 2025-10-25
tags: 
---
# 起因

我自己在构建React项目的时候，经常与客户端状态打交道，运用类似Redux，Tanstack store或者是Zustand这样的状态管理工具，在写[[揭榜挂帅比赛项目前端]] 与 [[洪鉴天枢 海峡两岸比赛项目]] 的时候，针对客户端状态的管理真的是一团糟，尽管用是用对了，但可维护性是真的一坨，我需要自己构建一遍轮子看他们是怎么来的，才能更熟练的写出维护性更好的代码

# 正文

Redux是采用的[[Flux模式]]，再此模式基础之上改进而来，Flux模式的核心思想为单项数据流，解决了MVC模式中数据混乱的问题。

有四大组件：

- Action：动作，描述发生了什么的动作
- Dispatcher：调度器，负责广播Action
- Stores：各自存储，并包含更新逻辑
- VIew：视图，从Store中获取数据并渲染

Redux改进的点是：Stores多个数据源统一用一个Store来进行管理，且用Reducer来代替Flux里面的Store内置逻辑，抽离了逻辑，放进一个[[纯函数]]当中

## Redux实现过程

```ts
interface Action {
	type: string;
	[key: string]: any;
}

type Reducer<S> = (state: S | undefined, action: Action) => S;
type Listener = () => void;

export function createStore<S>(reducer: Reducer<S>) {
	let currentState: S = reducer(undefined, { type: "INIT" });
	const listeners: Listener[] = [];

	function getState(): S {
		return currentState;
	}
	function dispatch(action: Action) {
		const newState = reducer(currentState, action);
		currentState = newState;
		listeners.forEach((listener) => listener());
	}
	function subscribe(listener: Listener) {
		listeners.push(listener);
		return () => {
			const index = listeners.indexOf(listener);
			if (index !== -1) {
				listeners.splice(index, 1);
			}
		};
	}
	return {
		getState,
		dispatch,
		subscribe,
	};
}
```

- getState用于获取当前最新State，
- dispatch是一个更新函数，只需传递action，就能更新state，并且广播每一个订阅了Store的View，
- subscribe是一个订阅函数，订阅过后你就能执行传递进去的你自己写的回调函数，在dispatch，也就是state更新的时候会自动执行，subscribe还会返回一个unsubscribe函数，这个函数用于取消订阅，手动取消可以避免造成内存泄露


至于如何使用，只需自己定义一个Reducer函数，定义State类型以及更新逻辑，再传递给写好的createStore就可以了

```ts
import { createStore } from "./store";
type stateType = number;
type CountAction = {
	type: string;
	payload?: number;
};

const countReducer = (state: stateType = 0, action: CountAction) => {
	switch (action.type) {
		case "INCREMENT":
			return state + (action.payload || 1);
		case "DECREMENT":
			return state - (action.payload || 1);
		default:
			return state;
	}
};

export const countStore = createStore(countReducer);
```



里面所涉及到的抽象模式：

[[观察者模式]]
[[Flux模式]]

里面所用到的思想与范式就是用的[[函数式编程]]这样的范式，具体表现为：
- [[纯函数]]：reducer
- 不可变性：我们总是用新值来替代旧值，而不是直接修改旧值
- 高阶函数：我们的 `subscribe` 函数会_返回_另一个函数（`unsubscribe` 函数）。一个接收函数作为参数、或返回一个函数的函数（函数作为一等公民），就是高阶函数，这是 FP 中常见的模式。


# reference

https://medium.com/@jamesonbrown/build-a-simple-redux-from-scratch-63908db092b9

https://nytimes.github.io/oak-byo-react-prosemirror-redux/post/build-your-own-redux/