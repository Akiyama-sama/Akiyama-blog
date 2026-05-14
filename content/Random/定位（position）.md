---
tags:
  - 前端实习挑战
  - 前端
  - CSS
URL: https://www.ruanyifeng.com/blog/2019/11/css-position.html
---


默认postion属性值为static，这个值会让元素位置由编写的HTML结构决定，是由浏览器自助决定的，此时这个元素上的top,right,left,bottom属性均无效。

而其他relative,absolute,fixed,sticky均是相对于一个基点的定位，他们之间的不同只是在于基点的不同罢了

`position: relative` 元素仍会保持其在文档流中的位置，即基点是是static原来的位置，但是可以使用top,right,left,bottom等属性进行偏移，还可以用于给子元素为 `position:absolute`的元素进行相对定位

`position: absolute` 元素将根据相对父级relative 的位置确定方向值，即基点在父元素为relative的元素上。

`position: fixed` 元素将根据视口确定方向值，即基点在viewport（浏览器窗口），这会导致元素不会随着滚动而变化，像是固定在网页中，也可以搭配`top`、`right`、`bottom` 或 `left`。

`position: sticky` 元素 仅当其处于停靠/卡住状态时才会应用方向值，这是一个动态设置为relative/fixed的属性值，前提是必须搭配`top`、`right`、`bottom` 或 `left`，sticky才能生效，

当页面滚动，父元素开始脱离视口时（即部分不可见），只要与`sticky`元素的距离达到生效门槛，`relative`定位自动切换为`fixed`定位；等到父元素完全脱离视口时（即完全不可见），`fixed`定位自动切换回`relative`定位。
例如：

```css
#toolbar {
  position: sticky; /* 其他浏览器 */
  top: 20px; /* 切换的门槛值*/
}
```

页面滚动，当#toolbar的父元素脱离视口的时候，一旦viewport顶部与#toolbar距离小于20px的门槛值的时候，position会变为fixed，一旦父元素完全脱离整个视口的时候，会变为relative