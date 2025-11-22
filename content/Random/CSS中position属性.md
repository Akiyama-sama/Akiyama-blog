---
date: 2025-11-21
tags:
  - CSS
---
CSS 的 `position` 属性有五种主要的属性值： `static` 、 `relative` 、 `absolute` 、 `fixed` 和 `sticky` 。每个属性值的作用和行为如下：

1. `static` ：这是默认值。元素按照正常的文档流进行排列，不会受到 `top`, `bottom`, `left`, `right` 属性的影响。
2. `relative` ：元素相对其正常位置进行定位。你依然可以使用 `top`, `bottom`, `left`, `right` 属性来调整元素位置，但元素仍然占据原本在文档流中的空间。
3. `absolute` ：元素被移出普通文档流，相对最近的已定位（ `relative`, `absolute`, `fixed`, `sticky` ）的祖先元素进行定位。如果没有找到这样的祖先元素，就会相对于初始包含块（通常为窗口）进行定位。
4. `fixed` ：元素相对于视口（浏览器窗口）进行定位。即使页面滚动，元素也会固定在相应位置。
5. `sticky` ：元素在跨越特定阈值之前表现为 `relative` ，之后表现为 `fixed` 。即元素会根据用户滚动行为在 `relative` 和 `fixed` 定位间切换。