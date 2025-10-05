---
tags:
  - '#pernamant'
---
闭包即封装整个函数，让函数里面的私有变量不会对外暴露，并且能够记忆这个私有变量，能在这个变量作用域以外的地方继续使用

这是一个简单示例
```js
function createCounter(){
	let count=0;
	return function (){
		count++;
		console.log(count)
	}
}
const counter=createCounter();
counter();//1
counter();//2
counter();//3
```

- `createCounter()` 在执行时，创建了一个局部变量 `count`，然后返回了一个匿名函数。
- 由于这个返回的匿名函数可以“访问并修改” `count`（它在 `createCounter()` 的作用域里被定义），这就形成了闭包。
- 这样，每次调用 `counter()` 时，都会在原有的 `count` 基础上进行自增，而不是从头开始。


# reference
[[GPT什么是闭包]]