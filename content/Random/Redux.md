---
tags:
  - '#pernamant'
---
Redux是一个管理状态的工具包
具体使用流程如下

1. 定义reducer函数（这个函数根据初始状态state和action返回一个新的状态）
2. 使用createStore方法传入reducer生成一个store实例
3. 使用store实例的subscribe方法订阅数据的变化（数据一旦改变就会触发reducer函数，得到新的状态）
4. 使用store的dispatch方法提交action对象触发数据变化
5. 使用store实例的getState方法获取最新状态
![file-20250330163119930](https://obsidian-picgo-mio.oss-cn-hangzhou.aliyuncs.com/file-20250330163119930.jpg)
# 在代码中的最佳实践

第一步：写小的store
```js
//1 导包createSlice
import { createSlice } from "@reduxjs/toolkit";
//2 编写切片store：slice ，与store一样，封装了state和修改state的方法
export const counterSlice=createSlice({
    name:'counter',
    initialState:{value:0},
    reducers:{
        increment:state=>{
            state.value+=1
        },
        decrement:state=>{
            state.value-=1
        }
        addByNum(state,action){
		    state.value+=action.payload
        }
    }
})
//3 选择性导出action方法
export const{increment,decrement} =counterSlice.actions
//4 默认导出reducer
export default counterSlice.reducer
```
第二步：组合小的store为大的store
```js
import counterReducer from "./counterStore";
import { configureStore } from "@reduxjs/toolkit";
const store = configureStore({
    reducer: {
       counter: counterReducer
    }
})
export default store
```

第三步：在根组件中引用store
```js
import { Provider } from 'react-redux';
import store from './modules/index.js'
const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(

  <React.StrictMode>
    <Provider store={store}>
    <App />
    </Provider>
  </React.StrictMode>

);
```

第四步：在组件中提取store
```js
import './App.css';
import { useDispatch, useSelector } from 'react-redux';
import { decrement, increment } from './modules/counterStore';
function App() {
  const { value } = useSelector(state => state.counter)
  const dispatch= useDispatch()
  return (
    <div className="App">
     <button onClick={()=>{dispatch(increment())}
      }>+</button>
      {value}
      <button onClick={()=>{dispatch(decrement())}
      }>-</button>
    </div>
  );
}
export default App;
```
# reference
