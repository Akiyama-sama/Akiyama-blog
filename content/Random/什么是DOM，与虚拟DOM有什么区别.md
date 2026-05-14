---
tags:
  - #pernamant
  - 前端实习挑战
  - 前端
  - React
---
[[DOM]]全程为Document Object Model，文档对象模型，主要用于让Javascript操作网页

![Drawing 2025-04-11 21.58.15.excalidraw](https://obsidian-picgo-mio.oss-cn-hangzhou.aliyuncs.com/Drawing%202025-04-11%2021.58.15.excalidraw.svg)

其中DOM的最小单位Node这个js对象中有很多属性，与方法，在真实场景中不需要用到Node中所有的属性与方法，把用到属性与方法抽象为一个[[虚拟DOM]]，通过比较虚拟DOM的变化，批量更新真实DOM，以此来优化性能

## 常见API

获取DOM元素：
	document.getElementById()  document.querySelector() document.getElementByClassName() 
修改元素内容
	element.innerHTML  element.textContent
修改元素属性
	element.setAttribute() element.removeAtrribute()
修改元素样式
	element.style.proterty
添加或删除元素
	document.createElemtent()  elementl.appendChild()
事件监听：
	element.addEventListener()












# reference
