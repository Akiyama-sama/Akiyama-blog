---
tags:
  - #pernamant
  - 前端实习挑战
  - 前端
  - CSS
---
!important是一种强制覆盖CSS样式规则的一种写法，将其对象的优先级为最高

示例：

```css
<!-- HTML -->
<div class="box" id="box">Hello World</div>
```

```css
#box { 
  color: red; 
}
.box { 
  color: blue !important; 
}
```
# reference
