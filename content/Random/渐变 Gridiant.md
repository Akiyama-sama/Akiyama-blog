---
tags:
  - 前端实习挑战
  - 前端
  - CSS
---

[`linear-gradient()`](https://developer.mozilla.org/docs/Web/CSS/linear-gradient\(\)) 函数逐步生成一种或多种颜色的图像

```css
.my-element {
    background: linear-gradient(black, white);
}
```

可以传递一个角度或表示角度的关键字。如果您选择使用关键字，请在 `to` 关键字后指定方向，只需在第一个参数上，加入方向，例如`to right`即可

```css
.my-element {
    background: linear-gradient(to right, black, white);
}
```

色标值定义了颜色停止并与其相邻颜色混合的位置。例如，一个渐变以 45 度角开始，从深红色开始，在渐变大小的 30% 处变为浅红色：它看起来像这样。

```css
.my-element {
    background: linear-gradient(45deg, darkred 30%, crimson);
}
```

[`conic-gradient()`](https://developer.mozilla.org/docs/Web/CSS/conic-gradient\(\))圆锥渐变是围绕着中心点进行渐变

[`repeating-linear-gradient()`](https://developer.mozilla.org/docs/Web/CSS/repeating-linear-gradient\(\))重复线性渐变，可以用来做蓝白碗背景的效果（笑）
 [`repeating-radial-gradient()`](https://developer.mozilla.org/docs/Web/CSS/repeating-radial-gradient\(\)) 和 [`repeating-conic-gradient()`](https://developer.mozilla.org/docs/Web/CSS/repeating-conic-gradient\(\)) 。这是其他渐变，具体看MDN文档

渐变的前一个参数，接受in+色彩空间，可以参考
https://developer.chrome.com/docs/css-ui/access-colors-spaces?hl=zh-cn
```css
.my-element {
  background: linear-gradient(in oklch, deeppink, yellow);
}
```

上面这样可以通过切换色彩空间来去除不饱和中间的颜色，因此在渐变不理想的时候可以试试这个