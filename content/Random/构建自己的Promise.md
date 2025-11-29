---
date: 2025-10-26
tags: 
---

Promise主要是利用的是一种叫做[[控制反转 IoC]]的一种设计模式，用这种模式在内部定义一个状态机：pending | fulfilled | rejected ，用传入的executor函数执行异步操作，然后用户手动执行Promise内部通过executor函数传递过来的resolve方法与reject方法对状态机进行修改，之后再根据状态机的状态来执行相应方法：.then() .catch()

```ts
type PromiseState = "pending" | "fulfilled" | "rejected";
type Reject = (reason: any) => void;
type Resolve = (value: any) => void;
type Executor = (resolve: Resolve, reject: Reject) => void;
type VoidFunction = (value?: any) => void;


class MyPromise {
	private state: PromiseState = "pending";
	private value: any;
	private reason: any;
	private onFulfilledCallbacks: VoidFunction[] = [];
	private onRejectedCallbacks: VoidFunction[] = [];
	constructor(executor: Executor) {
		const resolve: Resolve = (value) => {
			if (this.state == "pending") {
				this.state = "fulfilled";
				this.value = value
				this.successCallbacks.forEach(cb => cb(value));
			}
		};
		const reject:Reject=(reason)=>{
			if(this.state == 'pending') {
				this.state='rejected'
				this.reason = reason
				this.onRejectedCallbacks.forEach(fn => fn(this.reason));
			}
		}
		try{
			executor(resolve,reject)
		} catch(e){
			reject(e)
		}
	}
}

const promise = new MyPromise((resolve, reject) => {
  // 模拟异步操作，比如请求数据
  setTimeout(() => {
    const success = true;
    if (success) { //如果按照预期成功
      resolve("成功啦！");
    } else {       //如果出错
      reject("出错了！");
    }
  }, 1000); 
});
```

在使用promise的时候，我之前很纳闷，为何参数里面凭空多出来两个方法供我调用，我自己的概念中，函数参数是被传递的，而不是凭空多出来的，知道手写Promise，了解[[控制反转 IoC]]这个模式后才知道


```ts
then = (onFulfilled: Resolve, onRejected: Reject) => {
		return new MyPromise((resolve, reject) => {
			// 包装一下回调函数，加入错误处理
			const fulfilledWrapper = (value:any) => {
				try {
					const result = onFulfilled ? onFulfilled(value) : value;
					resolve(result); // 让返回的 Promise resolve
				} catch (e) {
					reject(e); // 出错就 reject
				}
			};

			const rejectedWrapper = (reason:any) => {
				try {
					const result = onRejected ? onRejected(reason) : reason;
					reject(result);
				} catch (e) {
					reject(e);
				}
			};

			if (this.state === "fulfilled") {
				fulfilledWrapper(this.value);
			} else if (this.state === "rejected") {
				rejectedWrapper(this.value);
			} else {
				this.onFulfilledCallbacks.push(fulfilledWrapper);
				this.onRejectedCallbacks.push(rejectedWrapper);
			}
		});
	};
```

这里的.then方法返回一个新的Promise，以支持传入执行新的异步函数，并再次进行.then这样的链式调用，让我们可以以同步的形式写出异步代码，解决了回调地狱


来看看这个.then方法：就是包装一个新的Promise，

在这个Promise当中：
- case: 之前的异步操作状态为fulfilled
	- 执行这个新包装的fulfilledWrapper函数，这个函数会执行新包装的Promise所传递resolve回调函数
- case: 之前的异步操作状态为rejected
	-  执行这个新包装的rejectedWrapper函数，这个函数会执行新包装的Promise所传递reject回调函数
- case: pending
	- 即要么是初始状态，要么是异步函数正在执行，这时候就要把resolve以及reject回调放在onFulfilledCallbacks以及onRejectedCallbacks回调函数队列当中，直到状态改变的时候再执行这个队列里面的异步回调


![](https://miro.medium.com/v2/resize:fit:1100/format:webp/0*zZRhLUW7g1nk8o7R)

