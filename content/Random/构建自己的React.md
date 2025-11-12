---
date: 2025-10-25
tags:
  - React
---
# 将TSX渲染到DOM上

```tsx
const dom =(
	<div>
		<p>text<p/>
	<div/>
)
```

Js引擎是识别不了这样的jsx语言的，我们必须把它转化为js

```js
const element ={
	type:"div",
	props:{
		children:[]
	}
}

const dom=document.createElemment(element.type)
root.appendChild(dom)

```


如何转化：

```ts
interface MyReactElementProps {
    [key:string]:any
    children:MyReactElement[]
}

interface MyReactTextElementProps {
    nodeValue:number | string
    children:[]
}

type MyReactElement ={
    type:string
    props:MyReactElementProps
}| {
    type:'TEXT_ELEMENT'
    props:MyReactTextElementProps
}
```


```tsx

function createElement(type: string, props:any,...children:any[]): MyReactElement {

	return {
		type,
		props:{
            ...props,
            children:children.map(child=>{
                typeof child === "object"
                    ? child
                    : createTextElement(child)
            })
        }
	};
}

function createTextElement(text:string):MyReactElement {
    return {
        type:"TEXT_ELEMENT",
        props:{
            nodeValue:text,
            children:[]
        }
    }
}

function render(element:MyReactElement,container:HTMLElement){
    //递归出口兼文字类型过滤
    if(element.type === "TEXT_ELEMENT"){
        const textDom = document.createTextNode(element.props.nodeValue)
        container.append(textDom)
        return
    }

    const dom = document.createElement(element.type)

    //把所有除了children的props传递给dom元素
    const IsProperty = key => key !=="children"
    Object.keys(element.props)
        .filter(IsProperty)
        .forEach(propName =>{
            dom[propName] = element.props[propName]
        })


    element.props.children.forEach(child=>{
        render(child,dom)
    })
    container.appendChild(dom)
}
```

# 直接渲染的问题

如果这个dom结构非常深入非常大，那么意味着这个js线程会一直进行，阻塞到浏览器的渲染进程或者其他事件，因此，我们需要将渲染的工作分为一个一个的小的单元（unit work），当浏览器空闲的时候，就可以调度这些一个一个的小的单元进行计算，渲染，当忙碌时，计算就会等待。

那React是如何实现这一步的呢？

我们需要引入两个新概念：
1. **一个工作循环 (Work Loop)**：一个不断执行小任务的循环。
2. **一个任务队列 (Task Queue)**：存放待办的小任务。


## workloop

这个是js版本的workloop：
```js
let nextUnitOfWork = null; // 这是我们的“任务队列”

function workLoop(deadline) {
  let shouldYield = false; // 是否应该“让出”主线程

  // 1. 只要还有任务，并且浏览器允许（没有紧急任务）
  while (nextUnitOfWork && !shouldYield) {
    // 2. 执行一小块任务，并返回*下一个*任务
    nextUnitOfWork = performUnitOfWork(
      nextUnitOfWork
    );

    // 3. 检查浏览器是否要求我们暂停
    // deadline.timeRemaining() 返回“空闲时间”还剩多少毫秒
    shouldYield = deadline.timeRemaining() < 1;
  }

  // 4. 当循环退出时（没任务了，或没时间了），
  //    再次请求浏览器在下次空闲时调用 workLoop
  requestIdleCallback(workLoop);
}

// 启动！
requestIdleCallback(workLoop);
```

当有工作（nextUnitOfWork），以及浏览器空闲（shouldYield）的时候，就会执行这个单元工作（也就是performUnitOfWork函数）

每个单元工作的内容是：
- 将这个单元的fiber创建出dom对象，赋值给它属性（渲染阶段）
- 链接下一个工作：遍历props.children，创建出fiber，并建立child和sibing节点的链接
- 返回下一个工作单元：
	- 优先返回child
	- 没有child，返回sibing
	- 两者都没有，返回到“叔叔节点”，直到根节点

当一个工作循环把每个fiber的渲染工作都做完的时候，在进行一次提交（commit），用户才能看到最新的dom结构。

这意味着，这里的fiber渲染不是挂载（append）的含义，只是计算整个fiber tree的数据，直到commit过后，才算真正的挂载完成

定义Fiber：

```ts
type Fiber = {
    // 元素类型 (e.g., "h1", "TEXT_ELEMENT")
    type: string; 
    // 元素属性 (e.g., { children: [...], id: "foo" })
    props: MyReactElementProps | MyReactTextElementProps; 

    // 真实的 DOM 节点 (一旦创建)
    dom: Node | null; 

    // --- Fiber 树的链接 ---
    parent: Fiber | null;  // 指向父 Fiber
    child: Fiber | null;   // 指向第一个子 Fiber
    sibling: Fiber | null; // 指向下一个兄弟 Fiber
}
```


