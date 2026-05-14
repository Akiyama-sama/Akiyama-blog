---
tags:
  - #pernamant
  - 前端实习挑战
  - 前端
  - HTML
---
## 作用不同
* src(source) 属性主要是指定**加载资源**的具体路径，常用在：`<script><img><audio><video><iframe>`上
* href(hyper reference)超链接引用。这个属性用于**指定当前标签的超链接地址**，用于跳转。例如`<a><link><area>`标签
## 资源加载不同
* 适用于src的标签，如`<script> `浏览器会等待这些全部加载完成后，再运行其他代码（这也是为什么scrpt放在最后），被称为[[阻塞加载]]
* 而适用于href的标签，如`<a>`,浏览器会并行处理，被称为[[非阻塞加载]]





# reference
[[HTML 的 src 和 href 属性有什么区别？ - 前端 HTML 面试题 - 面试鸭 - 程序员求职面试刷题神器]]