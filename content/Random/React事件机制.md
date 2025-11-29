---
tags:
  - '#pernamant'
---
React将所有的原生事件抽象包装层自己的合成事件，这样就不用花费心智在各个浏览器当中不同兼容性的原生事件了。

合成事件能模拟原生 DOM 事件所有能力的一个事件对象

例如：
React合成事件
```jsx
<button conClick={e=>{console.log(e.nativeEvent)}}
```

原生事件
```js
const onclick = e=>{
	console.log(e.nativeEvent)
}
```

## 事件处理方式

React在底层进行事件委托优化，将事件监听器统一附加到document节点上
React提供的事件对象与原生事件对象接口保持一致，修复了浏览器一些兼容问题


## 合成事件与原生事件的不同

**命名写法不同**
合成事件命名用[[驼峰命名法 (camelCase)]]
原生事件命名用全小写

**事件绑定写法不同**
合成事件用`conClick={}`来传递一个函数名
原生事件是直接用字符串：`onclick="handleClick()"`

**执行顺序不同**

原生事件绑定在具体的dom节点上，先进行执行，而React的合成事件都绑定在document对象上，当真实 DOM 元素触发事件，会冒泡到 document 对象后，再处理 React 事件







# reference
https://www.bilibili.com/video/BV1QZ42117jk?spm_id_from=333.788.videopod.episodes&vd_source=3c58ff149718957dce4ae97d14545646&p=6