## 重写render函数

在这里创建了一个新的Fiber对象（root Fiber）作为起始工作单元

```ts
let nextUnitOfWork :Fiber |null=null
let wipRoot : Fiber | null =null

function render(element:MyReactElement,container:HTMLElement){
    wipRoot ={
        type : "ROO_FIBER",
        props: {
            children:[element]
        },
        dom:container,
        child:null,
        sibling:null,
        parent:null
    }
    nextUnitOfWork = wipRoot
}
```

## 执行单个UnitOfWork的步骤

然后开始单个工作单元的执行：

```ts
function performUnitOfWork (fiber:Fiber){
    //TODO1: 计算当前fiber的dom
    const currentDom = fiber.type ==="TEXT_ELEMENT"
        ? document.createTextNode(fiber.props.nodeValue)
        : document.createElement(fiber.type)
    Object.keys(fiber.props)
        .filter(prop=>prop !== "children")
        .forEach(prop=>{
            currentDom[prop]=fiber.props[prop]
        })
    fiber.dom = currentDom

    //TODO2: 创建出child、sibling的fiber
    const elements = fiber.props.children;
    let preSibling: Fiber | null = null;

    for (let i = 0; i < elements.length; i++) {
        const element = elements[i];
        
        const newFiber: Fiber = {
            type: element.type,
            props: element.props,
            parent: fiber,
            dom: null,
            child: null,
            sibling: null
        };
        
        if (i === 0) {
            // 第一个孩子，链接到 fiber.child
            fiber.child = newFiber;
        } else if (preSibling) {
            // 其他孩子，链接到前一个兄弟的 sibling
            preSibling.sibling = newFiber;
        }

        // 更新 preSibling，让它指向当前节点，为下次循环做准备
        preSibling = newFiber; 
    }
    //TODO3: 返回下一个工作单元
    // 优先返回child
	//没有child，返回sibling
	//两者都没有，返回到“叔叔节点”，直到根节点

    // 1. 优先返回 child
    if (fiber.child) {
        return fiber.child;
    }

    // 2. 其次，返回 sibling
    if (fiber.sibling) {
        return fiber.sibling;
    }

    let newFiber:Fiber|null = fiber.parent
    while(newFiber){
        if(newFiber.sibling){
            return newFiber.sibling
        }
        newFiber = newFiber.parent
    }
    

    return null
}
```

## 渲染完成过后的提交函数

```ts
//负责递归的把每个fiber挂载到父dom上
function commitWork(fiber:Fiber,container:Node) {

    const currentDom = fiber?.dom 
    if(currentDom) container.appendChild(currentDom)

    if(fiber.child && fiber.dom){
        commitWork(fiber.child,fiber.dom)
    }
    if(fiber.sibling && fiber.dom){
        commitWork(fiber.sibling,container)
    }
    return
}
```

然后再放进workloop函数当中

```ts
function workLoop(deadline: IdleDeadline) {
    let shouldYield = false;

    while (nextUnitOfWork && !shouldYield) {
        nextUnitOfWork = performUnitOfWork(nextUnitOfWork);
        shouldYield = deadline.timeRemaining() < 1;
    }

    // ------------------------------------
    // 检查：如果工作完成了，就执行提交！
    // ------------------------------------
    if (!nextUnitOfWork && wipRoot) {
        // "渲染阶段" 完成，开始 "提交阶段"

        if(wipRoot.child && wipRoot.dom) {
             commitWork(wipRoot.child, wipRoot.dom);
        }
       
        wipRoot = null; // 提交后清空
    }

    requestIdleCallback(workLoop);
}

// 启动！
requestIdleCallback(workLoop);
```

## 处理函数式组件


```ts
type Fiber ={
    type:string | ComponentType  //更改一下类型
    props:MyReactElementProps | MyReactTextElementProps

    dom:Node | null

    child:Fiber | null
    sibling:Fiber | null
    parent:Fiber | null
}
```

因为添加了函数式组件，我们需要调整这三个函数：

