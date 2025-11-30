---
tags:
  - '#pernamant'
---
自定义[[hook]]用于抽象常用的逻辑进行复用，本质上是一个use打头的一个函数

## 步骤

1. 声明一个use打头的函数
2. 函数体内封装可复用的逻辑
3. 把组件要用到的状态和逻辑return出去（用对象或者数组）
4. 在哪个组件中使用就在哪个组件调用函数

## 例子

```jsx
function useToggle(){
	const [value,setValue]=useState(true);
	function togole(value){
		setValue(!value)
	}
	return {value,toggle}
}

function App(){
	const {value,toggle}=useToggle()
	return (
		<div>
			{value && <div>this is toggle </div> }
			<button onClick={toggle}>click</button>
		</div>
	)
}
```




# reference
