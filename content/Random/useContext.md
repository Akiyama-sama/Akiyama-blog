---
tags:
  - #pernamant
  - 前端实习挑战
  - 前端
  - React
---
这个Hook是用于解决父传子参数的问题
参数传递：App->A->B
当我直接想App->B传递参数时，useContext就有用了

## 步骤

1. 自定义hook文件，在这个文件用createContext方法创建一个上下文对象
2. 在顶层组建（APP）中，通过ctx.Provider提供数据
3. 在底层组件（B）中通过useContext函数获取数据

## 例子
```jsx
const MsgContext=createContext()

function A(){
return (
	<div>
		this is A component
		<B/>
	</div>
)

}
function B(){
	//底层组件用useContext消费数据
	const msg useContext(MsgContext)
	return
		<div>
		this is B compnent,{msg}
		</div>
}
function App(){
	const msg='this is msg';
	return (
		<div>
		//顶层组件用Provider提供数据
			<MsgContext.Provider value={msg}>
				this is App
				<A/>
			</MsgContext.Provider>
		</div>
	)
}
```






# reference