```ts
function performUnitOfWork(fiber: Fiber) {
  let elements: MyReactElement[]=[]
  if (typeof fiber.type === "function") {
    //如果是函数式组件，现处理函数中的逻辑，然后获取到返回值
    const element = fiber.type(fiber.props);
    elements= [element]

  } else {
    //如果不是函数式组件，是原宿主组件
    //TODO1: 计算当前fiber的dom
    const currentDom =
      fiber.type === "TEXT_ELEMENT"
        ? document.createTextNode(fiber.props.nodeValue)
        : document.createElement(fiber.type);
    Object.keys(fiber.props)
      .filter((prop) => prop !== "children")
      .forEach((prop) => {
        currentDom[prop] = fiber.props[prop];
      });
    fiber.dom = currentDom;

    //TODO2: 创建出child、sibling的fiber
    elements = fiber.props.children
    
  }

  reconcileChildren(fiber,elements)
  //TODO3: 返回下一个工作单元
  // 优先返回child
  //没有child，返回sibling
  //两者都没有，返回到“叔叔节点”，直到根节点

  // 1. 优先返回 child
  if (fiber.child) {
    return fiber.child;
  }

  // 2. 其次，返回 sibling
  if (fiber.sibling) {
    return fiber.sibling;
  }

  let newFiber: Fiber | null = fiber.parent;
  while (newFiber) {
    if (newFiber.sibling) {
      return newFiber.sibling;
    }
    newFiber = newFiber.parent;
  }

  return null;
}

function reconcileChildren (fiber:Fiber,elements:MyReactElement[]){
    let preSibling: Fiber | null = null;
    for (let i = 0; i < elements.length; i++) {
      const element = elements[i];

      const newFiber: Fiber = {
        type: element.type,
        props: element.props,
        parent: fiber,
        dom: null,
        child: null,
        sibling: null,
      };

      if (i === 0) {
        // 第一个孩子，链接到 fiber.child
        fiber.child = newFiber;
      } else if (preSibling) {
        // 其他孩子，链接到前一个兄弟的 sibling
        preSibling.sibling = newFiber;
      }

      // 更新 preSibling，让它指向当前节点，为下次循环做准备
      preSibling = newFiber;
    }
}

//负责递归的把每个fiber挂载到父dom上
function commitWork(fiber: Fiber, container: Node) {
  const currentDom = fiber.dom;
  if (currentDom) container.appendChild(currentDom);

  //处理一般的fiber
  if (fiber.child && currentDom) {
    commitWork(fiber.child, currentDom);
  }else if(fiber.child && !currentDom){
    //处理函数式组件的fiber的时候，把child的dom直接挂在到container当中
    commitWork(fiber.child,container)
  }

  if (fiber.sibling) {
    commitWork(fiber.sibling, container);
  }
  return;
}
```

这样，整个Fiber树就构建好了，我们在执行workloop函数的时候不会直接计算整个dom，而是在浏览器主线程空闲的时候执行一个又一个的fiber

这样，我们就可以尝试去做React中的hooks了

# 做useState

```ts
function useState<T>(initialState: T): [T, (action: T | ((prevState: T) => T)) => void] {
    
    // 1. 找到“旧”的 hook
    // 我们查看 wipFiber.alternate (旧 Fiber) 上的 hooks 数组
    const oldHook: Hook<T> | undefined = 
        wipFiber?.alternate?.hooks?.[hookIndex];

    // 2. 创建“新”的 hook
    const hook: Hook<T> = {
        state: oldHook ? oldHook.state : initialState, // 状态要么是旧的，要么是初始值
        queue: [] // 队列总是从空开始
    };

    // 3. (关键) 处理旧队列中的 setState 调用
    // 如果 oldHook 存在，说明上次渲染到这次渲染之间有 setState 被调用
    const actions = oldHook ? oldHook.queue : [];
    actions.forEach(action => {
        // 执行 action 来计算最新的 state
        if (typeof action === 'function') {
            hook.state = (action as (prevState: T) => T)(hook.state);
        } else {
            hook.state = action;
        }
    });

    // 4. `setState` 函数
    const setState = (action: T | ((prevState: T) => T)) => {
        if(!currentRoot) return
        // `setState` 并不立即执行，而是把“action”推进 hook 的队列里


        hook.queue.push(action);

        // --- 触发重渲染！ ---
        // 这是 `setState` 的魔力所在：
        // 它通过创建一个新的 wipRoot，重新启动 workLoop
        wipRoot = {
            type: currentRoot? currentRoot.type : "ROOT_FIBER",
            props: currentRoot.props,
            dom: currentRoot? currentRoot.dom : null, // 使用旧的 DOM
            parent: null,
            child: null,
            sibling: null,
            alternate: currentRoot, // 链接到旧树 (currentRoot)
            hooks: []
        };
        
        nextUnitOfWork = wipRoot;
    };

    // 5. 为下一次 useState 调用做准备
    if(wipFiber?.hooks) {
        wipFiber.hooks.push(hook); // 把新 hook 存到“新” Fiber 上
    }
    hookIndex++; // 索引 +1

    // 6. 返回
    return [hook.state, setState];
}
```



# reference

https://pomb.us/build-your-own-react/
https://github.com/chinanf-boy/didact-explain?tab=readme-ov-file#1-%E6%B8%B2%E6%9F%93dom%E5%85%83%E7%B4%A0
