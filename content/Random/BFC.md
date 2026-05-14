---
date: 2025-11-22
tags:
  - CSS
  - 前端实习挑战
  - 前端
---
全称为Block Formatting Context块级上下文

**触发元素与子元素的关系**

- 子元素为[[float]]的，计算其高度
- 子元素直接垂直排列，并塌陷 margin，取子元素 margin 直接最大的那个
- 隔离外部作用域

**触发元素与兄弟元素的关系**

- 兄弟元素为浮动元素时，触发元素能够"排斥"这个兄弟元素，即避开浮动元素

# 触发条件

| **属性**   | **触发值**                                                               |
| -------- | --------------------------------------------------------------------- |
| **根元素**  | `<html>`                                                              |
| **浮动**   | `float` 的值不为 `none`                                                   |
| **定位**   | `position` 为 `absolute` 或 `fixed`                                     |
| **显示类型** | `display` 为 `inline-block`, `table-cell`, `flow-root`, `flex`, `grid` |
| **溢出**   | `overflow` 的值不为 `visible` (如 `hidden`, `auto`, `scroll`)              |

最推荐 display:flow-root,这个无副作用，其他或多或少有副作用

**边界与包含块**

