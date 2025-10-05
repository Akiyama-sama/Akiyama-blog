---
tags:
  - "#project"
draft: "true"
---

## 主题选择

通过一个简单的计算器项目来带领React入门学习者快速上手React

## 目标受众

React初学者，仅仅能看懂初始的html 和 css 

## 内容大纲

* jsx语法介绍，使用大括号 `{}` 来嵌入 JavaScript 表达式（例如 `{value}`）。为什么在 JSX 中使用 `className` 而不是 `class`。
* 组件概念介绍
* useState的Hook介绍 
* `const [variable, setVariable] = useState(initialValue)`数组解构语法介绍
* React中的事件处理
* 列表渲染，js中map方法，slice方法

踩坑点介绍

* setState() 到底使用函数式更新，还是直接更新？
	* 更新值依赖于之前的值，就用函数式更新，不依赖就直接更新
* React中的事件处理函数如何进行传递`onClick={}` 
	* 不能直接传递函数`handleBtnClick(value)`,这个是函数调用语句，直接传递会造成React渲染->更新->再渲染的死循环，顺便解释React渲染机制。
	* 需要传递一个匿名函数`()=>{handleBtnClick(value)}` 解释需要这样传递原因。
* map函数中的参数value是怎么来的，为什么需要index传入给button

## 脚本撰写

**视频标题：** 你的第一个React项目，边学边做一个React计算器！！

### 第一幕：引言

229028÷2
120000−5000−486
10^5+14000+514


"大家好！欢迎来到『边学边做React项目』系列教程！本系列专为React初学者设计，即使你只掌握最基础的HTML结构、CSS布局和JavaScript流程语句，我也能带你从零开始，轻松搭建属于自己的React项目。
   
 在本期视频中，我将手把手教你开发一个简约现代的计算器应用。话不多说，让我们马上开始吧！

### 第二幕：安装环境
我们这里需要用到VS code和Node.js ，如果你的电脑上还没有安装，可以在b站搜索安装教程，这里就不进行演示了。

ok，IDE安装完毕过后，我们在一个本地文件夹中创建本项目，演示如何利用官方文档，用npm命令来安装React
介绍必要的学习资源：React官方中文文档，MDN文档


### 第三幕：开始编码

具体流程：
1. 介绍项目目录中间重要的文件，例如package.json中的scripts，还有index.html，以及React是如何绑定root的DOM元素来渲染所有的React组件的。
2. npm run dev解读React欢迎页面的DOM结构，介绍jsx语法
3. 删除不必要的代码
4. 根据项目演示图，来倒推DOM结构，写出必要的结构代码，写出html结构与css语法的时候要清晰的说明我是如何思考的，如何将页面中的元素抽象为一个个的DOM结构的，以及如何用css中的各个布局方式（flex grid)来实现这个布局的，写结构的时候先犯错，每个button单独写，然后再写数组渲染。
5. 开始使用useState，说明下为什么需要useState来存储需要改变的变量，顺便介绍数组赋值语法。
6. 写事件处理函数，注意需要提到eval的不安全性，可以用math.evaluate()等等代替。介绍useState的快照机制，函数中如何更新状态，用什么时候可以直接更新，什么时候使用函数式更新`setInputValue(inputValue=> inputValue+value)`
7. 写完后介绍React事件处理函数怎么写，用onClick 而不是 onclick。然后先用错误的方法来传递函数，查看控制台报错状态，以及报错原因，此时介绍一下React渲染机制：渲染->状态更新->渲染。改回正确的传递函数方式，讲解一下为什么要这样传递（传递匿名函数）

### 第四幕：完成编码，总结




