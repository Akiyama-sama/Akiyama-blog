---
date: 2025-11-20
tags:
  - "#CSS"
---
实现单行文本溢出隐藏可以通过使用 CSS 的 `white-space`, `overflow`, 以及 `text-overflow` 属性。具体代码如下：

```css
.single-line-ellipsis {
    white-space: nowrap; /* 白空间不换行 */
    overflow: hidden;    /* 溢出的部分隐藏 */
    text-overflow: ellipsis; /* 溢出部分用三个点表示 */
}
```

如果要实现多行文本溢出隐藏，可以使用 `-webkit-line-clamp` CSS 属性，结合 `display` 和 `webkit-box-orient` 等属性。具体代码如下：

```css
.multi-line-ellipsis {
    display: -webkit-box;        /* 弹性盒模型 */
    -webkit-box-orient: vertical;/* 垂直排列子元素 */
    -webkit-line-clamp: 2;       /* 限制最多显示两行 */
    overflow: hidden;            /* 溢出部分隐藏 */
}
```