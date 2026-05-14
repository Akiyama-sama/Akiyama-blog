---
date: 2025-11-20
tags:
  - #CSS
  - 前端实习挑战
  - 前端
  - CSS
---
transition是一种动画属性，不过是那种在开始与结束中间，只有一个中间状态的特殊[[animation关键字]]，一般在给元素设置hover，或者其他状态，或在三种状态下切换时所用的属性

有如下属性：

- transiton-property：指定哪些CSS属性播放转换动画，background-color就只指定背景色，transition-all指定所有可过渡的CSS元素，至于哪些CSS属性可以添加，可以参阅 [MDN 上的可动画 CSS 属性列表](https://developer.mozilla.org/docs/Web/CSS/CSS_animated_properties) ，一般像是颜色，大小之类的可以转换，像是平移旋转需要依赖transform属性
- transition-duration：过渡持续时间
- transition-function：与animation一样的动画函数
- transiton-dely：延迟发生时间