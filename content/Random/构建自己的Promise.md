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

class MyPromise {
	private state: PromiseState = "pending";
	private value: any;
	private reason: any;
	constructor(executor: Executor) {
		const resolve: Resolve = (value) => {
			if (this.state == "pending") {
				this.state = "fulfilled";
				this.value = value
			}
		};
		const reject:Reject=(reason)=>{
			if(this.state == 'pending') {
				this.state='rejected'
				this.reason = reason
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

这里的.then方法等水平上来了再理解吧，我现在有些蠢，在AI的帮助下也理解不了里面的逻辑


![](https://miro.medium.com/v2/resize:fit:1100/format:webp/0*zZRhLUW7g1nk8o7R)

