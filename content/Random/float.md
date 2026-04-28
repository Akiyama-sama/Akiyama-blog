---
date: 2025-11-22
tags:
  - CSS
---
一种CSS属性，允许这个元素脱离[[Nomal Flow]]但又不像position:absolute那样完全脱离文档流，而是会让那些inline的元素包裹这个元素

即 float 是半脱离，而 absolute 之类的是全脱离，文字之类的 inline 元素会感知这个半脱离的 float 元素，而不会感知 absolute 完全脱离的元素。

[[BFC 与 float 之间的关系]]



主要用于实现文字环绕图片的效果
# reference
https://developer.mozilla.org/zh-CN/docs/Web/CSS/Reference/Properties/float