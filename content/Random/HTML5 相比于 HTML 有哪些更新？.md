---
tags:
  - '#pernamant'
---
## 1. 语义化标签
具体可以看这个：
[[什么是HTML语义化]]
## 2. 增加多种媒体标签
例如audio video
## 3. 表单增强
HTML5 对表单控件也进行了扩展，增加了多种类型的输入控件，使得收集和验证用户输入更加方便：
- type="email"、type="url"：自动验证用户输入格式。
- type="number"、type="range"：输入数字或范围。
- type="search"：优化的搜索框。
- type="color"：颜色选择器。
- placeholder：输入框为空时显示的提示文字。
- required、pattern：简化了数据验证过程。
- time：时分秒
- data：日期选择年月日
- datatime：时间和日期(目前只有Safari支持)
- datatime-local：日期时间控件
- week：周控件
- month：月控件
## 4. 新的API
HTML5 引入了许多强大的 JavaScript API，支持更复杂的网页应用：
1）拖放API：允许用户拖放文件直接到网页中。

```html
<img draggable="true" />
```

2）[[Web Storage]]：提供 localStorage 和 sessionStorage，用于在客户端存储数据。 
3）Canvas API：用于在网页上绘制图形。

```html
<canvas id="myCanvas" width="200" height="100"></canvas>
```

4）Geolocation API：允许网站访问用户的地理位置。

## 5. 进度条
## 6. 离线缓存应用
Offline Web Applications：HTML5 提供了应用程序缓存，允许网站在离线状态下运行。

## 7、 WebSockets

提供了一种在单个连接上进行全双工通讯的方式，使得实时数据通讯（如聊天应用）更加有效和资源节约。

## 8、 更丰富的图形和效果

CSS3 Integration：HTML5 与 CSS3 紧密集成，支持更复杂和动态的视觉效果。 SVG Integration：支持可缩放矢量图形 (SVG) 的直接嵌入。

## 9、移除过时元素

比如纯表现的元素：basefont，big，center，font, s，strike，tt，u; 对可用性产生负面影响的元素：frame，frameset，noframes；

# reference
[[HTML5 相比于 HTML 有哪些更新？ - 前端 HTML 面试题 - 面试鸭 - 程序员求职面试刷题神器]]