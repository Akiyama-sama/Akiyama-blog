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


## 合成事件与原生事件的不同

**命名写法不同**
合成事件命名用[[驼峰命名法 (camelCase)]]
原生事件命名用全小写

**事件绑定写法不同**
合成事件用`conClick={}`来传递一个函数名
原生事件是直接用字符串：`onclick="handleClick()"`









# reference
https://www.bilibili.com/video/BV1QZ42117jk?spm_id_from=333.788.videopod.episodes&vd_source=3c58ff149718957dce4ae97d14545646&p=6